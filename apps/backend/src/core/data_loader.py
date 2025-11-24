import os
import pandas as pd
from typing import Optional

class DataLoader:
    """
    Loads datasets used for production simulation.
    """
    def __init__(self):
        # Resolve absolute path to the repo root
        self.root_dir = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "../../../..")
        )

        self.data_path = os.path.join(
            self.root_dir,
            "data",
            "production",
            "test_dataset_split.csv"
        )

    def load_test_dataset(self, subset_size: Optional[int] = None) -> pd.DataFrame:
        """
        Loads the pre-split test dataset for demo simulation.
        """
        if not os.path.exists(self.data_path):
            raise FileNotFoundError(f"Test dataset not found at: {self.data_path}")

        df = pd.read_csv(self.data_path)

        # Ensure datetime column is parsed
        df["datetime"] = pd.to_datetime(df["datetime"])

        # Optional subset 
        if subset_size is not None and subset_size < len(df):
            df = df.head(subset_size)

        print(f"Loaded test dataset: {df.shape[0]} rows, {df.shape[1]} columns")
        return df


data_loader = DataLoader()
