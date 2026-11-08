\# Job Tracker



A web application for tracking job applications and managing the job search process.



\*\*Live Demo:\*\* \[Job Tracker](https://job-tracker-0dyz.onrender.com)



\## Features



\- Add new job applications

\- View all applications

\- Edit application details

\- Delete applications

\- Search applications by company name or job title

\- Filter applications by status

\- Combine search and status filters

\- Dashboard with application statistics:

&#x20; - Total applications

&#x20; - Interviews

&#x20; - Offers

\- Persistent PostgreSQL database in production

\- SQLite support for local development

\- Automated tests with a separate test database



\## Technologies



\- \*\*Python 3.12\*\*

\- \*\*FastAPI\*\* — web framework

\- \*\*SQLAlchemy\*\* — ORM and database management

\- \*\*PostgreSQL\*\* — production database

\- \*\*Neon\*\* — serverless PostgreSQL hosting

\- \*\*SQLite\*\* — local development and testing

\- \*\*Jinja2\*\* — HTML templating

\- \*\*HTML / CSS\*\* — frontend

\- \*\*Pytest\*\* — automated testing

\- \*\*Render\*\* — application hosting



\## Architecture



The application uses FastAPI for its backend and SQLAlchemy for database operations.



\- In local development, the application uses SQLite by default.

\- In production, it connects to PostgreSQL using the `DATABASE\_URL` environment variable.

\- Neon hosts the production PostgreSQL database.

\- Render hosts the web application.



\## Installation



\### 1. Clone the repository



```bash

git clone https://github.com/heraxos/job-tracker.git

cd job-tracker

```



\### 2. Create a virtual environment



```bash

python -m venv .venv

```



Activate it on Windows:



```cmd

.venv\\Scripts\\activate

```



\### 3. Install dependencies



```bash

pip install -r requirements.txt

```



\### 4. Configure the database



By default, the application uses a local SQLite database.



To connect to PostgreSQL, set the `DATABASE\_URL` environment variable.



For local PostgreSQL configuration, you can create a `.env.local` file in the project root:



```env

DATABASE\_URL=your\_database\_connection\_string

```



Do not commit database credentials or `.env.local` to Git.



\### 5. Run the application



```bash

uvicorn app.main:app --reload

```



Open http://127.0.0.1:8000 in your browser.



\## Running Tests



Run the automated test suite:



```bash

pytest

```



Tests use a separate SQLite database to avoid modifying the application database.



\## Deployment



The application is deployed on \*\*Render\*\* and uses \*\*Neon PostgreSQL\*\* for persistent data storage.



\- Hosting: Render

\- Database: Neon PostgreSQL

\- Configuration: `DATABASE\_URL` environment variable



\*\*Live Application:\*\* https://job-tracker-0dyz.onrender.com



\## Screenshots



\### Dashboard



!\[Job Tracker Dashboard](screenshots/dashboard.png)



\### Dashboard — Detailed View



!\[Job Tracker Dashboard 2](screenshots/dashboard2.png)
