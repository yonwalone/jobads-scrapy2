import os
from src.job_url_scraper import JobUrlScraper
from utils import PROJECT_ROOT, API_URL


def main():
    VERSION = "20231017-dev-jobs"
    DATA_PATH = os.path.join(PROJECT_ROOT, "data", VERSION)
    OUTPUT_FILE = os.path.join(DATA_PATH, "job_ids.npy")
    CONFIG_FILE = os.path.join(DATA_PATH, "filter_config.json")

    id_scraper = JobUrlScraper(API_URL, OUTPUT_FILE, CONFIG_FILE)

    print("Fetching job data from API...")
    id_scraper.scrape_job_urls()
    print("Job IDs saved to ", OUTPUT_FILE)


if __name__ == "__main__":
    main()
