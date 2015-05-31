#!/usr/bin/env python
import sys
from io import StringIO
from jproperties import Properties


def _test_deserialize(*data):
	for s, items in data:
		props = Properties()
		props.load(StringIO(s))
		assert list(props.items()) == items


def test_eq_separator():
	_test_deserialize(
		("a=b", [("a", "b")]),
		("a= b", [("a", "b")]),
		("a = b", [("a", "b")]),
		("a =b", [("a", "b")]),
	)

def test_colon_separator():
	_test_deserialize(
		("a:b", [("a", "b")]),
		("a: b", [("a", "b")]),
		("a : b", [("a", "b")]),
		("a :b", [("a", "b")]),
	)


def test_space_separator():
	_test_deserialize(
		("a b", [("a", "b")]),
		("a  b", [("a", "b")]),
		("a        b", [("a", "b")]),
	)


def test_space_in_key():
	_test_deserialize(
		("key\ with\ spaces = b", [("key with spaces", "b")]),
		("key\ with\ spaces b", [("key with spaces", "b")]),
		("key\ with\ spaces : b", [("key with spaces", "b")]),
		("key\ with\ spaces\ : b", [("key with spaces ", "b")]),
		("key\ with\ spaces\  : b", [("key with spaces ", "b")]),
        ("\ before = n", [(" before", "b")])
	)


def test_space_surrounding_value():
	_test_deserialize(
		#("a = end ", [("a", "end ")]), # broken
		("a = \ start", [("a", " start")]),
	)


def test_key_with_no__value():
	_test_deserialize(
		("a =", [("a", "")]),
		#("a", [("a", "")]), # breaks in the parser line 154 SyntaxError
	)


def test_oddeties():
	_test_deserialize(
		("=", [("", "")]),    # Yes you can have a key with no value
		("=b", [("", "b")]),  # and a value with no key
	)


def test_delimters_in_value():
	_test_deserialize(
        ("a = http://", [("a", "http://")]),
        ("a = http\://", [("a", "http://")]),  # Some people believe you need to escape them Java says not
        ("a = value=1", [("a", "value=1")]),
        ("a = value\=1", [("a", "value=1")]),
    )


def test_special_characters_in_key():
	_test_deserialize(
        #("a = b\u0020", [("a", "b ")]), # Simple case within 127 range
        #("a = b\u2026", [("a", "b…")]), # Bust index out of range # Complex outside of normal code pages
    )


def main():
	for name, f in globals().items():
		if name.startswith("test_") and callable(f):
			f()


if __name__ == "__main__":
	main()
