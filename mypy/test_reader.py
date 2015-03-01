import unittest
import reader

class TestReaderTest(unittest.TestCase):

    def test_peek(self):
        a_reader = reader.Reader([])
        self.assertEqual(None, a_reader.peek())

    def test_peek_is_idempotent(self):
        a_reader = reader.Reader([1])
        self.assertEqual(1, a_reader.peek())
        self.assertEqual(1, a_reader.peek())

    def test_next(self):
        a_reader = reader.Reader([1])
