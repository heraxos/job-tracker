
from sqlalchemy import String, Integer, Date
from sqlalchemy.orm import Mapped, mapped_column
from datetime import date

from app.database import Base


class JobApplication(Base):
    __tablename__ = "applications"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    company: Mapped[str] = mapped_column(String(100))
    position: Mapped[str] = mapped_column(String(150))
    status: Mapped[str] = mapped_column(
        String(50),
        default="Applied"
    )
    applied_date: Mapped[date] = mapped_column(Date)

    notes: Mapped[str | None] = mapped_column(
    	String(1000),
    	nullable=True
    )