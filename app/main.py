from fastapi import FastAPI
from app.api.routes import router
from app.middleware import log_requests
from app.config import HOST, PORT

app = FastAPI()

app.middleware("http")(log_requests)
app.include_router(router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=HOST, port=PORT)
