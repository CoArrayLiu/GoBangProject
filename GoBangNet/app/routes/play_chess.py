from fastapi import APIRouter, Depends, HTTPException
from app.schemas.chess_model import chess_model
from app.services.analyze_chess import analyze_chess
router = APIRouter()



@router.post("/api/chess/next_step")
def analyze_next_step(chess_request: chess_model):
    pos = analyze_chess(chess_request.chess).move_3000()
    return {'pos': pos}


@router.post("/api/chess/next_step_low")
def analyze_next_step_low(chess_request: chess_model):
    pos = analyze_chess(chess_request.chess).move_2000()
    return {'pos': pos}


@router.post("/api/chess/next_step_bad")
def analyze_next_step_bad(chess_request: chess_model):
    pos = analyze_chess(chess_request.chess).move_3000()
    return {'pos': pos}

@router.post("/api/chess/next_step_best")
def analyze_next_step_best(chess_request: chess_model):
    pos = analyze_chess(chess_request.chess).move_5000()
    return {'pos': pos}