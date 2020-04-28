#!/usr/bin/env python
# -*- coding: utf-8 -*-

from enum import Enum


class ElementType(Enum):
    Label = 1
    Value = 2
    Form = 3
    VBox = 4
    HBox = 5
    Grid = 6
    ComboBox = 7
    CheckBox = 8
    Button = 9


class GraphicType(Enum):
    Rest = 1
    LeftTask = 2
    RightTask = 3
    LeftCorrectPrediction = 4
    RightCorrectPrediction = 5
    LeftIncorrectPrediction = 6
    RightIncorrectPrediction = 7


class ModelType(Enum):
    Executed = 1
    Imagined = 2


class ViewType(Enum):
    Settings = 1
    Experiment = 2
    Statistics = 3


class ProgressType(Enum):
    TaskStart = 1
    TaskResult = 2


class LabelType(Enum):
    Rest = 1
    Task = 2
    Prediction = 3
