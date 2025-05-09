from src.utils.arguments import arg_parser
from email.utils import formatdate
from dateutil.parser import parse
from datetime import datetime
from uuid import uuid4
from math import ceil
import requests
import json
import yaml
import copy
import csv
import os

prom_addr = arg_parser().get("prom.addr")


def prom_query(query, range_query=False, start="0", end="0",
               step="0", url=prom_addr) -> tuple[bool, int, dict]:
    """
    This function queries data from Prometheus
    based on the information provided by the
    user and returns the data as a dictionary.
    """
    try:
        r = requests.post(f"{url}/api/v1/{'query_range' if range_query else 'query'}",
                          data={
                              "query": query,
                              "start": start,
                              "end": end,
                              "step": step},
                          headers={"Content-Type": "application/x-www-form-urlencoded"})
    except BaseException as e:
        return False, 500, {"status": "error",
                            "error": f"Prometheus query has failed. {e}"}
    else:
        return True if r.status_code == 200 else False, r.status_code, r.json()


def replace_fields(data, custom_fields) -> None:
    """
    This function replaces (renames) the
    final Prometheus labels (fields) based
    on the 'replace_fields' object.
    """
    for source_field, target_field in custom_fields.items():
        try:
            if isinstance(data, list):
                data[data.index(source_field)] = target_field
            elif isinstance(data, dict):
                data[target_field] = data.pop(source_field)
        except (ValueError, KeyError):
            pass


def format_timestamp(timestamp, fmt) -> str:
    """
    This function converts Unix timestamps
    to several common time formats.
    """
    timestamp_formats = {
        "unix": timestamp,
        "rfc2822": formatdate(timestamp, localtime=True),
        "iso8601": datetime.fromtimestamp(timestamp).isoformat(),
        "rfc3339": datetime.fromtimestamp(timestamp).astimezone().isoformat(timespec='milliseconds'),
        "friendly": datetime.fromtimestamp(timestamp).strftime('%A, %B %d, %Y %I:%M:%S %p')
    }

    return timestamp_formats[fmt]


def auto_max_resolution(start: str, end: str) -> str:
    """
    This function calculates the best step value based
    on the Prometheus maximum resolution of 11,000
    points per time-series.
    """
    start_timestamp = parse(start).timestamp()
    end_timestamp = parse(end).timestamp()
    step_in_seconds = ceil((end_timestamp - start_timestamp) / 11000)
    return f"{abs(step_in_seconds)}s"


def data_processor(source_data: dict,
                   custom_fields: dict,
                   timestamp_format: str) -> tuple[list, list]:
    """
    This function preprocesses the results
    of the Prometheus query for future formatting.
    It returns all labels of the query result
    and the data of each time series.
    """
    data_raw = copy.deepcopy(source_data)
    data_processed, unique_labels = [], set()
    data_result = data_raw["data"]["result"]

    def vector_processor():
        for ts in data_result:
            ts_labels = set(ts["metric"].keys())
            unique_labels.update(ts_labels)
            series = ts["metric"]
            series["timestamp"] = format_timestamp(
                ts["value"][0], timestamp_format)
            series["value"] = ts["value"][1]
            replace_fields(series, custom_fields)
            data_processed.append(series)

    def matrix_processor():
        for ts in data_result:
            ts_labels = set(ts["metric"].keys())
            unique_labels.update(ts_labels)
            series = ts["metric"]
            for idx in range(len(ts["values"])):
                series_nested = copy.deepcopy(series)
                series_nested["timestamp"] = format_timestamp(
                    ts["values"][idx][0], timestamp_format)
                series_nested["value"] = ts["values"][idx][1]
                replace_fields(series_nested, custom_fields)
                data_processed.append(series_nested)
                del series_nested

    if data_raw["data"]["resultType"] == "vector":
        vector_processor()
    elif data_raw["data"]["resultType"] == "matrix":
        matrix_processor()

    unique_labels = sorted(unique_labels)
    unique_labels.extend(["timestamp", "value"])
    replace_fields(unique_labels, custom_fields)
    return unique_labels, data_processed


def cleanup_files(file) -> tuple[True, str]:
    """
    This function removes the generated file
    once it sends a response to the user.
    """
    try:
        os.remove(file)
    except BaseException as e:
        return False, str(e)
    else:
        return True, "File has been removed successfully"


def file_generator(file_format, data, fields):
    """
    This function generates a file depending
    on the provided file format/extension
    """

    file_path = f"/tmp/{str(uuid4())}.{file_format}"
    try:
        with open(file_path, 'w') as f:
            if file_format == "csv":
                writer = csv.DictWriter(
                    f, fieldnames=fields, extrasaction='ignore')
                writer.writeheader()
                writer.writerows(data)
            elif file_format in ["yml", "yaml"]:
                f.write(yaml.dump(data))
            elif file_format == "json":
                f.write(json.dumps(data))
            elif file_format in ["ndjson", "jsonlines"]:
                for i in data:
                    f.write(f"{json.dumps(i)}\n")
            else:
                cleanup_files(file_path)
                return False, "error", 400, "", f"Unsupported file format '{file_format}'"
    except BaseException as e:
        return False, "error", 500, "", str(e)
    else:
        return True, "success", 200, file_path, f"{file_format.upper()} file has been generated successfully"
