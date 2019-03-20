from enum import IntEnum, IntFlag, auto
from uuid import uuid4
import logging
from util.log import configure_logging


logger = logging.getLogger(__name__)


class UpdateableIntEnum(IntEnum):
    pass


class Priority(IntEnum):
    '''
    Nemo's idea have different priorities. Because nemo got so much of them, most of them have a low priority.

    TODO: Overwrite to automatically adjust parameter to lowest/highest value.

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


class UpdateableIntFlag(IntFlag):
    pass


class Tag(IntFlag):
    '''
    Nemo's ideas have lots of attributes. Most of them are stupid but also kinda cool.
    Some are reasonable, and later there will be more.
    Also, they can be more than one of that.

    Add Tags in runtime

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

    It should be possible, to create ideas from the to-be-implemented runtime shell.

    Nested ideas could be a thing. Or connection of ideas, which also are ideas.
    Bi-directional? Uni-directional? NETWORKX?

    Editable Tags

    Aufwand
    '''
    idea_prompt = ": "
    default_data_dir = "../data/ideas"

    def __init__(self, text, longtext=None, connected_ideas=None,
                 priority=Priority.default(), tags=Tag.default(),
                 url=None):
        self.uid = uuid4()
        self.text = text
        self.longtext = longtext

        if connected_ideas is not None:
            raise NotImplementedError("Implement 'connected ideas'.")
        self.connected_ideas = connected_ideas

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

        if url is not None:
            raise NotImplementedError("Ideas can have urls!")
        self.url = url

    @classmethod
    def from_prompt(cls):
        text = input("Enter text {}".format(Idea.idea_prompt))
        p = Priority(int(input("Enter priority (1=highest, {}=lowest) {}".format(len(Priority), Idea.idea_prompt))))
        return cls(text, priority=p, tags=Tag.REASONABLE)

    @classmethod
    def from_file(cls, filename, data_dir=default_data_dir):
        import pickle, os
        if not os.path.exists(data_dir):
            raise FileNotFoundError("No data directory.")
        fp = os.path.join(data_dir, filename)
        with open(fp, mode="rb") as file:
            logger.info("Creating {} from file: {}".format(cls.__name__, fp))
            return pickle.load(file)

    @classmethod
    def from_pickle(cls, b):
        import pickle
        return pickle.loads(b)

    @classmethod
    def mock(cls, text=None, longtext=None, priority=None, tags=None):
        import random
        text = text or "Mocked Idea"
        longtext = longtext or "This is some text with a randomly generated priority"
        priority = priority or Priority(random.randint(1, len(Priority)))
        tags = tags or Tag(random.randint(1, 2 ** len(Tag) - 1))
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
            if 1 <= new_prio <= len(Priority):
                self.priority = Priority(new_prio)
            else:
                logger.warning("Illegal argument for change_priority of idea '{}...'".format(str(self.uid)[:8]))
        elif new_prio is None:
            if promote:
                self.promote()
            else:
                self.demote()
        else:
            raise TypeError("Illegal argument {} for change_priority for idea '{}...'.".format(new_prio, str(self.uid)[:8]))

    '''Change priority to one higher (numerically lower). '''
    def promote(self):
        if self.priority == 1:
            logger.warning("Failure while trying to promote idea '{}...', already at highest priority.".format(str(self.uid)[:8]))
        else:
            self.priority = Priority(self.priority.value - 1)

    '''Change priority to one lower (numerically higher). '''
    def demote(self):
        if self.priority == len(Priority):
            logger.warning("Failure while trying to demote idea '{}...', already at lowest priority.".format(str(self.uid)[:8]))
        else:
            self.priority = Priority(self.priority.value + 1)

    def pickle(self):
        import pickle
        logger.debug("Pickling idea '{}...' to object".format(str(self.uid)[:8]))
        return pickle.dumps(self)

    ''' Serializes object to file '''
    def pickle_to(self, filename, data_dir=default_data_dir):
        import pickle, os
        if not os.path.exists(data_dir):
            logger.warning("Directory {} doesn't exist. Trying to create it.".format(data_dir))
            os.makedirs(data_dir)
        with open(os.path.join(data_dir, filename), mode="wb") as file:
            logger.debug("Pickling to idea '{}...' file: {}".format(str(self.uid)[:8], os.path.join(data_dir, filename)))
            pickle.dump(self, file)


if __name__ == '__main__':
    configure_logging()
    i = Idea.mock().change_priority(8)

