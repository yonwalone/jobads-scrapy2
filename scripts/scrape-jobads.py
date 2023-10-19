import os
import subprocess
from src.job_url_scraper import JobUrlScraper
from src.generate_pdfs import JobPdfGenerator
from utils import PROJECT_ROOT, API_URL


def fetch_job_ids(api_url, output_file, config_file):
    """
    Fetch job IDs using the JobUrlScraper.

    Args:
        api_url (str): The API endpoint to fetch job IDs.
        output_file (str): Path to save the fetched job IDs.
        config_file (str): Path to the configuration file for filtering.
    """
    id_scraper = JobUrlScraper(api_url, output_file, config_file)

    print("Fetching job data from API...")
    id_scraper.scrape_job_urls()
    print("Job IDs saved to ", output_file)


def run_spider(input_file, output_file):
    """
    Run the Scrapy spider using a subprocess.

    Args:
        input_file (str): Path to the input file containing job ad IDs.
        output_file (str): Path to save the scraped data.

    Returns:
        bool: True if the spider ran successfully, False otherwise.
    """
    print("Running Scrapy spider...")

    command = (
        f"scrapy crawl job_ads "
        f"-a inputfile={input_file} "
        f"-O {output_file} "
        "--nolog"
    )

    original_directory = os.getcwd()

    try:
        os.chdir(os.path.join(PROJECT_ROOT, "src", "jobads_scrapy"))

        subprocess.run(command, shell=True, check=True)

        print("Scrapy spider ran successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while running the Scrapy command: {e}")
        return False
    finally:
        os.chdir(original_directory)


def generate_pdfs(input_file, template_path, output_path):
    """
    Generate PDFs using the JobPdfGenerator.

    Args:
        input_file (str): Path to the input JSON file containing scraped job
            data.
        template_path (str): Path to the directory containing the HTML template
            file.
    """
    pdf_generator = JobPdfGenerator(
        template_path,
        input_file,
        PROJECT_ROOT,
        output_path
    )
    pdf_generator.load_job_data()
    pdf_generator.generate_pdfs()


def main():
    VERSION = "20231019-dev-jobs"
    DATA_PATH = os.path.join(PROJECT_ROOT, "data", VERSION)
    CONFIG_FILE = os.path.join(DATA_PATH, "filter_config.json")
    OUTPUT_FILE = os.path.join(DATA_PATH, "job_ids.npy")

    fetch_job_ids(API_URL, OUTPUT_FILE, CONFIG_FILE)

    input_file = OUTPUT_FILE
    output_file = os.path.join(DATA_PATH, "scraped_jobs.json")
    run_spider(input_file, output_file)

    while True:
        user_input = input("Do you want to generate PDFs? (yes/no): ")
        formatted_input = user_input.strip().lower()
        if formatted_input in ["yes", "no"]:
            break
        else:
            print("Invalid input. Please enter 'yes' or 'no'.")

    should_generate_pdfs = formatted_input == "yes"

    if should_generate_pdfs:
        output_path = os.path.join(DATA_PATH, "pdfs")
        template_path = os.path.join(
            PROJECT_ROOT, "src", "pdf_gen"
        )
        generate_pdfs(output_file, template_path, output_path)


if __name__ == "__main__":
    main()
