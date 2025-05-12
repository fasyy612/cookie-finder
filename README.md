# 🍪 Cookie Log Parser

A command-line utility to parse cookie logs and return the **most active cookie** for a specified date.

## 🚀 Features

- Parses a log file sorted by timestamp.
- Returns the **single most active cookie** on a given date.
- Accepts **ISO 8601** timestamp format only (e.g. `2018-12-09T14:19:00+00:00`).
- Clean, testable, and extendable codebase.
- Includes a full suite of `pytest` tests.

## 📝 Parameters

- Parameters

```-f, --file```
Path to the cookie log file (in CSV format).

```-d, --date```
Target date in YYYY-MM-DD format.

## How to run the file

```
$ python main.py -f cookie_log.csv -d 2018-12-09
```

## 📄 Input Format

The input CSV must follow this format:
```
cookie,timestamp
AtY0laUfhglK3lC7,2018-12-09T14:19:00+00:00
SAZuXPGUrfbcn5UA,2018-12-09T10:13:00+00:00
...
```
- The timestamp must be in ISO 8601 format.

- The File should include a header row.

- The timestamps must be in UTC.

## Assumptions

- Input file fits in memory.

- Only the first cookie with the highest count is returned (in case of ties).

- All timestamps are in UTC and conform to ISO 8601.

## 🧪 Running Tests

Tests are written using pytest.

📦 **Install pytest**

```
pip install pytest
```
✅ **Run the test suite**
```
pytest -v
```

## 🛠️ Potential Future Improvements

- Add a --all flag to show all tied cookies.

- Add additonal output formatting (e.g., JSON or CSV).

- Enable filtering by time range within a date.

- More verbose testing
