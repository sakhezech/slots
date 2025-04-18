small_nums = [
    (
        num,
        [
            '|     |',
            f'|{str(num).center(5)}|',
            '|     |',
        ],
    )
    for num in range(0, 10)
]
uppercase_letters = [
    (
        chr(65 + num),
        [
            '|   |',
            f'| {chr(65 + num)} |',
            '|   |',
        ],
    )
    for num in range(26)
]
lowercase_letters = [
    (
        chr(97 + num),
        [
            '|   |',
            f'| {chr(97 + num)} |',
            '|   |',
        ],
    )
    for num in range(26)
]

_charsets = {
    'small_nums': small_nums,
    'uppercase_letters': uppercase_letters,
    'lowercase_letters': lowercase_letters,
}
_ = _charsets
