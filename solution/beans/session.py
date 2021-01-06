class Session:
    def __init__(self, sid, is_new):
        self.__id = sid
        self.__is_new = is_new

    @property
    def id(self):
        return self.__id

    @property
    def is_new(self):
        return self.__is_new
