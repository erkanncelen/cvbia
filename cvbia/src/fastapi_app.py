import uvicorn
from fastapi import FastAPI


app = FastAPI()


@app.post(
    "/update",
    summary="Update CV information.",
    response_description="Status code.",
    response_model=str,
)
def update_cv() -> str:
    return "hey"


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
