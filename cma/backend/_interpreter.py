from cma.frontend import instructions


def built_label_table(code: list[instructions.Instruction]) -> dict[str, int]:
    table = {}

    for i, instruction in enumerate(code):
        for label in instruction.labels:
            # TODO: check for duplicated labels
            table[label] = i

    return table

def bool_to_int(value: bool) -> int:
    return 1 if value else 0

class Interpreter:
    def __init__(self, code: list[instructions.Instruction]):
        self._code = code
        self._stack = [0] * 256
        self._sp = 0
        self._pc = 0
        self._labels = built_label_table(code)

    @property
    def stack(self):
        return self._stack[: self._sp]

    def execute(self):
        while True:
            instruction = self._code[self._pc]
            self._pc += 1

            if isinstance(instruction, instructions.HALT):
                break

            self._execute(instruction)

    def _execute(self, instruction: instructions.Instruction):
        match instruction:
            case instructions.LOADC(value=value):
                self._stack[self._sp] = value
                self._sp += 1

            case instructions.ADD():
                self._stack[self._sp - 1] += self._stack[self._sp]
                self._sp -= 1

            case instructions.JMP(target=target):
                # TODO: report error for unknown label
                self._pc = self._labels[target]

            case instructions.LEQ():
                self._stack[self._sp - 2] = bool_to_int(self._stack[self._sp - 2] <= self._stack[self._sp - 1])
                self._sp -= 1

            case instructions.EQL():
                self._stack[self._sp - 2] = bool_to_int(self._stack[self._sp - 2] == self._stack[self._sp - 1])
                self._sp -= 1

            case instructions.GEQ():
                self._stack[self._sp - 2] = bool_to_int(self._stack[self._sp - 2] >= self._stack[self._sp - 1])
                self._sp -= 1
