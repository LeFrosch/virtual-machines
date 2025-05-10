_instruction_map = {}


class InstructionMeta(type):
    def __new__(mcs, name, bases, namespace):
        cls = super().__new__(mcs, name, bases, namespace)

        if len(bases) > 0:
            _instruction_map[name] = cls

        return cls


class Instruction(metaclass=InstructionMeta):
    def __init__(self, labels=None, arguments=None):
        self.labels = labels or []

        parameters = self.__class__.__annotations__

        if len(parameters) != len(arguments or []):
            raise TypeError(f'expected {len(parameters)} operands, got: {len(arguments)}')

        for (name, t), value in zip(self.__class__.__annotations__.items(), arguments or []):
            if not isinstance(value, t):
                raise TypeError(f'operand {name} is of type {t}, got: {value}')

            setattr(self, name, value)

    @property
    def opcode(self):
        return self.__class__.__name__

    @classmethod
    def create(cls, opcode: str, labels=None, arguments=None):
        if opcode not in _instruction_map:
            raise KeyError(f'unknown opcode: {opcode}')

        clazz = _instruction_map[opcode]
        return clazz(labels=labels, arguments=arguments)

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


class JMP(Instruction):
    target: str


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
