from idea import Idea, Priority


class Nemo(object):
    '''
    Nemo is a versatile, and flexible tool.
    It has ideas, and tries to learn new things, but also gets easily distracted with other topics.
    At first, there should be some kind of data structure to hold the ideas which are important,
    then the ones which are cool, and then the ones which are cool but too much future.
    '''
    major_version = 0
    minor_version = 1
    build_version = 7
    version_str = "{}.{}.{}".format(major_version, minor_version, build_version)
    repl_prompt = ">> "

    @classmethod
    def REPL(cls):
        run = True
        n = cls()
        print("Welcome to Nemo interactive shell")
        while run:
            cmd = input(cls.repl_prompt)
            if not cmd[0] == '!':
                print(n.eval(cmd))
            else:
                if cmd == '!quit':
                    run = False
                    print("Fin.")

    def __init__(self, *args, **kwargs):
        print(self)
        self.ideas = []
        self.ideas.extend([arg for arg in args if isinstance(arg, Idea)])

    def __getattr__(self, item):
        try:
            return self.__dict__[item]
        except KeyError:
            return "lol"
    __getitem__ = __getattr__

    def __str__(self):
        return "Nemo v{}".format(self.version_str)

    def eval(self, cmd):
        return self[cmd]

    def puke(self):
        for key in self.__dict__:
            print("{}: {}".format(key, self[key]))


if __name__ == '__main__':
    Nemo.REPL()
