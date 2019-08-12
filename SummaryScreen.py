import sys
sys.path.append('../')

from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import QApplication, QPushButton, QMessageBox, QMainWindow

class Window(QMainWindow):
    def __init__(self, app):
        from Model import BPXDatabase

        super(Window, self).__init__()
        [self.screenheight, self.screenwidth] = self.GetScreenDimensions()
        self.setGeometry(self.screenheight/9, self.screenwidth/9, 0.7 * self.screenheight, 0.7 * self.screenwidth)
        self.setWindowTitle('BPX LE Summary')
        self.setWindowIcon(QtGui.QIcon('bplogo.png'))
        app.setStyle("Fusion")        
        self.DBobj = BPXDatabase.GetDBEnvironment('ProdEDW', 'OVERRIDE')
        self.palette = self.GetPalette()
        self.Format()

    def Format(self):
        from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QScrollArea, QScrollBar, QSpacerItem, QSizePolicy, QAbstractScrollArea, QGroupBox
        from PyQt5.QtGui import QPixmap, QFont
        from PyQt5.QtCore import Qt

        self.setPalette(self.palette)
        #self.FormatButton()
        total_page_layout = QVBoxLayout()
        pic_label = QLabel()
        pixmap = QPixmap('bplogo_transparent.png')
        pixmap = pixmap.scaled(self.width() / 6, self.height() / 6, Qt.KeepAspectRatio, Qt.FastTransformation)
        pic_label.setPixmap(pixmap)        
        picture_layout = QHBoxLayout()
        picture_layout.addWidget(pic_label)
        picture_layout.setAlignment(Qt.AlignCenter)

        app_logo_layout = QHBoxLayout()
        app_label = QLabel()
        app_pixmap = QPixmap('applogo.png')
        app_pixmap = app_pixmap.scaled(self.width() / 6, self.height() / 6, Qt.KeepAspectRatio, Qt.FastTransformation)
        app_label.setPixmap(app_pixmap)
        app_logo_layout.addWidget(app_label)
        app_logo_layout.setAlignment(Qt.AlignCenter)

        title_layout = QHBoxLayout()
        title_label = QLabel('BPX LE Adjustment Utility')
        title_font = QFont( "Georgia", self.height() / 30, QFont.Bold)
        title_label.setFont(title_font)
        title_layout.addWidget(title_label)
        title_layout.setAlignment(Qt.AlignRight)

        header_layout = QHBoxLayout()
        header_layout.addLayout(app_logo_layout)     
        header_layout.addLayout(title_layout)
        header_layout.addLayout(picture_layout)

        total_page_layout.addLayout(header_layout)
        total_page_layout = self.FormatWellSelection(total_page_layout)        
        total_page_layout = self.FormatGraphArea(total_page_layout)

        total_page_layout = self.FormatTableArea(total_page_layout)
        total_page_layout = self.FormatBottomButtonRow(total_page_layout)

        group_box = QGroupBox()
        group_box.setLayout(total_page_layout)
        
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidget(group_box)
        self.scroll_area.setWidgetResizable(True)  
        # self.scroll_area.setFixedHeight(400)

        global_layout = QHBoxLayout()
        global_layout.addWidget(self.scroll_area)

        widget = QWidget() 
        widget.setLayout(global_layout)

        self.setCentralWidget(widget)


    def FormatWellSelection(self, total_page_layout):
        from PyQt5.QtWidgets import QHBoxLayout, QComboBox, QWidget, QVBoxLayout, QLabel, QSpacerItem, QGroupBox
        from PyQt5.QtCore import Qt
        import ScreenUtilities as su

        top_well_layout = QHBoxLayout()
        bottom_well_layout = QHBoxLayout()

        #Area selection
        self.area_cb = QComboBox()
        self.area_label = QLabel('Select Area: ')
        area_items = ['Angie', 'Arkoma West', 'Blackhawk', 'Blocker', 'Brookeland', 'Cotulla', 'East Carthage', 
        'Glenwood', 'Greater Arkoma', 'Karnes', 'LaHa_Area_1', 'Laha_Area_2', 'Laha_Area_3', 'Laha_Area_4', 'Oak Hill', 
        'Permian_Area_1','Permian_Area_2', 'Permian_Area_3', 'Permian_Area_4', 'Red Oak', 'SoHa', 'Stockman', 'Three_Rivers', 
        'Tilden', 'West Carthage', 'Woodlawn']
        self.area_cb.addItem('--')
        self.area_cb.addItems(area_items)
        self.area_cb.currentIndexChanged.connect(self.AreaCBSelected)
        self.area_cb.setPalette(self.palette)
        self.area_cb.setMinimumWidth(self.width() / 8)

        #Route selection
        self.route_cb = QComboBox()
        su.ClearCombobox(self.route_cb)
        self.route_cb_label = QLabel('Select Route')
        self.route_cb.setPalette(self.palette)
        self.route_cb.setMinimumWidth(self.width() / 8)
        
        self.route_cb.currentIndexChanged.connect(self.RouteCBSelected)

        #Well selection
        self.well_cb = QComboBox()        
        su.ClearCombobox(self.well_cb)
        self.well_cb_label = QLabel('Select Well: ')
        self.well_cb.setPalette(self.palette)
        self.well_cb.setMinimumWidth(self.width() / 8)

        #Wedge selection
        self.wedge_cb = QComboBox()
        self.wedg_cb_label = QLabel('Select Base or Wedge: ')
        su.ClearCombobox(self.wedge_cb)
        self.wedge_cb.addItem('Base')
        self.wedge_cb.addItem('Wedge')
        self.wedge_cb.setPalette(self.palette)
        self.wedge_cb.setMinimumWidth(self.width()/11)
        self.wedge_cb.setMaximumWidth(self.width()/9)
    
        top_well_layout.addWidget(self.area_label)   
        top_well_layout.addWidget(self.area_cb) 
        top_well_layout.addWidget(self.route_cb_label)            
        top_well_layout.addWidget(self.route_cb)
        top_well_layout.addWidget(self.well_cb_label)
        top_well_layout.addWidget(self.well_cb)        
        top_well_layout.setAlignment(Qt.AlignLeft)
        
        bottom_well_layout.addWidget(self.wedg_cb_label)
        bottom_well_layout.addWidget(self.wedge_cb)
        bottom_well_layout.setAlignment(Qt.AlignLeft)

        this_section_layout = QVBoxLayout()
        this_section_layout.addLayout(top_well_layout)
        spacer = QSpacerItem(0,  self.height() / 15)
        this_section_layout.addSpacerItem(spacer)
        this_section_layout.addLayout(bottom_well_layout)

        this_section_layout.setAlignment(Qt.AlignCenter)
        self.well_selection_group = QGroupBox()
        self.well_selection_group.setLayout(this_section_layout)

        spacer_layout = QHBoxLayout()
        horizontal_div = QSpacerItem(self.width() / 6, 0)
        spacer_layout.addSpacerItem(horizontal_div)
        spacer_layout.addWidget(self.well_selection_group)
        spacer_layout.addSpacerItem(horizontal_div)
    
        total_page_layout.addLayout(spacer_layout)
        
        return total_page_layout

    def AreaCBSelected(self):
        from PyQt5.QtWidgets import QHBoxLayout, QComboBox
        from Model import QueryFile, BPXDatabase
        import ScreenUtilities as su

        su.ClearCombobox(self.route_cb)
        su.ClearCombobox(self.well_cb)
        Area = self.area_cb.currentText()

        route_query = QueryFile.GetRoutes(Area)
        route_results = self.DBobj.Query(route_query)
        self.route_cb.addItems(route_results[1]['Route'])
        

    def RouteCBSelected(self):
        from PyQt5.QtWidgets import QHBoxLayout, QComboBox
        from Model import QueryFile, BPXDatabase
        import ScreenUtilities as su

        su.ClearCombobox(self.well_cb)
        Route = self.route_cb.currentText()
        Area = self.area_cb.currentText()

        well_query = QueryFile.GetWells(Area, Route)
        well_results = self.DBobj.Query(well_query)
        self.well_cb.addItems(well_results[1]['WellName'])

    def FormatGraphArea(self, total_page_layout):
        from PyQt5.QtWidgets import QCheckBox, QHBoxLayout, QVBoxLayout, QWidget, QSpacerItem, QSizePolicy, QGroupBox
        from matplotlib.figure import Figure
        from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

        layout = QHBoxLayout()
        checkbox_layout = QVBoxLayout()

        #Add the checkboxes
        self.ActualsCheck = QCheckBox() 
        self.ActualsCheck.setText('Actuals')
        self.LECheck = QCheckBox()
        self.LECheck.setText('LE')
        self.GFOzCheck = QCheckBox()
        self.GFOzCheck.setText('GFOz')
        self.PreviousLECheck = QCheckBox()
        self.PreviousLECheck.setText('Previous LE')
        self.FirstofMonthLE = QCheckBox()
        self.FirstofMonthLE.setText('First of Month LE')

        self.checkbox_group = QGroupBox()

        checkbox_layout.addWidget(self.ActualsCheck)
        checkbox_layout.addWidget(self.LECheck)
        checkbox_layout.addWidget(self.GFOzCheck)
        checkbox_layout.addWidget(self.PreviousLECheck)
        checkbox_layout.addWidget(self.FirstofMonthLE)

        self.checkbox_group.setLayout(checkbox_layout)
        self.checkbox_group.setFlat(True)

        #Add Graph
        figure = Figure()
        self.canvas = FigureCanvas(figure)
        self.canvas.setMinimumHeight(self.height() / 1.8)
        
        layout.addWidget(self.checkbox_group)
        layout.addWidget(self.canvas)
        layout.setAlignment(QtCore.Qt.AlignCenter)

        spacer = QSpacerItem(0, self.height() / 15)
        
        total_page_layout.addSpacerItem(spacer)
        total_page_layout.addLayout(layout)
        total_page_layout = self.AdjustButtonFormat(total_page_layout)

        return total_page_layout

    def AdjustButtonFormat(self, total_page_layout):
        from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QPushButton, QSpacerItem
        from PyQt5.QtCore import Qt

        adjust_LE_layout = QHBoxLayout()
        self.adjust_le_button = QPushButton('Adjust LE', self)
        self.adjust_le_button.clicked.connect(self.on_adjust_le_button_clicked)
        self.adjust_le_button.setMinimumHeight(self.height() / 20)
        self.adjust_le_button.setMinimumWidth(self.width () / 20)

        adjust_LE_layout.addWidget(self.adjust_le_button)
        #adjust_LE_layout.addStretch(1)
        spacer = QSpacerItem(self.width() / 5, 0)
        adjust_LE_layout.addSpacerItem(spacer)
        adjust_LE_layout.setAlignment(Qt.AlignRight)

        vertical_spacer = QSpacerItem(0, self.height() / 15)
        total_page_layout.addSpacerItem(vertical_spacer)
        total_page_layout.addLayout(adjust_LE_layout)
        return total_page_layout
    
    def on_adjust_le_button_clicked(self):

        alert = QMessageBox()
        palette = self.GetPalette()
        alert.setPalette(palette)
        alert.setText('Call Control logic to go to next screen')
        alert.exec_() 

    def FormatTableArea(self, total_page_layout):
        from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QTableWidget, QTableWidgetItem, QSpacerItem, QAbstractScrollArea, QHeaderView, QGroupBox
        from PyQt5.QtCore import Qt
        
        table_layout = QVBoxLayout()
        self.SummaryTable = QTableWidget()

        headers = ['Well Name', 'Corp ID', 'Area', 'Wedge', 'Midstream', 'Weekly LE MMBOED', 'Weekly Variance', 'Monthly Forecast LE MMBOED', 'Month Variance', 
        'Annual Forecast MMBOED','Annual Variance', 'Reason', 'Comments', 'Summary Date']

        column_count = len(headers)
        self.SummaryTable.setColumnCount(column_count)        
        self.SummaryTable.setHorizontalHeaderLabels(headers)
        self.SummaryTable.setRowCount(10)
        self.SummaryTable.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.SummaryTable.setMinimumHeight(self.height() / 2.2)
        self.SummaryTable.setMinimumWidth(self.width() / 2.2)
        
        horizontal_spacer = QSpacerItem(self.width() / 8, 0)
        vertical_spacer = QSpacerItem(0, self.height() / 15)
        header = self.SummaryTable.horizontalHeader()
        for idx in range(column_count):
            header.setSectionResizeMode(idx, QHeaderView.ResizeToContents)

        horizontal_table_layout = QHBoxLayout()        
        table_layout.addWidget(self.SummaryTable)
        table_layout.setAlignment(Qt.AlignCenter)
        table_layout = self.AddTableAreaButtons(table_layout)
        table_group = QGroupBox()
        table_group.setLayout(table_layout)
        table_group.setTitle('Summary Information')

        horizontal_table_layout.addSpacerItem(QSpacerItem(self.width() / 6, 0))
        horizontal_table_layout.addWidget(table_group)
        horizontal_table_layout.setAlignment(Qt.AlignCenter)
        horizontal_table_layout.addSpacerItem(QSpacerItem(self.width() / 6, 0))
        
        total_page_layout.addSpacerItem(vertical_spacer)
        total_page_layout.addLayout(horizontal_table_layout)
        total_page_layout.addSpacerItem(vertical_spacer)

        return total_page_layout

    def AddTableAreaButtons(self, page_layout):
        from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QSpacerItem

        self.new_summary_button = QPushButton('New Summary')
        self.new_summary_button.clicked.connect(self.on_new_summary_clicked)

        self.load_summary_button = QPushButton('Load Summary')
        self.load_summary_button.clicked.connect(self.on_load_summary_clicked)

        self.save_summary_button = QPushButton('Save Summary')
        self.save_summary_button.clicked.connect(self.on_save_summary_clicked)

        self.export_summary_button = QPushButton('Export Summary')
        self.export_summary_button.clicked.connect(self.export_summary_clicked)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.new_summary_button)
        button_layout.addWidget(self.load_summary_button)
        button_layout.addSpacerItem(QSpacerItem(self.width() / 2.3, 0))
        button_layout.addWidget(self.export_summary_button)
        button_layout.addWidget(self.save_summary_button)

        page_layout.addLayout(button_layout)

        return page_layout

    def on_new_summary_clicked(self):
        alert = QMessageBox()
        palette = self.GetPalette()
        alert.setPalette(palette)
        alert.setText('Call Control logic to create a new summary and let user select which forecast to use')
        alert.exec_() 

    def on_load_summary_clicked(self):
        alert = QMessageBox()
        palette = self.GetPalette()
        alert.setPalette(palette)
        alert.setText('Call control logic to load a summary from the database')
        alert.exec_() 

    def on_save_summary_clicked(self):
        alert = QMessageBox()
        palette = self.GetPalette()
        alert.setPalette(palette)
        alert.setText('Call control logic to save the new summary to the database.')
        alert.exec_() 

    def export_summary_clicked(self):
        alert = QMessageBox()
        palette = self.GetPalette()
        alert.setPalette(palette)
        alert.setText('Call control logic to export the screen summary to an excel spreadsheet.')
        alert.exec_() 

    def FormatBottomButtonRow(self, total_page_layout):
        from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QSpacerItem
        from PyQt5.QtCore import Qt

        self.netting_values_button = QPushButton('Edit Netting Values')
        self.netting_values_button.clicked.connect(self.on_netting_values_clicked)

        self.update_button = QPushButton('Update Page')
        self.update_button.clicked.connect(self.on_update_clicked)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.netting_values_button)
        button_layout.addSpacerItem(QSpacerItem(self.width() / 2, 0))
        button_layout.addWidget(self.update_button)

        button_layout.setAlignment(Qt.AlignCenter)

        total_page_layout.addSpacerItem(QSpacerItem(0, self.height() / 15))
        total_page_layout.addLayout(button_layout)

        return total_page_layout

    def on_netting_values_clicked(self):
        alert = QMessageBox()
        palette = self.GetPalette()
        alert.setPalette(palette)
        alert.setText('Call control logic to bring up modal screen of netting values from database and allow user to edit.')
        alert.exec_() 

    def on_update_clicked(self):
        alert = QMessageBox()
        palette = self.GetPalette()
        alert.setPalette(palette)
        alert.setText('Call control logic to update screen with latest information if LE info has changed in database.')
        alert.exec_() 

    def GetPalette(self):
        from PyQt5.QtCore import Qt
        from PyQt5.QtGui import QPalette, QColor

        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(53, 53, 53))
        palette.setColor(QPalette.WindowText, Qt.white)
        palette.setColor(QPalette.Base, QColor(25, 25, 25))
        palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
        palette.setColor(QPalette.ToolTipBase, Qt.white)
        palette.setColor(QPalette.ToolTipText, Qt.white)
        palette.setColor(QPalette.Text, Qt.white)
        palette.setColor(QPalette.Button, QColor(53, 53, 53))
        palette.setColor(QPalette.ButtonText, Qt.white)
        palette.setColor(QPalette.BrightText, Qt.red)
        palette.setColor(QPalette.Link, QColor(42, 130, 218))
        palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
        palette.setColor(QPalette.HighlightedText, Qt.black)        

        return palette

    def GetScreenDimensions(self):
        import ctypes
        user32 = ctypes.windll.user32
        screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
        return screensize

app = QApplication(sys.argv)
GUI = Window(app)
GUI.show()
sys.exit(app.exec_())



