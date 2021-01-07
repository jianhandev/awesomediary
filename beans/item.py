class Item:
    def __init__(self, name, count):
        self.__name = name
        self.__count = count

    @property
    def name(self):
        return self.__name

    @property
    def count(self):
        return self.__count
