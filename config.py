# config.py

# Target University Domains and Start URLs
UNIVERSITIES = [
    # England
    {"name": "University College London", "url": "https://www.ucl.ac.uk", "domain": "ucl.ac.uk"},
    {"name": "University of Manchester", "url": "https://www.manchester.ac.uk", "domain": "manchester.ac.uk"},
    {"name": "University of Birmingham", "url": "https://www.birmingham.ac.uk", "domain": "birmingham.ac.uk"},
    {"name": "University of Bristol", "url": "https://www.bristol.ac.uk", "domain": "bristol.ac.uk"},
    {"name": "University of Leeds", "url": "https://www.leeds.ac.uk", "domain": "leeds.ac.uk"},
    {"name": "University of Sheffield", "url": "https://www.sheffield.ac.uk", "domain": "sheffield.ac.uk"},
    {"name": "University of Nottingham", "url": "https://www.nottingham.ac.uk", "domain": "nottingham.ac.uk"},
    {"name": "University of Southampton", "url": "https://www.southampton.ac.uk", "domain": "southampton.ac.uk"},
    {"name": "University of Warwick", "url": "https://warwick.ac.uk", "domain": "warwick.ac.uk"},
    {"name": "Newcastle University", "url": "https://www.ncl.ac.uk", "domain": "ncl.ac.uk"},
    {"name": "University of Liverpool", "url": "https://www.liverpool.ac.uk", "domain": "liverpool.ac.uk"},
    {"name": "Queen Mary University of London", "url": "https://www.qmul.ac.uk", "domain": "qmul.ac.uk"},
    {"name": "University of Leicester", "url": "https://le.ac.uk", "domain": "le.ac.uk"},
    {"name": "Lancaster University", "url": "https://www.lancaster.ac.uk", "domain": "lancaster.ac.uk"},
    {"name": "University of Exeter", "url": "https://www.exeter.ac.uk", "domain": "exeter.ac.uk"},
    {"name": "University of York", "url": "https://www.york.ac.uk", "domain": "york.ac.uk"},
    # Scotland
    {"name": "University of Edinburgh", "url": "https://www.ed.ac.uk", "domain": "ed.ac.uk"},
    {"name": "University of Glasgow", "url": "https://www.gla.ac.uk", "domain": "gla.ac.uk"},
    {"name": "University of Aberdeen", "url": "https://www.abdn.ac.uk", "domain": "abdn.ac.uk"},
    {"name": "University of Dundee", "url": "https://www.dundee.ac.uk", "domain": "dundee.ac.uk"},
    # Wales
    {"name": "Cardiff University", "url": "https://www.cardiff.ac.uk", "domain": "cardiff.ac.uk"},
    {"name": "Swansea University", "url": "https://www.swansea.ac.uk", "domain": "swansea.ac.uk"},
    # Northern Ireland
    {"name": "Queen's University Belfast", "url": "https://www.qub.ac.uk", "domain": "qub.ac.uk"}
]

# Filtering Keywords
TARGET_ROLES = [
    "phd", "doctoral researcher", "postdoc", "postdoctoral", "research fellow", "fellow researcher", "phd student", "pgr", "postgraduate researcher"
]

TARGET_DEPARTMENTS = [
    "computer science", "engineering", "mathematics", "physics", "medical science", "medicine", "economics"
]

# Crawler Settings
MAX_DEPTH = 3 # Can be adjusted based on results (Warning: large datasets will take a long time to crawl)
CONCURRENCY_LIMIT = 5 # Avoid getting blocked
PAGE_LOAD_TIMEOUT = 30000 # 30 seconds
DELAY_BETWEEN_REQUESTS = 1 # seconds

# Output format
OUTPUT_FILE = "university_phds_and_postdocs.xlsx"
