from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes import play_chess

from app.GoBangZero import AIPlayer

from app.routes  import send_files

app = FastAPI()

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://127.0.0.1",
    "http://www.tongji.store",
    "http://www.tongji.store:80",
    "http://101.126.143.221",
    "http://101.126.143.221:80"
]  # 前端的地址

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Origin", "X-Requested-With", "Content-Type", "token", "Accept"],
)

# AIPlayer_Bad = AIPlayer.GoBangZeroV4("./app/model/15/500.model")
# AIPlayer_low = AIPlayer.GoBangZeroV4("./app/model/15/2000.model")
# AIPlayer = AIPlayer.GoBangZeroV4("./app/model/15/3140.model")

AIPlayer_1000 = AIPlayer.GoBangZeroV4("./app/model/rounds/1000.model")
AIPlayer_2000 = AIPlayer.GoBangZeroV4("./app/model/rounds/2000.model")
AIPlayer_3000 = AIPlayer.GoBangZeroV4("./app/model/rounds/3000.model")
AIPlayer_5000 = AIPlayer.GoBangZeroV4("./app/model/rounds/5000.model")



app.include_router(play_chess.router)
app.include_router(send_files.router)

@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI!"}