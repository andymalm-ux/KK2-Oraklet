from fastapi import APIRouter, File, HTTPException, UploadFile
import csv
import io
import pandas as pd

router = APIRouter()

csv_data = []

@router.post("/upload")
async def upload_csv(file: UploadFile = File(...)):
  global csv_data
  
  if file.filename and file.filename.endswith('.csv'):
    content = await file.read()

    csv_decode = io.StringIO(content.decode('utf-8'))
    csv_reader = csv.DictReader(csv_decode)    
    csv_data = list(csv_reader)

    return {"message": "File successfully uploaded"}, csv_data
  
  else:
    raise HTTPException(status_code=415, detail="You can only upload csv files")
  
@router.get("/data")
async def get_data():
  
  get_stored_data = csv_data

  if len(get_stored_data) == 0 :
    raise HTTPException(status_code=404, detail="You need to upload a csv file first.")
  else:
    return get_stored_data
  
@router.get ("/data/stats")
async def get_data_stats():
  
  get_data_stats = csv_data

  if len(get_data_stats) == 0 :
    raise HTTPException(status_code=404, detail="You need to upload a csv file first.")
  else:
    stats = pd.DataFrame(get_data_stats)
    return stats.describe().to_dict()