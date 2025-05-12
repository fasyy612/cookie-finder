import argparse
from parse_log_file import parse_log_file

def main():
    parser = argparse.ArgumentParser(description="Find the most active cookie at a given date.")
    parser.add_argument("-f", "--file", required=True, help="File path to the log file.")
    parser.add_argument("-d", "--date", required=True, help="Date in YYYY-MM-DD format.")

    args = parser.parse_args()
    try:
        result = parse_log_file(args.file, args.date)
        if result:
            print(result)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
