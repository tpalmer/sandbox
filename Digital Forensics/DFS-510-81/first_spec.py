#!/usr/local/bin/python3
from unittest.mock import patch
import unittest
from first import First


class FirstSpec(unittest.TestCase):
    @patch("first.getInput", return_value="LAZY")
    def test_found(self):
        f = First()
        # f.getInput.return_value = "LAZY"
        output = f.performSearch()
        assert output == "LAZY was found", "string found"

    # @patch('First.getInput()', return_value='lazy')
    # def testNotFound(self):
    #     """It should print 'not found' when the string does not match"""
    #     output = First.performSearch()
    #     assert output == "lazy was not found", "string not found"


if __name__ == '__main__':
    unittest.main()
