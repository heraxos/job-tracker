
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
