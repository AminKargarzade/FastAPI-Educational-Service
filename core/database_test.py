from sqlalchemy import (
    ForeignKey,
    create_engine,
    Column,
    Integer,
    String,
    Boolean,
)
from sqlalchemy.orm import relationship, sessionmaker, declarative_base

SQLALCHEMY_DATABASE_URL = "sqlite:///./sqlite.db"
# SQLALCHEMY_DATABASE_URL = "sqlite:///./memory:"

# for postgres or other relational databases
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver:port/db_name"
# SQLALCHEMY_DATABASE_URL = "mysql://username:password@localhost:port/db_name"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},  # only for sqlite
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# create base class for declaring tables
Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(30))
    email = Column(String())
    password = Column(String())
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)

    adresses = relationship("Address", backref="user")

    def __repr__(self):
        return f"User(id={self.id}, username={self.username}, email={self.email}, is_active={self.is_active}, is_verified={self.is_verified})"


class Address(Base):
    __tablename__ = "addresses"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"))

    city = Column(String())
    state = Column(String())
    zip_code = Column(String())

    # user = relationship("User", back_populates="addresses") backref will create this field automatically, so we don't need to define it explicitly.

    def __repr__(self):
        return f"Address(id={self.id}, user_id={self.user_id}, city={self.city}, state={self.state}, zip_code={self.zip_code})"


# to create tables and database
Base.metadata.create_all(engine)

session = SessionLocal()


# session.add(User(username="AminRastin", email="aminkargarzadeh26@gmail.com", password="hashed_password"))
# session.commit()

user = session.query(User).filter_by(username="AminRastin").one_or_none()

# addresses = [
#     Address(user_id=user.id, city="New York", state="NY", zip_code="10001"),
#     Address(user_id=user.id, city="Los Angeles", state="CA", zip_code="90210")
# ]

# session.add_all(addresses)
# session.commit()
# print(user.adresses)  # Accessing the related Address objects through the relationship
address = (
    session.query(Address).filter_by(user_id=user.id, city="New York").one_or_none()
)
print(
    address.user.username
)  # Accessing the related User object through the relationship
