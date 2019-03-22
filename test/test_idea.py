import unittest
from core.idea import Idea, Priority, Tag


class TestIdeaInit(unittest.TestCase):

    def test_init_empty_fails(self):
        with self.assertRaises(TypeError):
            Idea()

    def test_init_text(self):
        self.assertEqual("unittest", Idea("unittest").text)


if __name__ == '__main__':
    unittest.main()
