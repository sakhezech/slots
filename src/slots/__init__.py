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


class Column[T]:
    def __init__(
        self,
        chars: Collection[tuple[T, Sequence[str]]],
        spins: int = 0,
        start_idx: int = 0,
    ) -> None:
        self.charset = chars
        self.spins = spins

        height = -1
        width = -1

        if not self.charset:
            raise ValueError('charset has to have at least 1 character')

        self.charsheet: list[str] = []
        for _, char in self.charset:
            if height == -1:
                height = len(char)
                width = len(char[0])
            if len(char) != height or not all(
                len(line) == width for line in char
            ):
                raise ValueError('not all characters have the same size')

            self.charsheet.extend(
                [
                    '-' * width,
                    *char,
                ]
            )

        self.char_size = height
        self.sep_size = 1

        self.count = 0

        self.offset = self.char_size + self.sep_size
        self.max_idx = len(self.charset) * self.offset
        self.idx = start_idx * self.offset

        self._idx_to_val = {
            i * self.offset: val for i, (val, _) in enumerate(chars)
        }

    @property
    def idx(self) -> int:
        return self._idx

    @idx.setter
    def idx(self, value: int) -> None:
        self._idx = value
        if (self._idx >= self.max_idx) or (self._idx < 0):
            self._idx %= self.max_idx

    def rig_value(self, value: T) -> None:
        # NOTE: can't use dict because values can be unhashible
        for i, (v, _) in enumerate(self.charset):
            if v == value:
                break
        else:
            raise ValueError(f'no such value: {value}')
        curr = self.spins
        to = i
        self.spins += (to - curr) % len(self.charset)

    def get_value(self) -> T:
        return self._idx_to_val[self.idx]

    def get_frame(self) -> list[str]:
        start = self.idx
        end = self.idx + self.offset + self.sep_size

        if end > len(self.charsheet):
            frame = (
                self.charsheet[start:]
                + self.charsheet[: end - len(self.charsheet)]
            )
        else:
            frame = self.charsheet[start:end]
        return frame

    def advance_frame(self) -> bool:
        done = True
        if self.count < self.spins * self.offset:
            done = False
            self.count += 1
            self.idx += 1
        return done


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
