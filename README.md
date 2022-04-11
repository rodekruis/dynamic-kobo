# dynamic-kobo
[![PyPI Latest Release](https://img.shields.io/pypi/v/dynamic-kobo)](https://pypi.org/project/dynamic-kobo/)

Replace / update and redeploy KoBo forms.

Developed by Karla Peña Ramírez, packaged by [Jacopo Margutti](https://github.com/jmargutt).

## Requirements
1. [Python >= 3.7](https://www.python.org/downloads/)
2. [Firefox](https://www.mozilla.org/en-US/firefox/new/)
2. [Geckodriver](https://github.com/mozilla/geckodriver)

## Set up
1. Download and install [Firefox](https://www.mozilla.org/en-US/firefox/new/)
2. Download the geckodriver binary for your platform ([here](https://github.com/mozilla/geckodriver/releases))
3. Install from [PyPI](https://pypi.org/project/dynamic-kobo/)

```pip install dynamic-kobo```


## Usage
```
Usage: replace-redeploy [OPTIONS]

  replace KoBo form with a new one and redeploy

Options:
  --config            path to configuration file (.env)
  --headless          run headless (no GUI)
  --koboserver TEXT   URL of KoBo server, e.g. https://kobonew.ifrc.org/
  --username TEXT     username
  --password TEXT     password
  --formid TEXT       form (asset) ID
  --newform TEXT      absolute path to new form (.xlsx)
  --geckodriver TEXT  absolute path to geckodriver binary
  --help              show this message and exit
  ```
N.B. all options can be stored in a `.env` file, the script will load them automatically as environment variables. Example:
```
GECKODRIVER=C:\geckodriver\geckodriver.exe
KOBO_SERVER=https://kobonew.ifrc.org/
USERNAME=...
PASSWORD=...
FORM_ID=ai3sdfC1GnERTW72rwwSFq
NEW_FORM='C:\forms\new-form.xlsx'
```
