from core.idea import Idea, Priority, Tag
from uuid import uuid4
import logging
from util.log import configure_logging
from util.helpers import pickle_to, from_file


logger = logging.getLogger(__name__)


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
    build_version = 19
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
        return from_file(cls, filename, data_dir)

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
        logger.info(self)
        self.uid = uuid4()
        self.ideas = []
        for arg in args:
            self.add_idea(arg)
        self._unserialized = []
        logger.info("Created Nemo with uid={} and ideas={}".format(self.uid, self.ideas))

    def __call__(self, *args, **kwargs):
        logger.debug("In __call__, with args={} and kwargs={}".format(args, kwargs))
        print("WHAT DID YOU CALL ME?")

    def __enter__(self):
        logger.debug("In __enter__")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        logger.debug("In __exit__")

    def __del__(self):
        pass

    def __getattr__(self, item):
        logger.debug("In __getattr__, accessing {}".format(item))
        try:
            return self.__dict__[item]
        except KeyError:
            logger.warning("Trying to access '{}' in __getattr__.".format(item))
            return "lol, no attr with that name"

    def __setattr__(self, key, value):
        logger.debug("In __setattr__, setting '{}' to '{}'".format(key, value))
        try:
            if value is None:
                del self.__dict__[key]
            else:
                self.__dict__[key] = value
        except KeyError:
            logger.warning("Failure while trying to set '{}' to value '{}' in __setattr__.".format(key, value))

    def __getitem__(self, item):
        logger.debug("In __getitem__, accessing {}".format(item))
        try:
            return self.__dict__[item]
        except KeyError:
            logger.warning("Failure while trying to access '{}' in __getitem__.".format(item))
            return "lol, no item with that name"

    def __setitem__(self, key, value):
        logger.debug("In __setitem__, setting '{}' to '{}'".format(key, value))
        try:
            if value is None:
                del self.__dict__[key]
            else:
                self.__dict__[key] = value
        except KeyError:
            logger.warning("Failure while trying to set '{}' to value '{}' in __setitem__.".format(key, value))

    def __getstate__(self):
        logger.debug("In __getstate__")
        self._unserialized = None
        return self.__dict__

    def __setstate__(self, state):
        logger.debug("In __setstate__, with state: {}".format(state))
        self.__dict__ = state

    def __str__(self):
        logger.debug("In __str__")
        return self.version_str

    def add_idea(self, val):
        if isinstance(val, Idea):
            self.ideas.append(val)
        elif isinstance(val, list):
            for elem in val:
                self.add_idea(elem)
        else:
            logger.info("Skipping invalid element while adding ideas.")

    def eval(self, cmd):
        raise NotImplementedError

    def nope(self):
        return None

    def puke(self):
        for key in self.__dict__:
            print("{}: {}".format(key, self[key]))

    def to_file(self, filename, data_dir=default_data_dir):
        pickle_to(self, filename, data_dir)

    def pickle(self):
        import pickle
        logger.debug("Pickling to object")
        return pickle.dumps(self)

    def idea_by_uid(self, uid):
        logger.debug("Requesting idea by uid: {}".format(uid))
        for val in self.ideas:
            if val.uid == uid:
                return val
        logger.warning("No idea with uid: {} found.".format(uid))
        return None

    def ideas_by_priority(self, priority=Priority.MUST):
        logger.debug("Requesting ideas by priority: {}".format(str(priority)))
        return [val for val in self.ideas if val.priority == priority]

    def ideas_by_tag(self, tag=Tag.REASONABLE):
        logger.debug("Requesting ideas by tag: {}".format(str(tag)))
        return [val for val in self.ideas if tag in val.tags]


if __name__ == '__main__':
    configure_logging(threshold=logging.INFO)
    logger.info("Initialized logger {}".format(logger))
    n = Nemo.from_file("unserialized.pickle")
