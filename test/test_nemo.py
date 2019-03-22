import unittest
from core.nemo import Nemo
from core.idea import Idea
import random
import tempfile
import pickle


def gen_mock_ideas(num_ideas=random.randrange(10, 20)):
    return [Idea.mock() for _ in range(num_ideas)]


class TestNemoInit(unittest.TestCase):

    def test_init(self):
        self.assertIsInstance(Nemo(), Nemo)

    def test_init_with_ideas(self):
        ideas = gen_mock_ideas()
        self.assertEqual(ideas, Nemo(ideas).ideas)

    def test_init_with_mixed_ideas(self):
        ideas_1 = gen_mock_ideas()
        ideas_2 = gen_mock_ideas()
        nested_ideas = ideas_1.copy()
        nested_ideas.append(ideas_2.copy())
        combined_ideas = ideas_1.copy()
        combined_ideas.extend(ideas_2.copy())
        self.assertEqual(combined_ideas, Nemo(nested_ideas).ideas)

    def test_init_with_dirty_ideas(self):
        ideas_1 = gen_mock_ideas()
        ideas_2 = gen_mock_ideas()
        dirty_things = ["asdf", None, True, Idea, 2, 3.5, {'dirty': True}, [None, 2]]
        combined_ideas = ideas_1.copy()
        combined_ideas.extend(ideas_2.copy())
        dirty_ideas = ideas_1.copy()
        dirty_ideas.extend(dirty_things.copy())
        really_dirty_ideas = dirty_things.copy()
        really_dirty_ideas.extend(dirty_ideas)
        really_dirty_ideas.append(ideas_2.copy())
        really_dirty_ideas.extend(dirty_things.copy())
        self.assertEqual(combined_ideas, Nemo(really_dirty_ideas).ideas)


class TestNemoDunders(unittest.TestCase):
    def setUp(self):
        self.n = Nemo(gen_mock_ideas())

    def test_str(self):
        self.assertIsInstance(str(self.n), str)

    def test_enter_returns_nemo(self):
        with self.n as n:
            self.assertIs(self.n, n)


class TestNemoSerialization(unittest.TestCase):

    def setUp(self):
        self.n = Nemo(gen_mock_ideas())
        self.temp_file = tempfile.TemporaryFile()

    def tearDown(self):
        self.temp_file.close()

    @unittest.skip
    def test_nemo_can_be_pickled(self):
        raise NotImplementedError


class TestNemoIdeaApi(unittest.TestCase):
    def setUp(self):
        self.n = Nemo()
        self.i = gen_mock_ideas()


if __name__ == '__main__':
    unittest.main()
