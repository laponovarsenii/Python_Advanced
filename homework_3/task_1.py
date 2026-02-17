from sqlalchemy import (
    create_engine,
    Integer,
    String,
    Boolean,
    Numeric,
    ForeignKey,
)
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship,
    sessionmaker,

)

from db_connection import *
from pathlib import Path


BASE_DIR = Path(__file__).parents[0]
# print(__file__)
# print(BASE_DIR)

DATABASE_URL = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}"

engine = create_engine(DATABASE_URL, echo=False)


SessionLocal = sessionmaker(bind=engine)
session = SessionLocal()



class Base(DeclarativeBase):
    pass


class Category(Base):
    __tablename__ = "categories"


    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    name: Mapped[str] = mapped_column(String(100), nullable=False)

    description: Mapped[str | None] = mapped_column(String(255))

    products: Mapped[list["Product"]] = relationship(back_populates="category")



class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    name: Mapped[str] = mapped_column(String(100), nullable=False)

    price: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)

    in_stock: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)


    category_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("categories.id"),
        nullable=False,
    )
    category: Mapped[Category] = relationship(back_populates="products")


Base.metadata.create_all(bind=engine)