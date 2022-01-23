# -*- coding: utf-8 -*-

import math


def float_cast(value, default=0):
    try:
        value = float(value)
        return default if math.isnan(value) or math.isinf(value) else value
    except:
        return default


if __name__ == '__main__':
    print(float_cast(123))
    print(float_cast('123'))
    print(float_cast('abc'))
    print(float_cast('nan'))
