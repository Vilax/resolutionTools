#!./env/bin/python3
from PyQt5 import QtWidgets, QtGui, QtCore, uic
from PyQt5.QtWidgets import QFileDialog
import sys
import os
import icons.iconsresources
from subprocess import Popen
import configparser
from analyzeResults import Ui_AnalyzeResults


class Ui(QtWidgets.QMainWindow):

    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('GUI/localResolutionTools.ui', self)

        configFile = configparser.ConfigParser()
        configFile.read('config.ini')

        self.xmippPath = configFile['EXTERNAL_PROGRAMS']['XMIPP_PATH']
        # self.chimeraPath = configFile['EXTERNAL_PROGRAMS']['CHIMERA_PATH']

        # MonoTomo Parameters
        self.oddLabel_MT = self.findChild(QtWidgets.QLabel, 'oddLabel_MT')
        self.evenLabel_MT = self.findChild(QtWidgets.QLabel, 'evenLabel_MT')

        self.oddLine_MT = self.findChild(QtWidgets.QLineEdit, 'oddLine_MT')
        self.evenLine_MT = self.findChild(QtWidgets.QLineEdit, 'evenLine_MT')

        self.oddBrowse_MT = self.findChild(QtWidgets.QPushButton, 'oddBrowse_MT')
        self.evenBrowse_MT = self.findChild(QtWidgets.QPushButton, 'evenBrowse_MT')

        self.resolutionRangeLabel_MT = self.findChild(QtWidgets.QLabel, 'resolutionRangeLabel_MT')
        self.fromLabel_MT = self.findChild(QtWidgets.QLabel, 'fromLabel_MT')
        self.highResLine_MT = self.findChild(QtWidgets.QLineEdit, 'highResLine_MT')
        self.toLabel_MT = self.findChild(QtWidgets.QLabel, 'toLabel_MT')
        self.lowResLine_MT = self.findChild(QtWidgets.QLineEdit, 'lowResLine_MT')
        self.stepLabel_MT = self.findChild(QtWidgets.QLabel, 'stepLabel_MT')
        self.stepLine_MT = self.findChild(QtWidgets.QLineEdit, 'stepLine_MT')
        self.samplingLabel_MT = self.findChild(QtWidgets.QLabel, 'samplingLabel_MT')
        self.samplingLine_MT = self.findChild(QtWidgets.QLineEdit, 'samplingLine_MT')

        self.advancedCheckBox_MT = self.findChild(QtWidgets.QCheckBox, 'advancedCheckBox_MT')
        self.significanceLabel_MT = self.findChild(QtWidgets.QLabel, 'significanceLabel_MT')
        self.significanceLine_MT = self.findChild(QtWidgets.QLineEdit, 'significanceLine_MT')

        # MonoTomo callBacks
        self.oddBrowse_MT.clicked.connect(lambda: self.setBrowsePathToLineEdit(self.oddLine_MT))
        self.evenBrowse_MT.clicked.connect(lambda: self.setBrowsePathToLineEdit(self.evenLine_MT))
        self.ExecuteLabel_MT.clicked.connect(lambda: self.executeButtonMonoTomo())
        self.analyzeButton_MT.clicked.connect(lambda: self.analyzeResultsMonoTomo())


        # MonoRes Parameters
        self.usaHalfMapsLabel_MR = self.findChild(QtWidgets.QLabel, 'usaHalfMapsLabel_MR')
        self.halfMapsYes_MR = self.findChild(QtWidgets.QRadioButton, 'halfMapsYes_MR')
        self.halfMapsNo_MR = self.findChild(QtWidgets.QRadioButton, 'halfMapsNo_MR')

        self.halfMap1Label_MR = self.findChild(QtWidgets.QLabel, 'halfMap1Label_MR')
        self.halfMap2Label_MR = self.findChild(QtWidgets.QLabel, 'halfMap2Label_MR')
        self.halfMap1Line_MR = self.findChild(QtWidgets.QLineEdit, 'halfMap1Line_MR')
        self.halfMap2ine_MR = self.findChild(QtWidgets.QLineEdit, 'halfMap2Line_MR')
        self.halfMap1Browse_MR = self.findChild(QtWidgets.QPushButton, 'halfMap1Browse_MR')
        self.halfMap2Browse_MR = self.findChild(QtWidgets.QPushButton, 'halfMap2Browse_MR')

        self.maskLabel_MR = self.findChild(QtWidgets.QLabel, 'maskLabel_MR')
        self.maskLine_MR = self.findChild(QtWidgets.QLineEdit, 'maskLine_MR')
        self.maskBrowse_MR = self.findChild(QtWidgets.QPushButton, 'maskBrowse_MR')

        self.resolutionRangeLabel_MR = self.findChild(QtWidgets.QLabel, 'resolutionRangeLabel_MR')
        self.fromLabel_MR  = self.findChild(QtWidgets.QLabel, 'fromLabel_MR')
        self.toLabel_MR = self.findChild(QtWidgets.QLabel, 'toLabel_MR')
        self.stepLabel_MR = self.findChild(QtWidgets.QLabel, 'stepLabel_MR')
        self.samplingLabel_MR = self.findChild(QtWidgets.QLabel, 'samplingLabel_MR')

        self.highResLine_MR = self.findChild(QtWidgets.QLineEdit, 'highResLine_MR')
        self.lowResLine_MR = self.findChild(QtWidgets.QLineEdit, 'lowResLine_MR')
        self.stepLine_MR = self.findChild(QtWidgets.QLineEdit, 'stepLine_MR')
        self.samplingLine_MR = self.findChild(QtWidgets.QLineEdit, 'samplingLine_MR')

        self.advancedCheckBox_MR = self.findChild(QtWidgets.QCheckBox, 'advancedCheckBox_MR')
        self.significanceLabel_MR = self.findChild(QtWidgets.QLabel, 'significanceLabel_MR')
        self.significanceLine_MR = self.findChild(QtWidgets.QLineEdit, 'significanceLine_MR')

        self.GausianLabel_MR = self.findChild(QtWidgets.QLabel, 'GausianLabel_MR')
        self.GausianYes_MR = self.findChild(QtWidgets.QRadioButton, 'GausianYes_MR')
        self.GausianNo_MR = self.findChild(QtWidgets.QRadioButton, 'GausianNo_MR')

        # MonoRes callBacks
        self.halfMap1Browse_MR.clicked.connect(lambda: self.setBrowsePathToLineEdit(self.halfMap1Line_MR))
        self.halfMap1Browse_MR.clicked.connect(lambda: self.setBrowsePathToLineEdit(self.halfMap2Line_MR))
        self.maskBrowse_MR.clicked.connect(lambda: self.setBrowsePathToLineEdit(self.maskLine_MR))

        self.ExecuteLabel_MR.clicked.connect(lambda: self.executeButtonMonoDir())

        # MonoDir Parameters
        self.mapLabel_MD = self.findChild(QtWidgets.QLabel, 'mapLabel_MD')
        self.maskLabel_MD = self.findChild(QtWidgets.QLabel, 'maskLabel_MD')

        self.mapLine_MD = self.findChild(QtWidgets.QLineEdit, 'mapLine_MD')
        self.maskLine_MD = self.findChild(QtWidgets.QLineEdit, 'maskLine_MD')

        self.mapBrowse_MD = self.findChild(QtWidgets.QPushButton, 'mapBrowse_MD')
        self.maskBrowse_MD = self.findChild(QtWidgets.QPushButton, 'maskBrowse_MD')

        self.samplingLabel_MD = self.findChild(QtWidgets.QLabel, 'samplingLabel_MD')
        self.samplingLine_MD = self.findChild(QtWidgets.QLineEdit, 'samplingLine_MD')

        self.advancedCheckBox_MD = self.findChild(QtWidgets.QCheckBox, 'advancedCheckBox_MD')
        self.significanceLabel_MD = self.findChild(QtWidgets.QLabel, 'significanceLabel_MD')
        self.significanceLine_MD = self.findChild(QtWidgets.QLineEdit, 'significanceLine_MD')

        self.premaskedLabel_MD = self.findChild(QtWidgets.QLabel, 'premaskedLabel_MD')
        self.premaskedYes_MD = self.findChild(QtWidgets.QRadioButton, 'premaskedYes_MD')
        self.premaskedNo_MD = self.findChild(QtWidgets.QRadioButton, 'premaskedNo_MD')

        self.fastLabel_MD = self.findChild(QtWidgets.QLabel, 'fastLabel_MD')
        self.fastYes_MD = self.findChild(QtWidgets.QRadioButton, 'fastYes_MD')
        self.fastNo_MD = self.findChild(QtWidgets.QRadioButton, 'fastNo_MD')

        # MonoDir callBacks
        self.mapBrowse_MD.clicked.connect(lambda: self.setBrowsePathToLineEdit(self.mapLine_MD))
        self.maskBrowse_MD.clicked.connect(lambda: self.setBrowsePathToLineEdit(self.maskLine_MD))
        self.ExecuteLabel_MD.clicked.connect(lambda: self.executeButtonMonoDir())

        # Top Banner
        self.XmippButton = self.findChild(QtWidgets.QPushButton, 'XmippButton')
        self.helpButton = self.findChild(QtWidgets.QPushButton, 'helpButton')
        self.citeButton = self.findChild(QtWidgets.QPushButton, 'citeButton')
        self.pathButton = self.findChild(QtWidgets.QPushButton, 'pathButton')
        self.pathLineEdit = self.findChild(QtWidgets.QLineEdit, 'pathLineEdit')

        self.XmippButton.clicked.connect(self.labwebsite)
        self.helpButton.clicked.connect(self.helpApp)
        self.citeButton.clicked.connect(self.cite)
        self.pathButton.clicked.connect(self.browsePath)

        self.pathLineEdit.setText(os.getcwd())


        self.pathApp = self.pathLineEdit.text()
        self.resultsPath = self.createResultsFolder(self.pathApp)

        self.show()

    def browsePath(self):
        self.pathApp = QFileDialog.getExistingDirectory(self, "Set working directory",
                                                        QtCore.QCoreApplication.applicationDirPath())
        if self.pathApp == '':
            self.pathApp = str(os.getcwd())
        self.pathLineEdit.setText(self.pathApp)
        self.resultsPath = self.pathApp + "/results/"

    def labwebsite(self):
        QtGui.QDesktopServices.openUrl(QtCore.QUrl("https://github.com/I2PC/xmipp"))

    def helpApp(self):
        QtWidgets.QMessageBox.about(self, "About Local Resolution Tools",
                                    "<b>Local Resolution MonoRes</b><br>"
                                    "<small>This program may be used to estimate the directional FSC between two half maps. The directionality is measured by means of conical-like filters in Fourier Space. To avoid possible Gibbs effects the filters are gaussian functions with their respective maxima along the filtering direction. A set of 321 directions is used to cover the projection sphere, computing for each direction the directional FSC at 0.143 between the two half maps. The result is a set of 321 FSC curves. From then a 3DFSC is obtained by interpolation. Note that as well as it occurs with  global FSC, the directional FSC is mask dependent.</small><br>"
                                    "<br>"
                                    "<b>Local Resolution MonoTomo</b><br>"
                                    "<small>The  Fourier Shell Occupancy can be obtained from the set of directional FSC curves estimated before. To do that, the two half maps are used to determine the Global FSC at threshold 0.143. Then, the ratio between the number of directions with resolution higher (better) than the Global resolution and the total number of measured directions is calculated at different frequencies (resolutions). Note that this ratio is between 0 (all directions presents worse) resolution than the global FSC)  and 1 (all directions present better resolution than the FSC) at a given resolution. In the particular case for which the FSO curve takes the value of 0.5, then half of the directions are better, and the other half are worse than the FSC. Therefore, the FSO curve at 0.5 should be the FSC value. Note that a map is isotropic if all directional resolution are similar, and anisotropic is there are significant resolution values along  different directions. Thus, when the OFSC present a sharp cliff, it means step-like function the map will be isotropic. In contrast, when the FSO shows a slope the map will be anisotropic. The lesser slope the higher resolution isotropy. </small><br>"
                                    "<br>"
                                    "<b>Local Resolution MonoDir</b><br>"
                                    "<small>If a set of particle is provided, the algorithm will determine the contribution of each particle to the directional resolution and it's effect in the resolution anisotropy. It means to determine if the directional resolution is explained by particles. If not, then probably your set of particle contains empty particles (noise), the reconstruction presents heterogeneity or flexibility, in that the heterogeneity should be solved and the map reconstructed again</small>");

    def cite(self):
        QtWidgets.QMessageBox.about(self, "Reference of the algorithm",
                                    "Reference: J.L. Vilas, H.D. Tagare, XXXXX (2020)")

    def setBrowsePathToLineEdit(self, lineEdit):
        pathToset = QFileDialog.getOpenFileName(self, "Select", self.pathApp)
        lineEdit.setText(pathToset[0])

    def executeButtonMonoTomo(self):
        xmippCmdline, params = self.createXmippMonoTomoScript()

        if not os.path.exists(self.resultsPath):
            os.makedirs(self.resultsPath)

        xmippCmdline = xmippCmdline + " " + params
        env_var = os.environ
        os.environ['XMIPP_HOME'] = self.xmippPath
        os.environ['PATH'] = self.xmippPath + '/bin' + ':' + os.environ['PATH']
        if not 'LD_LIBRARY_PATH' in os.environ:
            os.environ['LD_LIBRARY_PATH'] = self.xmippPath + '/lib'
        else:
            os.environ['LD_LIBRARY_PATH'] += self.xmippPath + '/lib' + ':' + os.environ['LD_LIBRARY_PATH']

        print(xmippCmdline)
        self.ExecuteLabel_MT.setDisabled(True)
        self.analyzeButton_MT.setDisabled(True)
        #import subprocess
        #p = os.popen(xmippCmdline)
        #p.wait()
        os.system(xmippCmdline)

        cmdHist = self.createHistrogramMonoTomo()

        #p = os.popen(cmdHist)
        #p.wait()
        self.ExecuteLabel_MT.setEnabled(True)
        self.analyzeButton_MT.setEnabled(True)
        #os.system(cmdHist)

    def createHistrogramMonoTomo(self):
        M = float(self.lowResLine_MT.text())
        m = float(self.highResLine_MT.text())

        freq_step = float(self.stepLine_MT.text()) if (self.stepLine_MT.text() != '') else 10

        range_res = round((M - m) / freq_step)

        params = ' -i %s' % self.resultsPath + '/localResolutionTomogram.mrc'
        params += ' --steps %f' % range_res
        params += ' --range %f %f' % (m, M-freq_step)
        params += ' -o %s' % self.resultsPath + '/histogramMonoTomo.xmd'

        return 'xmipp_image_histogram' + params

    def analyzeResultsMonoTomo(self):
        self.window = QtWidgets.QMainWindow()
        self.ui = Ui_AnalyzeResults(self.resultsPath)

    def createResultsFolder(self, path):
        # ! usr/bin/python
        from datetime import datetime
        import os

        today = datetime.now()

        outputPath = path + "/results_" + today.strftime('%Y%m%d_') + str(today.hour) + str(today.minute)
        os.mkdir(outputPath)
        return outputPath

    def executeButtonMonoDir(self):
        xmippCmdline, params = self.createXmippScript()

        if not os.path.exists(self.resultsPath):
            os.makedirs(self.resultsPath)

        xmippCmdline = xmippCmdline + " " + params

        os.environ['XMIPP_HOME'] = self.xmippPath
        os.environ['PATH'] = self.xmippPath + '/bin' + ':' + os.environ['PATH']
        os.environ['LD_LIBRARY_PATH'] = self.xmippPath + '/lib' + ':' + os.environ['LD_LIBRARY_PATH']

        os.system(xmippCmdline)

        self.analyze.setEnabled(True)

    def addcolonmrc(self, fn):
        fn_slit = os.path.splitext(fn)
        if (fn_slit[-1] == ".mrc") or (fn_slit[-1] == ".map"):
            return fn + ":mrc"
        else:
            return fn

    def createXmippMonoTomoScript(self):
        program = "xmipp_resolution_monotomo "
        params = " --vol %s" % self.addcolonmrc(self.oddLine_MT.text())
        params += " --vol2 %s" % self.addcolonmrc(self.evenLine_MT.text())

        params += " --meanVol %s " % (self.resultsPath +'/meanTomogram.mrc')
        params += " --sampling_rate %s" % self.samplingLine_MT.text()
        params += " --minRes %s " % self.lowResLine_MT.text()
        params += " --maxRes %s " % self.highResLine_MT.text()
        params += " --step %s " % self.stepLine_MT.text()
        params += " --significance %s " % self.significanceLine_MT.text()
        params += " --threads %s " % '4' #self.threadsLine_MT.text()
        params += " -o %s " % (self.resultsPath + '/localResolutionTomogram.mrc')

        return program, params


    def createXmippMonoResScript(self):
        program = "xmipp_resolution_monogenic_signal "

        params = " --vol %s" % self.addcolonmrc(self.halfMap1Line_MR.text())
        params += " --vol2 %s" % self.addcolonmrc(self.halfMap2Line_MR.text())

        params += " --mask %s" % self.addcolonmrc(self.maskLine_MR.text())

        params += " --sampling_rate %s" % self.samplingLine_MR.text()
        params += " --minRes %s " % self.lowResLine_MR.text()
        params += " --maxRes %s " % self.highResLine_MR.text()
        params += " --step %s " % self.stepLine_MR.text()
        params += " --significance %s " % self.significanceLine_MR.text()
        params += " --threads %s " % self.threadsLine_MR.text()
        params += " -o %s " % xxxxxxxxx

        #gaussian = checkParam("--gaussian")
        #noiseOnlyInHalves = checkParam("--noiseonlyinhalves")

        return program, params

    def analyzeResultsBase(self, protocol):
        pass

    def createXmippMonoDirScript(self):
        program = "xmipp_resolution_direction "
        params = " --vol %s" % self.addcolonmrc(self.mapLine_MD.text())
        params += " --mask %s" % self.addcolonmrc(self.maskLine_MD.text())

        params += " --sampling_rate %s" % self.samplingLine_MD.text()
        params += " --significance %s " % self.significanceLine_MT.text()
        params += " --threads %s " % self.threadsLine_MT.text()
        params += " -o %s " % xxxxxxxxx

        return program, params


app = QtWidgets.QApplication(sys.argv)
window = Ui()
app.exec_()
