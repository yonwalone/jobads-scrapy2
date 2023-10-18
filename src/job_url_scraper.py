import requests
import numpy as np
import json


class JobUrlScraper:
    """
    A scraper for fetching job IDs from a specified job search API.

    This scraper fetches job data from the provided API URL, filters the jobs
    based on criteria specified in a configuration file, and saves the filtered
    job IDs to an output file.

    Attributes:
        url (str): The URL of the job search API.
        output_file (str): Path to the output file where job IDs will be saved.
        config (dict): Configuration containing filter criteria.
    """

    def __init__(self, url, output_file, config_file):
        """
        Initialize the JobUrlScraper instance.

        Args:
            url (str): The URL of the job search API.
            output_file (str): Path to the output file where job IDs will be
                saved.
            config_file (str): Path to the configuration file containing
                filter criteria.
        """
        self.url = url
        self.output_file = output_file
        self.config = self._load_config(config_file)

    def _load_config(self, config_file):
        """
        Load filter criteria from a configuration file.

        Args:
            config_file (str): Path to the configuration file.

        Returns:
            dict: Loaded filter criteria.
        """
        with open(config_file, 'r') as file:
            return json.load(file)

    def _fetch_data_from_api(self):
        """
        Retrieve job data from the API.

        Returns:
            dict: Job data in JSON format, or None if there's an error.
        """
        try:
            response = requests.get(self.url)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print("Error occurred:", e)
            return None

    def _filter_job_ids(self, data):
        """
        Extract and filter job IDs based on the specified criteria.

        Args:
            data (dict): Job data in JSON format.

        Returns:
            list[int]: List of filtered job IDs.
        """
        job_ids = []
        desired_job_functions = self.config["job_functions"]
        desired_organization_name = self.config["organization_name"]

        for item in data["SearchResult"]["SearchResultItems"]:
            is_desired_function = self._is_desired_job_function(
                item, desired_job_functions
            )
            is_desired_org = self._is_desired_organization(
                item, desired_organization_name
            )

            if is_desired_function and is_desired_org:
                job_ids.append(item["MatchedObjectDescriptor"]["ID"])

        return job_ids

    @staticmethod
    def _is_desired_job_function(item, desired_job_functions):
        """
        Determine if a job item matches the desired job functions.

        Args:
            item (dict): Individual job item.
            desired_job_functions (list[str]): List of desired job functions.

        Returns:
            bool: True if the job item matches, False otherwise.
        """
        categories = item["MatchedObjectDescriptor"]["JobCategory"]

        return any(
            category["Name"] in desired_job_functions
            for category in categories
        )

    @staticmethod
    def _is_desired_organization(item, desired_organization_name):
        """
        Determine if a job item belongs to the desired organization.

        Args:
            item (dict): Individual job item.
            desired_organization_name (str): Name of the desired organization.

        Returns:
            bool: True if the job item belongs to the desired organization,
                False otherwise.
        """
        descriptor = item["MatchedObjectDescriptor"]
        org_name = descriptor["ParentOrganizationName"]

        return org_name == desired_organization_name

    def scrape_job_urls(self):
        """
        Fetch, filter, and save job IDs.

        Retrieves job data from the API, filters the jobs based on the criteria
        from the configuration, and saves the filtered job IDs to the specified
        output file.
        """
        data = self._fetch_data_from_api()

        if data:
            job_ids = self._filter_job_ids(data)
            np.save(self.output_file, np.array(job_ids))
            print(f"Saved {len(job_ids)} job IDs to '{self.output_file}'")
