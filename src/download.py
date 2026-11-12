# use once to download the dataset from Zenodo and save it to the data/raw/zenodo directory
import requests
from pathlib import Path

# locate project root
PROJECT_ROOT = Path(__file__).resolve().parents[1]

# download destination
DOWNLOAD_DIR = PROJECT_ROOT / "data" / "raw" / "zenodo"
DOWNLOAD_DIR.mkdir(parents=True, exist_ok=True)

RECORD_URL = "https://zenodo.org/api/records/8339691"


def download_zenodo():

    response = requests.get(RECORD_URL, timeout=30)
    response.raise_for_status()

    record = response.json()

    for file in record["files"]:

        filename = file["key"]
        download_url = file["links"]["self"]
        expected_size = file["size"]

        file_path = DOWNLOAD_DIR / filename

        # Skip files already downloaded completely
        if file_path.exists() and file_path.stat().st_size == expected_size:
            print(f"Already downloaded: {filename}")
            continue

        print(f"Downloading: {filename}")

        try:
            with requests.get(
                download_url,
                stream=True,
                timeout=60
            ) as r:

                r.raise_for_status()

                with open(file_path, "wb") as f:
                    for chunk in r.iter_content(
                        chunk_size=1024 * 1024
                    ):
                        if chunk:
                            f.write(chunk)

            print(f"Saved: {filename}")

        except Exception:
            #remove incomplete download
            if file_path.exists():
                file_path.unlink()
            raise

    print("\nAll Zenodo files downloaded")


if __name__ == "__main__":
    download_zenodo()
