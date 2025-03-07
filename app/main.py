from fastapi import FastAPI
from api.routes import router
from middleware import log_requests
from config import HOST, PORT

app = FastAPI()

app.middleware("http")(log_requests)
app.include_router(router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=HOST, port=PORT)
