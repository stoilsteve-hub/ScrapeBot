import asyncio
from urllib.parse import urlparse, urljoin
import logging

# Try to import playwright with a helpful error message if missing
try:
    from playwright.async_api import async_playwright
except ImportError:
    logging.error("Playwright is not installed. Please run: pip install playwright && playwright install chromium")
    async_playwright = None

from bs4 import BeautifulSoup

from config import MAX_DEPTH, CONCURRENCY_LIMIT, PAGE_LOAD_TIMEOUT, DELAY_BETWEEN_REQUESTS
from parser import parse_profile_page

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class Crawler:
    def __init__(self, target_domains: list[dict]):
        self.target_domains = target_domains
        self.visited_urls = set()
        self.extracted_data = [] # List of dicts
        self.queue = asyncio.Queue()
        self.semaphore = asyncio.Semaphore(CONCURRENCY_LIMIT)
        
    def is_valid_url(self, url: str, base_domain: str) -> bool:
        """Check if URL belongs to the target domain and is a web page."""
        try:
            parsed = urlparse(url)
            # Must be http/https
            if parsed.scheme not in ('http', 'https'):
                return False
            # Must be within the base domain
            if not parsed.netloc.endswith(base_domain):
                return False
            # Skip media files, documents, etc.
            invalid_extensions = ('.pdf', '.jpg', '.jpeg', '.png', '.gif', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx', '.zip', '.tar', '.gz')
            if parsed.path.lower().endswith(invalid_extensions):
                return False
                
            # Avoid obvious spider traps (calendars, news pagination, dynamic views)
            if '?' in url:
                # Whitelist specific safe queries often used for pagination/profiles
                query = parsed.query.lower()
                safe_queries = ['page=', 'preventscrolltop=', 'prevent_scroll_top=']
                if not any(sq in query for sq in safe_queries):
                    return False
                
            trap_keywords = ['/news/', '/events/', '/tag/', '/category/', '/calendar/', '/date/', '/archive/', '/blog/']
            url_lower = url.lower()
            if any(trap in url_lower for trap in trap_keywords):
                return False
                
            return True
        except Exception:
            return False

    async def fetch_and_parse(self, context, url: str, depth: int, uni_info: dict):
        if depth > MAX_DEPTH:
            return
            
        async with self.semaphore:
            if url in self.visited_urls:
                return
            self.visited_urls.add(url)
            
            logging.info(f"Crawling (Depth {depth}): {url}")
            
            # Simple delay to avoid rate limits
            await asyncio.sleep(DELAY_BETWEEN_REQUESTS)

            try:
                # Use a fresh page for each request
                page = await context.new_page()
                # Basic evasion techniques
                await page.set_extra_http_headers({'Accept-Language': 'en-US,en;q=0.9'})
                
                response = await page.goto(url, timeout=PAGE_LOAD_TIMEOUT, wait_until='domcontentloaded')
                
                if not response or not response.ok:
                    logging.warning(f"Failed to fetch {url}: Status {response.status if response else 'Unknown'}")
                    await page.close()
                    return

                # Only process HTML
                content_type = response.headers.get('content-type', '')
                if 'text/html' not in content_type:
                    await page.close()
                    return

                try:
                    # Reveal email / Profile clicking logic
                    # We will find buttons or elements that might hide emails or act as profile headers
                    reveal_selectors = [
                        "button:has-text('email')",
                        "a:has-text('reveal')",
                        "button:has-text('show')",
                        "a:has-text('email')",
                        "h1",  # Click the main header in case it acts as a toggle
                        ".profile-name",
                        "[aria-label*='email' i]",
                        "[aria-label*='show' i]"
                    ]
                    for selector in reveal_selectors:
                        elements = await page.locator(selector).all()
                        for el in elements:
                            try:
                                if await el.is_visible(timeout=500):
                                    await el.click(timeout=1000)
                            except Exception:
                                pass # ignore unclickable or timeout errors safely
                                
                    await page.wait_for_timeout(1000) # Give JS a moment to inject new email into DOM
                except Exception as click_err:
                    logging.debug(f"Clicking reveal elements failed: {click_err}")

                html_content = await page.content()
                
                # 1. Parse for profile data
                profile_data = parse_profile_page(html_content, url)
                if profile_data:
                    profile_data["University"] = uni_info["name"]
                    # Store if unique email
                    if not any(d.get("Email") == profile_data["Email"] for d in self.extracted_data):
                        self.extracted_data.append(profile_data)
                        logging.info(f"+++ EXTRACTED: {profile_data['Full Name']} - {profile_data['Email']}")

                # 2. Extract links for further crawling if within depth
                if depth < MAX_DEPTH:
                    soup = BeautifulSoup(html_content, 'lxml')
                    for a_tag in soup.find_all('a', href=True):
                        href = a_tag['href']
                        next_url = urljoin(url, href)
                        # Strip fragments
                        next_url = next_url.split('#')[0]
                        if self.is_valid_url(next_url, uni_info["domain"]) and next_url not in self.visited_urls:
                            await self.queue.put((next_url, depth + 1, uni_info))

                await page.close()
                
            except Exception as e:
                logging.error(f"Error processing {url}: {e}")
                # Ensure page is closed even on exception
                try:
                    await page.close()
                except:
                    pass

    async def worker(self, context):
        """Consume URLs from the queue."""
        while True:
            try:
                url, depth, uni_info = await self.queue.get()
                await self.fetch_and_parse(context, url, depth, uni_info)
                self.queue.task_done()
            except asyncio.CancelledError:
                break
            except Exception as e:
                logging.error(f"Worker error: {e}")
                self.queue.task_done()

    async def run(self):
        if async_playwright is None:
            logging.error("Cannot run crawler: Playwright is not installed.")
            return []

        async with async_playwright() as p:
            # We use a browser context
            browser = await p.chromium.launch(headless=True)
            # Create a context with desktop User-Agent to avoid mobile views
            context = await browser.new_context(
                user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            )

            # Seed the queue with homepage URLs
            for uni in self.target_domains:
                await self.queue.put((uni["url"], 0, uni))

            # Start worker tasks
            num_workers = CONCURRENCY_LIMIT
            workers = [asyncio.create_task(self.worker(context)) for _ in range(num_workers)]

            # Wait for queue to be fully processed
            await self.queue.join()

            # Cancel workers
            for w in workers:
                w.cancel()
                
            await asyncio.gather(*workers, return_exceptions=True)
            await context.close()
            await browser.close()
            
        return self.extracted_data
