small_nums = [
    (
        num,
        [
            '|   |',
            f'| {str(num)} |',
            '|   |',
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
eight_segment = [
    (
        0,
        [
            '|┏━┓|',
            '|┃ ┃|',
            '|┗━┛|',
        ],
    ),
    (
        1,
        [
            '|  ╻|',
            '|  ┃|',
            '|  ╹|',
        ],
    ),
    (
        2,
        [
            '|╺━┓|',
            '|┏━┛|',
            '|┗━╸|',
        ],
    ),
    (
        3,
        [
            '|╺━┓|',
            '|╺━┫|',
            '|╺━┛|',
        ],
    ),
    (
        4,
        [
            '|╻ ╻|',
            '|┗━┫|',
            '|  ╹|',
        ],
    ),
    (
        5,
        [
            '|┏━╸|',
            '|┗━┓|',
            '|╺━┛|',
        ],
    ),
    (
        6,
        [
            '|┏━╸|',
            '|┣━┓|',
            '|┗━┛|',
        ],
    ),
    (
        7,
        [
            '|╺━┓|',
            '|  ┃|',
            '|  ╹|',
        ],
    ),
    (
        8,
        [
            '|┏━┓|',
            '|┣━┫|',
            '|┗━┛|',
        ],
    ),
    (
        9,
        [
            '|┏━┓|',
            '|┗━┫|',
            '|╺━┛|',
        ],
    ),
]

_charsets = {
    'small_nums': small_nums,
    'eight_segment': eight_segment,
    'uppercase_letters': uppercase_letters,
    'lowercase_letters': lowercase_letters,
}
_ = _charsets
