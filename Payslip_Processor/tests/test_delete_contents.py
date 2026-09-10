from src import delete_contents
import unittest

class TestDeletingContents(unittest.TestCase):
    def check_if_deletes(self):
        self.assertEqual(delete_contents.delete_contents(), "")

if __name__ == "__main__":
    unittest.main()