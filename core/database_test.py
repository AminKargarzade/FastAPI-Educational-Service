from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.orm import sessionmaker, declarative_base

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
    first_name = Column(String(30))
    last_name = Column(String(30), nullable=True)
    age = Column(Integer)
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)

    def __repr__(self):
        return f"User(id={self.id}, first_name={self.first_name}, last_name={self.last_name})"


# to create tables and database
Base.metadata.create_all(engine)

session = SessionLocal()

# Inserting Data
# amin = User(first_name="amin", age="21")
# session.add(amin)
# session.commit()

# Bulk Insert
# andreas = User(first_name="andreas", age="25")
# rastin = User(first_name="rastin", age="22")
# users = [andreas, rastin]
# session.add_all(users)
# session.commit()

# Retrieve All Data
# users = session.query(User).all()  # returns all users
# print(users)

# Retrieve data with filter
user = session.query(User).filter_by(first_name="amin", age=21).first()


# Updating a record of data
# user.last_name = "Rastin"
# session.commit()

# Deleting a record of data
if user:
    session.delete(user)
    session.commit()
