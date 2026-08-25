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

# /names/:id (GET(RETRIEVE), PUT/PATCH(UPDATE), DELETE)

@app.get("/")
def root():
    return {"message":"Hello, World!"}

@app.get("/names")
def retrieve_names_list():
    return names_list