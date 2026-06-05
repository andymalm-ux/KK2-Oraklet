import pandas as pd
from io import BytesIO
from starlette.testclient import TestClient as TestClient
from app.main import app

client = TestClient(app)

def create_test_csv():
  df = pd.DataFrame({"columns1": [1, 2, 3], "columns2": [4, 5, 6]})
  mock_csv = BytesIO()
  df.to_csv(mock_csv, index=False)
  mock_csv.seek(0)
  return mock_csv

def test_csv_upload():
  response = client.post("/upload", files={"file": ("test.csv", create_test_csv(), "text/csv")})

  assert response.status_code == 200