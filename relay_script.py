import yaml, logging, os, sys
from PyQt5.QtWidgets import QPushButton, QApplication, QMainWindow, \
                            QLabel, QAction, QColorDialog, QFontDialog
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QPixmap, QPalette, QColor
from PyQt5.QtCore import Qt


logging.basicConfig(level=logging.DEBUG,
                    format='%(message)s',
                    handlers=[logging.StreamHandler()])

THIS_FILEPATH = os.path.realpath(os.path.dirname(sys.argv[0]))


CSS_STANDARD = '''
                    Slider::handle:vertical{

                        height: 50px;
                        min-width: 50px;
                        image:url('%s');
                    }
                    Slider::groove:vertical{
                        width: 50px;
                        border: %s;
                    }
                    
    
                '''


CSS_OFFSCREEN_UP = '''
                        Slider::handle:vertical{
                            height: 50px;
                            min-width: 50px;
                            image:url('assets/scroll_icon_up.gif');
                        }
                    Slider::groove:vertical{
                        width: 50px;
                        border: %s;
                    }
                        
        
                    '''
                    

CSS_OFFSCREEN_DOWN = '''
                        Slider::handle:vertical{
                            height: 50px;
                            min-width: 50px;
                            image:url('assets/scroll_icon_down.gif');
                        }
                    Slider::groove:vertical{
                        width: 50px;
                        border: %s;
                    }
                        
        
                    '''

class Slider(QtWidgets.QSlider):
    absolute_position = 1
    slider_number = '0'
    team_icon = ''
    border_color = '2px solid rgb(205,30,30,255)'
    current_css = 'css_standard'
    def mousePressEvent(self, event):
        
        super(Slider, self).mousePressEvent(event)
        if event.button() == QtCore.Qt.LeftButton:
            val = self.pixelPosToRangeValue(event.pos())
            
            
            self.absolute_position = val + (self.parent().mainapp.current_view_limit - self.parent().mainapp.config['segments_view'])
            # print("Value: %s : Abs pos: %s " % ((val, self.absolute_position)))
            self.setValue(val)


            
            if self.absolute_position != self.parent().mainapp.config['segments']:
                flag = getattr(self.parent().mainapp, "flag%s" % self.slider_number)
                flag.setHidden(True)
            else:
                flag = getattr(self.parent().mainapp, "flag%s" % self.slider_number)
                flag.setHidden(False)
            
            self.parent().mainapp.assign_segments_and_sliders()
            self.parent().setFocus()
            
    def pixelPosToRangeValue(self, pos):
        opt = QtWidgets.QStyleOptionSlider()
        self.initStyleOption(opt)
        gr = self.style().subControlRect(QtWidgets.QStyle.CC_Slider, opt, QtWidgets.QStyle.SC_SliderGroove, self)
        sr = self.style().subControlRect(QtWidgets.QStyle.CC_Slider, opt, QtWidgets.QStyle.SC_SliderHandle, self)

        if self.orientation() == QtCore.Qt.Horizontal:
            sliderLength = sr.width()
            sliderMin = gr.x()
            sliderMax = gr.right() - sliderLength + 1
        else:
            sliderLength = sr.height()
            sliderMin = gr.y()
            sliderMax = gr.bottom() - sliderLength + 1;
        pr = pos - sr.center() + sr.topLeft()
        p = pr.x() if self.orientation() == QtCore.Qt.Horizontal else pr.y()
        return QtWidgets.QStyle.sliderValueFromPosition(self.minimum(), self.maximum(), p - sliderMin,
                                               sliderMax - sliderMin, opt.upsideDown)
    def wheelEvent(self,event):
        pass
    def keyPressEvent(self, event):
        key = event.key()
        if key == QtCore.Qt.Key_PageUp or key == QtCore.Qt.Key_PageDown: 
            pass


class SettingsWindow(QMainWindow):
    def __init__(self, mainwindow, app, parent = None):
        super(QMainWindow, self).__init__(parent)
        self.mainwindow = mainwindow
        self.app = app
        self.setFixedSize(300,160)
        self.setWindowTitle('Settings')
        self.icon = QtGui.QIcon()
        self.icon.addPixmap(QtGui.QPixmap(os.path.join(THIS_FILEPATH,"ico.ico")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.setWindowIcon(self.icon)
        
        self.color_chroma = QPushButton("Set chroma color",self)
        self.color_chroma.setGeometry(QtCore.QRect(5, 5,290, 30))
        self.color_chroma.clicked.connect(self.select_chroma)        
        
        self.color_text = QPushButton("Set text color",self)
        self.color_text.setGeometry(QtCore.QRect(5, 35,290, 30))
        self.color_text.clicked.connect(self.select_text_color)
        
        self.slider_border_text = QPushButton("Set slider border color",self)
        self.slider_border_text.setGeometry(QtCore.QRect(5, 65,290, 30))
        self.slider_border_text.clicked.connect(self.select_slider_border_color)
        
        self.font_text = QPushButton("Set text font",self)
        self.font_text.setGeometry(QtCore.QRect(5, 95,290, 30))
        self.font_text.clicked.connect(self.select_font)
        
        self.font_text = QPushButton("Toggle scroll buttons",self)
        self.font_text.setGeometry(QtCore.QRect(5, 125,290, 30))
        self.font_text.clicked.connect(self.toggle_hidden_buttons)
        
        
        
    def select_chroma(self):
        color = QColorDialog.getColor()
        self.mainwindow.mainapp.palette_custom.setColor(QPalette.Window, color)
        self.mainwindow.mainapp.app.setPalette(self.mainwindow.mainapp.palette_custom)
        
    def select_text_color(self):
        color = QColorDialog.getColor()
        self.mainwindow.mainapp.palette_custom.setColor(QPalette.WindowText, color)
        self.mainwindow.mainapp.palette_custom.setColor(QPalette.Text, color)
        self.mainwindow.mainapp.app.setPalette(self.mainwindow.mainapp.palette_custom)
        for segment in self.mainwindow.mainapp.all_segments:
            segment.setStyleSheet(segment.styleSheet())
    def select_slider_border_color(self):
        color = QColorDialog.getColor()
        for slider in self.mainwindow.mainapp.all_sliders:
            slider.border_color = "2px solid rgb%s" % str(color.getRgb())
            if slider.current_css == 'css_offscreen_up':
                
                slider.setStyleSheet(CSS_OFFSCREEN_UP % slider.border_color)
            if slider.current_css == 'css_offscreen_down':
                slider.setStyleSheet(CSS_OFFSCREEN_DOWN % slider.border_color)
            if slider.current_css == 'css_standard':
                slider.setStyleSheet(CSS_STANDARD % (slider.team_icon, slider.border_color))
        

    def select_font(self):
        
        font = QFontDialog.getFont()
        if font[1]:
            for segment in self.mainwindow.mainapp.all_segments:
                segment.setFont(font[0])
                segment.setStyleSheet(segment.styleSheet())
            for team_name in self.mainwindow.mainapp.all_team_names:
                team_name.setFont(font[0])
                team_name.setStyleSheet(segment.styleSheet())

    def toggle_hidden_buttons(self):
        if self.mainwindow.mainapp.segments_scroll_up.isVisible():
            self.mainwindow.mainapp.segments_scroll_up.hide()
            self.mainwindow.mainapp.segments_scroll_down.hide()
        else:
            self.mainwindow.mainapp.segments_scroll_up.show()
            self.mainwindow.mainapp.segments_scroll_down.show()
        
class MainWindow(QMainWindow):
    def __init__(self, mainapp, app, parent = None):
        super(QMainWindow, self).__init__(parent)
        self.app = app
        self.mainapp = mainapp
        self._createContextMenu()
        self.settings = SettingsWindow(self, self.app)
    w = None
    def closeEvent(self, event):
        if self.w:
            self.w.close()

        self.app.closeAllWindows()
    def wheelEvent(self,event):
        if event.angleDelta().y() > 0:
            self.mainapp.scroll_up_segments()
        if event.angleDelta().y() < 0:
            self.mainapp.scroll_down_segments()
    def _connectActions(self):
        # Connect File actions

        self.settings_action.triggered.connect(self.call_settings)
    def _createContextMenu(self):
        # Setting contextMenuPolicy
        self.setContextMenuPolicy(Qt.ActionsContextMenu)
        # Populating the widget with actions
        self.settings_action = QAction(self)
        self.settings_action.setText("Settings")
        self.addAction(self.settings_action)
        
        
    def call_settings(self):
        self.settings.show()
        
        
        
class MainApp(object):
    SCREEN_HEIGHT = 360
    SCREEN_WIDTH = 480
    SEGMENTS_VIEW_MIN = 6
    
    current_view_limit = 0
    
    def __init__(self):
        
        with open('config.yml', 'r') as f:
            self.config = yaml.safe_load(f)
        
        try:
            self.config['teams'] = max(len(self.config['team_names']), 4)
            self.config['segments'] = len(self.config['segment_names'])
            self.config['segments_view'] = min(self.config['segments'], self.SEGMENTS_VIEW_MIN)
            self.current_view_limit = self.config['segments_view']
            try:
                self.background_color = QColor(self.config['background_color'])
            except:
                self.background_color = QColor("#000000")
            try:
                self.font_color = QColor(self.config['font_color'])
            except:
                self.font_color = QColor("#ffffff")
            try:
                self.slider_border_color = QColor(self.config['slider_border_color'])
            except:
                self.slider_border_color = QColor("#cd1e1e")
            self.all_segments = []
            self.all_sliders = []
            self.all_team_names = []
            
        except:
            print("Error on converting teams/segments from config to integer. Check config.yml")
        
        self.app = QApplication([])
        self.window = MainWindow(self, self.app)
        self.window.setFixedSize(self.SCREEN_WIDTH,self.SCREEN_HEIGHT)
        self.window.setWindowTitle('Race/Relay Tracker')
        self.icon = QtGui.QIcon()
        self.icon.addPixmap(QtGui.QPixmap(os.path.join(THIS_FILEPATH,"ico.ico")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.window.setWindowIcon(self.icon)
        

        
        
        
        self.segments_scroll_up = QPushButton("",self.window)
        self.segments_scroll_up.setGeometry(QtCore.QRect(5, self.SCREEN_HEIGHT - 20, 40, 15))
        self.segments_scroll_up.clicked.connect(self.scroll_up_segments)
        icon  = QtGui.QIcon(os.path.join(THIS_FILEPATH,'assets','arrow_button_up.png'))
        self.segments_scroll_up.setIcon(icon)
        self.segments_scroll_up.hide()
        
        self.segments_scroll_down = QPushButton("",self.window)
        self.segments_scroll_down.setGeometry(QtCore.QRect(45, self.SCREEN_HEIGHT - 20, 40, 15))
        self.segments_scroll_down.clicked.connect(self.scroll_down_segments)
        icon  = QtGui.QIcon(os.path.join(THIS_FILEPATH,'assets','arrow_button_down.png'))
        self.segments_scroll_down.setIcon(icon)
        self.segments_scroll_down.hide()
        

        # Final settings
        self.app.setStyle('Fusion')
        try:
            self.app.setFont(QtGui.QFont(self.config['font'], 14))
        except:
            self.app.setFont(QtGui.QFont("Roboto", 14))
        
        palette = QPalette()
        palette.setColor(QPalette.Window, self.background_color)
        palette.setColor(QPalette.WindowText, self.font_color)
        palette.setColor(QPalette.Base, QColor(25, 25, 25))
        palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
        palette.setColor(QPalette.ToolTipBase, QColor(255, 255, 255))
        palette.setColor(QPalette.ToolTipText, QColor(255, 255, 255))
        palette.setColor(QPalette.Text, self.font_color)
        palette.setColor(QPalette.Button, QColor(53, 53, 53))
        palette.setColor(QPalette.ButtonText, QColor(255, 255, 255))
        palette.setColor(QPalette.BrightText, QColor(120, 120, 0))
        palette.setColor(QPalette.Link, QColor(42, 130, 218))
        palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
        palette.setColor(QPalette.HighlightedText, QColor(0, 0, 0))
        self.palette_custom = palette
        self.app.setPalette(self.palette_custom)

        for i in range(self.config['teams']):
            # print("Adding slider %s" % (i + 1))
            
            setattr(self, "slider%s" % str(i + 1), Slider(self.window))
            slider = getattr(self, "slider%s" % str(i + 1))
            slider.slider_number = str(i + 1)
            slider.team_icon = "%s/%s" % ('assets',self.config['team_icons'][i])
            slider.setGeometry(QtCore.QRect(70 + (i * 90), 30, 150, self.SCREEN_HEIGHT - 90))
            slider.valueChanged[int].connect(self.changeValue)
            slider.setTickInterval(0.25)
            slider.setRange(1, self.config['segments_view'])
            slider.setValue(0)

    
            slider.border_color = "2px solid rgb%s" % str(self.slider_border_color.getRgb())
            slider.setStyleSheet(CSS_STANDARD % (slider.team_icon, slider.border_color))
            
            
                
            self.all_sliders.append(slider)
            
            setattr(self, "flag%s" % str(i + 1), QLabel("",self.window))
            flag = getattr(self, "flag%s" % str(i + 1))
            flag.setGeometry(QtCore.QRect(180 + (i * 90), 30, 150, 60))
            flag.setHidden(True)
            flag_pixmap = QPixmap(os.path.join(THIS_FILEPATH,'assets','flag.png'))
            flag.setPixmap(flag_pixmap.scaled(25, 25, QtCore.Qt.KeepAspectRatio))
        


            setattr(self, "team_name%s" % str(i + 1), QLabel(self.config['team_names'][i],self.window))
            team_name = getattr(self, "team_name%s" % str(i + 1))
            team_name.setGeometry(QtCore.QRect(96 + (i * 90), 300, 100, 60))
            # team_name.setStyleSheet("border: 2px solid white;")
            team_name.setAlignment(Qt.AlignCenter)
            self.all_team_names.append(team_name)
            

            






        YSTART = 20
        YEND = self.SCREEN_HEIGHT - 90
        MARGIN_ICON = 16

        self.slider_length = self.SCREEN_HEIGHT - ( YSTART ) - (self.SCREEN_HEIGHT - YEND)

        for i in range(self.config['segments_view']):
            segment_name = self.config['segment_names'][self.config['segments_view'] - 1 - i]
            slider_y = int(round((self.slider_length - MARGIN_ICON * 2)* ((i) / (self.config['segments_view'] - 1) )))
            
            setattr(self, "segment%s" % str(i + 1), QLabel(segment_name, self.window))
            segment = getattr(self, "segment%s" % str(i + 1))
            segment.setGeometry(QtCore.QRect(2, 40 + slider_y, 100, 45))
            # segment.setStyleSheet("border:2px solid rgb(255, 255, 255); ")
            segment.setStyleSheet("padding:2px;")
            segment.setAlignment(QtCore.Qt.AlignTop)       
            self.all_segments.append(segment)


        self.window._connectActions()

    def scroll_up_segments(self):
        self.current_view_limit += 1
        self.current_view_limit = min(self.current_view_limit, self.config['segments'])
        self.assign_segments_and_sliders()
    def scroll_down_segments(self):
        self.current_view_limit -= 1
        self.current_view_limit = max(self.current_view_limit, self.config['segments_view'])
        self.assign_segments_and_sliders()


    def assign_segments_and_sliders(self):

        current_segments_idx = [i + 1 for i in range(self.current_view_limit - min(self.config['segments'],  self.SEGMENTS_VIEW_MIN), self.current_view_limit)]
        current_segments_idx = current_segments_idx[::-1]
        for i in range(self.config['segments_view']):
            segment = getattr(self, "segment%s" % str(i + 1))

            # print(self.config['segments'] - i)
            segment.setText(self.config['segment_names'][current_segments_idx[i]-1])
            
            
        for i in range(self.config['teams']):
            slider = getattr(self, "slider%s" % str(i + 1)) 
            new_pos = slider.absolute_position - (self.current_view_limit - self.config['segments_view'])
            # print("Set slider%s to %s" % (str(i + 1),new_pos))
            slider.setValue(new_pos)
            

            
            if slider.absolute_position > self.current_view_limit:
                slider.setStyleSheet(CSS_OFFSCREEN_UP % slider.border_color)
                slider.current_css = 'css_offscreen_up'
            elif new_pos <= 0:
                slider.setStyleSheet(CSS_OFFSCREEN_DOWN % slider.border_color)
                slider.current_css = 'css_offscreen_down'
            else:
                slider.setStyleSheet(CSS_STANDARD % (slider.team_icon, slider.border_color))
                slider.current_css = 'css_standard'
        
        pass
    def changeValue(self, value):
        # print(value)
        pass

if __name__ == '__main__':
    main_window = MainApp()
    main_window.window.show()
    main_window.app.exec_()