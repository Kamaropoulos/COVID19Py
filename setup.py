import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="COVID19Py", # Replace with your own username
    version="0.3.0",
    author="Konstantinos Kamaropoulos",
    author_email="k@kamaropoulos.com",
    description="A tiny Python package for easy access to up-to-date Coronavirus (COVID-19, SARS-CoV-2) cases data.",
    license = "GPLv3",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Kamaropoulos/covid19py",
    packages=["COVID19Py"],
    keywords = ['covid19', 'coronavirus', 'api', 'covid-19', 'wrapper'],
    classifiers=[
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'License :: OSI Approved :: GNU Affero General Public License v3',
        "Operating System :: OS Independent",
    ],
    python_requires='>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*',
)
