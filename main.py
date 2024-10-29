from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.print import router as print_router

app = FastAPI()

# Allow CORS for localhost:3000
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:3001",
        "http://localhost:8000",
        "https://burgerbraterei-tasks.vercel.app",
        "https://burgerbraterei-tasks-backend.vercel.app"
        "https://many-views-rescue.loca.lt"
    ],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

app.include_router(print_router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Label Printer API!"}

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8001)
