#!/usr/bin/env python
# -*- coding: utf-8 -*-

from glob import glob

from predict import predict_accuracy
from sklearn.model_selection import train_test_split
from tensorflow import global_variables_initializer
from tensorflow.keras import backend as K
from tensorflow.keras import callbacks
from tensorflow.keras.losses import binary_crossentropy
from tensorflow.keras.optimizers import Adam

"""
@input - model (Object); training data (List); training labels (List); validation data (List); validation labels (List); 
        testing data (List); testing labels (List); model name (String); optional args
         
Method that creates a new model and trains it on the input data. 
After training the saved weights for best validation loss are loaded and used for evaluation on test data.

@output - Trained model; Accuracy value (float); Truth values, if the prediction at index i was equal to the target label (List)
"""


def train_test_model(model, model_name, X_train, y_train, X_val, y_val, X_test, y_test, multi_branch, nr_of_epochs,
                     test_model=True):
    MODEL_LIST = glob('./model/*')
    new_model_name = './model/' + str(model_name) + '_' + str(len(MODEL_LIST)) + '.h5'
    print("New model name: " + new_model_name)
    acc = 0
    equals = []

    # Callbacks for saving best model, early stopping when validation accuracy does not increase and reducing
    # learning rate on plateau
    callbacks_list = [callbacks.ModelCheckpoint(new_model_name,
                                                save_best_only=True,
                                                monitor='val_loss'),
                      # callbacks.EarlyStopping(monitor='val_acc', patience=25),
                      callbacks.ReduceLROnPlateau(monitor='val_loss', factor=0.1, patience=5)]

    model.compile(loss=binary_crossentropy, optimizer=Adam(lr=0.001), metrics=['accuracy'])

    if multi_branch:
        history = model.fit([X_train, X_train, X_train], y_train, batch_size=64, shuffle=True, epochs=nr_of_epochs,
                            validation_data=([X_val, X_val, X_val], y_val), verbose=False, callbacks=callbacks_list)
    else:
        history = model.fit(X_train, y_train, batch_size=64, shuffle=True, epochs=nr_of_epochs,
                            validation_data=(X_val, y_val), verbose=False, callbacks=callbacks_list)

    # test model predictions
    if test_model:
        model.load_weights(new_model_name)
        acc, equals = predict_accuracy(model, X_test, y_test, new_model_name, multi_branch=multi_branch)

    return model, acc, equals


"""
@input - data (List); target labels (List); experiment object; optional args
         
Method that splits the input data into training and testing sets and evaluates the model.
If the use_kfold argument is True, the model is kfold cross-validated and the average cross-validation accuracy is printed.

@output - Experiment object with results
"""


def run_experiment(X, y, experiment, use_cpu=False, test_model=True):
    # Set the data format
    if use_cpu:
        K.set_image_data_format('channels_last')
    else:
        K.set_image_data_format('channels_first')

    # training/validation/test set split
    test_split = experiment.get_test_split()
    if test_split == 0:
        X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=experiment.get_val_split(), random_state=42)
        X_test, y_test = [], []
        test_model = False
    else:
        X_train_val, X_test, y_train_val, y_test = train_test_split(X, y, test_size=test_split, random_state=42)
        X_train, X_val, y_train, y_val = train_test_split(X_train_val, y_train_val,
                                                          test_size=experiment.get_val_split(), random_state=42)

    for model in experiment.get_models().values():
        _model = model.get_model()
        model_name = model.get_name() + '_' + experiment.get_exp_type()
        multi_branch = model.get_mb()

        # make sure weights are reset before training
        K.get_session().run(global_variables_initializer())

        # splitting training/testing sets
        _model, acc, equals = train_test_model(_model, model_name, X_train, y_train, X_val, y_val, X_test, y_test,
                                               multi_branch, experiment.get_epochs(), test_model=test_model)
        _model.save('./model/' + str(model_name) + '_best.h5')

        model.set_accuracy(acc)
        model.set_equals(equals)

    return experiment
