import unittest
from main import extract_title



class TestMain(unittest.TestCase):
    

    def test_extract_title(self):
        title = extract_title("./static/content/index.md")
        self.assertEqual(
            title,
            "Tolkien Fan Club"
        )

    def test_fail_extract_title(self):
        self.assertRaises(Exception, extract_title)