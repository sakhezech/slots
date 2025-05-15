import random
import time
from typing import Callable, Collection, Generator, Protocol, Sequence

from .modifier_functions import linear


class Spinnable[T](Protocol):
    spins: int
    charset: Collection[tuple[T, Sequence[str]]]

    def __init__(
        self, chars: Collection[tuple[T, Sequence[str]]], *args, **kwargs
    ) -> None: ...

    def rig_value(self, value: T) -> None: ...
    def get_value(self) -> T: ...
    def get_frame(self) -> list[str]: ...
    def advance_frame(self) -> bool: ...


class Slots[T]:
    def __init__(
        self,
        columns: list[Spinnable[T]],
    ) -> None:
        if len(columns) < 1:
            raise ValueError(
                f'number of columns must be greater than 0: {len(columns)}'
            )
        self.columns = columns

    def randomize(
        self, seed: int | str | bytes | bytearray | None = None
    ) -> None:
        rand = random.Random(seed)
        acc = 0
        for col in self.columns:
            acc += rand.randint(1, len(col.charset))
            col.spins += acc

    def rig_values(self, values: Sequence[T]) -> None:
        if len(self.columns) != len(values):
            raise ValueError(
                'number of columns and number of values are different: '
                f'{len(self.columns)} {len(values)}'
            )
        acc = 0
        for col, value in zip(self.columns, values):
            spin_before_rigging = col.spins

            col.spins += 1 + acc
            col.rig_value(value)

            spin_after_rigging = col.spins
            acc = spin_after_rigging - spin_before_rigging

    def get_values(self) -> list[T]:
        return [column.get_value() for column in self.columns]

    def get_frames(self) -> Generator[list[str]]:
        while True:
            frames = [column.get_frame() for column in self.columns]
            statuses = [column.advance_frame() for column in self.columns]

            height = len(frames[0])
            main_frame = [
                ''.join([char_lines[idx] for char_lines in frames])
                for idx in range(height)
            ]

            yield main_frame

            if all(statuses):
                break

    def spin(
        self,
        period: float = 0.05,
        modifier: Callable[[float, float], float] | None = None,
    ) -> None:
        if period <= 0:
            raise ValueError(f'period must be greater than 0: {period}')
        if modifier is None:
            modifier = linear
        frame_lines = None

        frames = list(self.get_frames())
        number_of_frames = len(frames)

        for i, frame_lines in enumerate(frames):
            print('\n'.join(frame_lines))
            time.sleep(modifier(period, i / number_of_frames))
            print(f'\x1b[{len(frame_lines)}A\r\x1b[J', end='')

        assert frame_lines
        print('\n'.join(frame_lines))
