# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\dvalovcin\Documents\GitHub\Interactivepg-waffle\interactivePG\fixes\LegendSettings.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_LegendSettingsDialog(object):
    def setupUi(self, LegendSettingsDialog):
        LegendSettingsDialog.setObjectName(_fromUtf8("LegendSettingsDialog"))
        LegendSettingsDialog.resize(174, 127)
        self.verticalLayout = QtGui.QVBoxLayout(LegendSettingsDialog)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.formLayout = QtGui.QFormLayout()
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.bBGColor = ColorButton(LegendSettingsDialog)
        self.bBGColor.setText(_fromUtf8(""))
        self.bBGColor.setObjectName(_fromUtf8("bBGColor"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.bBGColor)
        self.label = QtGui.QLabel(LegendSettingsDialog)
        self.label.setObjectName(_fromUtf8("label"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.label)
        self.label_2 = QtGui.QLabel(LegendSettingsDialog)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.label_2)
        self.bBorderColor = ColorButton(LegendSettingsDialog)
        self.bBorderColor.setText(_fromUtf8(""))
        self.bBorderColor.setObjectName(_fromUtf8("bBorderColor"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.bBorderColor)
        self.label_3 = QtGui.QLabel(LegendSettingsDialog)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.label_3)
        self.sbFontSize = SpinBox(LegendSettingsDialog)
        self.sbFontSize.setObjectName(_fromUtf8("sbFontSize"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.sbFontSize)
        self.verticalLayout.addLayout(self.formLayout)
        self.buttonBox = QtGui.QDialogButtonBox(LegendSettingsDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(LegendSettingsDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), LegendSettingsDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), LegendSettingsDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(LegendSettingsDialog)

    def retranslateUi(self, LegendSettingsDialog):
        LegendSettingsDialog.setWindowTitle(_translate("LegendSettingsDialog", "Legend Settings", None))
        self.label.setText(_translate("LegendSettingsDialog", "Background Color:", None))
        self.label_2.setText(_translate("LegendSettingsDialog", "Border Color:", None))
        self.label_3.setText(_translate("LegendSettingsDialog", "Font Size", None))

from pyqtgraph import ColorButton, SpinBox