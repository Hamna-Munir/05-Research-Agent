"""
tests/test_tools.py
Day 29-31 — tests for tools.py.

Run with:
    pytest tests/test_tools.py -v
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.tools import add, subtract, multiply, divide, calculate_percentage, word_count, execute_tool


def test_add():
    assert add(2, 3) == 5


def test_subtract():
    assert subtract(10, 4) == 6


def test_multiply():
    assert multiply(6, 7) == 42


def test_divide():
    assert divide(10, 2) == 5


def test_divide_by_zero_returns_error_not_exception():
    result = divide(10, 0)
    assert isinstance(result, str)
    assert "error" in result.lower()


def test_calculate_percentage():
    assert calculate_percentage(25, 200) == 12.5


def test_calculate_percentage_zero_whole():
    result = calculate_percentage(5, 0)
    assert isinstance(result, str)
    assert "error" in result.lower()


def test_word_count():
    assert word_count("The quick brown fox") == 4


def test_word_count_empty_text():
    result = word_count("")
    assert isinstance(result, str)
    assert "error" in result.lower()


def test_execute_tool_valid_call():
    result = execute_tool("add", {"a": 2, "b": 3})
    assert result == 5


def test_execute_tool_unknown_tool():
    result = execute_tool("nonexistent_tool", {})
    assert "unknown tool" in result.lower()


def test_execute_tool_bad_arguments_does_not_crash():
    result = execute_tool("add", {"a": 2})  # missing required 'b'
    assert isinstance(result, str)
    assert "error" in result.lower()
