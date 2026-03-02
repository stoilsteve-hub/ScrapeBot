# ScrapeBot

Python web scraper built with Playwright and BeautifulSoup to extract PhD and Postdoc profiles from 23 UK university directories.

## Features
- Concurrently crawls domains up to depth 3 (optimized for M5 Mac)
- Targets exact roles: PhD Student, Doctoral Researcher, Postdoc, Fellow Researcher
- Aggressively filters generic department and support pages with 100+ keyword blacklist
- Automatically clicks on profiles and "reveal" buttons to unhide JavaScript-protected emails
- Parses and whitelists specific paginated directories without getting trapped
- Terminal output to track live extraction progress
- Exports matches to `.xlsx` and `.csv` formats

## Requirements
```bash
pip install playwright pandas bs4 aiohttp lxml xlsxwriter nest_asyncio
playwright install chromium
```

## Usage
```bash
python main.py
```
*Note: Run `main.py` in the background for a full extraction across all configured universities.*
