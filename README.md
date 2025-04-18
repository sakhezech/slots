# slots

Gambling in real life. How did noone thing of this before?

![Showcase](./.github/showcase.gif)

## CLI

```console
$ slots -h
usage: slots [-h] [-v] [--seed SEED | -r VAL [VAL ...]] [-T PERIOD]
             [-c {...}]
             columns

positional arguments:
  columns               number of columns

options:
  -h, --help            show this help message and exit
  -v, --version         show program's version number and exit
  --seed SEED           random seed (defaults to None)
  -r, --rig VAL [VAL ...]
                        list of roll values, number of values must match
                        number of columns
  -T, --period PERIOD   interval between frames in seconds (defaults to 0.05)
  -c, --chars {...}
                        charset (defaults to small_nums)
```

You can make your own slots CLI.

```py
#!/usr/bin/env python3
import slots
from slots import predefined_charsets

yay_gambling = slots.Slots(predefined_charsets.small_nums, columns=10)

if __name__ == '__main__':
    from slots.__main__ import user_cli

    user_cli(yay_gambling)
```
