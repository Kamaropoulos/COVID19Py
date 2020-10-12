# COVID19Py
<!-- ALL-CONTRIBUTORS-BADGE:START - Do not remove or modify this section -->
[![Downloads](https://pepy.tech/badge/covid19py)](https://pepy.tech/project/covid19py)
[![Downloads](https://pepy.tech/badge/covid19py/month)](https://pepy.tech/project/covid19py/month)
[![Downloads](https://pepy.tech/badge/covid19py/week)](https://pepy.tech/project/covid19py/week)
[![GPLv3 License](https://img.shields.io/badge/License-GPL%20v3-yellow.svg)](https://opensource.org/licenses/)
[![All Contributors](https://img.shields.io/badge/all_contributors-2-orange.svg?style=flat-square)](#contributors-)
[![CodeFactor](https://www.codefactor.io/repository/github/kamaropoulos/covid19py/badge)](https://www.codefactor.io/repository/github/kamaropoulos/covid19py)
[![HitCount](http://hits.dwyl.com/Kamaropoulos/COVID19Py.svg)](http://hits.dwyl.com/Kamaropoulos/COVID19Py)
[![GitHub stars](https://img.shields.io/github/stars/Kamaropoulos/COVID19Py.svg?style=social&label=Star)](https://github.com/Kamaropoulos/COVID19Py)
<!-- ALL-CONTRIBUTORS-BADGE:END -->
A tiny Python package for easy access to up-to-date Coronavirus (COVID-19, SARS-CoV-2) cases data.
<!-- Python API Wrapper for tracking Coronavirus (COVID-19, SARS-CoV-2) via https://github.com/ExpDev07/coronavirus-tracker-api -->

## About

COVID19Py is a Python wrapper for the [ExpDev07/coronavirus-tracker-api](https://github.com/ExpDev07/coronavirus-tracker-api) REST API.
It retrieves data directly from [@ExpDev07](https://github.com/ExpDev07)'s backend but it can also be set up to use a different backend.

To achieve this, just pass the URL of the backend as a parameter to the library's constructor:
```python
import COVID19Py
covid19 = COVID19Py.COVID19("https://my-awesome-covid19-backend")
```
## Installation

In order install this package, simply run:

```bash
pip install COVID19Py
```

## Usage

To use COVID19Py, you first need to import the package and then create a new instance:

```python
import COVID19Py
covid19 = COVID19Py.COVID19()
```

### Choosing a data source

COVID19Py supports the retrieval of data from multiple data sources.
To choose a specific data source, simply pass it as a parameter to the library's constructor:
```python
covid19 = COVID19Py.COVID19(data_source="csbs")
```
For more details about the available data sources, please check the [API's documentation](https://github.com/ExpDev07/coronavirus-tracker-api/blob/master/README.md#picking-data-source).

### Getting latest amount of total confirmed cases, deaths, and recoveries:

```python
latest = covid19.getLatest()
```

### Getting all locations:

```python
locations = covid19.getLocations()
```

or:

```python
locations = covid19.getLocations(timelines=True)
```
to also get timelines.

You can also rank the results by `confirmed`, `deaths` or `recovered`.

```python
locations = covid19.getLocations(rank_by='recovered')
```

### Getting location by country code:

```python
location = covid19.getLocationByCountryCode("US")
```
or:
```python
location = covid19.getLocationByCountryCode("US", timelines=True)
```
to also get timelines.

### Getting a specific location (includes timelines by default):

```python
location = covid19.getLocationById(39)
```

### Getting all data at once:

You can also get all the available data with one command.

```python
data = covid19.getAll()
```
or:
```python
data = covid19.getAll(timelines=True)
```
to also get timelines.

`latest` will be available on `data["latest"]` and `locations` will be available on `data["locations"]`.

### Getting `latest` deltas:

When using `getAll()`, COVID19Py will also store the previous version of the retrieved data. This allows us to easily see how data changed since the last time we requested them.

```python
changes = covid19.getLatestChanges()
```
```json
{
    "confirmed": 512,
    "deaths": 16,
    "recovered": 1024
}
```
## Contributing

You will need to fork this repository onto your own GitHub account, then clone the repo to your local machine.

In the project directory, you will need to make sure the required packages are installed. To install requirements from the Pipfile, run a command like the following, which may depend on how you have package management set up:
```bash
pipenv install
```

## Contributors ✨

Thanks goes to these wonderful people ([emoji key](https://allcontributors.org/docs/en/emoji-key)):

<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- prettier-ignore-start -->
<!-- markdownlint-disable -->
<table>
  <tr>
    <td align="center"><a href="https://kamaropoulos.com"><img src="https://avatars0.githubusercontent.com/u/10237776?v=4" width="100px;" alt=""/><br /><sub><b>Konstantinos Kamaropoulos</b></sub></a><br /><a href="https://github.com/Kamaropoulos/COVID19Py/commits?author=Kamaropoulos" title="Code">💻</a> <a href="https://github.com/Kamaropoulos/COVID19Py/commits?author=Kamaropoulos" title="Documentation">📖</a> <a href="#example-Kamaropoulos" title="Examples">💡</a></td>
    <td align="center"><a href="http://www.jaroddeweese.com"><img src="https://avatars1.githubusercontent.com/u/32393906?v=4" width="100px;" alt=""/><br /><sub><b>Jarod DeWeese</b></sub></a><br /><a href="https://github.com/Kamaropoulos/COVID19Py/commits?author=jdeweese1" title="Code">💻</a> <a href="https://github.com/Kamaropoulos/COVID19Py/commits?author=jdeweese1" title="Documentation">📖</a></td>
  </tr>
</table>

<!-- markdownlint-enable -->
<!-- prettier-ignore-end -->
<!-- ALL-CONTRIBUTORS-LIST:END -->

This project follows the [all-contributors](https://github.com/all-contributors/all-contributors) specification. Contributions of any kind welcome!
