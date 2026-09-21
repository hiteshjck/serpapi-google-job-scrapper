import os
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv
import serpapi

# Load environment variables from a .env file if available
load_dotenv()

def search_jobs(role: str, location: str, max_pages: int = 10) -> list[dict]:
    """
    Fetches job listings from Google Jobs using the SerpApi client.

    Args:
        role (str): The job title or search query (e.g., 'Data Engineer').
        location (str): The geographical location (e.g., 'Bengaluru, Karnataka, India').
        max_pages (int): Maximum number of search result pages to retrieve.

    Returns:
        list[dict]: A list of dictionary records containing job metadata and application links.
    """
    api_key = os.getenv("SERPAPI_KEY")
    if not api_key:
        raise ValueError("SERPAPI_KEY environment variable is missing. Please check your config.")

    client = serpapi.Client(api_key=api_key)
    all_jobs = []
    next_page_token = None

    for page in range(1, max_pages + 1):
        params = {
            "engine": "google_jobs",
            "q": role,
            "location": location
        }

        if next_page_token:
            params["next_page_token"] = next_page_token

        print(f"Fetching page {page} for '{role}' in '{location}'...")
        results = client.search(params)
        jobs = results.get("jobs_results", [])

        for job in jobs:
            apply_options = job.get("apply_options", [])
            # Extract raw URLs from apply options
            links = [opt.get("link") for opt in apply_options if opt.get("link")]
            
            job_data = {
                "title": job.get("title"),
                "company": job.get("company_name"),
                "location": job.get("location"),
                "apply_links": "\n".join(links)
            }
            all_jobs.append(job_data)

        pagination = results.get("serpapi_pagination", {})
        next_page_token = pagination.get("next_page_token")

        if not next_page_token:
            print("No more pages available.")
            break

    return all_jobs


def export_jobs_to_excel(jobs: list[dict], role: str) -> None:
    """
    Processes fetched job records, formats application links, and outputs to Excel.
    """
    if not jobs:
        print("No job data to export.")
        return

    df = pd.DataFrame(jobs)

    # Format application links as Excel HYPERLINK formulas
    def create_excel_hyperlinks(links_str: str) -> str:
        if not links_str:
            return ""
        urls = links_str.split("\n")
        return "\n".join([f'=HYPERLINK("{url}", "Apply Here")' for url in urls])

    df['apply_links'] = df['apply_links'].apply(create_excel_hyperlinks)

    now = datetime.now()
    sanitized_role = role.lower().replace(" ", "_")
    output_file = f"{sanitized_role}_jobs_{now.strftime('%b%d')}.xlsx"

    df.to_excel(output_file, index=False)
    print(f"\nSuccessfully saved {len(df)} jobs to {output_file}")


if __name__ == "__main__":
    SEARCH_ROLE = "Data Engineer"
    SEARCH_LOCATION = "Bengaluru, Karnataka, India"

    retrieved_jobs = search_jobs(role=SEARCH_ROLE, location=SEARCH_LOCATION, max_pages=10)
    export_jobs_to_excel(retrieved_jobs, role=SEARCH_ROLE)
