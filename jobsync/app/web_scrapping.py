import requests
from bs4 import BeautifulSoup
import json
import time


BASE_URL = "https://weworkremotely.com"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}


def fetch_jobs_from_category(category_url):
    """
    Fetch all job listings from a specific category URL.
    """
    print(f"Scraping jobs from category: {category_url}")
    response = requests.get(category_url, headers=HEADERS)
    if response.status_code != 200:
        print(f"❌ Failed to fetch data from {category_url}. Status code: {response.status_code}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    job_sections = soup.find_all("li", class_="feature")

    if not job_sections:
        print(f"⚠️ No jobs found in category: {category_url}")
        return []

    jobs = []

    for job in job_sections:
        try:
            title = job.find("span", class_="title").text.strip() if job.find("span", class_="title") else "Unknown Title"
            company = job.find("span", class_="company").text.strip() if job.find("span", class_="company") else "Unknown Company"
            external_url = BASE_URL + job.find("a")["href"] if job.find("a") else None
            posted_time = job.find("span", class_="date").text.strip() if job.find("span", class_="date") else "Unknown Time"

            jobs.append({
                "title": title,
                "company": company,
                "external_url": external_url,
                "posted_time": posted_time,
                "location": "Remote",  # Default assumption
            })
        except Exception as e:
            print(f"⚠️ Error processing job: {e}")

    return jobs


def scrape_all_categories():
    """
    Scrape job listings from all available categories in the "Programming" dropdown.
    """
    categories = [
        "/categories/remote-full-stack-programming-jobs#job-listings",
        "/categories/remote-front-end-programming-jobs#job-listings",
        "/categories/remote-back-end-programming-jobs#job-listings",
        "/categories/remote-design-jobs#job-listings",
        "/categories/remote-devops-sysadmin-jobs#job-listings",
        "/categories/remote-management-and-finance-jobs#job-listings",
        "/categories/remote-product-jobs",
        "/categories/remote-customer-support-jobs#job-listings",
        "/categories/remote-sales-and-marketing-jobs#job-listings",
        "/categories/all-other-remote-jobs#job-listings",
        "/remote-full-time-jobs#job-listings",
        "/remote-contract-jobs#job-listings",
    ]

    all_jobs = []

    for category in categories:
        category_url = BASE_URL + category
        jobs = fetch_jobs_from_category(category_url)
        all_jobs.extend(jobs)
        time.sleep(2)  # Avoid sending requests too quickly

    # Save the jobs to a JSON file
    with open("weworkremotely_jobs_by_category.json", "w", encoding="utf-8") as f:
        json.dump(all_jobs, f, indent=4)

    print(f"✅ Scraped {len(all_jobs)} jobs across all categories. Data saved to 'weworkremotely_jobs_by_category.json'")


if __name__ == "__main__":
    scrape_all_categories()
