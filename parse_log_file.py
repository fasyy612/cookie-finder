from datetime import datetime

def parse_log_file(filename: str, date: str):
    """
    Parses the log file and returns the most active cookie(s) for the given date.
    :param filename: File path to the log file.
    :param date: Date string in YYYY-MM-DD format.
    :return: List of most active cookie(s) for the day.
    """
    cookie_dict = {}
    input_date = datetime.strptime(date, "%Y-%m-%d").date()

    try:
        with open(filename, "r") as file:
            next(file)  # Skip header
            for line_number, line in enumerate(file, start=2):
                line = line.strip()
                if not line:
                    continue  # Skip blank lines
                line_parts = line.split(",")
                if len(line_parts) != 2:
                    raise RuntimeError(f"Error in line format at {line_number}: {line}")
                cookie, timestamp = line_parts
                try:
                    log_date = datetime.fromisoformat(timestamp).date()
                except ValueError as value_error:
                    raise ValueError(f"Invalid timestamp at line {line_number}: '{timestamp}'") from value_error
                if log_date == input_date:
                    cookie_dict[cookie] = cookie_dict.get(cookie, 0) + 1
    except FileNotFoundError:
        raise FileNotFoundError(f"File '{filename}' is not found.")
    except Exception as error:
        raise RuntimeError(f"Encountered an error processing file: {error}")

    if not cookie_dict:
        return None

    max_count = max(cookie_dict.values())
    for cookie in cookie_dict:
        if cookie_dict[cookie] == max_count:
            return cookie
