from core.MayaWidget import MayaWidget
from PySide6.QtWidgets import QVBoxLayout, QHBoxLayout, QTextEdit, QPushButton, QLabel, QLineEdit, QColorDialog, QWidget
import maya.cmds as mc

import importlib
import core.MayaUtilities
importlib.reload(core.MayaUtilities)

class ControlColorer:
    def __init__(self):
        self.controllerColorRGB = [0,0,0] 

    def SetColorOverride(self):
        selection = mc.ls(selection=True, ufe=True)
        if not selection:
            raise Exception("Please make a selection before applying the color override")
                     
        mc.editDisplayLayerMembers("defaultLayer", selection, noRecurse=True)
        for item in selection:

            mc.setAttr(item + ".overrideEnabled", 1)
            mc.setAttr(item + ".overrideRGBColors", 1)

            mc.setAttr(item + ".overrideColorR", self.controllerColorRGB[0])
            mc.setAttr(item + ".overrideColorG", self.controllerColorRGB[1])
            mc.setAttr(item + ".overrideColorB", self.controllerColorRGB[2])

class ControlColorerWidget(MayaWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Control Curve Recolorer")
        self.masterLayout = QVBoxLayout()
        self.infoLayout = QHBoxLayout() 
        self.setLayout(self.masterLayout)  
        self.colorer = ControlColorer()
        self.colorSelected = False

        self.masterLayout.addWidget(QLabel("Select the curve(s) you want to recolor, and then: "))

        self.infoLayout = QHBoxLayout()
        self.masterLayout.addLayout(self.infoLayout)
        self.infoLayout.addWidget(QLabel("Select a Base Color:"))

        self.controlColorBtn = QPushButton("Select Color")
        self.controlColorBtn.clicked.connect(self.controlColorBtnClicked)
        self.infoLayout.addWidget (self.controlColorBtn)

        self.controlColorBtn = QPushButton("Apply Color to Selected")
        self.controlColorBtn.clicked.connect(self.setColorOverrideBtnClicked)
        self.masterLayout.addWidget (self.controlColorBtn)

    def controlColorBtnClicked(self):
        pickedColor = QColorDialog().getColor()
        self.colorer.controllerColorRGB[0] = pickedColor.redF()
        self.colorer.controllerColorRGB[1] = pickedColor.greenF()
        self.colorer.controllerColorRGB[2] = pickedColor.blueF()
        print(self.colorer.controllerColorRGB)
        self.colorSelected = True

    def setColorOverrideBtnClicked(self):
        selection = mc.ls(selection=True, ufe=True)
        if not selection:
            self.raiseSelectionWarning()
            return
        
        if not self.colorSelected:
            self.raiseColorWarning()
            return
        
        self.colorer.SetColorOverride()   

    def raiseSelectionWarning(self):       
        self.popupWindow = QWidget()
        self.popupWindow.setWindowTitle("Warning")
        self.popupWindow.setFixedSize(250,80)
        self.popupLayout = QVBoxLayout()
        self.popupWindow.setLayout(self.popupLayout)

        self.popupInfoLabel = QLabel("Please make a selection before applying.")
        self.popupLayout.addWidget(self.popupInfoLabel)

        self.popupCloseBtn = QPushButton("Ok")
        self.popupCloseBtn.clicked.connect(self.popupCloseBtnClicked)
        self.popupLayout.addWidget(self.popupCloseBtn)

        self.popupWindow.show()
        raise Exception("Please make a selection before applying the color override")

    def raiseColorWarning(self):       
        self.popupWindow = QWidget()
        self.popupWindow.setWindowTitle("Warning")
        self.popupWindow.setFixedSize(250,80)
        self.popupLayout = QVBoxLayout()
        self.popupWindow.setLayout(self.popupLayout)

        self.popupInfoLabel = QLabel("Please select a color before applying.")
        self.popupLayout.addWidget(self.popupInfoLabel)

        self.popupCloseBtn = QPushButton("Ok")
        self.popupCloseBtn.clicked.connect(self.popupCloseBtnClicked)
        self.popupLayout.addWidget(self.popupCloseBtn)

        self.popupWindow.show()
        raise Exception("Please select a color before applying")
    
    def popupCloseBtnClicked(self):
        if hasattr(self, "popupWindow") and self.popupWindow:
            self.popupWindow.close()
                    
    def getWidgetHash(self):
        return "3923fcd8bf8e146af389a6de3aff0f88f88663498ae29837e621n3ben923f8"  

def Run():
        controlColorerWidget = ControlColorerWidget()
        controlColorerWidget.show()

Run()