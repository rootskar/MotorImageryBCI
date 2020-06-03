#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "Karel Roots"

import os.path

import numpy as np
from predictions import Predictions
from sklearn.model_selection import train_test_split
from tensorflow.keras import backend as K
from tensorflow.keras import callbacks
from tensorflow.keras.losses import binary_crossentropy
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.utils import to_categorical

class Classifier(object):

    def __init__(self, transfer_learning, run_type, subject_id, selected_model, models):
        self.DISABLED_LAYERS = {
            'EEGNet_Fusion': [(0, 8), (14, 22), (28, 36)],
            'EEGNet': [(0, 8)],
            'ShallowConvNet': [(0, 2)],
            'DeepConvNet': [(0, 15)]
        }
        self.transfer_learning = transfer_learning
        self.run_type = run_type
        self.subject_id = subject_id
        self.selected_model = selected_model
        self.selected_model_name = selected_model.get_name()
        self.models = models
        self.tl_file_name = self.get_tl_file_name(self.selected_model_name)
        K.set_image_data_format('channels_last')

    def disable_layers(self, model, model_name):
        key = model_name[:model_name.rfind('_')]
        for layers_range in self.DISABLED_LAYERS[key]:
            for layer in (model.layers)[layers_range[0]:layers_range[1]]:
                layer.trainable = False

        return model

    def predict(self, task):
        data = task.get_data()['samples']
        data = data.reshape(data.shape[0], data.shape[1], data.shape[2], 1)
        all_preds = []
        for model_obj in self.models:
            all_preds.append(self.get_model_predictions(model_obj.get_model(), model_obj.get_name(), data))

        selected_model_preds = self.get_model_predictions(self.selected_model.get_model(),
                                                          self.selected_model.get_name(), data)

        return selected_model_preds, all_preds

    def get_model_predictions(self, model, model_name, data):
        tl_file_name = self.get_tl_file_name(model_name)
        if os.path.isfile(tl_file_name):
            model.load_weights(tl_file_name)
        probs = model.predict([data, data, data])
        preds = probs.argmax(axis=-1)

        return Predictions(model_name, preds)

    def get_tl_file_name(self, model_name):
        run_str = 'Executed' if self.run_type == 0 else 'Imagined'
        if run_str.lower() in model_name.lower():
            return './models/{}_subj_id_{}.h5'.format(model_name, str(self.subject_id))
        else:
            return './models/{}_{}_subj_id_{}.h5'.format(model_name, run_str, str(self.subject_id))

    def run_transfer_learning(self, data):
        X = np.array(data['samples'])
        if len(X.shape) < 4:
            print("Not running TL. Data was not correctly collected")
            return
        X = X.reshape(-1, X.shape[2], X.shape[3], 1)
        y = np.array(data['labels'])
        y = to_categorical(y, 2)
        X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.1, random_state=42)

        for model_obj in self.models:
            model = model_obj.get_model()
            model_name = model_obj.get_name()
            tl_file_name = self.get_tl_file_name(model_name)

            # loading TL weights for current subject if file exists, otherwise saving to a new file
            if os.path.isfile(tl_file_name):
                try:
                    model.load_weights(tl_file_name)
                except:
                    pass

            model = self.disable_layers(model, model_name)

            callbacks_list = [callbacks.ModelCheckpoint(tl_file_name,
                                                        save_best_only=True, monitor='val_loss'),
                              callbacks.ReduceLROnPlateau(monitor='val_loss', factor=0.1, patience=5)]

            model.compile(loss=binary_crossentropy, optimizer=Adam(lr=0.001), metrics=['accuracy'])
            model.fit([X_train, X_train, X_train], y_train, batch_size=64, epochs=100,
                    validation_data=([X_val, X_val, X_val], y_val), verbose=False, callbacks=callbacks_list)
