from typing import Collection, Sequence


class Wheel[T]:
    def __init__(
        self,
        chars: Collection[tuple[T, Sequence[str]]],
        spins: int = 0,
        start_idx: int = 0,
        window_size: int | None = None,
    ) -> None:
        self.charset = chars
        self.spins = spins
        if window_size is None:
            window_size = len(self.charset)

        height = -1
        width = -1

        if not self.charset:
            raise ValueError('charset has to have at least 1 character')

        for _, char in self.charset:
            if height == -1:
                height = len(char)
                width = len(char[0])
            if len(char) != height or not all(
                len(line) == width for line in char
            ):
                raise ValueError('not all characters have the same size')

        self.offset = width

        left_chars = window_size // 2
        right_chars = window_size - left_chars - 1
        self.arrow_line = (
            ' ' * left_chars * self.offset
            + '^'.center(self.offset)
            + ' ' * right_chars * self.offset
        )
        self._res_idx_offset = left_chars * self.offset

        self.charsheet = [
            ''.join([char_lines[idx] for _, char_lines in self.charset])
            for idx in range(height)
        ]
        self.charsheet.insert(0, '-' * len(self.charsheet[0]))
        self.charsheet.append('-' * len(self.charsheet[0]))

        self.count = 0

        self.window_size = window_size * self.offset
        self.max_idx = len(self.charset) * self.offset
        self.idx = (start_idx - left_chars) * self.offset

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

    def get_value(self) -> T:
        self.idx += self._res_idx_offset
        idx = self.idx
        self.idx -= self._res_idx_offset
        return self._idx_to_val[idx]

    def get_frame(self) -> list[str]:
        start = self.idx
        end = self.idx + self.window_size

        if end > len(self.charsheet[0]):
            frame = [
                line[self.idx :] + line[: end - len(self.charsheet[0])]
                for line in self.charsheet
            ]
        else:
            frame = [line[start:end] for line in self.charsheet]
        frame.append(self.arrow_line)
        return frame

    def advance_frame(self) -> bool:
        done = True
        if self.count < self.spins * self.offset:
            done = False
            self.count += 1
            self.idx += 1
        return done
