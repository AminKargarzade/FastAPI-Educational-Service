from fastapi import FastAPI


app = FastAPI()

names_list = [
    {"id":1, "name":"amin"},
    {"id":2, "name":"nima"},
    {"id":3, "name":"andreas"},
    {"id":4, "name":"rastin"},
    {"id":5, "name":"soheil"},
]

# /names (GET(RETRIEVE), POST(CREATE))
@app.get("/names")
def retrieve_names_list():
    return names_list


# /names/:id (GET(RETRIEVE), PUT/PATCH(UPDATE), DELETE)
@app.get("/names/{name_id}")
def retrieve_name_detail(name_id:int):
    for name in names_list:
        if name["id"] == name_id:
            return name
    return {"detail":"object not found!"}


@app.get("/")
def root():
    return {"message":"Hello, World!"}