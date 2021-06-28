class GameOperation:

    @staticmethod
    def s(*args, **kwargs):

        def get_func(func):

            return GameOperation(func, *args, **kwargs)

        return get_func

    def __repr__(self):

        return f"""GameOp[{self.__func__.__name__}]"""

    def __init__(self, func, *args, **kwargs):

        self.__func__ = func
        self.__args__ = args
        self.__kwargs__ = kwargs

    def exec(self):

        result =  self.__func__(*self.__args__, **self.__kwargs__)

        return result