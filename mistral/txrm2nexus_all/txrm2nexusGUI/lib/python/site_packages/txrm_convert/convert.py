'''
Created on Aug 13, 2013

@author: mrosanes
'''



from PyQt4 import QtGui
from PyQt4 import QtCore
import os


class Convertion(QtGui.QTabWidget):
    
    def __init__(self):
        super(Convertion, self).__init__()
        self.initUI()
        
        
    def initUI(self):     
         
        self.tabWidget = QtGui.QTabWidget()
        self.tabWidget.setWindowTitle('txm2nexus')  
        self.tabWidget.resize(700,400)
        
        
        ########
        self.createTabTxrm2Nexus()
        
        ########
        self.createTabMosaic2Nexus()
        
        #######
        self.createTabNormalize()

        #######
        self.createTabAutoTxrm2Nexus()
        
        #######
        self.createTabAutoMosaic2Nexus()
        
        #######
        self.createTabAutoNormalize()
        
        
        self.tabWidget.show()



    #######################################################
    
    def createTabTxrm2Nexus(self): 
        
        self.tab_txrm2nexus=QtGui.QWidget()

        
        self.setGeometry(500, 300, 700, 400)
        self.setWindowTitle('txrm2nexus_GUI')
        
        
        self.btn_tom_txrm = QtGui.QPushButton('Tomography', self.tab_txrm2nexus)
        self.btn_tom_txrm.move(20, 20)
        self.connect(self.btn_tom_txrm, QtCore.SIGNAL('clicked()'), self.showDialogTomoTxrm)        
        
        self.tom = QtGui.QLineEdit(self.tab_txrm2nexus)
        self.tom.setText('enter_a_tomo.txrm')
        self.tom.setGeometry(170, 20, 500, 22)
        
        
        self.btn_bright = QtGui.QPushButton('Bright_Field', self.tab_txrm2nexus)
        self.btn_bright.move(20, 60)
        self.connect(self.btn_bright, QtCore.SIGNAL('clicked()'), self.showDialogBrightTxrm)  
        
        self.bright = QtGui.QLineEdit(self.tab_txrm2nexus)
        self.bright.setText('enter_a_bright_field.txrm')
        self.bright.setGeometry(170, 60, 500, 22)
        
        
        self.btn_output_txrm = QtGui.QPushButton('Output_HDF5', self.tab_txrm2nexus)
        self.btn_output_txrm.move(20, 100)
        self.connect(self.btn_output_txrm, QtCore.SIGNAL('clicked()'), self.showDialogOutputTxrm)  
        
        self.output_txrm = QtGui.QLineEdit(self.tab_txrm2nexus)
        self.output_txrm.setText('enter_an_output_name.hdf5')
        self.output_txrm.setGeometry(170, 100, 500, 22)


        self.btn_order = QtGui.QPushButton('Order', self.tab_txrm2nexus)
        self.btn_order.move(20, 140)
        self.connect(self.btn_order, QtCore.SIGNAL('clicked()'), self.showDialogOrderTxrm)         
        
        self.order = QtGui.QLineEdit(self.tab_txrm2nexus)
        self.order.setText('sb')
        self.order.setGeometry(170, 140, 500, 22)
        
        
        self.btn_first = QtGui.QPushButton('first_image', self.tab_txrm2nexus)
        self.btn_first.move(20, 180)
        self.connect(self.btn_first, QtCore.SIGNAL('clicked()'), self.showDialogFirstTxrm)        
        
        self.first = QtGui.QLineEdit(self.tab_txrm2nexus)
        self.first.setText('enter_first_image_at_0_degrees.txrm')
        self.first.setGeometry(170, 180, 500, 22)
        
        
        self.btn_last = QtGui.QPushButton('last_image', self.tab_txrm2nexus)
        self.btn_last.move(20, 220)
        self.connect(self.btn_last, QtCore.SIGNAL('clicked()'), self.showDialogLastTxrm)        
              
        self.last = QtGui.QLineEdit(self.tab_txrm2nexus)
        self.last.setText('enter_last_image_at_0_degrees.txrm')
        self.last.setGeometry(170, 220, 500, 22)
        
        
        self.btn_command_txrm = QtGui.QPushButton('command', self.tab_txrm2nexus)
        self.btn_command_txrm.move(20, 260)
        self.connect(self.btn_command_txrm, QtCore.SIGNAL('clicked()'), self.showCommandLineTxrm)   
        
        self.program_call_txrm = QtGui.QLineEdit(self.tab_txrm2nexus)
        self.program_call_txrm.setGeometry(170, 260, 500, 22)


        self.btn_help_txrm = QtGui.QPushButton('Help in Console', self.tab_txrm2nexus)
        self.btn_help_txrm.move(20, 300)
        self.connect(self.btn_help_txrm, QtCore.SIGNAL('clicked()'), self.helpConsoleTxrm)    
        
        
        self.btn_accept_txrm = QtGui.QPushButton('Accept', self.tab_txrm2nexus)
        self.btn_accept_txrm.move(490, 300)
        self.connect(self.btn_accept_txrm, QtCore.SIGNAL('clicked()'), self.acceptExecutionTxrm)         
        
        
        self.btn_close_txrm = QtGui.QPushButton('Close', self.tab_txrm2nexus)
        self.btn_close_txrm.move(570, 300)
        self.connect(self.btn_close_txrm, QtCore.SIGNAL('clicked()'), self.closeTxrm)        
        
        
        self.tabWidget.addTab(self.tab_txrm2nexus,"txrm2nexus")

     
        
    def commandLineStringTxrm(self):
        tom_file = self.tom.text()
        brigth_file = self.bright.text()
        order_dsb = self.order.text()
        output_file = self.output_txrm.text()
        first_image_file = self.first.text()
        last_image_file = self.last.text()
        
        if ((first_image_file != ' ' and first_image_file != 'enter_first_image_at_0_degrees.txrm') or (last_image_file != ' ' and last_image_file != 'enter_last_image_at_0_degrees.txrm')):
            program_call_qtext = ('txrm2nexus ' + tom_file + ' ' + brigth_file + ' ' + output_file + ' -o=' + order_dsb + 
                             ' -zi=' + first_image_file + ' -zf=' +  last_image_file)
        else:
            program_call_qtext = ('txrm2nexus ' + tom_file + ' ' + brigth_file + ' ' + output_file + ' -o=' + order_dsb)
            
        program_call_string = str(program_call_qtext)    
        return program_call_string
        
        
        
    def showCommandLineTxrm(self):
        txrm2nexus_command = self.commandLineStringTxrm()
        self.program_call_txrm.setText(txrm2nexus_command)
        
         
    def acceptExecutionTxrm(self):

        txrm2nexus_command = self.commandLineStringTxrm()
        os.system(txrm2nexus_command)
            
    def closeTxrm(self):
        QtCore.QCoreApplication.instance().quit()           
        
    
    def helpConsoleTxrm(self):
        txrm2nexus_command_help = 'txrm2nexus --h'
        os.system(txrm2nexus_command_help)   
        
            
    def showDialogTomoTxrm(self):     
        text, ok = QtGui.QInputDialog.getText(self, 'Tomography', 
            'Enter the tomography filename:')
        if ok:
            self.tom.setText(str(text))
   

    def showDialogBrightTxrm(self):
        text, ok = QtGui.QInputDialog.getText(self, 'Bright Field', 
                'Enter the brightfield filename:')
        if ok:
            self.bright.setText(str(text))
      
    
    def showDialogOutputTxrm(self):
        text, ok = QtGui.QInputDialog.getText(self, 'Output', 
                'Enter the output filename:')
        if ok:
            self.output_txrm.setText(str(text))
            
                            
    def showDialogOrderTxrm(self):
        text, ok = QtGui.QInputDialog.getText(self, 'Order', 
                'Enter the Order of tomos, brightfields and darkfields (default: sb):')
        if ok:
            self.order.setText(str(text))
        
        
    def showDialogFirstTxrm(self):
        text, ok = QtGui.QInputDialog.getText(self, 'First Image', 
                'Enter the filename from the first image at 0 degrees:')
        if ok:
            self.first.setText(str(text))    
        

    def showDialogLastTxrm(self):
        text, ok = QtGui.QInputDialog.getText(self, 'Last Image', 
                'Enter the filename from the last image at 0 degrees:')
        if ok:
            self.last.setText(str(text))  
            
            
            
            
            
            
            

    #######################################################
    
    def createTabMosaic2Nexus(self): 
        
        self.tab_mosaic2nexus=QtGui.QWidget()
             
        self.btn_mosaic = QtGui.QPushButton('Mosaic', self.tab_mosaic2nexus)
        self.btn_mosaic.move(20, 40)
        self.connect(self.btn_mosaic, QtCore.SIGNAL('clicked()'), self.showDialogMosaic)        
        
        self.mosaic = QtGui.QLineEdit(self.tab_mosaic2nexus)
        self.mosaic.setText('enter_a_mosaic.xrm')
        self.mosaic.setGeometry(170, 40, 500, 22)
        
        self.btn_output_mosaic = QtGui.QPushButton('Output_HDF5', self.tab_mosaic2nexus)
        self.btn_output_mosaic.move(20, 80)
        self.connect(self.btn_output_mosaic, QtCore.SIGNAL('clicked()'), self.showDialogOutputMosaic)  
        
        self.output_mosaic = QtGui.QLineEdit(self.tab_mosaic2nexus)
        self.output_mosaic.setText('enter_an_output_name.hdf5')
        self.output_mosaic.setGeometry(170, 80, 500, 22)

        self.btn_command_mosaic = QtGui.QPushButton('command', self.tab_mosaic2nexus)
        self.btn_command_mosaic.move(20, 120)
        self.connect(self.btn_command_mosaic, QtCore.SIGNAL('clicked()'), self.showCommandLineMosaic)   
        
        self.program_call_mosaic = QtGui.QLineEdit(self.tab_mosaic2nexus)
        self.program_call_mosaic.setGeometry(170, 120, 500, 22)


        self.btn_help_mosaic = QtGui.QPushButton('Help in Console', self.tab_mosaic2nexus)
        self.btn_help_mosaic.move(20, 300)
        self.connect(self.btn_help_mosaic, QtCore.SIGNAL('clicked()'), self.helpConsoleMosaic)    
        
        
        self.btn_accept_mosaic = QtGui.QPushButton('Accept', self.tab_mosaic2nexus)
        self.btn_accept_mosaic.move(490, 300)
        self.connect(self.btn_accept_mosaic, QtCore.SIGNAL('clicked()'), self.acceptExecutionMosaic)         
        
        
        self.btn_close_mosaic = QtGui.QPushButton('Close', self.tab_mosaic2nexus)
        self.btn_close_mosaic.move(570, 300)
        self.connect(self.btn_close_mosaic, QtCore.SIGNAL('clicked()'), self.closeMosaic)
      
        self.tabWidget.addTab(self.tab_mosaic2nexus,"mosaic2nexus")    
        
        
        
    def commandLineStringMosaic(self):
        mosaic_file = self.mosaic.text()
        output_file = self.output_mosaic.text()
        
        program_call_qtext = ('mosaic2nexus ' + mosaic_file + ' ' + output_file)
            
        program_call_string = str(program_call_qtext)    
        return program_call_string
        
    
    def showCommandLineMosaic(self):
        mosaic2nexus_command = self.commandLineStringMosaic()
        self.program_call_mosaic.setText(mosaic2nexus_command)
        
    
    def acceptExecutionMosaic(self):
        mosaic2nexus_command = self.commandLineStringMosaic()            
        os.system(mosaic2nexus_command)
     
            
    def closeMosaic(self):
        QtCore.QCoreApplication.instance().quit()           
        
    
    def helpConsoleMosaic(self):
        mosaic2nexus_command_help = 'mosaic2nexus --h'
        os.system(mosaic2nexus_command_help)   
        
            
    def showDialogMosaic(self):     
        text, ok = QtGui.QInputDialog.getText(self, 'Mosaic', 
            'Enter the mosaic filename:')
        if ok:
            self.mosaic.setText(str(text))
   
         
    def showDialogOutputMosaic(self):
        text, ok = QtGui.QInputDialog.getText(self, 'Output', 
                'Enter the output hdf5 filename:')
        if ok:
            self.output_mosaic.setText(str(text))   
   
 

    
            
    #######################################################
    
    def createTabNormalize(self): 
        
        self.tab_normalize = QtGui.QWidget()  
        
        self.btn_tom_normalize = QtGui.QPushButton('Input Tomography', self.tab_normalize)
        self.btn_tom_normalize.move(20, 20)
        self.connect(self.btn_tom_normalize, QtCore.SIGNAL('clicked()'), self.showDialogTomoNormalize)        
        
        self.tom_normal = QtGui.QLineEdit(self.tab_normalize)
        self.tom_normal.setText('enter_a_complete_hdf5_NeXus_tomo.hdf5')
        self.tom_normal.setGeometry(170, 20, 500, 22)
    
        self.btn_ffexptime = QtGui.QPushButton('FFexpTime', self.tab_normalize)
        self.btn_ffexptime.move(20, 60)
        self.connect(self.btn_ffexptime, QtCore.SIGNAL('clicked()'), self.showDialogFFexptime)        
        
        self.ffexptime = QtGui.QLineEdit(self.tab_normalize)
        self.ffexptime.setText('FF exposure time (if not indicated, extracted from FF information of hdf5).')
        self.ffexptime.setGeometry(170, 60, 500, 22)
        
        self.btn_command_normalize = QtGui.QPushButton('command', self.tab_normalize)
        self.btn_command_normalize.move(20, 100)
        self.connect(self.btn_command_normalize, QtCore.SIGNAL('clicked()'), self.showCommandLineNormalize)   
        
        self.program_call_normalize = QtGui.QLineEdit(self.tab_normalize)
        self.program_call_normalize.setGeometry(170, 100, 500, 22)


        self.btn_help_normalize = QtGui.QPushButton('Help in Console', self.tab_normalize)
        self.btn_help_normalize.move(20, 300)
        self.connect(self.btn_help_normalize, QtCore.SIGNAL('clicked()'), self.helpConsoleNormalize)    
        
        
        self.btn_accept_normalize = QtGui.QPushButton('Accept', self.tab_normalize)
        self.btn_accept_normalize.move(490, 300)
        self.connect(self.btn_accept_normalize, QtCore.SIGNAL('clicked()'), self.acceptExecutionNormalize)         
        
        
        self.btn_close_normalize = QtGui.QPushButton('Close', self.tab_normalize)
        self.btn_close_normalize.move(570, 300)
        self.connect(self.btn_close_normalize, QtCore.SIGNAL('clicked()'), self.closeNormalize)        
        
        self.tabWidget.addTab(self.tab_normalize,"normalize")
       
     
        
    def commandLineStringNormalize(self):
        normalize_input_file = self.tom_normal.text()
        
        ffexptime_text = self.ffexptime.text()
        
        ffexptime_number_ok = 1
        try: 
            float(ffexptime_text)                                                                                                                                                                       
        except:                                                                                                                                                                                     
            ffexptime_number_ok = 0
            
        
        if ffexptime_number_ok == 0 or float(ffexptime_text) == 0:
            program_call_qtext = ('normalize ' + normalize_input_file)
        else:
            program_call_qtext = ('normalize ' + normalize_input_file + ' -e=' + self.ffexptime.text())
                
        program_call_string = str(program_call_qtext)    
        return program_call_string
        
        
        
    def showCommandLineNormalize(self):
        normalize_command = self.commandLineStringNormalize()
        self.program_call_normalize.setText(normalize_command)
        
         
    def acceptExecutionNormalize(self):

        normalize_command = self.commandLineStringNormalize()
        os.system(normalize_command)
            
    def closeNormalize(self):
        QtCore.QCoreApplication.instance().quit()           
        
    
    def helpConsoleNormalize(self):
        normalize_command_help = 'normalize --h'
        os.system(normalize_command_help)   
        
            
    def showDialogTomoNormalize(self):     
        text, ok = QtGui.QInputDialog.getText(self, 'Tomography NeXus HDF5', 
            'Enter the filename of the complete NeXus HDF5 tomography:')
        if ok:
            self.tom_normal.setText(str(text))
   
   
    def showDialogFFexptime(self):
        text, ok = QtGui.QInputDialog.getText(self, 'FF exposure time', 
            'Optional: Indicate the FF exposure time (If nothing indicated it is extracted from the FF information in the hdf5).')
        if ok:
            self.ffexptime.setText(str(text)) 
            
    
    
    
    
    
    
    
    #######################################################
    
    def createTabAutoTxrm2Nexus(self): 
     

        self.tab_autotxrm2nexus = QtGui.QWidget()  
        
        self.btn_auto_txrm_folder = QtGui.QPushButton('Input Folder', self.tab_autotxrm2nexus)
        self.btn_auto_txrm_folder.move(20, 20)
        self.connect(self.btn_auto_txrm_folder, QtCore.SIGNAL('clicked()'), self.showDialogTomoAutoTxrm)        
        
        self.folder_autotxrm = QtGui.QLineEdit(self.tab_autotxrm2nexus)
        self.folder_autotxrm.setText('enter_the_folder_where_tomoSubFolders_are_located')
        self.folder_autotxrm.setGeometry(170, 20, 500, 22)
        
        self.btn_command_autotxrm = QtGui.QPushButton('command', self.tab_autotxrm2nexus)
        self.btn_command_autotxrm.move(20, 100)
        self.connect(self.btn_command_autotxrm, QtCore.SIGNAL('clicked()'), self.showCommandLineAutoTxrm)   
        
        self.program_call_autotxrm = QtGui.QLineEdit(self.tab_autotxrm2nexus)
        self.program_call_autotxrm.setGeometry(170, 100, 500, 22)


        self.btn_help_autotxrm = QtGui.QPushButton('Help in Console', self.tab_autotxrm2nexus)
        self.btn_help_autotxrm.move(20, 300)
        self.connect(self.btn_help_autotxrm, QtCore.SIGNAL('clicked()'), self.helpConsoleAutoTxrm)    
        
        
        self.btn_accept_autotxrm = QtGui.QPushButton('Accept', self.tab_autotxrm2nexus)
        self.btn_accept_autotxrm.move(490, 300)
        self.connect(self.btn_accept_autotxrm, QtCore.SIGNAL('clicked()'), self.acceptExecutionAutoTxrm)         
        
        
        self.btn_close_autotxrm = QtGui.QPushButton('Close', self.tab_autotxrm2nexus)
        self.btn_close_autotxrm.move(570, 300)
        self.connect(self.btn_close_autotxrm, QtCore.SIGNAL('clicked()'), self.closeAutoTxrm)        
        
        self.tabWidget.addTab(self.tab_autotxrm2nexus,"autotxrm2nexus")
       
     
        
    def commandLineStringAutoTxrm(self):
        txrms_folder_text = self.folder_autotxrm.text()
        program_call_qtext = ('autotxrm2nexus ' + txrms_folder_text)
                
        program_call_string = str(program_call_qtext)    
        return program_call_string
            
        
    def showCommandLineAutoTxrm(self):
        autotxrm_command = self.commandLineStringAutoTxrm()
        self.program_call_autotxrm.setText(autotxrm_command)
        
         
    def acceptExecutionAutoTxrm(self):
        autotxrm_command = self.commandLineStringAutoTxrm()
        os.system(autotxrm_command)
            
    def closeAutoTxrm(self):
        QtCore.QCoreApplication.instance().quit()           
        
    
    def helpConsoleAutoTxrm(self):
        autotxrm_command_help = 'autotxrm2nexus --h'
        os.system(autotxrm_command_help)   
        
            
    def showDialogTomoAutoTxrm(self):     
        text, ok = QtGui.QInputDialog.getText(self, 'Folder with subfolders tomo1, tomo2..', 
            'Enter the folder where subfolders tomo1, tomo2, tomo3, etc. are located (these subfolders contain the .txrm files with the tomos to be converted to NeXus HDF5).')
        if ok:
            self.folder_autotxrm.setText(str(text))
                   



    
    
    #######################################################
    
    def createTabAutoMosaic2Nexus(self): 
        
        self.tab_automosaic2nexus = QtGui.QWidget()  
        
        self.btn_auto_mosaic_folder = QtGui.QPushButton('Input Folder', self.tab_automosaic2nexus)
        self.btn_auto_mosaic_folder.move(20, 20)
        self.connect(self.btn_auto_mosaic_folder, QtCore.SIGNAL('clicked()'), self.showDialogTomoAutoMosaic)        
        
        self.folder_automosaic = QtGui.QLineEdit(self.tab_automosaic2nexus)
        self.folder_automosaic.setText('enter_the_folder_where_mosaicSubFolders_are_located')
        self.folder_automosaic.setGeometry(170, 20, 500, 22)
        
        self.btn_command_automosaic = QtGui.QPushButton('command', self.tab_automosaic2nexus)
        self.btn_command_automosaic.move(20, 100)
        self.connect(self.btn_command_automosaic, QtCore.SIGNAL('clicked()'), self.showCommandLineAutoMosaic)   
        
        self.program_call_automosaic = QtGui.QLineEdit(self.tab_automosaic2nexus)
        self.program_call_automosaic.setGeometry(170, 100, 500, 22)


        self.btn_help_automosaic = QtGui.QPushButton('Help in Console', self.tab_automosaic2nexus)
        self.btn_help_automosaic.move(20, 300)
        self.connect(self.btn_help_automosaic, QtCore.SIGNAL('clicked()'), self.helpConsoleAutoMosaic)    
        
        
        self.btn_accept_automosaic = QtGui.QPushButton('Accept', self.tab_automosaic2nexus)
        self.btn_accept_automosaic.move(490, 300)
        self.connect(self.btn_accept_automosaic, QtCore.SIGNAL('clicked()'), self.acceptExecutionAutoMosaic)         
        
        
        self.btn_close_automosaic = QtGui.QPushButton('Close', self.tab_automosaic2nexus)
        self.btn_close_automosaic.move(570, 300)
        self.connect(self.btn_close_automosaic, QtCore.SIGNAL('clicked()'), self.closeAutoMosaic)        
        
        self.tabWidget.addTab(self.tab_automosaic2nexus,"automosaic2nexus")
       
     
        
    def commandLineStringAutoMosaic(self):
        mosaics_folder_text = self.folder_automosaic.text()
        program_call_qtext = ('automosaic2nexus ' + mosaics_folder_text)
                
        program_call_string = str(program_call_qtext)    
        return program_call_string
            
        
    def showCommandLineAutoMosaic(self):
        automosaic_command = self.commandLineStringAutoMosaic()
        self.program_call_automosaic.setText(automosaic_command)
        
         
    def acceptExecutionAutoMosaic(self):
        automosaic_command = self.commandLineStringAutoMosaic()
        os.system(automosaic_command)
            
    def closeAutoMosaic(self):
        QtCore.QCoreApplication.instance().quit()           
        
    
    def helpConsoleAutoMosaic(self):
        automosaic_command_help = 'automosaic2nexus --h'
        os.system(automosaic_command_help)   
        
            
    def showDialogTomoAutoMosaic(self):     
        text, ok = QtGui.QInputDialog.getText(self, 'Folder with subfolders mosaic1, mosaic2...', 
            'Enter the folder where subfolders mosaic1, mosaic2, mosaic3, etc. are located (these subfolders contain the .xrm files with the mosaics to be converted to NeXus HDF5).')
        if ok:
            self.folder_automosaic.setText(str(text))
                




    
        
    #######################################################
        
    def createTabAutoNormalize(self): 
        
        self.tab_autonormalize = QtGui.QWidget()  
        
        self.btn_auto_normalize_folder = QtGui.QPushButton('Input Folder', self.tab_autonormalize)
        self.btn_auto_normalize_folder.move(20, 20)
        self.connect(self.btn_auto_normalize_folder, QtCore.SIGNAL('clicked()'), self.showDialogAutoNormalizeFolder)        
        
        self.folder_autonormal = QtGui.QLineEdit(self.tab_autonormalize)
        self.folder_autonormal.setText('enter_the_folder_where_HDF5tomoSubFolders_are_located')
        self.folder_autonormal.setGeometry(170, 20, 500, 22)
    
        
        self.btn_command_normalize = QtGui.QPushButton('command', self.tab_autonormalize)
        self.btn_command_normalize.move(20, 100)
        self.connect(self.btn_command_normalize, QtCore.SIGNAL('clicked()'), self.showCommandLineAutoNormalize)   
        
        self.program_call_autonormalize = QtGui.QLineEdit(self.tab_autonormalize)
        self.program_call_autonormalize.setGeometry(170, 100, 500, 22)


        self.btn_help_autonormalize = QtGui.QPushButton('Help in Console', self.tab_autonormalize)
        self.btn_help_autonormalize.move(20, 300)
        self.connect(self.btn_help_autonormalize, QtCore.SIGNAL('clicked()'), self.helpConsoleAutoNormalize)    
        
        
        self.btn_accept_autonormalize = QtGui.QPushButton('Accept', self.tab_autonormalize)
        self.btn_accept_autonormalize.move(490, 300)
        self.connect(self.btn_accept_autonormalize, QtCore.SIGNAL('clicked()'), self.acceptExecutionAutoNormalize)         
        
        
        self.btn_close_autonormalize = QtGui.QPushButton('Close', self.tab_autonormalize)
        self.btn_close_autonormalize.move(570, 300)
        self.connect(self.btn_close_autonormalize, QtCore.SIGNAL('clicked()'), self.closeAutoNormalize)        
        
        self.tabWidget.addTab(self.tab_autonormalize,"autonormalize")
       
       
         
    def commandLineStringAutoNormalize(self):       
        tomos_folder_text = self.folder_autonormal.text()
        program_call_qtext = ('autonormalize ' + tomos_folder_text)
  
        program_call_string = str(program_call_qtext)    
        return program_call_string
        
                
    def showCommandLineAutoNormalize(self):
        autonormalize_command = self.commandLineStringAutoNormalize()
        self.program_call_autonormalize.setText(autonormalize_command)
        
         
    def acceptExecutionAutoNormalize(self):
        autonormalize_command = self.commandLineStringAutoNormalize()             
        os.system(autonormalize_command)
    
            
    def closeAutoNormalize(self):
        QtCore.QCoreApplication.instance().quit()           
        
    
    def helpConsoleAutoNormalize(self):
        autonormalize_command_help = 'autonormalize --h'
        os.system(autonormalize_command_help)   
        
            
    def showDialogAutoNormalizeFolder(self):     
        text, ok = QtGui.QInputDialog.getText(self, 'Folder with subfolders tomo1, tomo2...', 
            'Enter the folder where subfolders tomo1, tomo2, tomo3, etc. are located (these subfolders contain the .hdf5 files with the tomographies to be normalized)' )
        if ok:
            self.folder_autonormal.setText(str(text))
   
   

            
            
            
            
    
    

            
            
      
            
   
