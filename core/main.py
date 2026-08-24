from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"message":"Hello, World!"}


# another way of running a fastapi project!
# import uvicorn
# if __name__ == "__main__":
#     uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

# OR via this command (uvicorn main:app --reload --host 0.0.0.0 --port 8000) in core directory!

# but the suitable one is (fastapi dev core/main.py), just pay attention to fastapi-cli
#with your module version because it tore me up to fix it! 