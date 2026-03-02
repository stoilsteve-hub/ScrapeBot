import asyncio
import logging
from config import UNIVERSITIES, OUTPUT_FILE
from crawler import Crawler
from data_exporter import export_to_excel

# For running python in environments with existing event loops (like Jupyter)
try:
    import nest_asyncio
    nest_asyncio.apply()
except ImportError:
    nest_asyncio = None

# Configure root logger
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

async def main():
    print(f"\n🚀 STARTING SCRAPER: Targeting {len(UNIVERSITIES)} universities...\n")
    
    # Initialize the Crawler with our configured domains
    crawler = Crawler(UNIVERSITIES)
    
    # Run the crawler and get the extracted profiles
    print("🕷️  Crawler unleashed! Searching web for PhDs and Postdocs...\n")

    try:
        extracted_data = await crawler.run()
    except asyncio.CancelledError:
        print("\n🛑 Crawler tasks cancelled.")
        extracted_data = crawler.extracted_data
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        extracted_data = crawler.extracted_data
    
    print(f"\n✅ CRAWL COMPLETE! 🎓 Total profiles extracted: {len(extracted_data)}")
    
    # Export the populated data
    export_to_excel(extracted_data, OUTPUT_FILE)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n🛑 Scraping manually interrupted. Saving data and exiting gracefully...")
