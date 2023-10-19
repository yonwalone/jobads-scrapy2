import scrapy
import numpy as np


class JobAdsSpider(scrapy.Spider):
    """
    This scrapy spider crawls job ads of the defined urls.

    Args:
        scrapy.Spider: The base class for the spider.

    Yields:
        dict: A dictionary containing the extracted job ad data.
    """
    name = "job_ads"
    allowed_domains = ["jobs.porsche.com"]

    def __init__(self, inputfile=None, *args, **kwargs):
        """
        Initialize the spider with optional input file.

        Args:
            inputfile (str, optional): Path to the input file containing job ad
                IDs.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Attributes:
            start_urls (list): List of start URLs generated from the input
                file.
        """
        super().__init__(*args, **kwargs)
        self.start_urls = self._generate_start_urls(inputfile)

    @staticmethod
    def _generate_start_urls(inputfile):
        """
        Generate start URLs from the input file.

        Args:
            inputfile (str): Path to the input file containing job ad IDs.

        Returns:
            list: List of start URLs.
        """
        ids = np.load(inputfile)
        base_url = 'https://jobs.porsche.com/index.php?ac=jobad&id='
        return [base_url + str(item) for item in ids]

    def parse(self, response):
        """
        Parses the job ad webpage and extracts relevant information.

        Args:
            response (scrapy.http.Response): The response object representing
            the webpage.

        Yields:
            dict: A dictionary containing the extracted job ad data.
        """
        yield {
            'title': self._extract_title(response),
            'code': self._extract_code(response),
            'entry_type': self._extract_entry_type(response),
            'location': self._extract_location(response),
            'company': self._extract_company(response),
            'tasks': self._extract_tasks(response),
            'requirements': self._extract_requirements(response)
        }

    @staticmethod
    def _extract_title(response):
        """
        Extract job title from the response.

        Args:
            response (scrapy.http.Response): The response object.

        Returns:
            str: Job title.
        """
        return response.css("h1.margin-bottom-gutter::text").get()

    @staticmethod
    def _extract_code(response):
        """
        Extract job code from the response.

        Args:
            response (scrapy.http.Response): The response object.

        Returns:
            str: Job code.
        """
        return response.css("span.jobad-base-info-content::text").get()

    @staticmethod
    def _extract_entry_type(response):
        """
        Extract job entry type from the response.

        Args:
            response (scrapy.http.Response): The response object.

        Returns:
            str: Job entry type.
        """
        return response.css("span.jobad-base-info-content::text").getall()[1]

    @staticmethod
    def _extract_location(response):
        """
        Extract job location from the response.

        Args:
            response (scrapy.http.Response): The response object.

        Returns:
            str: Job location.
        """
        return response.css("span.jobad-base-info-content::text").getall()[2]

    @staticmethod
    def _extract_company(response):
        """
        Extract company name from the response.

        Args:
            response (scrapy.http.Response): The response object.

        Returns:
            str: Company name.
        """
        return response.css("span.jobad-base-info-content::text").getall()[3]

    @staticmethod
    def _extract_tasks(response):
        """
        Extract list of tasks from the response.

        Args:
            response (scrapy.http.Response): The response object.

        Returns:
            list: List of tasks.
        """
        xpath_query = ('//*[@id="aria-panel-task"]/div/ul/li/span')
        task_elements = response.xpath(xpath_query)

        return [
            task_element.xpath("text()").get()
            for task_element in task_elements
        ]

    @staticmethod
    def _extract_requirements(response):
        """
        Extract list of requirements from the response.

        Args:
            response (scrapy.http.Response): The response object.

        Returns:
            list: List of requirements.
        """
        xpath_query = ('//*[@id="aria-panel-your-profile"]/div/ul/li/span')
        requirement_elements = response.xpath(xpath_query)

        return [
            element.xpath("text()").get()
            for element in requirement_elements
        ]
