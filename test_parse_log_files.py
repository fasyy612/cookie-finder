import os
import tempfile
import pytest
from parse_log_file import parse_log_file

def create_temp_log_file(tmp_path, content: str):
    file_path = tmp_path / "cookie_log.csv"
    file_path.write_text(content)
    return str(file_path)

def test_single_most_active_cookie(tmp_path):
    content = (
        "cookie,timestamp\n"
        "cookie_1_example,2018-12-09T01:00:00+00:00\n"
        "cookie_2_example,2018-12-09T02:00:00+00:00\n"
        "cookie_1_example,2018-12-09T03:00:00+00:00\n"
    )
    path = create_temp_log_file(tmp_path, content)
    result = parse_log_file(path, "2018-12-09")
    assert result == "cookie_1_example"

def test_multiple_most_active_cookies(tmp_path):
    content = (
        "cookie,timestamp\n"
        "cookie_1_example,2018-12-09T01:00:00+00:00\n"
        "cookie_2_example,2018-12-09T02:00:00+00:00\n"
        "cookie_2_example,2018-12-09T03:00:00+00:00\n"
        "cookie_1_example,2018-12-09T04:00:00+00:00\n"
    )
    path = create_temp_log_file(tmp_path, content)
    result = parse_log_file(path, "2018-12-09")
    assert result in {"cookie_1_example", "cookie_2_example"}

def test_no_matching_date_returns_none(tmp_path):
    content = (
        "cookie,timestamp\n"
        "cookie_1_example,2018-12-08T23:59:59+00:00\n"
        "cookie_2_example,2018-12-10T00:00:01+00:00\n"
    )
    path = create_temp_log_file(tmp_path, content)
    result = parse_log_file(path, "2018-12-09")
    assert result == None

def test_header_only_file_returns_none(tmp_path):
    path = create_temp_log_file(tmp_path, "cookie,timestamp\n")
    result = parse_log_file(path, "2018-12-09")
    assert result == None

def test_blank_lines_are_skipped(tmp_path):
    content = (
        "cookie,timestamp\n"
        "\n"
        "cookie_1_example,2018-12-09T01:00:00+00:00\n"
        "\n"
        "cookie_1_example,2018-12-09T01:30:00+00:00\n"
    )
    path = create_temp_log_file(tmp_path, content)
    result = parse_log_file(path, "2018-12-09")
    assert result == "cookie_1_example"

def test_wrong_formatted_line_raises_error(tmp_path):
    content = (
        "cookie,timestamp\n"
        "cookie_1_example,2018-12-09T01:00:00+00:00\n"
        "wrong_formatted_line\n"
    )
    path = create_temp_log_file(tmp_path, content)
    with pytest.raises(RuntimeError, match="Error in line format"):
        parse_log_file(path, "2018-12-09")

def test_invalid_timestamp_raises_error(tmp_path):
    content = (
        "cookie,timestamp\n"
        "cookie_1_example,09-12-2018 01:00\n"
    )
    file_path = create_temp_log_file(tmp_path, content)
    with pytest.raises(RuntimeError, match="Invalid timestamp"):
        parse_log_file(file_path, "2018-12-09")

def test_file_does_not_exist_raises():
    with pytest.raises(FileNotFoundError):
        parse_log_file("does_not_exist.csv", "2018-12-09")

def test_timezone_boundaries(tmp_path):
    content = (
        "cookie,timestamp\n"
        "cookie_1_example,2018-12-09T23:59:59+00:00\n"
        "cookie_2_example,2018-12-09T00:00:00+00:00\n"
        "cookie_1_example,2018-12-09T13:00:00+00:00\n"
    )
    path = create_temp_log_file(tmp_path, content)
    result = parse_log_file(path, "2018-12-09")
    assert result == "cookie_1_example"
