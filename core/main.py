from fastapi import FastAPI, Query, status, HTTPException
from typing import Annotated, Optional
import random

app = FastAPI()

names_list = [
    {"id":1, "name":"amin"},
    {"id":2, "name":"nima"},
    {"id":3, "name":"andreas"},
    {"id":4, "name":"rastin"},
    {"id":5, "name":"soheil"},
    {"id":6, "name":"amin"},
    {"id":7, "name":"amin"},
]

# /names (GET(RETRIEVE), POST(CREATE))
@app.get("/names")
# def retrieve_names_list(q : str | None = None):
# def retrieve_names_list(q : Optional[str] = None):
# def retrieve_names_list(q : Annotated[str | None, Query(max_length=50)] = None):
def retrieve_names_list(q : str | None = Query(default=None, max_length=50)):
    if q:
        return [item for item in names_list if item["name"] == q] # [operation iteration condition]        
    return names_list

@app.post("/names", status_code=status.HTTP_201_CREATED)
def create_name(name:str):
    name_obj = {"id":random.randint(6, 100),"name":name}  # type: ignore
    names_list.append(name_obj)
    return name_obj


# /names/:id (GET(RETRIEVE), PUT/PATCH(UPDATE), DELETE)
@app.get("/names/{name_id}")
def retrieve_name_detail(name_id:int):
    for name in names_list:
        if name["id"] == name_id:
            return name
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Object Not Found :( ! ")

@app.put("/names/{name_id}", status_code=status.HTTP_200_OK)
def update_name_detail(name_id:int, name:str):
    for item in names_list:
        if item["id"] == name_id: 
            item["name"] = name 
            return item
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Object Not Found :( ! ")

@app.delete("/names/{name_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_name(name_id:int):
    for item in names_list:
        if item["id"] == name_id:
            names_list.remove(item)
            return {"detail":"object removed successfully!"}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Object Not Found :( ! ")

@app.get("/")
def root():
    return {"message":"Hello, World!"}