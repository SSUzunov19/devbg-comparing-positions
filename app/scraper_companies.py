import requests
from bs4 import BeautifulSoup
import re

# Defining a function to scrape company information
def scrape_companies():
    # Sending a request to the website URL
    response = requests.get("https://dev.bg/company/")
    # Parsing the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.text, "html.parser")
    # Extracting all the div elements with class 'company-list-item'
    company_list_items = soup.select("div.company-list-item")
    # Creating an empty list to store the details of all companies
    companies = []

    # Looping through each company list item
    for item in company_list_items:
        # Extracting the company name and its URL link from the company list item
        name = item.select_one("h6.company-name").text.strip()
        link = item.select_one("a[href]")["href"]
        
        # Sending a request to the URL of the company and parsing its HTML content
        response = requests.get(link)
        soup = BeautifulSoup(response.text, "html.parser")
        # Extracting the description of the company from the HTML content
        description = soup.select_one("div.box-row.company-info-1").text.strip()

        # Extracting the company's activities from the description
        activity_pattern = re.compile(r'Дейности\n(.*?)\n\n', re.DOTALL)
        try:
            activity = re.search(activity_pattern, description).group(1)
        except AttributeError:
            activity = None

        # Extracting the sector of the company from the description
        sector_pattern = re.compile(r'Сектор \n(.*?)\n\n', re.DOTALL)
        try:
            sector = re.search(sector_pattern, description).group(1).strip()
        except AttributeError:
            sector = None

        # Extracting the central office of the company from the description
        central_office_pattern = re.compile(r'Централен офис\n(.*?)$', re.DOTALL)
        try:
            central_office = re.search(central_office_pattern, description).group(1)
        except AttributeError:
            central_office = None

        # Extracting the technologies used by the company
        technologies_div = soup.find('div', id='technologies')
        if technologies_div:
            tags = technologies_div.find_all('div', {'class': 'tag-name'})
            technologies = [tag.text for tag in tags]
        else:
            technologies = []

        # Extracting other company information from the HTML content
        company_info_divs = soup.find_all('div', {'class': 'box-company-info'})
        company_info = {}
        company_info_counter = 0
        for div in company_info_divs:
            try:
                value = div.find('p', {'class': 'bold'}).text.strip()
            except AttributeError:
                value = None
            company_info[company_info_counter] = value
            company_info_counter+=1

        # Creating a dictionary to store all the details of a company
        company = {
            "name": name,
            "link": link,
            "activity": activity,
            "sector": sector,
            "central_office": central_office,
            "technologies": technologies,
            "year_of_establishment": company_info.get(0),
            "global_employees": company_info.get(1),
            "established_in_bulgaria": company_info.get(2),
            "employees_in_bulgaria": company_info.get(3),
            "offices_in_bulgaria": company_info.get(4),
            "iT_employees_in_bulgaria": company_info.get(5)
        }

        print(company)

        # Adding the dictionary to the list of companies
        companies.append(company)


    # Returning the list of all the companies' details
    return companies