import re
from bs4 import BeautifulSoup
from config import TARGET_ROLES, TARGET_DEPARTMENTS

def is_phd_or_postdoc(text: str) -> bool:
    """Check if the text implies a PhD or Postdoc role, and explicitly NOT a professor."""
    text_lower = text.lower()
    
    # First, explicitly exclude professors, lecturers, or directors
    blacklist_roles = ["professor", "lecturer", "reader in", "director of", "head of department"]
    for role in blacklist_roles:
        if re.search(r'\b' + re.escape(role) + r'\b', text_lower):
            return False
            
    # Then check for target roles
    for role in TARGET_ROLES:
        if re.search(r'\b' + re.escape(role) + r'\b', text_lower):
            return True
    return False

def is_target_department(text: str) -> bool:
    """Check if the text implies one of the target departments."""
    text_lower = text.lower()
    for dept in TARGET_DEPARTMENTS:
        # Simple substring match might be too broad (e.g. 'engineering' in 'software engineering')
        if dept in text_lower:
            return True
    return False

def extract_email(text: str) -> str | None:
    """Extract an email address from text using regex."""
    # A standard reasonable email regex
    match = re.search(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', text)
    if match:
        # Exclude common false positives like "info@...", "admissions@..."
        email = match.group(0)
        ignorable_prefixes = ["info@", "admin@", "admissions@", "enquiries@", "webmaster@"]
        if any(email.lower().startswith(p) for p in ignorable_prefixes):
            return None
        return email
    return None

def extract_name_from_email(email: str) -> tuple[str, str]:
    """Fallback: try to guess a name from email if we couldn't parse it well."""
    if not email:
        return "", ""
    local_part = email.split('@')[0]
    parts = re.split(r'[._-]', local_part)
    if len(parts) >= 2:
        first_name = parts[0].capitalize()
        last_name = parts[-1].capitalize()
        return first_name, f"{first_name} {last_name}"
    elif len(parts) == 1:
        first_name = parts[0].capitalize()
        return first_name, first_name
    return "", ""

def is_likely_name(name: str) -> bool:
    """Heuristic to check if a string looks like a person's name."""
    if not name:
        return False
        
    # Remove common titles for the sake of length checking
    clean_name = re.sub(r'^(Prof|Dr|Mr|Mrs|Ms|Professor|Doctor)\.?\s+', '', name, flags=re.IGNORECASE)
    parts = clean_name.split()
    
    # Names usually have 2-4 parts
    if not (2 <= len(parts) <= 4):
        return False
        
    # Check if parts are capitalized and don't contain weird characters
    # Allowing hyphens and apostrophes and periods and international characters
    for part in parts:
        if not re.match(r"^[A-ZÀ-ÖØ-Þ][a-zA-Zà-öø-ÿ\-\'\.]*$", part):
            return False
            
    # Blacklist common non-name words that might appear in titles
    blacklist = [
        "engage", "with", "us", "news", "event", "events", "department", "school", "faculty", 
        "contact", "about", "home", "research", "projects", "publications", "welcome",
        "science", "computer", "mathematics", "physics", "medical", "engineering", "economics",
        "institute", "centre", "center", "laboratory", "university", "college", "group", "team"
    ]
    if any(word.lower() in [p.lower() for p in parts] for word in blacklist):
        return False
        
    return True

def parse_profile_page(html_content: str, url: str) -> dict | None:
    """
    Attempts to parse a profile page. Returns a dictionary with extracted data 
    if it seems to be a valid target profile, otherwise None.
    """
    soup = BeautifulSoup(html_content, 'lxml')
    text = soup.get_text(separator=' ', strip=True)
    
    # 1. Broadly check if it's the right person AND right department based on whole page text
    if not is_phd_or_postdoc(text):
        return None
        
    if not is_target_department(text):
        return None

    # 2. Try to find the email
    email = None
    # Look in mailto links first (highest confidence)
    for a_tag in soup.find_all('a', href=re.compile(r'^mailto:')):
        email_cand = extract_email(a_tag.get('href', ''))
        if email_cand:
            email = email_cand
            break
            
    # Fallback to general text search if mailto fails
    if not email:
        email = extract_email(text)
        
    if not email:
        return None # We must have an email

    # 3. Try to extract Name
    full_name = ""
    first_name = ""
    h1 = soup.find('h1')
    
    # Validate the H1 using our new strict name heuristic
    if h1:
        extracted_h1 = h1.get_text(strip=True).replace('\n', ' ')
        if is_likely_name(extracted_h1):
            full_name = extracted_h1
            parts = full_name.split()
            if parts:
                first_name = parts[0]
            
    # If H1 wasn't a valid name, fallback to inferring from email
    if not full_name:
        first_name, full_name = extract_name_from_email(email)
        # If the inferred name from email still doesn't look like a real name, abandon the page
        if not is_likely_name(full_name):
            return None

    # 4. Determine Department (heuristic: find the first target department mentioned)
    department = ""
    text_lower = text.lower()
    for dept in TARGET_DEPARTMENTS:
        if dept in text_lower:
            department = dept.title()
            break

    return {
        "First Name": first_name,
        "Full Name": full_name,
        "Email": email,
        "Department/Research Area": department,
        "University": "", # Will be filled by crawler based on config
        "Source/Link": url
    }
