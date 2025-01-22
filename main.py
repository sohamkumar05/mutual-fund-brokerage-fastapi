from fastapi import FastAPI

app = FastAPI()


@app.post("/register")
def register():
    pass


@app.post("/login")
def login():
    pass


@app.get("/fund-families")
def get_fund_families():
    pass


@app.get("/schemes")
def get_all_schemes():
    pass


@app.get("/portfolio")
def get_portfolio():
    pass


@app.post("/portfolio")
def invest_in_scheme():
    pass


@app.delete("/portfolio")
def withdraw_from_scheme():
    pass
