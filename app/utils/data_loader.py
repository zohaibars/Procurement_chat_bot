import pandas as pd
import os
from app.core.database import Database
from config.settings import settings

class DataLoader:
    @staticmethod
    def load_csv_data():
        """Load CSV data into MongoDB if collection is empty"""
        collection = Database.connect()
        print("Checking collection status...")
        
        if collection.count_documents({}) == 0:
            try:
                csv_path = settings.CSV_DATA_PATH
                if os.path.exists(csv_path):
                    print(f"Loading data from {csv_path}...")
                    df = pd.read_csv(csv_path)
                    records = df.to_dict('records')
                    collection.insert_many(records)
                    print(f"Successfully loaded {len(records)} documents into MongoDB")
                else:
                    print(f"CSV file not found at {csv_path}")
                    raise FileNotFoundError(f"CSV file not found at {csv_path}")
            except Exception as e:
                print(f"Error loading CSV data: {e}")
                raise

    @staticmethod
    def verify_data():
        """Verify that data has been loaded correctly"""
        collection = Database.connect()
        count = collection.count_documents({})
        return {
            "documents_count": count,
            "status": "Data loaded successfully" if count > 0 else "No data found"
        }

data_loader = DataLoader()