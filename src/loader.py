import pandas as pd
import csv
import sys
from pathlib import Path

csv.field_size_limit(sys.maxsize)


def load_csv_folder(folder_path):

    folder_path = Path(folder_path)

    df_list = []

    for file_path in folder_path.glob("*.csv"):

        print(f"Loading {file_path.name}...")

        try:
            temp_df = pd.read_csv(
                file_path,
                engine="python"
            )

            temp_df["source_file"] = file_path.name

            df_list.append(temp_df)

            print(f"SUCCESS: {len(temp_df)} rows")

        except Exception as e:
            print(f"FAILED: {file_path.name}")
            print(e)

    if not df_list:
        raise ValueError("No CSV files were successfully loaded.")

    return pd.concat(df_list, ignore_index=True)