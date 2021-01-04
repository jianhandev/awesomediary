class User:
    def __init__(self, user_id, user_name):
        self.__id = user_id
        self.__name = user_name

    @property
    def id(self):
        return self.__id

    @property
    def name(self):
        return self.__name
