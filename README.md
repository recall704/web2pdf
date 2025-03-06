# Web to PDF Converter

A simple Python script that converts web pages to PDF files using Playwright.

## Prerequisites

- Python 3.x
- Playwright

## Installation

1. Install the required packages:
```bash
pip install -r requirements.txt
```

2. Install Playwright browsers:
```bash
playwright install chromium
```

## Usage

```bash
python web2pdf.py -i <input_url> -o <output_pdf>
```

Arguments:
- `-i` or `--url`: Input URL of the webpage to convert
- `-o` or `--output`: Output PDF file path

Example:
```bash
python web2pdf.py -i https://www.example.com -o example.pdf
```
