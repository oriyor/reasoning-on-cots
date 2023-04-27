import csv
from tqdm import tqdm
import pandas as pd
import json
from datetime import datetime


def file_as_string(file_path):
    with open(file_path, "r") as file:
        file_str = file.read()
    return file_str.strip()


def timestamp_string():
    now = datetime.now()
    now = str(now).split(".")[0].strip()
    return str(now).replace(" ", "_").replace(":", "-")


def chunk_list_to_sublists(original_list, chunk_size):
    chunked_list = list()
    for i in range(0, len(original_list), chunk_size):
        chunked_list.append(original_list[i : i + chunk_size])
    return chunked_list


def read_csv_to_dict(csv_file, encoding=None):
    # replace NaN values (empty cell) with ""
    dict_from_csv = (
        pd.read_csv(csv_file, encoding=encoding).fillna("").to_dict("records")
    )
    return dict_from_csv


def write_to_json(data, json_file, encoding=None):
    encoding = "utf-8" if encoding is None else encoding
    with open(json_file, mode="w+", encoding=encoding) as file:
        json.dump(data, file, indent=4)
    return True


def load_json(filepath, encoding=None):
    encoding = "utf-8" if encoding is None else encoding
    with open(filepath, mode="r", encoding=encoding) as reader:
        text = reader.read()
    return json.loads(text)


def load_jsonl(filepath, encoding=None):
    encoding = "utf-8" if encoding is None else encoding
    with open(filepath, "r", encoding=encoding) as reader:
        data = [json.loads(line) for line in reader]
    return data


def jaccard_similarity(list1, list2):
    intersection = len(list(set(list1).intersection(list2)))
    union = (len(list1) + len(list2)) - intersection
    return float(intersection) / union


def remove_duplicates_from_list(items_list):
    return list(dict.fromkeys(items_list))


def write_dict_list_to_csv(dict_list, dict_keys_list, output_csv):
    csv_columns = dict_keys_list
    with open(output_csv, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
        writer.writeheader()
        for i in tqdm(range(len(dict_list))):
            data = dict_list[i]
            writer.writerow(data)
    return True
