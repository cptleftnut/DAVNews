from fastapi import FastAPI, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware

from api.websockets import router as ws_router

app = FastAPI(title="DAVNews Core API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(ws_router)


@app.get("/health")
def health_check():
    return {"status": "production_ready"}


@app.post("/trigger-cycle")
async def trigger_cycle(background_tasks: BackgroundTasks):
    from services.scout import run_pipeline

    background_tasks.add_task(run_pipeline)
    return {"message": "Cycle initiated"}
