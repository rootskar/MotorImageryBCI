#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import time

from PyQt5 import QtCore, QtGui, QtWidgets
from enums import ElementType, GraphicType, ModelType, ViewType, ProgressType, LabelType
from experiment import Experiment
from models import Models
from worker import Worker


class Ui_MainWindow(object):

    def createUiElement(self, type, name, parent=None, font=None,
                        alignment=QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter,
                        layoutDirection=QtCore.Qt.LeftToRight, maximumSize=None, minimumSize=None, fixedSize=None,
                        isHidden=False, value="", items=[], margins=None):
        if type == ElementType.Label:
            uiElement = QtWidgets.QLabel(parent)
            uiElement.setObjectName(name)
            uiElement.setText(value)
            if alignment:
                uiElement.setAlignment(alignment)
            if font:
                uiElement.setFont(font)
        elif type == ElementType.Value:
            uiElement = QtWidgets.QLineEdit(parent)
            uiElement.setLayoutDirection(layoutDirection)
            uiElement.setText(value)
        elif type == ElementType.Form:
            uiElement = QtWidgets.QFormLayout()
            uiElement.setAlignment(alignment)
            if margins:
                uiElement.setContentsMargins(*margins)
        elif type == ElementType.VBox:
            if parent:
                uiElement = QtWidgets.QVBoxLayout(parent)
            else:
                uiElement = QtWidgets.QVBoxLayout()
            if margins:
                uiElement.setContentsMargins(*margins)
        elif type == ElementType.HBox:
            uiElement = QtWidgets.QHBoxLayout()
        elif type == ElementType.ComboBox:
            uiElement = QtWidgets.QComboBox(parent)
            for item in items:
                uiElement.addItem(item)
        elif type == ElementType.CheckBox:
            uiElement = QtWidgets.QCheckBox(parent)
            uiElement.setLayoutDirection(layoutDirection)
        elif type == ElementType.Button:
            uiElement = QtWidgets.QPushButton(parent)
        else:
            raise AttributeError("Invalid UI element type")

        if maximumSize:
            uiElement.setMaximumSize(maximumSize)
        if minimumSize:
            uiElement.setMinimumSize(minimumSize)
        if fixedSize:
            uiElement.setFixedSize(*fixedSize)
        if isHidden:
            uiElement.setHidden(True)

        uiElement.setObjectName(name)

        return uiElement

    def setupUi(self, mainWindow):
        self.mainWindow = mainWindow
        self.mainWindow.setObjectName("mainWindow")

        self.translate = QtCore.QCoreApplication.translate
        self.threadpool = QtCore.QThreadPool()
        self.models = Models()

        self.statusBar = QtWidgets.QStatusBar(mainWindow)
        self.statusBar.setObjectName("statusBar")
        self.statusBar.clearMessage()
        self.mainWindow.setStatusBar(self.statusBar)

        self.menuBar = QtWidgets.QMenuBar(mainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 680, 20))
        self.menuBar.setObjectName("menuBar")
        self.mainWindow.setMenuBar(self.menuBar)

        self.loadNewModelMenu = QtWidgets.QMenu(self.menuBar)
        self.loadNewModelMenu.setObjectName("loadNewModelMenu")

        self.actionLoadExecutedModel = QtWidgets.QAction("actionLoadExecutedModel", mainWindow)
        self.actionLoadImaginedModel = QtWidgets.QAction("actionLoadImaginedModel", mainWindow)
        self.addActions(self.loadNewModelMenu, [self.actionLoadExecutedModel, self.actionLoadImaginedModel])
        self.addActions(self.menuBar, [self.loadNewModelMenu.menuAction()])

        self.actionLoadExecutedModel.triggered.connect(lambda: self.loadModel(ModelType.Executed))
        self.actionLoadImaginedModel.triggered.connect(lambda: self.loadModel(ModelType.Imagined))

        self.retranslateUi()
        self.defineEvents(mainWindow)

        self.setupSettingsViewUi()

    def loadModel(self, model_type):
        if model_type == ModelType.Executed:
            model_path, _ = QtWidgets.QFileDialog.getOpenFileName(self.mainWindow, 'Load executed model', os.getcwd(),
                                                                  "Model files (*.h5)")
        elif model_type == ModelType.Imagined:
            model_path, _ = QtWidgets.QFileDialog.getOpenFileName(self.mainWindow, 'Load imagined model', os.getcwd(),
                                                                  "Model files (*.h5)")
        else:
            raise Exception("Invalid model type")

        if model_path == '':
            return

        model_name = model_path[model_path.rfind('/') + len('/'):model_path.rfind('.h5')]
        try:
            self.models.add_model(model_name, model_type, model_path)
            self.displayNewModelNames(self.runTypeComboBox.currentIndex())
        except AttributeError:
            self.displayError("Model with that name is already loaded")
        except OSError:
            self.displayError("Model loading failed")

    def retranslateUi(self):
        self.loadNewModelMenu.setTitle(self.translate("mainWindow", "Load new model"))
        self.actionLoadExecutedModel.setText(self.translate("mainWindow", "Load executed task model"))
        self.actionLoadImaginedModel.setText(self.translate("mainWindow", "Load imagined task model"))

    def toggleActionsEnabled(self, value):
        self.actionLoadExecutedModel.setEnabled(value)
        self.actionLoadImaginedModel.setEnabled(value)

    def setupSettingsViewUi(self):
        self.nrOfTasks = None
        self.subjectId = None
        self.runType = None
        self.transferLearningEnabled = None
        self.selectedModelName = None
        self.debugMode = None
        self.showingPredictions = None
        self.evaluateAllModels = None
        self.view = ViewType.Settings
        self.toggleActionsEnabled(True)

        self.mainWindow.setFixedSize(QtCore.QSize(340, 340))
        self.centerOnScreen()

        self.settingsWidget = QtWidgets.QWidget(self.mainWindow)
        self.settingsWidget.setMaximumSize(QtCore.QSize(340, 340))
        self.settingsWidget.setObjectName("settingsWidget")
        self.mainWindow.setCentralWidget(self.settingsWidget)

        self.settingsLayout = self.createUiElement(ElementType.VBox, "settingsLayout", parent=self.settingsWidget,
                                                   margins=(10, 10, 10, 10))

        self.settingsForm = self.createUiElement(ElementType.Form, "settingsForm", parent=self.settingsWidget,
                                                 alignment=QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter,
                                                 margins=(10, 10, 10, 10))
        self.settingsLayout.addLayout(self.settingsForm)

        self.settingsLabel = self.createUiElement(ElementType.Label, "settingsLabel", parent=self.settingsWidget,
                                                  font=QtGui.QFont("Times", 14, QtGui.QFont.Bold),
                                                  alignment=QtCore.Qt.AlignVCenter)
        self.settingsForm.addRow(self.settingsLabel)

        self.subjectIdLabel = self.createUiElement(ElementType.Label, "subjectIdLabel", parent=self.settingsWidget)
        self.subjectIdValue = self.createUiElement(ElementType.Value, "subjectIdValue", parent=self.settingsWidget,
                                                   maximumSize=QtCore.QSize(170, 50), value="1")
        self.settingsForm.addRow(self.subjectIdLabel, self.subjectIdValue)

        self.nrOfTasksLabel = self.createUiElement(ElementType.Label, "nrOfTasksLabel", parent=self.settingsWidget)
        self.nrOfTasksValue = self.createUiElement(ElementType.Value, "nrOfTasksValue", parent=self.settingsWidget,
                                                   maximumSize=QtCore.QSize(170, 50), value="16")
        self.settingsForm.addRow(self.nrOfTasksLabel, self.nrOfTasksValue)

        self.runTypeComboBoxLabel = self.createUiElement(ElementType.Label, "runTypeComboBoxLabel",
                                                         parent=self.settingsWidget, )
        self.runTypeComboBox = self.createUiElement(ElementType.ComboBox, "runTypeComboBox", parent=self.settingsWidget,
                                                    maximumSize=QtCore.QSize(170, 50),
                                                    items=["Executed tasks", "Imagined tasks"])
        self.runTypeComboBox.currentIndexChanged.connect(self.displayNewModelNames)
        self.settingsForm.addRow(self.runTypeComboBoxLabel, self.runTypeComboBox)

        modelNames = [model.get_name() for model in self.models.get_models(ModelType.Executed)]
        self.modelComboBoxLabel = self.createUiElement(ElementType.Label, "modelComboBoxLabel",
                                                       parent=self.settingsWidget, )
        self.modelComboBox = self.createUiElement(ElementType.ComboBox, "modelComboBox", parent=self.settingsWidget,
                                                  maximumSize=QtCore.QSize(170, 50), items=modelNames)
        self.modelComboBox.currentIndexChanged.connect(self.toggleTransferLearningCheckboxEnabled)
        self.settingsForm.addRow(self.modelComboBoxLabel, self.modelComboBox)

        self.showPredictionsCheckboxLabel = self.createUiElement(ElementType.Label, "showPredictionsCheckboxLabel",
                                                                 parent=self.settingsWidget)
        self.showPredictionsCheckbox = self.createUiElement(ElementType.CheckBox, "showPredictionsCheckbox",
                                                            parent=self.settingsWidget)
        self.settingsForm.addRow(self.showPredictionsCheckboxLabel, self.showPredictionsCheckbox)

        self.transferLearningCheckboxLabel = self.createUiElement(ElementType.Label, "transferLearningCheckboxLabel",
                                                                  parent=self.settingsWidget)
        self.transferLearningCheckbox = self.createUiElement(ElementType.CheckBox, "transferLearningCheckboxLabel",
                                                             parent=self.settingsWidget)
        self.settingsForm.addRow(self.transferLearningCheckboxLabel, self.transferLearningCheckbox)

        self.evaluateAllModelsLabel = self.createUiElement(ElementType.Label, "evaluateAllModelsLabel",
                                                           parent=self.settingsWidget)
        self.evaluateAllModelsCheckBox = self.createUiElement(ElementType.CheckBox, "evaluateAllModelsCheckBox",
                                                              parent=self.settingsWidget)
        self.settingsForm.addRow(self.evaluateAllModelsLabel, self.evaluateAllModelsCheckBox)

        self.debugModeCheckboxLabel = self.createUiElement(ElementType.Label, "debugModeLabel",
                                                           parent=self.settingsWidget)
        self.debugModeCheckbox = self.createUiElement(ElementType.CheckBox, "debugModeCheckbox",
                                                      parent=self.settingsWidget)
        self.settingsForm.addRow(self.debugModeCheckboxLabel, self.debugModeCheckbox)

        self.startButton = self.createUiElement(ElementType.Button, "startButton", parent=self.settingsWidget,
                                                fixedSize=(320, 40))
        self.settingsLayout.addWidget(self.startButton)
        self.startButton.clicked.connect(self.startExperiment)

        self.retranslateSettingsView()

    def displayNewModelNames(self, selectionIndex):
        self.modelComboBox.clear()
        model_type = ModelType.Executed if selectionIndex == 0 else ModelType.Imagined
        self.modelComboBox.addItems([model.get_name() for model in self.models.get_models(model_type)])

    def toggleTransferLearningCheckboxEnabled(self, selectionIndex):
        if any(tl_model in self.modelComboBox.currentText() for tl_model in
               ['EEGNet', 'EEGNet_Fusion', 'ShallowConvNet', 'DeepConvNet']):
            self.transferLearningCheckbox.setEnabled(True)
        else:
            self.transferLearningCheckbox.setChecked(False)
            self.transferLearningCheckbox.setEnabled(False)

    def retranslateSettingsView(self):
        self.mainWindow.setWindowTitle(self.translate("mainWindow", "BCI Application v1.0"))
        self.startButton.setText(self.translate("mainWindow", "Start"))
        self.settingsLabel.setText(self.translate("mainWindow", "Settings"))
        self.subjectIdLabel.setText(self.translate("mainWindow", "Current subject ID:"))
        self.modelComboBoxLabel.setText(self.translate("mainWindow", "Classifier model:"))
        self.transferLearningCheckboxLabel.setText(self.translate("mainWindow", "Enable transfer learning:"))
        self.showPredictionsCheckboxLabel.setText(self.translate("mainWindow", "Show predictions:"))
        self.evaluateAllModelsLabel.setText(self.translate("mainWindow", "Evaluate all models:"))
        self.debugModeCheckboxLabel.setText(self.translate("mainWindow", "Enable debug mode:"))
        self.nrOfTasksLabel.setText(self.translate("mainWindow", "Number of tasks to perform:"))
        self.runTypeComboBoxLabel.setText(self.translate("mainWindow", "Run type:"))

    def setupExperimentViewUi(self):
        self.mainWindow.setFixedSize(QtCore.QSize(1024, 768))
        self.centerOnScreen()
        self.view = ViewType.Experiment
        self.toggleActionsEnabled(False)

        self.experimentWidget = QtWidgets.QWidget(mainWindow)
        self.experimentWidget.setMaximumSize(QtCore.QSize(1024, 768))
        self.experimentWidget.setObjectName("experimentWidget")
        self.mainWindow.setCentralWidget(self.experimentWidget)

        self.experimentLayout = self.createUiElement(ElementType.VBox, "experimentLayout", parent=self.experimentWidget,
                                                     margins=(10, 10, 10, 10))

        self.experimentLabel = self.createUiElement(ElementType.Label, "experimentLabel", parent=self.experimentWidget,
                                                    font=QtGui.QFont("Roboto", 16, QtGui.QFont.Bold),
                                                    alignment=QtCore.Qt.AlignVCenter | QtCore.Qt.AlignHCenter,
                                                    margins=(50, 0, 0, 0))
        self.updateExperimentLabel(LabelType.Rest)
        self.experimentLayout.addWidget(self.experimentLabel)

        self.graphicsLayout = self.createUiElement(ElementType.HBox, "graphicsLayout", parent=self.experimentWidget)
        self.experimentLayout.addLayout(self.graphicsLayout)

        self.experimentGraphic = self.createUiElement(ElementType.Label, "experimentGraphic",
                                                      parent=self.experimentWidget)
        self.graphicsLayout.addWidget(self.experimentGraphic)

        self.stopButton = self.createUiElement(ElementType.Button, "stopButton", parent=self.experimentWidget,
                                               fixedSize=(1004, 40))
        self.stopButton.setEnabled(False)
        self.experimentLayout.addWidget(self.stopButton)
        self.stopButton.clicked.connect(self.experiment.stop)

        self.taskNrLabel = self.createUiElement(ElementType.Label, "taskNrLabel")
        self.taskNr = 0

        self.updateGraphics(GraphicType.Rest)  # show rest state graphics

        self.retranslateExperimentView('executed' if self.runType == 0 else 'imagined')

        self.statusBar.showMessage(self.taskNrLabel.text() + str(self.taskNr))  # update status bar

    def retranslateExperimentView(self, run_type):
        self.stopButton.setText(self.translate("mainWindow", "Stop"))
        self.taskNrLabel.setText(self.translate("mainWindow", "Running {} task number: ".format(run_type)))

    def centerOnScreen(self):
        resolution = QtWidgets.QDesktopWidget().screenGeometry()  # TODO: QDesktopWidget deprecated
        self.mainWindow.move((resolution.width() / 2) - (self.mainWindow.frameSize().width() / 2),
                             (resolution.height() / 2) - (self.mainWindow.frameSize().height() / 2))

    def updateTaskNr(self, new_nr):
        self.taskNr += 1
        self.statusBar.showMessage(self.taskNrLabel.text() + str(self.taskNr))

    def setupStatisticsViewUi(self):
        self.mainWindow.setFixedSize(QtCore.QSize(360, 360))
        self.centerOnScreen()
        self.view = ViewType.Statistics
        self.statistics = self.experiment.get_statistics()

        self.statisticsWidget = QtWidgets.QWidget(self.mainWindow)
        self.statisticsWidget.setMaximumSize(QtCore.QSize(360, 340))
        self.statisticsWidget.setObjectName("statisticsWidget")
        self.mainWindow.setCentralWidget(self.statisticsWidget)

        self.statisticsLayout = self.createUiElement(ElementType.VBox, "statisticsLayout", parent=self.statisticsWidget,
                                                     margins=(10, 10, 10, 10))

        self.statisticsForm = self.createUiElement(ElementType.Form, "statisticsForm", parent=self.statisticsWidget,
                                                   alignment=QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter,
                                                   margins=(50, 10, 10, 10))
        self.statisticsLayout.addLayout(self.statisticsForm)

        self.statisticsFormLabel = self.createUiElement(ElementType.Label, "statisticsFormLabel",
                                                        parent=self.statisticsWidget,
                                                        font=QtGui.QFont("Times", 14, QtGui.QFont.Bold),
                                                        alignment=QtCore.Qt.AlignVCenter)
        self.statisticsForm.addRow(self.statisticsFormLabel)

        modelType = ModelType.Executed if self.runType == 0 else ModelType.Imagined
        self.modelSelectionComboboxLabel = self.createUiElement(ElementType.Label, "modelSelectionComboboxLabel",
                                                                parent=self.statisticsWidget)

        all_model_names = [model.get_name() for model in self.models.get_models(modelType)]
        model_names = all_model_names if self.evaluateAllModels else [self.selectedModelName]
        self.modelSelectionCombobox = self.createUiElement(ElementType.ComboBox, "modelSelectionCombobox",
                                                           parent=self.statisticsWidget,
                                                           maximumSize=QtCore.QSize(160, 50),
                                                           items=model_names)
        self.statisticsForm.addRow(self.modelSelectionComboboxLabel, self.modelSelectionCombobox)
        self.modelSelectionCombobox.currentTextChanged.connect(self.displayNewStatistics)

        self.runTypeLabel = self.createUiElement(ElementType.Label, "runTypeLabel", parent=self.statisticsWidget)
        self.runTypeValue = self.createUiElement(ElementType.Label, "runTypeValue", parent=self.statisticsWidget,
                                                 alignment=None)
        self.statisticsForm.addRow(self.runTypeLabel, self.runTypeValue)

        self.transferLearningLabel = self.createUiElement(ElementType.Label, "transferLearningLabel",
                                                          parent=self.statisticsWidget)
        self.transferLearningValue = self.createUiElement(ElementType.Label, "transferLearningValue",
                                                          parent=self.statisticsWidget, alignment=None)
        self.statisticsForm.addRow(self.transferLearningLabel, self.transferLearningValue)

        self.leftHandPredictionsLabel = self.createUiElement(ElementType.Label, "leftHandPredictionsLabel",
                                                             parent=self.statisticsWidget)
        self.leftHandPredictionsValue = self.createUiElement(ElementType.Label, "leftHandPredictionsValue",
                                                             parent=self.statisticsWidget, alignment=None)
        self.statisticsForm.addRow(self.leftHandPredictionsLabel, self.leftHandPredictionsValue)

        self.rightHandPredictionsLabel = self.createUiElement(ElementType.Label, "rightHandPredictionsLabel",
                                                              parent=self.statisticsWidget)
        self.rightHandPredictionsValue = self.createUiElement(ElementType.Label, "rightHandPredictionsValue",
                                                              parent=self.statisticsWidget, alignment=None)
        self.statisticsForm.addRow(self.rightHandPredictionsLabel, self.rightHandPredictionsValue)

        self.correctPredictionsLabel = self.createUiElement(ElementType.Label, "correctPredictionsLabel",
                                                            parent=self.statisticsWidget)
        self.correctPredictionsValue = self.createUiElement(ElementType.Label, "correctPredictionsValue",
                                                            parent=self.statisticsWidget, alignment=None)
        self.statisticsForm.addRow(self.correctPredictionsLabel, self.correctPredictionsValue)

        self.incorrectPredictionsLabel = self.createUiElement(ElementType.Label, "incorrectPredictionsLabel",
                                                              parent=self.statisticsWidget)
        self.incorrectPredictionsValue = self.createUiElement(ElementType.Label, "incorrectPredictionsValue",
                                                              parent=self.statisticsWidget, alignment=None)
        self.statisticsForm.addRow(self.incorrectPredictionsLabel, self.incorrectPredictionsValue)

        self.totalPredictionsLabel = self.createUiElement(ElementType.Label, "totalPredictionsLabel",
                                                          parent=self.statisticsWidget)
        self.totalPredictionsValue = self.createUiElement(ElementType.Label, "totalPredictionsValue",
                                                          parent=self.statisticsWidget, alignment=None)
        self.statisticsForm.addRow(self.totalPredictionsLabel, self.totalPredictionsValue)

        self.accuracyLabel = self.createUiElement(ElementType.Label, "accuracyLabel", parent=self.statisticsWidget)
        self.accuracyValue = self.createUiElement(ElementType.Label, "accuracyValue", parent=self.statisticsWidget,
                                                  alignment=None)
        self.statisticsForm.addRow(self.accuracyLabel, self.accuracyValue)

        self.totalRuntimeLabel = self.createUiElement(ElementType.Label, "totalRuntimeLabel",
                                                      parent=self.statisticsWidget)
        self.totalRuntimeValue = self.createUiElement(ElementType.Label, "totalRuntimeValue",
                                                      parent=self.statisticsWidget, alignment=None)
        self.statisticsForm.addRow(self.totalRuntimeLabel, self.totalRuntimeValue)

        self.statisticsButtonLayout = self.createUiElement(ElementType.HBox, "statisticsButtonLayout",
                                                           parent=self.statisticsWidget)
        self.statisticsLayout.addLayout(self.statisticsButtonLayout)

        self.reRunExperimentButton = self.createUiElement(ElementType.Button, "reRunExperimentButton",
                                                          parent=self.statisticsWidget, fixedSize=(150, 40))
        self.statisticsButtonLayout.addWidget(self.reRunExperimentButton)
        self.reRunExperimentButton.clicked.connect(self.startExperiment)

        self.newExperimentButton = self.createUiElement(ElementType.Button, "newExperimentButton",
                                                        parent=self.statisticsWidget, fixedSize=(150, 40))
        self.statisticsButtonLayout.addWidget(self.newExperimentButton)
        self.newExperimentButton.clicked.connect(self.setupSettingsViewUi)

        # By default select and show statistics for the model selected in settings
        model_index = self.modelSelectionCombobox.findText(self.selectedModelName, QtCore.Qt.MatchFixedString)
        if model_index >= 0:
            self.modelSelectionCombobox.setCurrentIndex(model_index)
        self.displayNewStatistics(self.modelSelectionCombobox.currentText())

        self.statusBar.clearMessage()

        self.retranslateStatisticsView()

    def retranslateStatisticsView(self):
        self.statisticsFormLabel.setText(self.translate("mainWindow", "Statistics"))
        self.modelSelectionComboboxLabel.setText(self.translate("mainWindow", "Show model: "))
        self.runTypeLabel.setText(self.translate("mainWindow", "Experiment type: "))
        self.transferLearningLabel.setText(self.translate("mainWindow", "Transfer learning used: "))
        self.leftHandPredictionsLabel.setText(self.translate("mainWindow", "Left hand predictions:"))
        self.rightHandPredictionsLabel.setText(self.translate("mainWindow", "Right hand predictions:"))
        self.correctPredictionsLabel.setText(self.translate("mainWindow", "Correct predictions:"))
        self.incorrectPredictionsLabel.setText(self.translate("mainWindow", "Incorrect predictions:"))
        self.totalPredictionsLabel.setText(self.translate("mainWindow", "Total predictions:"))
        self.accuracyLabel.setText(self.translate("mainWindow", "Prediction accuracy:"))
        self.totalRuntimeLabel.setText(self.translate("mainWindow", "Experiment run time:"))
        self.reRunExperimentButton.setText(self.translate("mainWindow", "Run experiment again"))
        self.newExperimentButton.setText(self.translate("mainWindow", "New experiment"))

    def displayNewStatistics(self, model_name):
        model_stats = self.statistics[model_name]

        runTypeMsg = "Executed movement" if model_stats.get_run_type() == 0 else "Imagined movement"
        self.runTypeValue.setText(runTypeMsg)

        transferLearningMsg = "Yes" if self.transferLearningEnabled else "No"
        self.transferLearningValue.setText(transferLearningMsg)

        leftHandPredictions = str(model_stats.get_left_hand_total())
        self.leftHandPredictionsValue.setText(leftHandPredictions)

        rightHandPredictions = str(model_stats.get_right_hand_total())
        self.rightHandPredictionsValue.setText(rightHandPredictions)

        correctPredictions = str(model_stats.get_correct_total())
        self.correctPredictionsValue.setText(correctPredictions)

        incorrectPredictions = str(model_stats.get_incorrect_total())
        self.incorrectPredictionsValue.setText(incorrectPredictions)

        totalPredictions = str(model_stats.get_total_tasks())
        self.totalPredictionsValue.setText(totalPredictions)

        accuracy = '{:.2%}'.format(model_stats.get_accuracy())
        self.accuracyValue.setText(accuracy)

        minutes, seconds = self.calculate_runtime(model_stats.get_total_time())
        totalRuntime = '{} minutes and {} seconds'.format(minutes, seconds)
        self.totalRuntimeValue.setText(totalRuntime)

    def calculate_runtime(self, runtime):
        minutes = int(runtime / 60)
        seconds = int(runtime - minutes * 60)
        return minutes, seconds

    def addActions(self, item, actions):
        for action in actions:
            item.addAction(action)

    def defineEvents(self, mainWindow):
        QtCore.QMetaObject.connectSlotsByName(mainWindow)

    def exitGracefully(self):
        self.stopExperiment(quitCalled=True)
        sys.exit()

    def startExperiment(self):
        try:
            self.validateInputFields()
        except AssertionError:
            self.displayError("Please fill all input fields")
            return
        except AttributeError:
            self.displayError("Input fields must be positive integers")
            return

        self.runType = self.runType if self.runType != None else self.runTypeComboBox.currentIndex()
        self.transferLearningEnabled = self.transferLearningEnabled if self.transferLearningEnabled != None else self.transferLearningCheckbox.isChecked()
        self.showingPredictions = self.showingPredictions if self.showingPredictions != None else self.showPredictionsCheckbox.isChecked()
        self.selectedModelName = self.selectedModelName if self.selectedModelName != None else str(
            self.modelComboBox.currentText())
        self.debugMode = self.debugMode if self.debugMode != None else self.debugModeCheckbox.isChecked()
        self.models.set_selected(self.runType, self.selectedModelName)
        self.evaluateAllModels = self.evaluateAllModels if self.evaluateAllModels != None else self.evaluateAllModelsCheckBox.isChecked()
        selectedModel = self.models.get_selected()
        if self.evaluateAllModels:
            modelType = ModelType.Executed if self.runType == 0 else ModelType.Imagined
            models = self.models.get_models(modelType)
        else:
            models = [selectedModel]

        self.experiment = Experiment(self.subjectId, self.runType, selectedModel, self.nrOfTasks,
                                     self.showingPredictions, self.transferLearningEnabled, self.debugMode, models)

        self.setupExperimentViewUi()

        try:
            self.runExperiment()
        except Exception as e:
            self.handleException(e)

    def validateInputFields(self):
        if (not self.nrOfTasks \
            or not self.subjectId) \
                and (not self.nrOfTasksValue.text() \
                     or not self.subjectIdValue.text()):
            raise AssertionError
        if not self.nrOfTasks or not self.subjectId:
            try:
                nrOfTasks = int(self.nrOfTasksValue.text())
                subjectId = int(self.subjectIdValue.text())
                if nrOfTasks < 1 or subjectId < 1:
                    raise AttributeError
                self.nrOfTasks = nrOfTasks
                self.subjectId = subjectId
            except:
                raise AttributeError

    def displayError(self, message):
        QtWidgets.QMessageBox.critical(self.mainWindow, "Error", message)

    def handleException(self, exception):
        exc_type, msg, trace = exception
        print(trace)
        self.displayError(str(msg))

    def stopExperiment(self, quitCalled=False):
        if not hasattr(self, 'experiment'):
            return
        self.threadpool.waitForDone(1)
        self.experiment.stop()
        self.experiment.set_run_time(time.time() - self.experimentStartTime)
        if quitCalled:
            return
        self.setupStatisticsViewUi()
        if self.transferLearningEnabled:
            self.transferLearningRunning(True)
            try:
                worker = Worker(self.experiment.apply_transfer_learning)
                worker.signals.finished.connect(self.onTransferLearningFinished)
                worker.signals.error.connect(self.onTransferLearningFinished)
                self.threadpool.start(worker)
            except Exception as e:
                self.handleException(e)

    def onTransferLearningFinished(self):
        self.transferLearningRunning(False)

    def runExperiment(self):
        worker = Worker(self.experiment.run)
        worker.signals.progress.connect(self.determineExperimentAction)
        worker.signals.error.connect(self.handleException)
        worker.signals.finished.connect(self.stopExperiment)
        self.threadpool.start(worker)
        self.experimentStartTime = time.time()

    def determineExperimentAction(self, *args):
        if self.view != ViewType.Experiment:
            return
        task, progress_type = args[0]
        if progress_type == ProgressType.TaskStart:
            self.updateExperimentUi(task)
            self.stopButton.setEnabled(True)
        elif progress_type == ProgressType.TaskResult:
            if self.showingPredictions:
                self.showPrediction(task)
            else:
                self.showRest()
        else:
            raise Exception("Invalid progress type")

    def showRest(self):
        self.updateExperimentLabel(LabelType.Rest)
        self.updateGraphics(GraphicType.Rest)

    def transferLearningRunning(self, running):
        self.reRunExperimentButton.setEnabled(not running)
        self.newExperimentButton.setEnabled(not running)
        if running:
            msg = "Running transfer learning. Please wait..."
        else:
            msg = "Transfer learning finished"
        self.statusBar.showMessage(msg)

    def updateExperimentUi(self, task):
        self.updateExperimentLabel(LabelType.Task)
        self.updateTaskNr(task.get_task_nr())
        graphic_type = GraphicType.LeftTask if task.get_task_type() == 0 else GraphicType.RightTask
        self.updateGraphics(graphic_type)

    def showPrediction(self, task):
        task_label = task.get_task_type()
        prediction = task.get_majority_prediction()
        if prediction == 0 and task_label == prediction:
            self.updateGraphics(GraphicType.LeftCorrectPrediction)
        elif prediction == 0 and task_label != prediction:
            self.updateGraphics(GraphicType.LeftIncorrectPrediction)
        elif prediction == 1 and task_label == prediction:
            self.updateGraphics(GraphicType.RightCorrectPrediction)
        elif prediction == 1 and task_label != prediction:
            self.updateGraphics(GraphicType.RightIncorrectPrediction)
        else:
            raise AttributeError("Invalid prediction value {}".format(prediction))

        self.updateExperimentLabel(LabelType.Prediction)

    def updateExperimentLabel(self, labelType):
        if labelType == LabelType.Prediction:
            self.experimentLabel.setText("The model predicts that the previous task was")
        elif labelType == LabelType.Task:
            self.experimentLabel.setText("Please perform the task indicated by the circle")
        elif labelType == LabelType.Rest:
            self.experimentLabel.setText("Please rest before the next task")
        else:
            raise AttributeError("Invalid label type")

    def updateGraphics(self, graphic_type):
        pixmap = self.getTaskGraphic(graphic_type)
        self.experimentGraphic.setPixmap(pixmap)

    def getTaskGraphic(self, graphic_type):
        file_locations = {
            GraphicType.LeftTask: "./images/circle_left.jpg",
            GraphicType.RightTask: "./images/circle_right.jpg",
            GraphicType.Rest: "./images/blank.jpg",
            GraphicType.LeftCorrectPrediction: "./images/circle_left_correct.jpg",
            GraphicType.RightCorrectPrediction: "./images/circle_right_correct.jpg",
            GraphicType.LeftIncorrectPrediction: "./images/circle_left_incorrect.jpg",
            GraphicType.RightIncorrectPrediction: "./images/circle_right_incorrect.jpg"
        }

        return QtGui.QPixmap(file_locations.get(graphic_type))


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(mainWindow)
    mainWindow.show()
    mainWindow.setWindowState(QtCore.Qt.WindowActive)
    sys.exit(app.exec_())
