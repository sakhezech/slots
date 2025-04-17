import random
import time
from typing import Generator


class Column[T]:
    def __init__(
        self,
        chars: list[tuple[T, str]],
        spins: int,
        start_idx: int = 0,
    ) -> None:
        self.chars: list[str] = []
        # HACK: hardcoded characters
        # get a list of characters, paddings, and separators here
        # and construct the list
        for _, char in chars:
            self.chars.extend(
                [
                    '-----',
                    '|   |',
                    f'| {char} |',
                    '|   |',
                ]
            )
        self.char_size = 3
        self.sep_size = 1
        self.num_of_chars = len(chars)

        self.count = 0

        self.offset = self.char_size + self.sep_size
        self.max_idx = self.num_of_chars * self.offset
        self.idx = start_idx * self.offset
        self.steps_to_take = spins * self.offset

        self._idx_to_val = {
            i * self.offset: val for i, (val, _) in enumerate(chars)
        }

    @property
    def idx(self) -> int:
        return self._idx

    @idx.setter
    def idx(self, value: int) -> None:
        self._idx = value
        if (self._idx > self.max_idx) or (self._idx < 0):
            self._idx %= self.max_idx

    def get_value(self) -> T:
        return self._idx_to_val[self.idx]

    def get_frame(self) -> list[str]:
        start = self.idx
        end = self.idx + self.offset + self.sep_size

        if end > len(self.chars):
            frame = self.chars[start:] + self.chars[: end - len(self.chars)]
        else:
            frame = self.chars[start:end]
        return frame

    def advance_frame(self) -> bool:
        done = True
        if self.count < self.steps_to_take:
            done = False
            self.count += 1
            self.idx += 1
        return done


class Slots[T]:
    def __init__(
        self,
        chars: list[tuple[T, str]],
        num_of_columns: int = 3,
        seed: int | str | bytes | bytearray | None = None,
    ) -> None:
        self.num_of_columns = num_of_columns
        self.rand = random.Random(seed)
        self.columns: list[Column] = []

        spin_num = 0
        for _ in range(self.num_of_columns):
            # HACK: arbitrary numbers
            spin_num += self.rand.randint(1, 10)
            self.columns.append(Column(chars, spin_num))

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

    def spin(self) -> None:
        frame_lines = None

        for frame_lines in self.get_frames():
            print('\n'.join(frame_lines))
            # HACK: arbitrary time
            time.sleep(0.1)
            print(f'\x1b[{len(frame_lines)}A\r\x1b[J', end='')

        if frame_lines:
            print('\n'.join(frame_lines))
