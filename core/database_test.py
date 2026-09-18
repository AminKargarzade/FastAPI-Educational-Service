from datetime import datetime

from sqlalchemy import (
    DateTime,
    ForeignKey,
    Text,
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
    posts = relationship("Post", backref="user")
    comments = relationship("Comment", backref="user")
    profile = relationship(
        "Profile", backref="user", uselist=False
    )  # uselist=False indicates a one-to-one relationship

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


class Profile(Base):
    __tablename__ = "profiles"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)
    # Alternative best practice
    # user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)  # This will make user_id the primary key of the Profile table, ensuring a one-to-one relationship with the User table.

    first_name = Column(String())
    last_name = Column(String())
    bio = Column(Text(), nullable=True)

    def __repr__(self):
        return f"Profile(id={self.id}, user_id={self.user_id}, first_name={self.first_name}, last_name={self.last_name}, bio={self.bio})"


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    title = Column(String())
    content = Column(Text())

    comments = relationship("Comment", backref="post")

    created_date = Column(DateTime(), default=datetime.now)
    updated_date = Column(DateTime(), default=datetime.now, onupdate=datetime.now)

    def __repr__(self):
        return f"Post(id={self.id}, user_id={self.user_id}, title={self.title}, content={self.content})"


from sqlalchemy.orm import backref


class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, autoincrement=True)
    post_id = Column(Integer, ForeignKey("posts.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    parent_id = Column(
        Integer, ForeignKey("comments.id"), nullable=True
    )  # self-referential foreign key for nested comments

    # parent = relationship(
    #     "Comment", back_populates="children", remote_side=[id]
    # )  # relationship for nested comments
    children = relationship(
        "Comment", backref=backref("parent", remote_side=[id])
    )  # relationship for nested comments

    content = Column(Text())

    created_date = Column(DateTime(), default=datetime.now)
    updated_date = Column(DateTime(), default=datetime.now, onupdate=datetime.now)

    def __repr__(self):
        return f"Comment(id={self.id}, post_id={self.post_id}, user_id={self.user_id}, parent_id={self.parent_id}, content={self.content})"


# to create tables and database
Base.metadata.create_all(engine)

session = SessionLocal()

user = session.query(User).filter_by(username="AminRastin").one_or_none()
post = user.posts[0]

comments = session.query(Comment).filter_by(post_id=post.id, parent_id=None).all()

for comment in comments:
    print(comment.children)
