from fastapi import APIRouter, File, UploadFile
import csv
import io

router = APIRouter()

@router.post("/upload")
async def upload_csv(file: UploadFile = File(...)):
  
  if file.filename and file.filename.endswith('.csv'):
    content = await file.read()

    csv_data = io.StringIO(content.decode('utf-8'))
    csv_reader = csv.DictReader(csv_data)
    json_data = [row for row in csv_reader]

    return json_data
  
  else:
    return {"error": "Only csv files are allowed."}