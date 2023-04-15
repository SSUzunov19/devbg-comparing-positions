from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from app.api import app as api_app
from app.database import mydb

app = FastAPI()

# Mount the static directory to serve static files
app.mount("/static", StaticFiles(directory="./static"), name="static")

# Mount the API sub-app
app.mount("/api", api_app)

# Create an instance of the Jinja2 templates engine
templates = Jinja2Templates(directory="./templates")

# Define a route for the home page
@app.get("/", response_class=HTMLResponse)
def main(request: Request):
    # Render the HTML template using Jinja2
    return templates.TemplateResponse("index.html", {"request": request})

# Define a route for counting open positions
@app.get("/count_open_positions", response_class=JSONResponse)
def count_open_positions():
    # Create a cursor to execute SQL queries on the database
    cursor = mydb.cursor()

    # Define the SQL query to count open positions by location
    sql = "SELECT location, COUNT(*) as count FROM jobs WHERE is_deleted = 0 GROUP BY location"

    # Execute the SQL query
    cursor.execute(sql)

    # Fetch the results
    result = cursor.fetchall()

    # Create a list of dictionaries to hold the city counts
    city_counts = []

    # Loop through the results and append them to the city counts list
    for row in result:
        city_counts.append({'city': row[0], 'count': row[1]})

    # Return the city counts as a JSON response
    return {'city_counts': city_counts}

# Define a route for the companies page
@app.get("/companies", response_class=HTMLResponse)
def index(request: Request):
    # Render the HTML template using Jinja2
    return templates.TemplateResponse("companies.html", {"request": request})

# Define a route for the positions page
@app.get("/positions", response_class=HTMLResponse)
def loans(request: Request):
    # Render the HTML template using Jinja2
    return templates.TemplateResponse("positions.html", {"request": request})

# Define a route for searching companies
@app.get("/search_companies", response_class=JSONResponse)
def search_companies(search: str = ''):
    # Create a cursor to execute SQL queries on the database
    cursor = mydb.cursor()

    # Define the SQL query to search for companies by name
    if search.strip():
        sql = "SELECT * FROM companies WHERE name LIKE %s"
        # Surround the search term with '%' to match any characters before and after the search term
        values = ('%' + search + '%',)
    else:
        sql = "SELECT * FROM companies"
        values = ()

    # Execute the SQL query
    cursor.execute(sql, values)

    # Fetch the results
    result = cursor.fetchall()

    # Create a list of dictionaries to hold the companies
    companies = []

    # Loop through the results and append them to the companies list
    for company in result:
        companies.append({
            'name': company[1],
            'link': company[2],
            'activity': company[3],
            'sector': company[4],
            'central_office': company[5],
            'technologies': company[6].split(",") if company[6] else [],
            'year_of_establishment': company[7],
            'global_employees': company[8],
            'established_in_bulgaria': company[9],
            'employees_in_bulgaria': company[10],
            'offices_in_bulgaria': company[11],
            'iT_employees_in_bulgaria': company[12],
        })

    # Return the companies as a JSON response
    return {'companies': companies}

@app.get("/search_positions", response_class=JSONResponse)
def search_positions(search: str = ''):
    # Create a cursor to execute SQL queries on the database
    cursor = mydb.cursor()
    # Define the SQL query to search for positions by title
    if search.strip():
        sql = "SELECT * FROM jobs WHERE title LIKE %s"
        # Surround the search term with '%' to match any characters before and after the search term
        values = ('%' + search + '%',)
    else:
        sql = "SELECT * FROM jobs"
        values = ()

    # Execute the SQL query
    cursor.execute(sql, values)

    # Fetch the results
    result = cursor.fetchall()

    # Create a list of dictionaries to hold the positions
    positions = []

    # Loop through the results and append them to the positions list
    for position in result:
        positions.append({
            'title': position[1],
            'company': position[2],
            'location': position[3],
            'date': position[4],
            'link': position[5],
            'categories': position[6].split(",") if position[6] else [],
            'job_description': position[7],
            'min_salary': position[8],
            'max_salary': position[9]
        })

    # Return the positions as a JSON response
    return {'positions': positions}

