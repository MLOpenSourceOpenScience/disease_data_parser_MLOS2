# disease_data_parser_MLOS2

## Abstract

- This repository is based on the research held in RPI. Read the paper here: https://ntrs.nasa.gov/citations/20240015043

### Dependencies

- python (earliest version confirmed supported: 3.9.62)
- PyPDF2 `pip3 install PyPDF2`
- pymupdf `pip3 install PyMuPDF`
- dateutil `pip install python-dateutil`
- requests `pip install requests`

### Running the code

#### Preparation

- We use the HERE API to retrieve location information.
  - In the `Modules/location_interface` file on line 23, please insert your own API key, which can obtain from <https://www.here.com>.

#### Web Scraping

- selenium `pip3 install selenium`
  - More instructions depending on OS: <https://selenium-python.readthedocs.io/installation.html#introduction>
  - Driver version: ChromeDriver 114.0.5735.90

## Datasets

### Google Drive

- <https://drive.google.com/drive/folders/1Y9nzi3MxFRZtAcrWKIAazCqqMwzwBmrg?usp=sharing>
