"""Python setup.py for tech_stack_ai_configuration_data_scraper package"""
import io
import os
from setuptools import find_packages, setup


def read(*paths, **kwargs):
    """Read the contents of a text file safely.
    >>> read("tech_stack_ai_configuration_data_scraper", "VERSION")
    '0.1.0'
    >>> read("README.md")
    ...
    """

    content = ""
    with io.open(
        os.path.join(os.path.dirname(__file__), *paths),
        encoding=kwargs.get("encoding", "utf8"),
    ) as open_file:
        content = open_file.read().strip()
    return content


def read_requirements(path):
    return [
        line.strip()
        for line in read(path).split("\n")
        if not line.startswith(('"', "#", "-", "git+"))
    ]


setup(
    name="tech_stack_ai_configuration_data_scraper",
    version=read("tech_stack_ai_configuration_data_scraper", "VERSION"),
    description="Awesome tech_stack_ai_configuration_data_scraper created by jonasfroeller",
    url="https://github.com/jonasfroeller/tech-stack-ai-configuration-data-scraper/",
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    author="jonasfroeller",
    packages=find_packages(exclude=["tests", ".github"]),
    install_requires=read_requirements("requirements.txt"),
    entry_points={
        "console_scripts": ["tech_stack_ai_configuration_data_scraper = tech_stack_ai_configuration_data_scraper.__main__:main"]
    },
    extras_require={"test": read_requirements("requirements-test.txt")},
)
