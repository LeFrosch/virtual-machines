import unittest

from cma.frontend import parse
from cma.backend import Interpreter
from test.utils import FileTestMeta


class FileTest(unittest.TestCase, metaclass=FileTestMeta, path=__file__):
    def assert_mem(self, mem: list[int], expected: str):
        actual = '\n'.join('%02d: %d' % (i, it) for i, it in enumerate(mem))
        self.assertEqual(expected, actual)

    def do_test(self, input: str, stack: str = None, heap: str = None):
        interpreter = Interpreter(parse(input))
        interpreter.execute()

        if stack is None and heap is None:
            self.fail('nothing to check')

        if stack is not None:
            self.assert_mem(interpreter.stack, stack)

        if heap is not None:
            self.assert_mem(interpreter.heap, heap)
