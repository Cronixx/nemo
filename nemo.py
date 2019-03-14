from idea import Idea


class Nemo(object):
    '''
    Nemo is a versatile, and flexible tool.
    It has ideas, and tries to learn new things, but also gets easily distracted with other topics.
    At first, there should be some kind of data structure to hold the ideas which are important,
    then the ones which are cool, and then the ones which are cool but too much future.

    Nemo is also able to save its state by pickling himself to "Pickle-Nemo"

    Nemo can be interacted with by a simple REPL-Shell, which has yet to be implemented.
    Maybe, a command-parser should become its own object?
    '''
    major_version = 0
    minor_version = 1
    build_version = 11
    version_str = "{}.{}.{}".format(major_version, minor_version, build_version)
    repl_prompt = ">> \t"

    @classmethod
    def REPL(cls):
        run = True
        repl_nemo = cls()
        print("Welcome to Nemo's interactive shell")
        while run:
            cmd = input(cls.repl_prompt)
            if not cmd[0] == '!':
                print(repl_nemo.eval(cmd))
            else:
                if cmd == '!quit':
                    run = False
                    print("Fin.")

    @classmethod
    def from_file(cls, filename):
        import pickle
        with open(filename, mode="rb") as file:
            return pickle.load(file)

    def __init__(self, *args, **kwargs):
        print(self)
        self.ideas = [arg for arg in args if isinstance(arg, Idea)]

    def __getattr__(self, item):
        try:
            return self.__dict__[item]
        except KeyError:
            print("Trying to access '{}'.".format(item))
    __getitem__ = __getattr__

    def __getstate__(self):
        return self.__dict__

    def __setstate__(self, state):
        self.__dict__ = state

    def __str__(self):
        return "Nemo v{}".format(self.version_str)

    def add_idea(self, idea):
        if isinstance(idea, Idea):
            self.ideas.append(idea)
        else:
            self.ideas.extend(idea)

    def eval(self, cmd):
        return self[cmd]

    def nope(self):
        return None

    def puke(self):
        for key in self.__dict__:
            print("{}: {}".format(key, self[key]))

    def pickle_to(self, filename):
        import pickle
        with open(filename, mode="wb") as file:
            pickle.dump(self, file)


if __name__ == '__main__':
    n = Nemo()
    for _ in range(42):
        n.add_idea(Idea.mock())
    n.puke()
