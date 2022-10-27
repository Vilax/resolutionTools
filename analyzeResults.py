#!../env/bin/python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 30 15:46:30 2020
@author: vilas
"""

from PyQt5 import QtWidgets, uic
# from PyQt5.QtWidgets import QFileDialog

# import os
import icons

# from confPaths import confPaths

X_AXIS = 0
Y_AXIS = 1
Z_AXIS = 2

FN_MEAN_TOMOGRAM = 'meanTomogram.mrc'
FN_LOCAL_RESOLUTION_TOMOGRAM = 'localResolutionTomogram.mrc'

class Ui_AnalyzeResults(QtWidgets.QDialog):
    def __init__(self, resultsPath):
        super(Ui_AnalyzeResults, self).__init__()
        uic.loadUi('GUI/monotomoViewer.ui', self)
        self.resultsPath = resultsPath

        self.show()

        # MonoTomo params
        self.histogramButton_MT = self.findChild(QtWidgets.QPushButton, 'histogramButton_MT')
        self.localResSlicesButton_MT = self.findChild(QtWidgets.QPushButton, 'localResSlicesButton_MT')
        self.tomogramSlicesButton_MT = self.findChild(QtWidgets.QPushButton, 'tomogramSlicesButton_MT')
        self.singleLocalResButton_MT = self.findChild(QtWidgets.QPushButton, 'singleLocalResButton_MT')

        self.singleLocalResButton_MT = self.findChild(QtWidgets.QPushButton, 'singleLocalResButton_MT')
        self.singleSliceLocalResNumberLine_MT = self.findChild(QtWidgets.QLineEdit, 'singleSliceLocalResNumberLine_MT')
        self.X_radioButton_MT = self.findChild(QtWidgets.QRadioButton, 'X_radioButton_MT')
        self.Y_radioButton_MT = self.findChild(QtWidgets.QRadioButton, 'Y_radioButton_MT')
        self.Z_radioButton_MT = self.findChild(QtWidgets.QRadioButton, 'Z_radioButton_MT')

        self.resolutionComboBox = self.findChild(QtWidgets.QComboBox, 'resolutionComboBox')
        self.viewerlowResLine_MT = self.findChild(QtWidgets.QLineEdit, 'viewerlowResLine_MT')
        self.viewerhighResLine_MT = self.findChild(QtWidgets.QLineEdit, 'viewerhighResLine_MT')

        self.viewerpathLineEdit_MT = self.findChild(QtWidgets.QLineEdit, 'viewerpathLineEdit_MT')
        self.viewerpathLineEdit_MT.setText(self.resultsPath)

        # MonoTomo CallBacks
        self.histogramButton_MT.clicked.connect(lambda: self.showHistogram())
        self.localResSlicesButton_MT.clicked.connect(lambda: self.showResolutionSlices())
        self.tomogramSlicesButton_MT.clicked.connect(lambda: self.showTomogramSlices())
        self.singleLocalResButton_MT.clicked.connect(lambda: self.singleResolutionSlice())

    def showHistogram(self):
        pass

    def showResolutionSlices(self):
        import os
        filename = os.path.join(self.viewerpathLineEdit_MT.text(), FN_LOCAL_RESOLUTION_TOMOGRAM)
        ax = self.getAxis()
        lowres, highres = self.getLocalResolutionRange()
        self.showSlices(ax, filename, highres, lowres)

    def showTomogramSlices(self):
        import os
        filename = os.path.join(self.viewerpathLineEdit_MT.text(), FN_MEAN_TOMOGRAM)
        ax = self.getAxis()
        self.showSlices(ax, filename)

    def getLocalResolutionRange(self):
        lowres = self.viewerlowResLine_MT.text()
        highres = self.viewerhighResLine_MT.text()
        if lowres == '':
            lowres = 150
        else:
            lowres = float(lowres)
        if highres == '':
            highres = 0
        else:
            highres = float(highres)
        return lowres, highres

    def singleResolutionSlice(self):
        import os
        filename = os.path.join(self.viewerpathLineEdit_MT.text(), FN_MEAN_TOMOGRAM)
        ax = self.getAxis()
        lowres, highres = self.getLocalResolutionRange()
        slicenumber = self.singleSliceLocalResNumberLine_MT.text()
        self.showSingleSlice(ax, filename, slicenumber, highres, lowres)

    def showSingleSlice(self, axisType, fileName, slicenumber, minVal = None, maxVal = None):
        colormap = self.resolutionComboBox.currentText()

        import matplotlib.pyplot as plt
        # subplot(r,c) provide the no. of rows and columns

        import mrcfile
        with mrcfile.open(fileName) as mrc:
            tomoData = mrc.data

        xdim, ydim, zdim = tomoData.shape
        print(xdim)
        print(ydim)
        print(zdim)

        if axisType == X_AXIS:
            if slicenumber == '':
                slicenumber = xdim/2
            plt.imshow(tomoData[:, :, int(slicenumber)], cmap=colormap, vmin=minVal, vmax=maxVal)
        if axisType == Y_AXIS:
            if slicenumber == '':
                slicenumber = ydim/2
            plt.imshow(tomoData[:, int(slicenumber), :], cmap=colormap, vmin=minVal, vmax=maxVal)
        if axisType == Z_AXIS:
            if slicenumber == '':
                slicenumber = zdim/2
            plt.imshow(tomoData[:, :, int(slicenumber)], cmap=colormap, vmin=minVal, vmax=maxVal)
        plt.show()

    def showSlices(self, axisType, fileName, minVal=None, maxVal=None):
        colormap = self.resolutionComboBox.currentText()

        import matplotlib.pyplot as plt
        # subplot(r,c) provide the no. of rows and columns
        fig, axarr = plt.subplots(2, 2)

        import mrcfile
        with mrcfile.open(fileName) as mrc:
            tomoData = mrc.data

        xdim, ydim, zdim = tomoData.shape

        if axisType == X_AXIS:
            axarr[0, 0].imshow(tomoData[:, :, round(0 * zdim / 5)], cmap=colormap, vmin=minVal, vmax=maxVal)
            axarr[0, 1].imshow(tomoData[:, :, round(1 * zdim / 5)], cmap=colormap, vmin=minVal, vmax=maxVal)
            axarr[1, 0].imshow(tomoData[:, :, round(2 * zdim / 5)], cmap=colormap, vmin=minVal, vmax=maxVal)
            im = axarr[1, 1].imshow(tomoData[:, :, round(3 * zdim / 5)], cmap=colormap, vmin=minVal, vmax=maxVal)
        if axisType == Y_AXIS:
            axarr[0, 0].imshow(tomoData[:, round(0 * ydim / 5), :], cmap=colormap, vmin=minVal, vmax=maxVal)
            axarr[0, 1].imshow(tomoData[:, round(1 * ydim / 5), :], cmap=colormap, vmin=minVal, vmax=maxVal)
            axarr[1, 0].imshow(tomoData[:, round(2 * ydim / 5), :], cmap=colormap, vmin=minVal, vmax=maxVal)
            im = axarr[1, 1].imshow(tomoData[:, round(3 * ydim / 5), :], cmap=colormap, vmin=minVal, vmax=maxVal)
        if axisType == Z_AXIS:
            axarr[0, 0].imshow(tomoData[round(0 * xdim / 5), :, :], cmap=colormap, vmin=minVal, vmax=maxVal)
            axarr[0, 1].imshow(tomoData[round(1 * xdim / 5), :, :], cmap=colormap, vmin=minVal, vmax=maxVal)
            axarr[1, 0].imshow(tomoData[round(2 * xdim / 5), :, :], cmap=colormap, vmin=minVal, vmax=maxVal)
            im = axarr[1, 1].imshow(tomoData[round(3 * xdim / 5), :, :], cmap=colormap, vmin=minVal, vmax=maxVal)

        fig.subplots_adjust(right=0.8)
        cbar_ax = fig.add_axes([0.85, 0.15, 0.05, 0.7])
        fig.colorbar(im, cax=cbar_ax)

        plt.show()

    def getAxis(self):
        if self.X_radioButton_MT.isChecked():
            ax = X_AXIS
        if self.Y_radioButton_MT.isChecked():
            ax = Y_AXIS
        if self.Z_radioButton_MT.isChecked():
            ax = Z_AXIS

        return ax