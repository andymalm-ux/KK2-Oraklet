from fastapi import APIRouter, File, HTTPException, Request, UploadFile
import csv
import io
import pandas as pd

router = APIRouter()

csv_data = []

@router.post("/upload")
async def upload_csv(
    request: Request,
    file: UploadFile = File(...)
):
    if not file.filename.endswith(".csv"):
        raise HTTPException(
            status_code=415,
            detail="You can only upload csv files"
        )

    content = await file.read()

    csv_decode = io.StringIO(
        content.decode("utf-8")
    )

    csv_reader = csv.DictReader(csv_decode)

    request.app.state.csv_data = list(csv_reader)

    return {"rows": len(request.app.state.csv_data)}
  
@router.get("/data")
async def get_data(request: Request):
  
  get_stored_data = request.app.state.csv_data

  if len(get_stored_data) == 0 :
    raise HTTPException(status_code=404, detail="You need to upload a csv file first.")
  else:
    return get_stored_data
  
@router.get ("/data/stats")
async def get_data_stats(request: Request):
  
  get_data_stats = request.app.state.csv_data

  if len(get_data_stats) == 0 :
    raise HTTPException(status_code=404, detail="You need to upload a csv file first.")
  else:
    stats = pd.DataFrame(get_data_stats)
    return stats.describe().to_dict()
  
@router.get ("/health")
def health_check():
   return {"status": "OK"}
