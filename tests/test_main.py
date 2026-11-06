from fastapi.testclient import TestClient
from sqlalchemy import select
from datetime import date
from app.main import app
from app.database import SessionLocal
from app.models import JobApplication

client = TestClient(app)


def test_homepage():
    response = client.get("/")

    assert response.status_code == 200
    assert "Job Tracker" in response.text


def test_add_application():
    company_name = "Pytest Test Company"

    response = client.post(
        "/applications",
        data={
            "company": company_name,
            "position": "Python Developer",
            "status": "Applied"
        },
        follow_redirects=False
    )

    assert response.status_code == 303

    with SessionLocal() as db:
        application = db.scalar(
            select(JobApplication).where(
                JobApplication.company == company_name
            )
        )

        assert application is not None
        assert application.position == "Python Developer"

        db.delete(application)
        db.commit()

def test_search_application():
    company_name = "Search Test Company"

    with SessionLocal() as db:
        application = JobApplication(
            company=company_name,
            position="Junior Python Developer",
            status="Applied",
	    applied_date=date.today()
        )
        db.add(application)
        db.commit()

    response = client.get("/?search=Search+Test+Company")

    assert response.status_code == 200
    assert company_name in response.text
    assert "Junior Python Developer" in response.text

    with SessionLocal() as db:
        application = db.scalar(
            select(JobApplication).where(
                JobApplication.company == company_name
            )
        )
        if application is not None:
            db.delete(application)
            db.commit()