import os


def find_project_root(marker_file='README.md'):
    """
    Find the project root directory by searching for a marker file.

    Args:
        marker_file (str): The name of the file that marks the project root.

    Returns:
        str: The path to the project root directory, or None if not found.
    """
    current_dir = os.path.abspath(os.path.dirname(__file__))

    while current_dir != os.path.dirname(current_dir):
        if os.path.exists(os.path.join(current_dir, marker_file)):
            return current_dir
        current_dir = os.path.dirname(current_dir)

    return None


PROJECT_ROOT = find_project_root()
API_URL = (
    "https://porsche-beesite-production-gjb.app.beesite.de/search/?data=%7B"
    "%22LanguageCode%22%3A%22DE%22%2C%22SearchParameters%22%3A%7B%22FirstItem"
    "%22%3A1%2C%22CountItem%22%3A1567%2C%22Sort%22%3A%5B%7B%22Criterion%22%"
    "3A%22PublicationStartDate%22%2C%22Direction%22%3A%22DESC%22%7D%5D%2C%22"
    "MatchedObjectDescriptor%22%3A%5B%22ID%22%2C%22PositionTitle%22%2C%22"
    "PositionURI%22%2C%22PositionShortURI%22%2C%22PositionLocation.CountryName"
    "%22%2C%22PositionLocation.CityName%22%2C%22PositionLocation.Longitude"
    "%22%2C%22PositionLocation.Latitude%22%2C%22PositionLocation.PostalCode"
    "%22%2C%22PositionLocation.StreetName%22%2C%22PositionLocation.Building"
    "Number%22%2C%22PositionLocation.Distance%22%2C%22JobCategory.Name%22%"
    "2C%22PublicationStartDate%22%2C%22ParentOrganizationName%22%2C%22"
    "ParentOrganization%22%2C%22OrganizationShortName%22%2C%22CareerLevel.Name"
    "%22%2C%22JobSector.Name%22%2C%22PositionIndustry.Name%22%2C%22Publication"
    "Code%22%2C%22PublicationChannel.Id%22%5D%7D%2C%22SearchCriteria%22%3A%5B%"
    "7B%22CriterionName%22%3A%22PublicationChannel.Code%22%2C%22CriterionValue"
    "%22%3A%5B%2212%22%5D%7D%5D%7D"
)
