# Task Management
This is a Python application utilizing FastAPI, Alembic, PostgreSQL and SQLAlchemy
## Database
![alt text](/assets/db_er_disgram.png)
## Requirements
- python3
- pip3
- postgresql
## Set Up
Follow these steps to set up the project on your local machine:

1. Create a `.env` file by referencing the `.env.example` file. Fill in the values for each environment variable specified there.
2. **Database Configuration**:
   - Create an `alembic.ini` file by referencing the `alembic.ini.example` file. Replace `<DB_URL>` with your actual database URL.
3. **Install Dependencies and Set Up Database**:
   - Run the following command to set up your python virtual environment, install necessary libraries from `requirements.txt`, and perform database migrations with Alembic:
     ```bash
     make setup
     ```
4. **Start the Server**:
   - To start the server, run:
     ```bash
     make start
     ```
5. **Access the API Documentation**:
   - After starting the server, you can access the API documentation and interact with the API through Swagger UI at:
     [http://localhost:8000/docs](http://localhost:8000/docs)
6. **Tear down Database**:
   - To tear down the database after you're finished, run:
     ```bash
     make tear_down
     ```
