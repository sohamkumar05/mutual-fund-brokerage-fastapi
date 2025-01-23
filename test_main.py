import pytest
from fastapi.testclient import TestClient
from main import app
from unittest.mock import patch

client = TestClient(app)

# Utility to mock the JWT token generator for login & register
def mock_generate_jwt_token(payload):
    return "mocked_jwt_token"

# Mock API responses
def mock_call_api(payload):
    if "Mutual_Fund_Family" in payload:
        return [{"Mutual_Fund_Family": "Family A"}, {"Mutual_Fund_Family": "Family B"}]
    if "Scheme_Code" in payload:
        return [{"Scheme_Code": 123456, "Net_Asset_Value": 100}]
    return [
        {
            "Scheme_Code": 125502,
            "ISIN_Div_Payout_ISIN_Growth": "-",
            "ISIN_Div_Reinvestment": "INF200K01V16",
            "Scheme_Name": "SBI Banking & PSU Fund - Direct Plan - Daily Income Distribution cum Capital Withdrawal Option (IDCW)",
            "Net_Asset_Value": 1398.4709,
            "Date": "22-Jan-2025",
            "Scheme_Type": "Open Ended Schemes",
            "Scheme_Category": "Debt Scheme - Banking and PSU Fund",
            "Mutual_Fund_Family": "SBI Mutual Fund"
        },
        {
            "Scheme_Code": 125503,
            "ISIN_Div_Payout_ISIN_Growth": "INF200K01V08",
            "ISIN_Div_Reinvestment": "-",
            "Scheme_Name": "SBI BANKING & PSU FUND - Direct Plan - Growth",
            "Net_Asset_Value": 3174.9311,
            "Date": "22-Jan-2025",
            "Scheme_Type": "Open Ended Schemes",
            "Scheme_Category": "Debt Scheme - Banking and PSU Fund",
            "Mutual_Fund_Family": "SBI Mutual Fund"
        },
        {
            "Scheme_Code": 125505,
            "ISIN_Div_Payout_ISIN_Growth": "INF200K01V40",
            "ISIN_Div_Reinvestment": "INF200K01V57",
            "Scheme_Name": "SBI Banking & PSU Fund - Direct Plan - Monthly Income Distribution cum Capital Withdrawal Option (IDCW)",
            "Net_Asset_Value": 1277.9379,
            "Date": "22-Jan-2025",
            "Scheme_Type": "Open Ended Schemes",
            "Scheme_Category": "Debt Scheme - Banking and PSU Fund",
            "Mutual_Fund_Family": "SBI Mutual Fund"
        }
    ]

# Test registration
@pytest.fixture
def register_data():
    return {
        "name": "Test User",
        "email": "test@example.com",
        "password": "testpassword123"
    }

@patch('main.call_api', mock_call_api)
def test_register(register_data):
    response = client.post("/register", json=register_data)
    assert response.status_code == 200
    assert "token" in response.json()

# Test login
@pytest.fixture
def login_data():
    return {
        "email": "test@example.com",
        "password": "testpassword123"
    }

@patch('main.call_api', mock_call_api)
def test_login(login_data):
    response = client.post("/login", json=login_data)
    assert response.status_code == 200
    assert "token" in response.json()

# Test getting fund families
@patch('main.call_api', mock_call_api)
def test_get_fund_families(login_data):
    response = client.post("/login", json=login_data)
    res = client.get("/fund-families", headers={"Authorization": f"Bearer {response.json()['token']}"})
    assert res.status_code == 200
    assert "fund_families" in res.json()
    assert len(res.json()["fund_families"]) > 0

# Test getting all schemes
@patch('main.call_api', mock_call_api)
def test_get_all_schemes(login_data):
    response = client.post("/login", json=login_data)
    response = client.get("/schemes?mutual_fund_family=Family A", headers={"Authorization": f"Bearer {response.json()['token']}"})
    assert response.status_code == 200
    assert "schemes" in response.json()
    assert len(response.json()["schemes"]) >= 0


# Test investing in a scheme
@pytest.fixture
def portfolio_data():
    return {
        "scheme_code": "123456"
    }

@patch('main.call_api', mock_call_api)
def test_invest_in_scheme(portfolio_data, login_data):
    res = client.post("/login", json=login_data)
    response = client.post("/portfolio", headers={"Authorization": f"Bearer {res.json()['token']}"}, json=portfolio_data)
    assert response.status_code == 200
    assert "message" in response.json()
    assert response.json()["message"] == "Scheme successfully added to portfolio."

# Test getting user portfolio
@patch('main.call_api', mock_call_api)
def test_get_portfolio(login_data):
    res = client.post("/login", json=login_data)
    response = client.get("/portfolio", headers={"Authorization": f"Bearer {res.json()['token']}"})
    assert response.status_code == 200
    assert "investments" in response.json()
    assert "total_value" in response.json()
    assert "percentage_increase" in response.json()


# Test withdrawing from a scheme
def test_withdraw_from_scheme(portfolio_data, login_data):
    res = client.post("/login", json=login_data)
    response = client.delete(f"/portfolio/{portfolio_data['scheme_code']}", headers={"Authorization": f"Bearer {res.json()['token']}"})
    assert response.status_code == 200
    assert "message" in response.json()
    assert response.json()["message"] == "Scheme successfully removed from portfolio."
