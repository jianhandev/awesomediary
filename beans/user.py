class User:
    def __init__(self, user_id, user_name, handle):
        self.__id = user_id
        self.__name = user_name
        self.__handle = handle

    @property
    def id(self):
        return self.__id

    @property
    def name(self):
        return self.__name
    
    @property
    def handle(self):
        return self.__handle

