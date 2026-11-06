from fastapi.testclient import TestClient
from sqlalchemy import select
from datetime import date
from app.main import app, get_db
from app.database import Base, create_test_database
from app.models import JobApplication

client = TestClient(app)

test_engine, TestSessionLocal = create_test_database()
Base.metadata.create_all(bind=test_engine)

def override_get_db():
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

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

    with TestSessionLocal() as db:
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

    with TestSessionLocal() as db:
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

    with TestSessionLocal() as db:
        application = db.scalar(
            select(JobApplication).where(
                JobApplication.company == company_name
            )
        )
        if application is not None:
            db.delete(application)
            db.commit()

def test_filter_by_status():
    company_name = "Filter Test Company"

    with TestSessionLocal() as db:
        application = JobApplication(
            company=company_name,
            position="Python Developer",
            status="Interview",
            applied_date=date.today()
        )

        db.add(application)
        db.commit()

    response = client.get("/?status=Interview")

    assert response.status_code == 200
    assert company_name in response.text
    assert "Собеседование" in response.text

    with TestSessionLocal() as db:
        application = db.scalar(
            select(JobApplication).where(
                JobApplication.company == company_name
            )
        )

        if application is not None:
            db.delete(application)
            db.commit()

def test_edit_application():
    company_name = "Edit Test Company"

    with TestSessionLocal() as db:
        application = JobApplication(
            company=company_name,
            position="Junior Developer",
            status="Applied",
            applied_date=date.today()
        )

        db.add(application)
        db.commit()
        application_id = application.id

    response = client.post(
        f"/applications/{application_id}/edit",
        data={
            "company": "Updated Test Company",
            "position": "Python Developer",
            "status": "Interview"
        },
        follow_redirects=False
    )

    assert response.status_code == 303

    with TestSessionLocal() as db:
        updated = db.get(JobApplication, application_id)

        assert updated is not None
        assert updated.company == "Updated Test Company"
        assert updated.position == "Python Developer"
        assert updated.status == "Interview"

        db.delete(updated)
        db.commit()

def test_delete_application():
    company_name = "Delete Test Company"

    with TestSessionLocal() as db:
        application = JobApplication(
            company=company_name,
            position="Python Developer",
            status="Applied",
            applied_date=date.today()
        )

        db.add(application)
        db.commit()
        application_id = application.id

    response = client.post(
        f"/applications/{application_id}/delete",
        follow_redirects=False
    )

    assert response.status_code == 303

    with TestSessionLocal() as db:
        deleted = db.get(JobApplication, application_id)
        assert deleted is None