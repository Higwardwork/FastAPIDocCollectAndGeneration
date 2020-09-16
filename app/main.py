from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/item/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}


# if __name__ == "__main__":
#     uvicorn.run("main:app", host="127.0.0.1", port=3010, log_config="logging.conf",log_level="debug", use_colors=True)
