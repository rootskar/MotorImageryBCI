#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "Karel Roots"

from glob import glob

from enums import ModelType
from tensorflow.keras.models import load_model
from utils import square, log


class Models(object):

    def __init__(self):
        # populate models from ./models
        self.executed_models = []
        self.imagined_models = []
        self.selected_model = None
        self.load_models()

    def add_model(self, model_name, model_type, model_path):
        self.check_if_exists(model_name, model_type)

        new_model = Model(model_name, model_type, model_path)
        if model_type == ModelType.Executed:
            self.executed_models.append(new_model)
        elif model_type == ModelType.Imagined:
            self.imagined_models.append(new_model)
        else:
            raise AttributeError("Invalid model type")

    def set_selected(self, model_type, model_name):
        self.selected_model = self.find_model(model_type, model_name)

    def get_selected(self):
        return self.selected_model

    def find_model(self, model_type, model_name):
        models = self.executed_models if model_type == 0 else self.imagined_models
        for model in models:
            if model.get_name() == model_name:
                return model

        return None

    def load_models(self):
        MODELS = glob('models/*.h5')
        FNAMES = sorted([model[model.rfind('\\') + 1:] for model in MODELS])
        for FNAME in FNAMES:
            fname = FNAME.lower()
            if 'subj_id' in fname:
                continue
            elif 'executed' in fname:
                model_type = ModelType.Executed
            elif 'imagined' in fname:
                model_type = ModelType.Imagined
            else:
                continue
            name_without_extension = FNAME[:-3]
            self.add_model(name_without_extension, model_type, './models/{}'.format(FNAME))

    def get_models(self, model_type):
        if model_type == ModelType.Executed:
            return self.executed_models
        elif model_type == ModelType.Imagined:
            return self.imagined_models
        else:
            raise AttributeError("Invalid model type")

    def check_if_exists(self, model_name, model_type):
        if model_type == ModelType.Executed:
            models = self.executed_models
        elif model_type == ModelType.Imagined:
            models = self.imagined_models
        else:
            raise AttributeError
        if any(model.get_name() == model_name for model in models):
            raise AttributeError


class Model(object):

    def __init__(self, model_name, model_type, model_path):
        self.model_name = model_name
        self.model_type = model_type
        self.model_path = model_path
        self.model = load_model(model_path, custom_objects={"square": square, "log": log})

    def get_model(self):
        return self.model

    def get_name(self):
        return self.model_name

    def get_type(self):
        return self.model_type

    def get_path(self):
        return self.model_path
