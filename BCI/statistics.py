#!/usr/bin/env python
# -*- coding: utf-8 -*-

from file_writer import FileWriter
import numpy as np


class Statistics(object):

    def __init__(self, subject_id, run_type, transfer_learning, model_name):
        self.subject_id = subject_id
        self.run_type = run_type
        self.transfer_learning = transfer_learning
        self.model_name = model_name
        self.left_hand_total = 0
        self.right_hand_total = 0
        self.left_hand_correct = 0
        self.right_hand_correct = 0
        self.total_time_taken = 0  # int in seconds
        self.predictions = []
        self.file_writer = FileWriter()

    def record_task(self, hand, predictions):
        self.predictions.extend(predictions)
        for prediction in predictions:
            if hand == 0:
                if hand == prediction:
                    self.left_hand_correct += 1
                    self.left_hand_total += 1
                else:
                    self.right_hand_total += 1
            elif hand == 1:
                if hand == prediction:
                    self.right_hand_correct += 1
                    self.right_hand_total += 1
                else:
                    self.left_hand_total += 1
            else:
                raise AttributeError("Invalid task type (0 or 1)")

    def save_statistics(self):
        stats_to_save = [self.subject_id, self.parse_model_name(self.model_name),
                         self.run_type, self.transfer_learning,
                         self.get_left_hand_correct(), self.get_right_hand_correct(),
                         self.get_left_hand_incorrect(), self.get_right_hand_incorrect(),
                         self.get_left_hand_total(), self.get_right_hand_total(),
                         self.get_total_tasks(), self.get_correct_total(),
                         self.get_incorrect_total(), '{:.2}'.format(float(self.get_accuracy())),
                         self.get_total_time()]
        self.file_writer.save_stats(stats_to_save)
        self.save_predictions()

    def parse_model_name(self, model_name):
        return model_name[:model_name.rfind('_')]

    def save_predictions(self):
        stats_to_save = [self.model_name, self.run_type, self.transfer_learning, ','.join(map(str, self.predictions))]
        self.file_writer.save_predictions(stats_to_save)

    def get_run_type(self):
        return self.run_type

    def set_total_time(self, time):
        self.total_time_taken = time

    def get_total_time(self):
        return self.total_time_taken

    def get_total_tasks(self):
        return self.left_hand_total + self.right_hand_total

    def get_left_hand_correct(self):
        return self.left_hand_correct

    def get_right_hand_correct(self):
        return self.right_hand_correct

    def get_left_hand_incorrect(self):
        return self.left_hand_total - self.left_hand_correct

    def get_right_hand_incorrect(self):
        return self.right_hand_total - self.right_hand_correct

    def get_correct_total(self):
        return self.right_hand_correct + self.left_hand_correct

    def get_incorrect_total(self):
        return self.get_left_hand_incorrect() + self.get_right_hand_incorrect()

    def get_left_hand_total(self):
        return self.left_hand_total

    def get_right_hand_total(self):
        return self.right_hand_total

    def get_accuracy(self):
        if self.get_correct_total() == 0:
            return 0
        return np.round(self.get_correct_total() / self.get_total_tasks(), 3)
