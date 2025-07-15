#!/usr/bin/env python3
"""Unit tests for utility functions in the utils module.

This module contains unit tests for:
- `access_nested_map`: accessing values in nested dictionaries.
- `get_json`: fetching and parsing JSON from a URL.
- `memoize`: caching method results to avoid redundant computation.
"""

import unittest
from unittest.mock import patch, Mock
from parameterized import parameterized
from utils import access_nested_map, get_json, memoize
from client import GithubOrgClient


class TestAccessNestedMap(unittest.TestCase):
    """Test suite for the access_nested_map utility function."""

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(self, nested_map, path, expected):
        """
        Test that access_nested_map returns correct value for valid paths.
        """
        result = access_nested_map(nested_map, path)
        self.assertEqual(result, expected)

    @parameterized.expand([
        ({}, ("a",)),
        ({"a": 1}, ("a", "b")),
    ])
    def test_access_nested_map_exception(self, nested_map, path):
        """
        Test that access_nested_map raises KeyError for invalid paths.
        """
        with self.assertRaises(KeyError) as context:
            access_nested_map(nested_map, path)
        expected_message = repr(path[-1])
        self.assertEqual(str(context.exception), expected_message)


class TestGetJson(unittest.TestCase):
    """Test suite for the get_json utility function."""

    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False}),
    ])
    def test_get_json(self, test_url, test_payload):
        """
        Test that get_json returns correct JSON and calls requests.get once.
        """
        with patch("utils.requests.get") as mock_get:
            mock_resp = Mock()
            mock_resp.json.return_value = test_payload
            mock_get.return_value = mock_resp

            result = get_json(test_url)
            mock_get.assert_called_once_with(test_url)
            self.assertEqual(result, test_payload)


class TestMemoize(unittest.TestCase):
    """Test suite for the memoize decorator."""

    def test_memoize(self):
        """
        Test that memoize caches results and calls the method only once.
        """
        class TestClass:
            def a_method(self):
                return 42

            @memoize
            def a_property(self):
                return self.a_method()

        with patch.object(TestClass, 'a_method', return_value=42) as mocked:
            obj = TestClass()
            self.assertEqual(obj.a_property, 42)
            self.assertEqual(obj.a_property, 42)
            mocked.assert_called_once()


class TestGithubOrgClient(unittest.TestCase):
    """Test suite for the GithubOrgClient class."""

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch("client.get_json")
    def test_org(self, org_name, mock_get_json):
        """
        Test that GithubOrgClient.org returns expected payload from get_json.
        """
        test_payload = {"name": org_name}
        mock_get_json.return_value = test_payload

        client = GithubOrgClient(org_name)
        result = client.org

        self.assertEqual(result, test_payload)
        mock_get_json.assert_called_once_with(
            f"https://api.github.com/orgs/{org_name}"
        )
