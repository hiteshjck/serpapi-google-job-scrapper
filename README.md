# Google Jobs Scraper & Excel Exporter

A Python tool that queries the Google Jobs engine via [SerpApi](https://serpapi.com/) and exports aggregated job listings—including formatted direct application links—into a clean Excel spreadsheet.

## Features

- **Automated Pagination:** Configurable maximum page retrieval depth using SerpApi's `next_page_token`.
- **Structured Output:** Extracts job title, company name, location, and apply URLs.
- **Excel Link Formatting:** Uses Excel `=HYPERLINK()` formulas to allow direct clicking from spreadsheet cells.
- **Environment Security:** Uses `.env` management to protect API credentials.

## Prerequisites

- Python 3.9 or higher
- A active [SerpApi Key](https://serpapi.com/)

## Installation

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/your-username/google-jobs-scraper.git](https://github.com/your-username/google-jobs-scraper.git)
   cd google-jobs-scraper
