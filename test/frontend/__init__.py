import unittest

from cma.frontend import parse
from test.utils import FileTestMeta


class FileTest(unittest.TestCase, metaclass=FileTestMeta, path=__file__):
    def do_test(self, input: str, output: str):
        actual = '\n'.join([repr(it) for it in parse(input)])
        self.assertEqual(output, actual)
