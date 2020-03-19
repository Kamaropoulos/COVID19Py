import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="COVID19Py", # Replace with your own username
    version="0.1.0",
    author="Konstantinos Kamaropoulos",
    author_email="k@kamaropoulos.com",
    description="Python API Wrapper for tracking Coronavirus (COVID-19, SARS-CoV-2) via https://github.com/ExpDev07/coronavirus-tracker-api",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Kamaropoulos/covid19py",
    packages=setuptools.find_packages(),
    keywords = ['covid19', 'coronavirus', 'api'],
    classifiers=[
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        # "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*',
)