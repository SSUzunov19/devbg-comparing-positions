import requests
from bs4 import BeautifulSoup
import re

# Scrape job categories
def scrape_job_categories():
    # Get category URLs
    category_urls = get_category_urls()

    # Scrape job listings for each category URL
    job_listings = []
    for url in category_urls:
        listings = scrape_job_listings(url)
        job_listings.extend(listings)

    # Return the list of job listings
    return job_listings

# Get category URLs
def get_category_urls():
    # Send a GET request to the website
    response = requests.get("https://dev.bg/")

    # Parse the response using BeautifulSoup
    soup = BeautifulSoup(response.text, "html.parser")

    # Select the category links
    links = soup.select("a.show-all-jobs-cat, a.see-all")

    # Get the href attribute from each link and store in a list
    category_urls = [link["href"] for link in links]

    # Return the list of category URLs
    return category_urls

# Get job details
def get_job_details(link_soup):
    # Get the job description
    job_description_elem = link_soup.select_one("div.job_description")
    job_description = job_description_elem.text.strip().replace("\n\n\n", "\n").replace("\n\n", "\n") if job_description_elem else None

    # Get the job categories
    categories = []
    categories_elem = link_soup.select_one("div.categories-wrap")
    if categories_elem:
        category_tags = categories_elem.select("a.pill")
        for tag in category_tags:
            text = tag.text.strip()
            match = re.match(r"^(.+)\(\d+\)$", text)
            name = match.group(1).strip() if match else text
            categories.append(name)

    # Return the categories and job description
    return categories, job_description

# Scrape job listings for a given URL
def scrape_job_listings(url):
    # Initialize the list of job listings
    job_listings = []

    # Start with the first page
    page_counter = 2

    # Loop through all pages of the category
    while True:
        # Send a GET request to the category URL
        response = requests.get(url)

        # Parse the response using BeautifulSoup
        soup = BeautifulSoup(response.text, "html.parser")

        # Select all job listings on the page
        listings = soup.select("div.job-list-item")

        # Loop through each job listing and extract details
        for listing in listings:
            # Get the job location
            location_elem = listing.select_one("span.badge")
            location_text = location_elem.text.strip() if location_elem else None
            match = re.search(r"(\w+)\s*Hybrid", location_text) if location_text else None
            location = match.group(1) + ", Hybrid" if match else location_text

            # Get the job link
            link_elem = listing.select_one("a[href]")
            link = link_elem["href"] if link_elem else None

            # Get job details by following the link
            link_response = requests.get(link) if link else None
            link_soup = BeautifulSoup(link_response.text, "html.parser") if link_response else None
            categories, job_description = get_job_details(link_soup) if link_soup else (None, None)

            # Get the job salary
            salary_elem = listing.select_one("span.has-tooltip")
            salary_text = salary_elem.text.strip() if salary_elem else None
            salary_pattern = r"([\d ]+)\s*-\s*([\d ]+)\s*лв\."
            match = re.search(salary_pattern, salary_text) if salary_text else None
            
            salary = []
            min_salary = int(match.group(1).replace(" ", "")) if match else None
            max_salary = int(match.group(2).replace(" ", "")) if match else None

            salary = {
                "min": min_salary,
                "max": max_salary
            }

            # Create a dictionary for the job listing
            job = {
                "title": listing.select_one("h6.job-title").text.strip(),
                "company": listing.select_one("span.company-name").text.strip(),
                "location": location,
                "date": listing.select_one("span.date").text.strip(),
                "link": link,
                "categories": categories,
                "job_description": job_description,
                "salary": salary
            }

            # Append the job listing to the list
            job_listings.append(job)

        # Print the URL for debugging purposes
        print(url)

        # Check if there are more pages
        last_page_elem = soup.select_one("a.facetwp-page.last")
        last_page = int(last_page_elem["data-page"]) if last_page_elem else None
        if last_page and page_counter > last_page:
            break

        # Update the URL for the next page
        if "?_paged=" in url:
            page_counter+=1
            url = url.replace(f"_paged={page_counter - 1}", f"_paged={page_counter}")
        else:
            url += "?_paged=2"

    # Return the list of job listings
    return job_listings