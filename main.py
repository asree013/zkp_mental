from run_zkp import get_student
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.responses import RedirectResponse

@asynccontextmanager
async def lifespan(app: FastAPI):
    print({
        "message": "Server is Running in Port 8000",
        "link": "http://localhost:8000/docs"
    })
    
    yield 
    
    print("Serverกำลังจะปิดตัวลง...")

app = FastAPI(lifespan=lifespan)

@app.get('/')
def root():
    return RedirectResponse(url='/docs')

@app.get('/get-zpk')
def get_zpk(count_student: int):
    result = get_student(count_student)
    print(result)
    return {
        "data": result,
        "message": "fetch data success",
        "status": 200
    }
