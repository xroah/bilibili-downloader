class Singleton(object):
    def __new__(cls, *args, **kwargs):
        print(cls)
        if not hasattr(cls, "_instance"):
            cls._instance = super().__new__(cls)

        return cls._instance
