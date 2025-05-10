import unittest

from cma.frontend import parse
from cma.backend import Interpreter
from test.utils import FileTestMeta


class FileTest(unittest.TestCase, metaclass=FileTestMeta, path=__file__):
    def do_test(self, input: str, output: str):
        interpreter = Interpreter(parse(input))
        interpreter.execute()

        actual = '\n'.join('%02d: %d' % (i, it) for i, it in enumerate(interpreter.stack))
        self.assertEqual(output, actual)
