import numpy as np
import pyqtgraph
from PyQt4 import QtCore, QtGui
import pyqtgraph.console as pgc
from AxisSettings_ui import Ui_AxisSettingsDialog

# pyqtgraph's axis item is slightly broken
# it doesn't account for the increase
# in font size of the tick labels
# which causes them to clip if you want to change
# those. I intercept them here to fix those

class AxisSettingsDialog(QtGui.QDialog):
    def __init__(self, *args, **kwargs):
        self.axisItem = kwargs.pop("axisItem", pyqtgraph.AxisItem("bottom"))
        super(AxisSettingsDialog, self).__init__(*args, **kwargs)
        self.initialSettings = {
            "visible":self.axisItem.isVisible(),
            "title": self.axisItem.labelText,
            "size": self.axisItem.labelStyle.get("font-size","10pt").split("pt")[0],
            "from": self.axisItem.range[0],
            "to": self.axisItem.range[1],
            "type": self.axisItem.logMode,
            "color": self.axisItem.pen().color(),
            "width": self.axisItem.pen().width()
        }

        if self.axisItem._tickSpacing is None:
            self.initialSettings["majSpac"] = -1
            self.initialSettings["minSpac"] = -1
        elif len(self.axisItem._tickSpacing)==2:
            self.initialSettings["majSpac"] = \
                self.axisItem._tickSpacing[0][0]
            self.initialSettings["minSpac"] = \
                self.axisItem._tickSpacing[1][0]
        else:
            self.initialSettings["majSpac"] = -2
            self.initialSettings["minSpac"] = -2




        self.ui = Ui_AxisSettingsDialog()
        self.ui.setupUi(self)
        self.initUI()

        self._allSignals = [
            self.ui.cbVisible.stateChanged,
            self.ui.tTitle.editingFinished,
            self.ui.sbSize.sigValueChanging,
            self.ui.tFrom.textAccepted,
            self.ui.tTo.textAccepted,
            self.ui.cbMode.currentIndexChanged,
            self.ui.tMajSpacing.textAccepted,
            self.ui.tMinSpacing.textAccepted,
            self.ui.bColor.sigColorChanging,
            self.ui.tWidth.textAccepted
            ]
        for sig in self._allSignals:
            sig.connect(self.updateSettings)
        self.ui.sbSize.setOpts(int=True, step=1, bounds=(1,100))

    def initUI(self, blockSignals = False):
        if blockSignals:
            for sig in self._allSignals:
                sig.disconnect(self.updateSettings)
        self.ui.cbVisible.setChecked(self.initialSettings["visible"])
        self.ui.tTitle.setText("{}".format(self.initialSettings["title"]))
        self.ui.sbSize.setValue(int(self.initialSettings["size"]))
        self.ui.tFrom.setText("{}".format(self.initialSettings["from"]))
        self.ui.tTo.setText("{}".format(self.initialSettings["to"]))
        self.ui.cbMode.setCurrentIndex(self.initialSettings["type"])
        self.ui.tMajSpacing.setText("{}".format(self.initialSettings["majSpac"]))
        self.ui.tMinSpacing.setText("{}".format(self.initialSettings["minSpac"]))
        if self.initialSettings["majSpac"] == -2:
            self.ui.tMinSpacing.setEnabled(False)
            self.ui.tMajSpacing.setEnabled(False)
            self.ui.tMinSpacing.setText("{}".format("Custom?"))
            self.ui.tMajSpacing.setText("{}".format("Custom?"))
        self.ui.bColor.setColor(self.initialSettings["color"])
        self.ui.tWidth.setText("{}".format(self.initialSettings["width"]))

        if blockSignals:
            for sig in self._allSignals:
                sig.connect(self.updateSettings)

    def updateSettings(self):
        self.axisItem.setVisible(self.ui.cbVisible.isChecked())
        self.axisItem.setLabel(
                self.ui.tTitle.text(),
                **{"font-size":"{}pt".format(self.ui.sbSize.value())})
        self.axisItem.tickFont.setPointSize(self.ui.sbSize.value())
        # self.axisItem.setRange(self.ui.tFrom.value(), self.ui.tTo.value())
        if self.axisItem.orientation in ["top", "bottom"]:
            self.axisItem.getViewBox().setRange(xRange=[self.ui.tFrom.value(),
                                                        self.ui.tTo.value()],
                                                padding=0)
            self.axisItem.parentItem().setLogMode(x=self.ui.cbMode.currentIndex())
        else:
            self.axisItem.getViewBox().setRange(yRange=[self.ui.tFrom.value(),
                                                        self.ui.tTo.value()],
                                                padding=0)
            self.axisItem.parentItem().setLogMode(y=self.ui.cbMode.currentIndex())


        if self.ui.tMajSpacing.value()==-2:
            pass
        elif self.ui.tMajSpacing.value()==-1:
            self.axisItem.setTickSpacing()
        else:
            if self.ui.tMinSpacing.value()==-1:
                self.axisItem.setTickSpacing(self.ui.tMajSpacing.value(),self.ui.tMajSpacing.value())
            else:
                self.axisItem.setTickSpacing(self.ui.tMajSpacing.value(),self.ui.tMinSpacing.value())
        self.axisItem.setPen(color=self.ui.bColor.color(), width=self.ui.tWidth.value())

        # self.axisItem._updateMaxTextSize(100)
        if self.axisItem.orientation in ["top", "bottom"]:
            self.axisItem.textHeight = 0
            self.axisItem._updateHeight()
        else:
            self.axisItem.textWidth = 0
            self.axisItem._updateWidth()
        self.axisItem.update()


    @staticmethod
    def makeSettings(axisItem):
        dialog = AxisSettingsDialog(axisItem=axisItem)
        ok = dialog.exec_()
        if not ok:
            dialog.initUI(True)
            dialog.updateSettings()


oldDrawSpecs = pyqtgraph.AxisItem.generateDrawSpecs
def newDrawSpecs(self, p):
    if False:
        self = pyqtgraph.AxisItem
    axisSpec, tickSpecs, textSpecs = oldDrawSpecs(self, p)


    bounds = self.mapRectFromParent(self.geometry())

    linkedView = self.linkedView()
    if linkedView is None or self.grid is False:
        tickBounds = bounds
    else:
        tickBounds = linkedView.mapRectToItem(self, linkedView.boundingRect())

    if self.orientation == 'left':
        span = (bounds.topRight(), bounds.bottomRight())
        tickStart = tickBounds.right()
        tickStop = bounds.right()
        tickDir = -1
        axis = 0
    elif self.orientation == 'right':
        span = (bounds.topLeft(), bounds.bottomLeft())
        tickStart = tickBounds.left()
        tickStop = bounds.left()
        tickDir = 1
        axis = 0
    elif self.orientation == 'top':
        span = (bounds.bottomLeft(), bounds.bottomRight())
        tickStart = tickBounds.bottom()
        tickStop = bounds.bottom()
        tickDir = -1
        axis = 1
    elif self.orientation == 'bottom':
        span = (bounds.topLeft(), bounds.topRight())
        tickStart = tickBounds.top()
        tickStop = bounds.top()
        tickDir = 1
        axis = 1

    tickFontSize = 10.
    if self.tickFont is not None:
        tickFontSize = float(self.tickFont.pointSize())

    textOffset = self.style['tickTextOffset'][axis]

    newTextSpecs = []
    textSize2 = 0
    for ii, (rect, textFlags, vstr) in enumerate(textSpecs):
        if False:
            rect = QtCore.QRectF()

        x = tickSpecs[ii][2]
        if axis:
            # tickStop = x.y()
            x = x.x()
        else:
            # tickStop = x.x()
            x = x.y()


        rect.setWidth(rect.width() * tickFontSize/7.)
        rect.setHeight(rect.height() * tickFontSize/5.)

        # if self.style["tickLength"]<0:
        #     tickStop += 2*abs(self.style["tickLength"])
        textRect = rect
        height = textRect.height()
        width = textRect.width()

        length = self.style["tickLength"]
        # tickStop = max(0, tickStop)

        offset = max(0,length) + textOffset
        # offset = max(0,abs(self.style['tickLength'])) + textOffset

        if self.orientation == 'left':
            textFlags = QtCore.Qt.TextDontClip|QtCore.Qt.AlignRight|QtCore.Qt.AlignVCenter
            rect = QtCore.QRectF(tickStop-offset-width, x-(height/2), width, height)
        elif self.orientation == 'right':
            textFlags = QtCore.Qt.TextDontClip|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter
            rect = QtCore.QRectF(tickStop+offset, x-(height/2), width, height)
        elif self.orientation == 'top':
            textFlags = QtCore.Qt.TextDontClip|QtCore.Qt.AlignCenter|QtCore.Qt.AlignBottom
            rect = QtCore.QRectF(x-width/2., tickStop-offset-height, width, height)
        elif self.orientation == 'bottom':
            textFlags = QtCore.Qt.TextDontClip|QtCore.Qt.AlignCenter|QtCore.Qt.AlignTop
            rect = QtCore.QRectF(x-width/2., tickStop+offset, width, height)



        newTextSpecs.append((rect, textFlags, vstr))



    if axis == 0:
        textSize = np.sum([r[0].height() for r in newTextSpecs])
        textSize2 = np.max([r[0].width() for r in newTextSpecs])
    else:
        textSize = np.sum([r[0].width() for r in newTextSpecs])
        textSize2 = np.max([r[0].height() for r in newTextSpecs])

    self._updateMaxTextSize(textSize2)
    return axisSpec, tickSpecs, newTextSpecs

oldinit = pyqtgraph.AxisItem.__init__
def __init__(self, *args, **kwargs):
    oldinit(self, *args, **kwargs)
    try:
        self.parent().scene().sigMouseClicked.connect(self.mouseClickEvent)
    except AttributeError:
        # breaks when initialized before given a scene
        pass

def mouseClickEvent(self, ev):
    if ev.double():
        # self.a = pgc.ConsoleWidget(namespace={"self":self})
        # self.a.show()

        AxisSettingsDialog.makeSettings(axisItem=self)



pyqtgraph.AxisItem.generateDrawSpecs = newDrawSpecs
pyqtgraph.AxisItem.__init__ = __init__
pyqtgraph.AxisItem.mouseClickEvent = mouseClickEvent














































