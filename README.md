# dynamic-kobo
Scripts to replace / update / redeploy KoBo forms.

Developed by Karla Peña Ramírez, packaged by [Jacopo Margutti](https://github.com/jmargutt).

## Requirements
1. [Python >= 3.7](https://www.python.org/downloads/)
2. [Firefox](https://www.mozilla.org/en-US/firefox/new/)
2. [Geckodriver](https://github.com/mozilla/geckodriver) (the Firefox webdriver); download it from [here](https://github.com/mozilla/geckodriver/releases).

## Set up
Install required Python packages
```pip install -r requirements.txt```

## Usage
```
Usage: replace_redeploy.py [OPTIONS]

  replace KoBo form with a new one and redeploy

Options:
  --headless          run headless (no GUI)
  --koboserver TEXT   URL of KoBo server, e.g. https://kobonew.ifrc.org/
  --username TEXT     username
  --password TEXT     password
  --formid TEXT       form (asset) ID
  --newform TEXT      absolute path to new form xlsx
  --geckodriver TEXT  absolute path to geckodriver
  --help              Show this message and exit.
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
