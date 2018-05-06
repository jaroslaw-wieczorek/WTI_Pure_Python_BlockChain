from itertools import tee, islice, chain

class Utilities:

    def previous_and_next(some_iterable):
        """This is great, incredibly useful.
            https://stackoverflow.com/questions/1011938/python-previous-and-next-values-inside-a-loop/1012089#1012089"""
        prevs, items, nexts = tee(some_iterable, 3)
        prevs = chain([None], prevs)
        nexts = chain(islice(nexts, 1, None), [None])
        return zip(prevs, items, nexts)
