from enum import IntEnum, IntFlag


class Priority(IntEnum):
    MUST = 1
    SHOULD = 2
    COULD = 3

    @classmethod
    def default(cls):
        return cls.COULD

    def __str__(self):
        return "__str__"

    def __repr__(self):
        return self.name


class Tag(IntFlag):
    COOL = 1
    STUPID = 2

    @classmethod
    def default(cls):
        return cls.COOL & cls.STUPID


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
        self.priority = priority
        self.tags = tags

    def __str__(self):
        return "__str__"

    def __repr__(self):
        return "|{}|: {}".format(str(self.priority), self.text, self.longtext)

    ''' Change priority. If not stated otherwise, promote to one priority higher. '''
    def change_prio(self, new_prio=None, promote=True):
        if isinstance(new_prio, Priority):
            self.priority = new_prio
            return
        if promote:
            # check if priority is already highest (numerically smallest)
            self.priority = Priority(self.priority.value - 1)
        else:
            # check if priority is already lowest (numerically highest)
            self.priority = Priority(self.priority.value + 1)
