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

def test_get_data():
  upload_response = client.post("/upload", files={"file": ("test.csv", create_test_csv(), "text/csv")})

  assert upload_response.status_code ==200

  data_response = client.get("/data")

  assert data_response.status_code == 200

  data = data_response.json()

  assert len(data) == 3
  assert data[0]["columns1"] == "1"
  assert data[0]["columns2"] == "4"

def test_get_data_stats():
  upload_response = client.post("/upload", files={"file": ("test.csv", create_test_csv(), "text/csv")})

  assert upload_response.status_code ==200

  stats_response = client.get("/data/stats")

  assert stats_response.status_code == 200

  stats = stats_response.json()

  assert "columns1" in stats
  assert "columns2" in stats


def test_get_data_without_upload():

  app.state.csv_data = []

  response = client.get("/data")

  assert response.status_code == 404