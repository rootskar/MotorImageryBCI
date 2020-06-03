#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "Karel Roots"

from tensorflow.keras import backend as K


def divide_chunks(data, chunks):
    for i in range(0, len(data), chunks):
        yield data[i:i + chunks]


# need these for ShallowConvNet
def square(x):
    return K.square(x)


def log(x):
    return K.log(K.clip(x, min_value=1e-7, max_value=10000))
