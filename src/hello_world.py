import numpy as np


class HelloWorld:
    def __init__(self, output):
        self.output = output


    def return_output(self):
        """
        This is a multiline comment. It usually contains documentation.
        And a second line
        """
        return self.output


    def do_maths(self):
        """
        Returns a filled array
        """
        return np.full((2,3), 5) * 10


    @staticmethod
    def static_call(str1, str2="World"):
        return str1 + str2
