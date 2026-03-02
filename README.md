# ScrapeBot

Python web scraper built with Playwright and BeautifulSoup to extract PhD and Postdoc profiles from 23 UK university directories.

## Features
- Concurrently crawls domains up to depth 3
- Targets exact roles: PhD Student, Doctoral Researcher, Postdoc, Fellow Researcher
- Excludes professors, lecturers, and directors
- Avoids spider traps (calendars, news archives, tags)
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
