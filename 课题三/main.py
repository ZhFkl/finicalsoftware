from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

import router.task1 as task1
import router.task2 as task2
import router.task3 as task3
import router.data_show as data_show

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(task1.task31)
app.include_router(task2.task2)
app.include_router(task3.task3)
app.include_router(data_show.data_show)
app.mount("/data", StaticFiles(directory="data"), name="data")

@app.get("/")
def read_root():
    return {"Hello": "World"}

