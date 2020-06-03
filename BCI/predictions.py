#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "Karel Roots"


class Predictions(object):

    def __init__(self, model_name, predictions):
        self.model_name = model_name
        self.predictions = predictions

    def get_predictions(self):
        return self.predictions

    def set_predictions(self, predictions):
        self.predictions = predictions

    def get_model_name(self):
        return self.model_name

    def set_model_name(self, name):
        self.model_name = name
