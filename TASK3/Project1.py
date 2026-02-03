             #Project 1: CSV → Excel Converter  

import pandas as pd
import argparse
import logging
import os

# ---------- Logging Setup ----------
logging.basicConfig(
    filename="converter.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


def clean_data(df):
    """
    Clean and normalize data
    """
    # Fill missing values
    df.fillna("N/A", inplace=True)

    # Convert date columns if present
    for col in df.columns:
        if "date" in col.lower():
            df[col] = pd.to_datetime(df[col], errors="coerce")

    # Simple column rename (example)
    df.columns = [col.strip().lower().replace(" ", "_") for col in df.columns]

    return df


def convert_csv_to_excel(input_file, output_file):
    try:
        if not os.path.exists(input_file):
            print("❌ CSV file not found.")
            return

        logging.info(f"Reading CSV file: {input_file}")
        df = pd.read_csv(input_file)

        df = clean_data(df)

        df.to_excel(output_file, index=False, engine="openpyxl")
        logging.info(f"Excel file created: {output_file}")

        print(f"✅ Conversion successful! Saved as: {output_file}")

    except pd.errors.EmptyDataError:
        print("❌ CSV file is empty.")
        logging.error("CSV file is empty.")

    except Exception as e:
        print("❌ Something went wrong.")
        logging.error(str(e))


def main():
    parser = argparse.ArgumentParser(description="CSV to Excel Converter")

    parser.add_argument(
        "--input",
        required=True,
        help="Path to input CSV file"
    )

    parser.add_argument(
        "--output",
        required=True,
        help="Path to output Excel file (.xlsx)"
    )

    args = parser.parse_args()

    convert_csv_to_excel(args.input, args.output)


# ---------- Run Program ----------
if __name__ == "__main__":
    main()
