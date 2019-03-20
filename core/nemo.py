from core.idea import Idea, Priority, Tag
from uuid import uuid4


class Nemo(object):
    '''
    Nemo is a versatile, and flexible tool.
    It has ideas, and tries to learn new things, but also gets easily distracted with other topics.

    Nemo can be interacted with by a simple REPL-Shell, which has yet to be implemented.
    Maybe, a command-parser should become its own object?

    DirWatcher!

    Distributed and Synchronized

    integrate (with) shelve

    automated loading/restoring and saving of state upon creating/destruction (with contextmanager?)
    '''
    major_version = 0
    minor_version = 1
    build_version = 15
    version_str = "Nemo v{}.{}.{}".format(major_version, minor_version, build_version)
    repl_prompt = ">> "
    default_data_dir = "../data/nemo"

    @classmethod
    def REPL(cls):
        run = True
        repl_nemo_obj = cls()
        print("Welcome to Nemo's interactive shell")
        while run:
            cmd = input(cls.repl_prompt)
            raise NotImplementedError

    @classmethod
    def from_file(cls, filename, data_dir=default_data_dir):
        import pickle, os
        if not os.path.exists(data_dir):
            raise FileNotFoundError("No data directory.")
        with open(os.path.join(data_dir, filename), mode="rb") as file:
            return pickle.load(file)

    @classmethod
    def from_pickle(cls, b):
        import pickle
        return pickle.loads(b)

    @classmethod
    def mock(cls, num_ideas=20):
        nemo = cls()
        for _ in range(num_ideas):
            nemo.add_idea(Idea.mock())
        return nemo

    def __init__(self, *args, **kwargs):
        print(Nemo.version_str)
        self.uid = uuid4()
        self.ideas = [arg for arg in args if isinstance(arg, Idea)]

    def __call__(self, *args, **kwargs):
        print("WHAT DID YOU CALL ME?")

    def __enter__(self):
        print("entered")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print("exited")

    def __getattr__(self, item, debug=False):
        try:
            return self.__dict__[item]
        except KeyError:
            print("Trying to access '{}'.".format(item))
            return "lol"
    __getitem__ = __getattr__

    def __getstate__(self):
        return self.__dict__

    def __setstate__(self, state):
        self.__dict__ = state

    def __str__(self):
        return self.version_str

    def add_idea(self, idea):
        if isinstance(idea, Idea):
            self.ideas.append(idea)
        elif isinstance(idea, list):
            self.ideas.extend(idea)
        else:
            raise NotImplementedError("Adding unknown element to ideas.")

    def eval(self, cmd):
        return self[cmd]()

    def nope(self):
        return None

    def puke(self):
        for key in self.__dict__:
            print("{}: {}".format(key, self[key]))

    def pickle_to(self, filename, data_dir=default_data_dir):
        import pickle, os
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)
        with open(os.path.join(data_dir, filename), mode="wb") as file:
            pickle.dump(self, file)

    def pickle(self):
        import pickle
        return pickle.dumps(self)

    def idea_by_uid(self, uid):
        for idea in self.ideas:
            if idea.uid == uid:
                return idea
        return None

    def ideas_by_priority(self, priority=Priority.MUST):
        return [idea for idea in self.ideas if idea.priority == priority]

    def ideas_by_tag(self, tag=Tag.REASONABLE):
        return [idea for idea in self.ideas if tag in idea.tags]


if __name__ == '__main__':
    n = Nemo()

