#download data from zenodo as CSV files
import requests
from pathlib import Path

#create download directory
download_dir = Path("data/raw/zenodo")
download_dir.mkdir(parents=True, exist_ok=True)

url = "https://zenodo.org/api/records/8339691"

response = requests.get(url)
response.raise_for_status()

record = response.json()

for file in record["files"]:

    filename = file["key"]
    download_url = file["links"]["self"]

    #save file inside Zenodo folder
    file_path = download_dir / filename

    print(f"Downloading {filename}...")

    r = requests.get(download_url, stream=True)
    r.raise_for_status()

    with open(file_path, "wb") as f:
        for chunk in r.iter_content(chunk_size=1024 * 1024):
            if chunk:
                f.write(chunk)

    print(f"saved to {file_path}")

print("\nall files downloaded successfully")