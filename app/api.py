from fastapi import FastAPI
from app.scraper_companies import scrape_companies
from app.scraper_positions import scrape_job_categories
from app.database import mydb

# Create a FastAPI instance
app = FastAPI()

# Define a route to scrape companies and store them in the database
@app.get("/get/companies")
def get_companies():
    # Scrape companies
    companies = scrape_companies()

    # Create a cursor to execute SQL queries
    cursor = mydb.cursor()

    # Insert or update each company in the database
    for i, company in enumerate(companies):
        print(f"Inserting or updating company {i+1} of {len(companies)}...")
        sql = """
        INSERT INTO companies (
            name,
            link,
            activity,
            sector,
            central_office,
            technologies,
            year_of_establishment,
            global_employees,
            established_in_bulgaria,
            employees_in_bulgaria,
            offices_in_bulgaria,
            iT_employees_in_bulgaria,
            is_deleted
        ) VALUES (
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, FALSE
        ) ON DUPLICATE KEY UPDATE
            activity = VALUES(activity),
            sector = VALUES(sector),
            central_office = VALUES(central_office),
            technologies = VALUES(technologies),
            year_of_establishment = VALUES(year_of_establishment),
            global_employees = VALUES(global_employees),
            established_in_bulgaria = VALUES(established_in_bulgaria),
            employees_in_bulgaria = VALUES(employees_in_bulgaria),
            offices_in_bulgaria = VALUES(offices_in_bulgaria),
            iT_employees_in_bulgaria = VALUES(iT_employees_in_bulgaria),
            is_deleted = FALSE
        """
        values = (
            company["name"],
            company["link"],
            company["activity"],
            company["sector"],
            company["central_office"],
            ",".join(company["technologies"]),
            company["year_of_establishment"],
            company["global_employees"],
            company["established_in_bulgaria"],
            company["employees_in_bulgaria"],
            company["offices_in_bulgaria"],
            company["iT_employees_in_bulgaria"]
        )
        cursor.execute(sql, values)

    # Commit changes to the database
    mydb.commit()
    print("Done inserting or updating companies.")

    # Return the list of scraped companies
    return companies


# Define a route to scrape job positions and store them in the database
@app.get("/get/positions")
def get_positions():
    # Scrape job positions
    positions = scrape_job_categories()

    cursor = mydb.cursor()
    
    # Insert or update jobs from the scrape
    for position in positions:
        print(f"Inserting or updating job {position['title']}...")
        sql = """
        INSERT INTO jobs (
            title,
            company,
            location,
            date,
            link,
            categories,
            job_description,
            min_salary,
            max_salary,
            is_deleted
        ) VALUES (
            %s, %s, %s, %s, %s, %s, %s, %s, %s, FALSE
        ) ON DUPLICATE KEY UPDATE
            company = VALUES(company),
            location = VALUES(location),
            date = VALUES(date),
            categories = VALUES(categories),
            job_description = VALUES(job_description),
            min_salary = VALUES(min_salary),
            max_salary = VALUES(max_salary),
            is_deleted = FALSE
        """
        values = (
            position["title"],
            position["company"],
            position["location"],
            position["date"],
            position["link"],
            ",".join(position["categories"]),
            position["job description"],
            position["salary"]["min"],
            position["salary"]["max"]
        )
        cursor.execute(sql, values)

    # Commit changes to the database and print a message when done inserting or updating jobs
    mydb.commit()
    print("Done inserting or updating jobs.")

    return positions

# Define two endpoints to display companies and positions from the database
@app.get("/show/companies")
def show_companies():
    # Retrieve companies from the database and return as a dictionary
    cursor = mydb.cursor(dictionary=True)
    cursor.execute("SELECT * FROM companies")
    companies = cursor.fetchall()
    return {"companies": companies}

@app.get("/show/positions")
def show_positions():
    # Retrieve positions from the database and return as a dictionary
    cursor = mydb.cursor(dictionary=True)
    cursor.execute("SELECT * FROM jobs")
    positions = cursor.fetchall()
    return {"positions": positions}
