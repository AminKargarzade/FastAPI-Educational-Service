from fastapi import (
    Depends,
    FastAPI,
    Query,
    status,
    HTTPException,
    Path,
    Form,
    Body,
    File,
    UploadFile,
)

# from typing import Annotated, Optional
from fastapi.responses import JSONResponse
import random
from typing import List
from database import Base, engine, get_db, Person
from sqlalchemy.orm import Session

from contextlib import asynccontextmanager
from schemas import PersonCreateSchema, PersonResponseSchema, PersonUpdateSchema


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Application Startup babay")
    yield
    print("Application ShutDown honey")


app = FastAPI(lifespan=lifespan)


# @app.on_event("startup")
# async def startup_event():
#     print("starting the application")
# This is used before the version    ^
# 0.95.00 now we have something new  | (Lookup)
# that is called (lifespan)          |
# @app.on_event("shutdown")
# async def shutdown_event():
#     print("shuttingdown the application")


# /names (GET(RETRIEVE), POST(CREATE))
@app.get("/names", response_model=List[PersonResponseSchema])
# def retrieve_names_list(q : str | None = None):
# def retrieve_names_list(q : Optional[str] = None):
# def retrieve_names_list(q : Annotated[str | None, Query(max_length=50)] = None):
def retrieve_names_list(
    q: str | None = Query(
        deprecated=True,
        alias="search",
        description="it will be searched with the name you provided",
        example="Andreas",
        default=None,
        max_length=50,
    ),
    db: Session = Depends(get_db),
):

    query = db.query(Person)
    if q:
        query = query.filter_by(name=q)
    result = query.all()
    # if q:
    #     return [
    #         item for item in names_list if item["name"] == q
    #     ]  # [operation iteration condition]
    return result


from dataclasses import dataclass


@dataclass
class Student:
    name: str
    age: int


@dataclass
class StudentResponse:
    id: int
    name: str
    age: int


@app.post(
    "/names", status_code=status.HTTP_201_CREATED, response_model=PersonResponseSchema
)
# def create_name(name: str = Body(embed=True)):
def create_name(request: PersonCreateSchema, db: Session = Depends(get_db)):
    # name_obj = {"id": random.randint(6, 100), "name": person.name}  # type: ignore
    # names_list.append(name_obj)
    new_person = Person(name=request.name)
    db.add(new_person)
    db.commit()
    db.refresh(new_person)
    return new_person


# /names/:id (GET(RETRIEVE), PUT/PATCH(UPDATE), DELETE)
@app.get("/names/{name_id}", response_model=PersonResponseSchema)
def retrieve_name_detail(
    name_id: int = Path(
        title="object id",
        description="the ID of the name in names_list",
    ),
    db: Session = Depends(get_db),
):
    # for name in names_list:
    #     if name["id"] == name_id:
    #         return name

    person = db.query(Person).filter_by(id=name_id).one_or_none()
    if person:
        return person
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Object Not Found :( ! "
        )


@app.put(
    "/names/{name_id}",
    status_code=status.HTTP_200_OK,
    response_model=PersonResponseSchema,
)
def update_name_detail(
    request: PersonUpdateSchema, name_id: int = Path(), db: Session = Depends(get_db)
):
    # for item in names_list:
    #     if item["id"] == name_id:
    #         item["name"] = person.name
    #         return item
    person = db.query(Person).filter_by(id=name_id).one_or_none()
    if person:
        person.name = request.name
        db.commit()
        db.refresh(person)
        return person
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Object Not Found :( ! "
        )


@app.delete("/names/{name_id}")
def delete_name(name_id: int, db: Session = Depends(get_db)):
    # for item in names_list:
    #     if item["id"] == name_id:
    #         names_list.remove(item)
    person = db.query(Person).filter_by(id=name_id).one_or_none()
    if person:
        db.delete(person)
        db.commit()
        return JSONResponse(
            content={"detail": "Object Removed Successfully!"},
            status_code=status.HTTP_200_OK,
        )
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Object Not Found :( ! "
        )


@app.get("/")
def root():
    content = {"message": "Hello, World!"}
    return JSONResponse(content=content, status_code=status.HTTP_202_ACCEPTED)


# @app.post("/upload_file/")
# async def upload_file(file: bytes = File(...)):
#     print(file)
#     return {"file_size": len(file)}


@app.post("/upload_file/")
async def upload_file(file: UploadFile = File(...)):
    content = await file.read()  # Asynchronous reading !
    return {
        "filename": file.filename,
        "content_type": file.content_type,
        "file_size": len(content),
    }


@app.post("/upload-multiple/")
async def upload_multiple(files: List[UploadFile]):
    return [
        {"filename": file.filename, "content_type": file.content_type} for file in files
    ]
