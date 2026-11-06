from datetime import date

from fastapi import FastAPI, Request, Form, Depends
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy import select, or_

from app.database import engine, Base, SessionLocal
from sqlalchemy.orm import Session
from app.models import JobApplication

app = FastAPI(title="Job Tracker")

Base.metadata.create_all(bind=engine)

app.mount(
    "/static",
    StaticFiles(directory="app/static"),
    name="static"
)

templates = Jinja2Templates(directory="app/templates")
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
async def home(
    request: Request,
    search: str = "",
    status: str = "",
    db: Session = Depends(get_db)
):
    all_applications = db.scalars(
        select(JobApplication)
    ).all()

    statement = select(JobApplication).order_by(
        JobApplication.id.desc()
    )

    if search.strip():
        pattern = f"%{search.strip()}%"

        statement = statement.where(
            or_(
                JobApplication.company.ilike(pattern),
                JobApplication.position.ilike(pattern)
            )
        )

    if status:
        statement = statement.where(
            JobApplication.status == status
        )

    applications = db.scalars(statement).all()

    total = len(all_applications)
    interviews = sum(
        item.status == "Interview" for item in all_applications
    )
    offers = sum(
        item.status == "Offer" for item in all_applications
    )

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "applications": applications,
            "total": total,
            "interviews": interviews,
            "offers": offers,
            "search": search,
            "status": status
        }
    )


@app.post("/applications")
async def add_application(
    company: str = Form(...),
    position: str = Form(...),
    status: str = Form(...),
    db: Session = Depends(get_db)
):
    application = JobApplication(
        company=company,
        position=position,
        status=status,
        applied_date=date.today()
    )

    db.add(application)
    db.commit()

    return RedirectResponse("/", status_code=303)


@app.get("/applications/{application_id}/edit")
async def edit_application_page(
    request: Request,
    application_id: int,
    db: Session = Depends(get_db)
):
    application = db.get(JobApplication, application_id)

    if application is None:
        return templates.TemplateResponse(
            request=request,
            name="index.html",
            context={
                "applications": [],
                "total": 0,
                "interviews": 0,
                "offers": 0,
                "error": "Вакансия не найдена"
            },
            status_code=404
        )

    return templates.TemplateResponse(
        request=request,
        name="edit.html",
        context={"application": application}
    )


@app.post("/applications/{application_id}/edit")
async def update_application(
    application_id: int,
    company: str = Form(...),
    position: str = Form(...),
    status: str = Form(...),
    db: Session = Depends(get_db)
):
    application = db.get(JobApplication, application_id)

    if application is None:
        return {"error": "Вакансия не найдена"}

    application.company = company
    application.position = position
    application.status = status

    db.commit()

    return RedirectResponse("/", status_code=303)

@app.post("/applications/{application_id}/delete")
async def delete_application(
    application_id: int,
    db: Session = Depends(get_db)
):
    application = db.get(JobApplication, application_id)

    if application is not None:
        db.delete(application)
        db.commit()

    return RedirectResponse("/", status_code=303)
