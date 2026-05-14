from collections import Counter
import re
from rich import print
from rich.table import Table

# parse log line to dict
def parse_log_line(line: str) -> dict:
    pattern = r"(\d{4}-\d{2}-\d{2}) (\d{2}:\d{2}:\d{2}) (\w+) (.*)"
    match = re.match(pattern, line)

    pattern = r"(\d{4}-\d{2}-\d{2}) (\d{2}:\d{2}:\d{2}) (\w+) (.*)"
    match = re.match(pattern, line)

    if not match:
        return None

    return {
        "date": match.group(1),
        "time": match.group(2),
        "level": match.group(3).upper(),
        "message": match.group(4)
    }

# load logs from file to list
def load_logs(file_path: str) -> list:
    logs = []
    try:
        with open(file_path, 'r') as file:
            for line in file:
                line = line.strip()
                if not line:
                    continue
                parsed_line = parse_log_line(line)
                if parsed_line:
                    logs.append(parse_log_line(line))
                else:
                    print(f"Invalid log line: {line}")
                    continue
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return []

    except PermissionError:
        print(f"No access to file: {file_path}")
        return []
    return logs

# filter logs by level
def filter_logs_by_level(logs: list, level: str) -> list:
    return [ log for log in logs if log is not None and log["level"].upper() == level.upper()]

# count logs by level
def count_logs_by_level(logs: list) -> dict:
    levels = [log["level"] for log in logs]
    return dict(Counter(levels))

# display log counts in table
def display_log_counts(counts: dict):
    table = Table(title="Log Counts")
    table.add_column("Level", justify="center", style="cyan")
    table.add_column("Count", justify="center", style="green")
                    
    for level, count in counts.items():
        table.add_row(level, str(count))
    print(table)