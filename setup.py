from setuptools import setup, find_packages

with open("README.md", "r") as readme_file:
    readme = readme_file.read()

requirements = [""]

setup(
    name="OpenPIL_AI",
    version="1.0.1",
    author="Malik Ahmed",
    author_email="malik@openpil.org",
    description="AI that extracts clinical drug information from Summary of Product Characteristics pdf documents. This includes information on active-substances, active-excipients, formulation, drug-drug-interactions and drug-class-interactions.",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/OpenPIL/OpenPIL",
    packages=find_packages(),
    install_requires=requirements,
    classifiers=[
        "Programming Language :: C",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
)
