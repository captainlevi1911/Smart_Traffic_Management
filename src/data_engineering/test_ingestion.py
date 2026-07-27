from src.data_engineering.ingestion import read_csv_file
from src.data_engineering.config import RAW_DATA_DIR


def test_read_csv():

    sample_file = RAW_DATA_DIR / "sample.csv"

    df = read_csv_file(sample_file)

    print(df.head())


if __name__ == "__main__":
    test_read_csv()