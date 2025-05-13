from common import first

_instruction_map = {}


class InstructionMeta(type):
    def __new__(mcs, name, bases, namespace):
        cls = super().__new__(mcs, name, bases, namespace)

        if len(bases) > 0:
            _instruction_map[name] = cls

        return cls


class Instruction(metaclass=InstructionMeta):
    def __init__(self, labels=None, argument=None):
        self.labels = labels or []

        parameter = first(self.__class__.__annotations__.items())
        if parameter is None:
            return

        name, t = parameter
        value = argument if argument is not None else getattr(self, name, None)

        if not isinstance(value, t):
            raise TypeError(f'instruction {self.opcode} operand {name} is of type {t}, got: {value}')

        setattr(self, name, value)

    @property
    def opcode(self):
        return self.__class__.__name__

    @classmethod
    def create(cls, opcode: str, labels=None, argument=None):
        if opcode not in _instruction_map:
            raise KeyError(f'unknown opcode: {opcode}')

        clazz = _instruction_map[opcode]
        return clazz(labels=labels, argument=argument)

    def __repr__(self):
        parameters = self.__class__.__annotations__

        if len(parameters) == 0:
            return f'<{self.opcode}>'

        arguments = ', '.join(repr(getattr(self, it)) for it in list(parameters))
        return f'<{self.opcode} {arguments}>'


class ADD(Instruction):
    pass


class MUL(Instruction):
    pass


class LOADC(Instruction):
    value: int


class JUMP(Instruction):
    target: str


class JUMPZ(Instruction):
    target: str


class JUMPI(Instruction):
    table: int


class HALT(Instruction):
    pass


class LEQ(Instruction):
    pass


class EQL(Instruction):
    pass


class GEQ(Instruction):
    pass


class SUB(Instruction):
    pass


class DIV(Instruction):
    pass


class NEG(Instruction):
    pass


class ALLOC(Instruction):
    size: int


class DUP(Instruction):
    pass


class POP(Instruction):
    count: int = 1


class STORE(Instruction):
    size: int = 1


class LOAD(Instruction):
    size: int = 1


class NEW(Instruction):
    pass


class FREE(Instruction):
    pass
