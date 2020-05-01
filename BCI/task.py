#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np


class Task(object):

    def __init__(self, task_nr, task_type, run_time=5):
        self.task_nr = task_nr
        self.task_type = task_type  # 0 - left hand, 1 - right hand
        self.run_time = run_time  # int in seconds
        self.all_predictions = []  # List of Predictions objects for all models
        self.selected_model_predictions = None  # Selected model Predictions object

    def set_data(self, data):
        self.data = data

    def set_predictions(self, selected_model_preds, all_preds):
        self.selected_model_predictions = selected_model_preds
        self.all_predictions = all_preds

    def get_data(self):
        return self.data

    def get_run_time(self):
        return self.run_time

    def get_task_nr(self):
        return self.task_nr

    def get_task_type(self):
        return self.task_type

    def get_all_predictions(self):
        return self.all_predictions

    def get_selected_model_predictions(self):
        return self.selected_model_predictions

    def get_majority_prediction(self):
        counts = np.bincount(self.selected_model_predictions.get_predictions())
        return np.argmax(counts)


class ExecutedTask(Task):

    def __init__(self, task_nr, task_type):
        super(ExecutedTask, self).__init__(task_nr, task_type)
        self.run_type = 0


class ImaginedTask(Task):

    def __init__(self, task_nr, task_type):
        super(ImaginedTask, self).__init__(task_nr, task_type)
        self.run_type = 1
