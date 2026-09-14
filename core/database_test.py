from datetime import datetime

from sqlalchemy import (
    DateTime,
    Float,
    ForeignKey,
    create_engine,
    Column,
    Integer,
    String,
    Boolean,
    func,
    or_,
    and_,
    not_,
)
from sqlalchemy.orm import relationship, relationship, sessionmaker, declarative_base

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
    orders = relationship("Order", back_populates="user")

    def __repr__(self):
        return f"User(id={self.id}, first_name={self.first_name}, last_name={self.last_name})"


class Order(Base):
    __tablename__ = "order"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    total_amount = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="orders")


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

users_all = session.query(User).all()

# query all users with age greater than or equal to 25
users_filtered = session.query(User).filter(User.age >= 25).all()

print("ALL Users: ", len(users_all))
print("Filtered Users: ", len(users_filtered))

# add multiple filters
# query all users with age greater than or equal to 25 and name equals to something
users_filtered = session.query(User).filter(User.age >= 25, User.name == "ali").all()

# or you can use where
users_filtered = session.query(User).where(User.age >= 25, User.name == "ali").all()

# users with similar name containing specific substrings
users_similar_name = session.query(User).filter(User.name.like("%ali%")).all()

# users with case insensitive match
users_similar_name = session.query(User).filter(User.name.ilike("%ali%")).all()

# users with starting and ending chars
users_starting_ali = session.query(User).filter(User.name.like("Ali%")).all()
users_ending_ali = session.query(User).filter(User.name.like("%Ali")).all()


# query those who has ali as name or age above 25
users_filtered = (
    session.query(User).filter(or_(User.age >= 25, User.name == "ali")).all()
)

# query those who has ali as name and age above 25
users_filtered = (
    session.query(User).filter(and_(User.age >= 25, User.name == "ali")).all()
)

# query those who name is not ali
users_filtered = session.query(User).filter(not_(User.name == "ali")).all()

# getting users which are not named ali or age between 35,60
users = session.query(User).filter(
    or_(not_(User.name == "ali"), and_(User.age > 35, User.age < 60))
)


# 1. Count Total Users
total_users = session.query(func.count(User.id)).scalar()
print("Total Users:", total_users)

# 2. Find the Average Age of Users
average_age = session.query(func.avg(User.age)).scalar()
print("Average Age:", average_age)

# 3. Find the Maximum and Minimum Age
max_age = session.query(func.max(User.age)).scalar()
min_age = session.query(func.min(User.age)).scalar()
print(f"Max Age: {max_age}, Min Age: {min_age}")

# 4. Find the Total Number of Orders
total_orders = session.query(func.count(Order.id)).scalar()
print("Total Orders:", total_orders)

# 5. Find the Sum of All Order Amounts
total_revenue = session.query(func.sum(Order.total_amount)).scalar()
print("Total Revenue:", total_revenue)

# 6. Find the Average Order Value
average_order_value = session.query(func.avg(Order.total_amount)).scalar()
print("Average Order Value:", average_order_value)

# 7. Find Users Who Have Placed the Most Orders
most_active_users = (
    session.query(User.name, func.count(Order.id).label("order_count"))
    .join(Order)
    .group_by(User.id)
    .order_by(func.count(Order.id).desc())
    .limit(5)
    .all()
)
print("Top 5 Active Users by Order Count:", most_active_users)

# 8. Find Users with the Highest Total Spending
top_spenders = (
    session.query(User.name, func.sum(Order.total_amount).label("total_spent"))
    .join(Order)
    .group_by(User.id)
    .order_by(func.sum(Order.total_amount).desc())
    .limit(5)
    .all()
)
print("Top 5 Users by Spending:", top_spenders)

# 9. Find Users Who Have Not Placed Any Orders
users_without_orders = (
    session.query(User).outerjoin(Order).filter(Order.id == None).all()
)
print("Users Without Orders:", [user.name for user in users_without_orders])

# 10. Find the Most Recent Order Date
latest_order_date = session.query(func.max(Order.created_at)).scalar()
print("Most Recent Order Date:", latest_order_date)

# Close the session
session.close()


from sqlalchemy import text

# Example 1: Count Users with a Specific Condition (Raw SQL)
query = text("SELECT COUNT(*) FROM user WHERE age >= :min_age")
result = session.execute(query, {"min_age": 25}).scalar()
print("Users with age >= 25:", result)

# Example 2: Find the Average Age of Users (Raw SQL)
query = text("SELECT AVG(age) FROM user")
result = session.execute(query).scalar()
print("Average Age of Users:", result)

# Example 3: Get Users with a Specific Name (Raw SQL)
query = text("SELECT * FROM user WHERE name = :name")
result = session.execute(query, {"name": "Ali"}).fetchall()
print("Users named Ali:", [user.name for user in result])

# Example 4: Aggregate Query for the Total Revenue (Raw SQL)
query = text("SELECT SUM(total_amount) FROM order")
result = session.execute(query).scalar()
print("Total Revenue:", result)


# 1. محاسبه تعداد سفارش‌ها برای هر کاربر
users_order_count = (
    session.query(User.id, User.name, func.count(Order.id).label("order_count"))
    .join(Order)
    .group_by(User.id)
    .all()
)

for user in users_order_count:
    print(f"User: {user.name}, Order Count: {user.order_count}")


# 2. محاسبه مجموع مبلغ سفارش‌ها برای هر کاربر
users_total_spent = (
    session.query(User.id, User.name, func.sum(Order.total_amount).label("total_spent"))
    .join(Order)
    .group_by(User.id)
    .all()
)

for user in users_total_spent:
    print(f"User: {user.name}, Total Spent: {user.total_spent}")
