#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv
from datetime import datetime


class FileWriter(object):

    def __init__(self):
        self.BASE_PATH = './results/'

    def save_stats(self, stats):
        date_time = datetime.now()
        stats.insert(0, date_time)
        self.write_to_file(stats, 'results.csv')

    def save_predictions(self, predictions):
        date_time = datetime.now()
        predictions.insert(0, date_time)
        self.write_to_file(predictions, 'predictions.csv')

    def write_to_file(self, row, file_name):
        file_name = self.BASE_PATH + file_name
        with open(file_name, mode='a', newline='') as statistics_file:
            writer = csv.writer(statistics_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            writer.writerow(row)
