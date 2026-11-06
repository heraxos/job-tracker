
from datetime import date

from fastapi import FastAPI, Request, Form
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy import select, func

from app.database import engine, Base, SessionLocal
from app.models import JobApplication

app = FastAPI(title="Job Tracker")

Base.metadata.create_all(bind=engine)

app.mount(
    "/static",
    StaticFiles(directory="app/static"),
    name="static"
)

templates = Jinja2Templates(directory="app/templates")


@app.get("/")
async def home(request: Request):
    with SessionLocal() as db:
        applications = db.scalars(
            select(JobApplication).order_by(
                JobApplication.id.desc()
            )
        ).all()

        total = len(applications)
        interviews = sum(
            item.status == "Interview" for item in applications
        )
        offers = sum(
            item.status == "Offer" for item in applications
        )

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "applications": applications,
            "total": total,
            "interviews": interviews,
            "offers": offers
        }
    )


@app.post("/applications")
async def add_application(
    company: str = Form(...),
    position: str = Form(...),
    status: str = Form(...),
):
    with SessionLocal() as db:
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
    application_id: int
):
    with SessionLocal() as db:
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
    status: str = Form(...)
):
    with SessionLocal() as db:
        application = db.get(JobApplication, application_id)

        if application is None:
            return {"error": "Вакансия не найдена"}

        application.company = company
        application.position = position
        application.status = status

        db.commit()

    return RedirectResponse("/", status_code=303)

@app.post("/applications/{application_id}/delete")
async def delete_application(application_id: int):
    with SessionLocal() as db:
        application = db.get(JobApplication, application_id)

        if application is not None:
            db.delete(application)
            db.commit()

    return RedirectResponse("/", status_code=303)