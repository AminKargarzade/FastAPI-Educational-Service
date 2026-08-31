from fastapi import FastAPI, Query, status, HTTPException, Path, Form, Body, File, UploadFile

# from typing import Annotated, Optional
from fastapi.responses import JSONResponse
import random
from typing import List

app = FastAPI()

names_list = [
    {"id": 1, "name": "amin"},
    {"id": 2, "name": "nima"},
    {"id": 3, "name": "andreas"},
    {"id": 4, "name": "rastin"},
    {"id": 5, "name": "soheil"},
    {"id": 6, "name": "amin"},
    {"id": 7, "name": "amin"},
]


# /names (GET(RETRIEVE), POST(CREATE))
@app.get("/names")
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
    )
):
    if q:
        return [
            item for item in names_list if item["name"] == q
        ]  # [operation iteration condition]
    return names_list


@app.post("/names", status_code=status.HTTP_201_CREATED)
def create_name(name: str = Body(embed=True)):
    name_obj = {"id": random.randint(6, 100), "name": name}  # type: ignore
    names_list.append(name_obj)
    return name_obj


# /names/:id (GET(RETRIEVE), PUT/PATCH(UPDATE), DELETE)
@app.get("/names/{name_id}")
def retrieve_name_detail(
    name_id: int = Path(
        alias="object_id",
        title="object id",
        description="the ID of the name in names_list",
    )
):
    for name in names_list:
        if name["id"] == name_id:
            return name
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="Object Not Found :( ! "
    )


@app.put("/names/{name_id}", status_code=status.HTTP_200_OK)
def update_name_detail(name_id: int = Path(), name: str = Form()):
    for item in names_list:
        if item["id"] == name_id:
            item["name"] = name
            return item
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="Object Not Found :( ! "
    )


@app.delete("/names/{name_id}")
def delete_name(name_id: int):
    for item in names_list:
        if item["id"] == name_id:
            names_list.remove(item)
            return JSONResponse(
                content={"detail": "Object Removed Successfully!"},
                status_code=status.HTTP_200_OK,
            )
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
    content = await file.read() # Asynchronous reading !
    return {"filename": file.filename, "content_type": file.content_type, "file_size": len(content)}

@app.post("/upload-multiple/")
async def upload_multiple(files: List[UploadFile]):
    return [
        {"filename": file.filename, "content_type": file.content_type}
        for file in files
    ]