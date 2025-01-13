from fastapi import APIRouter, Depends, HTTPException
from werkzeug.utils import send_from_directory
from fastapi.responses import FileResponse
import os
router = APIRouter()


@router.get("/api/dataset/files")
def send_dataset_files():
    directory_path = os.path.abspath("./app/files/")
    file_path = os.path.join(directory_path, "TrainData.zip")
    if not os.path.exists(file_path):
        print("未找到文件")
        return HTTPException(status_code=404, detail="File not found.")

    return FileResponse(file_path, media_type="application/zip",filename="TrainData.zip")
