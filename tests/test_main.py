from fastapi.testclient import TestClient
from app.main import app

# Create a test client object using FastAPI app
client = TestClient(app)

# Test the main route
def test_main():
    # Send a GET request to the root path
    response = client.get("/")
    # Assert the response status code is 200 (OK)
    assert response.status_code == 200
    # Assert the response content type is HTML
    assert "text/html" in response.headers["content-type"]
    # Assert the response body contains "Main Page" text
    assert "Main Page" in response.text

# Test the companies route
def test_index():
    # Send a GET request to the companies path
    response = client.get("/companies")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    # Assert the response body contains "Companies" text
    assert "Companies" in response.text

# Test the positions route
def test_loans():
    # Send a GET request to the positions path
    response = client.get("/positions")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    # Assert the response body contains "Positions" text
    assert "Positions" in response.text

# Test the search companies route
def test_search_companies():
    # Send a GET request to the search_companies path with a query parameter
    response = client.get("/search_companies?search=Strypes")
    assert response.status_code == 200
    # Assert the response JSON contains only 1 company
    assert len(response.json()["companies"]) == 1
    # Assert the response JSON contains the expected company name
    assert response.json()["companies"][0]["name"] == "Strypes"

    # Send a GET request to the search_companies path without a query parameter
    response = client.get("/search_companies")
    assert response.status_code == 200
    # Assert the response JSON contains at least one company
    assert len(response.json()["companies"]) > 0

# Test the search positions route
def test_search_positions():
    # Send a GET request to the search_positions path with a query parameter
    response = client.get("/search_positions?search=Senior%20Python%20Developer")
    assert response.status_code == 200
    # Assert the response JSON contains at least one position
    assert len(response.json()["positions"]) > 0
    
    # Send a GET request to the search_positions path without a query parameter
    assert response.status_code == 200
    # Assert the response JSON contains at least one position
    assert len(response.json()["positions"]) > 0
