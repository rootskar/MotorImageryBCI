#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
from statistics import Statistics

import numpy as np
from classifier import Classifier
from enums import ProgressType
from preprocess import preprocess_data
from signal_reader import SignalReader
from task import ExecutedTask, ImaginedTask
from utils import divide_chunks


class Experiment(object):

    def __init__(self, subject_id, run_type, selected_model, nr_of_tasks, showing_predictions, transfer_learning,
                 debug_mode, models, sample_rate=128):
        self.subject_id = subject_id
        self.run_type = run_type
        self.selected_model = selected_model
        self.nr_of_tasks = nr_of_tasks
        self.experiment_running = False
        self.showing_predictions = showing_predictions
        self.transfer_learning = transfer_learning
        self.models = models
        self.sample_rate = sample_rate
        self.signal_reader = SignalReader(mock_server=debug_mode)
        self.classifier = Classifier(transfer_learning, run_type, subject_id, selected_model, models)
        # dict with model name as key, corresponding statistics object as value
        self.statistics = dict(zip([model.get_name() for model in models],
                                   [Statistics(subject_id, run_type, transfer_learning, model.get_name()) for model in
                                    models]))
        self.tasks = self.generate_tasks(run_type, nr_of_tasks)
        self.current_task_id = 0
        self.recorded_data = {
            "samples": [],
            "labels": []
        }

    # Generates a list of tasks alternating between left/right and starting with right hand task
    def generate_tasks(self, run_type, nr_of_tasks):
        return [self.generate_task(run_type, i + 1, 0) if i % 2
                else self.generate_task(run_type, i + 1, 1) for i in range(nr_of_tasks)]

    def generate_task(self, run_type, task_nr, task_type):
        if run_type == 0:
            return ExecutedTask(task_nr, task_type)
        elif run_type == 1:
            return ImaginedTask(task_nr, task_type)
        raise AttributeError("Invalid run type {}".format(run_type))

    def run(self, progress_callback):
        print("Running experiment")
        self.experiment_running = True
        rest_time = 1  # number of seconds to show rest/prediction
        try:
            self.signal_reader.open_stream()
        except ConnectionRefusedError:
            raise Exception("Connection to EEG device could not be made")

        time.sleep(rest_time)  # show rest
        for i in range(self.nr_of_tasks):
            # stop if experiment was stopped externally
            if not self.experiment_running:
                break

            task = self.get_next_task()
            progress_callback.emit((task, ProgressType.TaskStart))
            try:
                recorded_task = self.record_and_predict(task)
            except ConnectionResetError:
                raise Exception("Connection to EEG device was closed")
            except OSError:
                break
            progress_callback.emit((recorded_task, ProgressType.TaskResult))

            # not showing rest state after last task
            if i == self.nr_of_tasks - 1 and not self.showing_predictions:
                break

            time.sleep(rest_time)  # show rest/prediction

        self.save_statistics()

    def save_statistics(self):
        for stats in self.statistics.values():
            stats.save_statistics()

    def get_next_task(self):
        next_task = self.tasks[self.current_task_id]
        self.current_task_id += 1
        return next_task

    def record_and_predict(self, task):
        task_data = self.record_data(task)
        task.set_data(task_data)

        selected_model_preds, all_preds = self.classifier.predict(task)
        task.set_predictions(selected_model_preds, all_preds)
        print('Real: {} Predicted: {}'.format(task.get_task_type(), task.get_majority_prediction()))

        for preds in all_preds:
            model_name = preds.get_model_name()
            self.statistics[model_name].record_task(task.get_task_type(), preds.get_predictions())

        return task

    def apply_transfer_learning(self, progress_callback):
        # apply transfer learning if option enabled
        if self.transfer_learning:
            self.classifier.run_transfer_learning(self.recorded_data)

    def record_data(self, task, preprocess=True):
        samples_to_collect = task.get_run_time() * self.sample_rate
        channels = 14
        samples_per_chunk = 80
        chunks = int(samples_to_collect / samples_per_chunk)
        data_array = np.zeros((channels, chunks, samples_per_chunk))

        data = self.signal_reader.read_signals(8960)
        # print(len(data))

        # (640, 14) => (14, 640)
        data = np.array(data).swapaxes(0, 1)

        if preprocess:
            for i, channel_data in enumerate(data):
                processed_data = preprocess_data(channel_data, sample_rate=128, notch=True, bp_filter=True,
                                                 artifact_removal=True)
                data_array[i] = list(divide_chunks(processed_data, 80))
        else:
            data_array = data

        # (14, 8, 80) => (14, 80, 8) => (8, 80, 14)
        samples = data_array.swapaxes(1, 2).swapaxes(0, 2)
        labels = [task.get_task_type()] * 8  # all 8 labels have same target

        # save all data for transfer learning
        if self.transfer_learning:
            self.recorded_data['samples'].append(samples)
            self.recorded_data['labels'].extend(labels)

        task_data = {
            "samples": samples,
            "labels": labels
        }

        return task_data

    def stop(self):
        self.experiment_running = False
        self.signal_reader.close_stream()

    def get_statistics(self):
        return self.statistics

    def set_run_time(self, time):
        for stats in self.statistics.values():
            stats.set_total_time(time)
