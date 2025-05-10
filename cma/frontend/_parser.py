import lark
import typing

from ._instructions import Instruction


def to_list(value):
    return [] if value is None else [value]


class Transformer(lark.Transformer):
    def start(self, children):
        return [it for it in children if isinstance(it, Instruction)]

    def line(self, children):
        return children[0]

    def instruction(self, children):
        return Instruction.create(
            opcode=str(children[1]),
            labels=to_list(children[0]),
            arguments=to_list(children[2]),
        )

    def operand_int(self, children):
        return int(children[0])

    def operand_ref(self, children):
        return str(children[0])

    def label(self, children):
        return str(children[0])


_parser = lark.Lark.open(
    'grammar.lark',
    rel_to=__file__,
    start='start',
    parser='lalr',
    transformer=Transformer(),
)


def parse(text: str) -> list[Instruction]:
    return typing.cast(list[Instruction], _parser.parse(text + '\n'))
