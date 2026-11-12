# use in notebooks to load the dataset from the data/raw/zenodo directory
import pandas as pd
import csv
import sys
from pathlib import Path

# Allow large email fields
csv.field_size_limit(sys.maxsize)


def load_csv_folder(folder_path):

    folder_path = Path(folder_path)

    if not folder_path.exists():
        raise FileNotFoundError(
            f"Folder not found: {folder_path}"
        )

    csv_files = sorted(folder_path.glob("*.csv"))

    if not csv_files:
        raise ValueError("No CSV files found.")

    df_list = []

    for file_path in csv_files:

        print(f"Loading {file_path.name}...")

        try:
            temp_df = pd.read_csv(
                file_path,
                engine="python"
            )

            temp_df["source_file"] = file_path.name

            df_list.append(temp_df)

            print(f"Loaded {len(temp_df)} rows")

        except Exception as e:
            raise RuntimeError(
                f"Failed to load {file_path.name}: {e}"
            ) from e

    data_df = pd.concat(
        df_list,
        ignore_index=True,
        sort=False
    )

    print("\nAll datasets combined")
    print("Total rows:", len(data_df))
    print("Total columns:", len(data_df.columns))

    return data_df
