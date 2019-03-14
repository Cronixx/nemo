from enum import IntEnum, IntFlag, auto


class Priority(IntEnum):
    '''
    Nemo's idea have different priorities. Because nemo got so much of them, most of them have a low priority.
    '''
    MUST = auto()
    SHOULD = auto()
    COULD = auto()
    UNIMPORTANT = auto()

    @classmethod
    def default(cls):
        return cls.COULD

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return self.name


class Tag(IntFlag):
    '''
    Nemo's ideas have lots of attributes. Most of them are stupid but also kinda cool.
    Some are reasonable, and later there will be more.
    Also, they can be more than one of that.
    '''
    COOL = auto()
    STUPID = auto()
    REASONABLE = auto()

    @classmethod
    def default(cls):
        return cls.COOL | cls.STUPID


class Idea(object):
    '''
    Nemo has lots of ideas, therefore there should be an idea object.

    Ideas have a priority, a (short) text, and optionally a long text.
    Per default, ideas have COULD status. That means, that they are purely optional and should be regarded
    as ideas with the lowest (numerically highest) priority.

    Ideas can also have tags. Per default, all ideas are cool and stupid.
    '''
    def __init__(self, text, longtext=None, priority=Priority.default(), tags=Tag.default()):
        self.text = text
        self.longtext = longtext

        if isinstance(priority, int):
            priority = Priority(priority)
        if not isinstance(priority, Priority):
            raise ValueError("Illegal Argument for 'priority'.")
        self.priority = priority

        if isinstance(tags, int):
            tags = Tag(tags)
        if not isinstance(tags, Tag):
            raise ValueError("Illegal Argument for 'tags'.")
        self.tags = tags

    @classmethod
    def from_prompt(cls):
        pass

    @classmethod
    def mock(cls, text=None, longtext=None, priority=None, tags=None):
        import random
        if text is None:
            text = "Mocked Idea"
        if longtext is None:
            longtext = "This is some text with a randomly generated priority"
        if priority is None:
            priority = Priority(random.randint(1, len(Priority)))
        if tags is None:
            tags = Tag(random.randint(1, 2 ** len(Tag) - 1))
        return cls(text=text, longtext=longtext, priority=priority, tags=tags)

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return "|{}|: {} - {} - {}".format(str(self.priority), self.text, self.longtext, str(self.tags))

    ''' Change priority. If not stated otherwise, promote to one priority higher. '''
    def change_priority(self, new_prio=None, promote=True):
        if isinstance(new_prio, Priority):
            self.priority = new_prio
        elif isinstance(new_prio, int):
            self.priority = Priority(new_prio)
        elif new_prio is None:
            try:
                if promote:
                    # check if priority is already highest (numerically smallest)
                    self.priority = Priority(self.priority.value - 1)
                else:
                    # check if priority is already lowest (numerically highest)
                    self.priority = Priority(self.priority.value + 1)
            except ValueError:
                if promote:
                    error_hint = "highest"
                else:
                    error_hint = "lowest"
                print("Already at {} priority.".format(error_hint))
        else:
            raise TypeError("Illegal argument {} for change_priority.".format(new_prio))


if __name__ == '__main__':
    num_ideas = 50
    for _ in range(num_ideas):
        i = Idea.mock()
        i.change_priority()
