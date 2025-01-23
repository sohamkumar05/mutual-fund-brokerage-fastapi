# mutual-fund-brokerage-fastapi

## Steps to setup:
1. Clone the repository. You can use command `git clone https://github.com/sohamkumar05/mutual-fund-brokerage-fastapi.git`.
2. Add all the environment variables in the `.env` file
```
DB_HOST=
DB_USER=
DB_PASSWORD=
DB_NAME=
RAPID_API_KEY=
RAPID_API_HOST=
JWT_SECRET=
```
3. Create and activate the Python virtual environment. To create and activate a Python virtual environment, run `python -m venv venv` in the terminal, then activate it with `venv\Scripts\activate` on Windows or `source venv/bin/activate` on Linux.
4. Install all Python dependencies with the command `pip install -r requirements.txt`.
5. Run the queries from **setup.sql** to setup the database.
6. Launch the application with the command `fastapi run`.

Tests can be run using **pytest** command.
API collection can be imported from the file **Mutual Fund Brokerage FastAPI.postman_collection.json**.