from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Float, DateTime
from sqlalchemy.orm import sessionmaker, declarative_base, relationship
from .config import settings

engine = create_engine(
    settings.SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}  # only for sqlite
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# create base class for declaring tables
Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50))

    transactions = relationship("Transaction", back_populates="user")


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50))
    type = Column(String(10))  # income / expense

    transactions = relationship("Transaction", back_populates="category")


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    category_id = Column(Integer, ForeignKey("categories.id"))
    amount = Column(Float)
    type = Column(String(10))  # income or expense
    date = Column(DateTime)
    description = Column(String(255))

    user = relationship("User", back_populates="transactions")
    category = relationship("Category", back_populates="transactions")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
