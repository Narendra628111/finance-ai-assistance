from fastapi import FastAPI

app = FastAPI(
    title="Finance AI Assistant",
    version="1.0.0"
)


@app.get("/")
def health():
    return {
        "status": "running",
        "message": "Finance AI Assistant Backend"
    }