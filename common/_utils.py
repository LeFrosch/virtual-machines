import typing

T = typing.TypeVar('T', covariant=True)


class SupportsIter(typing.Protocol[T]):
    def __iter__(self) -> T: ...


def first(xs: SupportsIter) -> typing.Optional[T]:
    return next(iter(xs), None)


def nth(xs: list[T], n: int) -> typing.Optional[T]:
    if len(xs) <= n:
        return None
    else:
        return xs[n]
