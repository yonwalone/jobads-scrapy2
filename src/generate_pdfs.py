import os
import json
import re
import jinja2
import pdfkit


class JobPdfGenerator:
    """
    A class to generate PDFs for job listings based on scraped job data.

    This class uses the Jinja2 template engine to render job data into HTML
    format, and then converts the rendered HTML into PDFs using pdfkit. The
    class provides methods to generate individual PDFs for each job listing and
    a consolidated PDF containing employer information.

    Attributes:
        template_path (str): Path to the directory containing the HTML template
            file.
        job_data_path (str): Path to the JSON file containing job data.
        project_root (str): Path to the project root directory.
        template_env (jinja2.Environment): Jinja2 environment for template
            rendering.
        job_data (list): List of dictionaries containing job data loaded from
            the JSON file.

    Methods:
        load_job_data(): Load job data from the specified JSON file.
        _render_html(job): Render HTML content for a given job using the Jinja2
            template.
        generate_pdfs(): Generate individual PDF files for each job listing.
        generate_info_pdfs(): Generate a consolidated PDF containing employer
            information.
        convert_to_array(): Convert the job data into an array format suitable
            for the employer info PDF.
    """
    def __init__(
            self,
            template_path,
            job_data_path,
            project_root,
            output_path
    ):
        """
        Initialize the JobPdfGenerator class.

        Args:
            template_path (str): Path to the directory containing the HTML
                template file.
            job_data_path (str): Path to the JSON file containing job data.
        """
        self.template_path = template_path
        self.job_data_path = job_data_path
        self.project_root = project_root
        self.output_path = output_path
        self.template_env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(self.template_path)
        )
        self.job_data = self.load_job_data()

    def load_job_data(self):
        """
        Load job data from the specified JSON file.

        Returns:
            list: List of job data dictionaries.
        """
        with open(self.job_data_path, 'r') as file:
            print(f"Loading job data from {self.job_data_path}")
            data = json.load(file)
            print(f"Loaded {len(data)} jobs")

            return data

    def _render_html(self, job):
        """Render HTML content for a given job using Jinja2 template."""
        tasks_list = [f'<li>{task}</li>' for task in job['tasks']]
        requirements_list = [
            f'<li>{requirement}</li>' for requirement in job['requirements']
        ]

        context = {
            'title': job['title'],
            'code': job['code'],
            'entry_type': job['entry_type'],
            'location': job['location'],
            'company': job['company'],
            'tasks': '\n'.join(tasks_list),
            'requirements': '\n'.join(requirements_list)
        }

        template = self.template_env.get_template('template.html')

        return template.render(context)

    def generate_pdfs(self):
        """
        Generate PDF files based on the loaded job data and the provided HTML
        template.
        """
        config = pdfkit.configuration(wkhtmltopdf='/usr/local/bin/wkhtmltopdf')
        css_path = os.path.join(self.template_path, 'style.css')

        for job in self.job_data:
            print(f"Generating PDF for job {job['code']}")
            html_content = self._render_html(job)
            job_id = re.search(r'\d+', job['code']).group().lstrip('0')

            output_path = os.path.join(self.output_path, f"{job_id}.pdf")

            pdfkit.from_string(
                html_content,
                output_path,
                configuration=config,
                css=css_path
            )
            print(f"PDF for job {job['code']} generated successfully")

    def convert_to_array(self):
        """
        Converts the job data into an array format.

        Returns:
            list: A list of dictionaries in the format:
                [{'title': title1, 'text': text1},...]
        """
        titles = self.job_data[0]['title']
        texts = self.job_data[0]['text']

        return [
            {'title': title, 'text': text}
            for title, text in zip(titles, texts)
        ]
