import csv
import pandas as pd
import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def _concatenate_non_empty_cells(reader):
    concatenated_data = []
    for row in reader:
        if not row:
            continue
        concatenated_row = "".join(cell for cell in row if cell.strip())
        concatenated_data.append([concatenated_row])
    return concatenated_data


def concatenate_non_empty_cells_from_file(input_file):
    try:
        with open(input_file, "r", newline="") as csvfile:
            reader = csv.reader(csvfile)
            concatenated_data = _concatenate_non_empty_cells(reader)
        result_df = pd.DataFrame(concatenated_data, columns=["concatenated"])
        return result_df
    except Exception as e:
        logger.error("Error processing input file: %s", e)
        raise ValueError("Error reading input file")


def concatenate_non_empty_cells_stream(file_stream):
    try:
        reader = csv.reader(file_stream)
        concatenated_data = _concatenate_non_empty_cells(reader)
        result_df = pd.DataFrame(concatenated_data, columns=["concatenated"])
        return result_df
    except Exception as e:
        logger.error("Error processing stream: %s", e)
        raise ValueError("Malformed CSV input")


def save_to_file(df, input_file):
    try:
        output_file_name = os.path.basename(input_file)[:4] + "_concat.csv"
        output_file = os.path.join(os.path.dirname(input_file), output_file_name)
        df.to_csv(output_file, index=False, header=True)
        logger.info("Concatenated output saved to: %s", output_file)
        return output_file
    except Exception as e:
        logger.error("Error saving file: %s", e)
        raise ValueError("Error saving output file")
