from PyQt5.QtGui import QIcon, QKeyEvent, QPalette,QKeySequence
from PyQt5.QtWidgets import QApplication,QWidget,QHBoxLayout,QPushButton,QVBoxLayout,QDialog,QLabel,QSlider,QStyle, QSizePolicy,QFileDialog,QShortcut,QMenu, QAction,QMenuBar,QLineEdit
import sys 
from PyQt5.QtMultimedia import QMediaPlayer,QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt,QUrl,QTime

class InfoDialog(QDialog):
  def __init__(self, parent=None):
    super().__init__(parent=parent)

    self.setWindowTitle("Info (shortcuts)")
    self.setGeometry(800, 400, 300, 300)

    self.layout = QVBoxLayout()
    m1 = QLabel("FullScreen     -  F / Double Click")
    m2 = QLabel("Close App      -  Ctrl + Q")
    m3 = QLabel("Open File      -  Ctrl + O")
    m4 = QLabel("Hide toggle    -  H")
    m5 = QLabel("Forward 10sec  -  →")
    m6 = QLabel("Backward 10sec -  ←")
    m7 = QLabel("Forward 1min   -  Shift + →")
    m8 = QLabel("Backward 1min  -  Shift + ←")
    m9 = QLabel("Volume UP      -  ↑")
    m10 = QLabel("Volume UP     -  ↓")
    m11 = QLabel("Mute          -  Ctrl + M")
    
    self.layout.addWidget(m1)
    self.layout.addWidget(m2)
    self.layout.addWidget(m3)
    self.layout.addWidget(m4)
    self.layout.addWidget(m5)
    self.layout.addWidget(m6)
    self.layout.addWidget(m7)
    self.layout.addWidget(m8)
    self.layout.addWidget(m9)
    self.layout.addWidget(m10)
    self.layout.addWidget(m11)
    self.setLayout(self.layout)

class Window(QWidget):
  def __init__(self, parent=None):
    super(Window, self).__init__(parent)

    self.setWindowTitle("Media Player")
    self.setGeometry(450, 200, 1000, 700)
    self.setWindowIcon(QIcon('icons/icon.png'))

    palette = self.palette()
    palette.setColor(QPalette.Window, Qt.black)
    self.setPalette(palette)

    self.ui()
    self.show() 

  def ui(self):

    # create media player object 
    self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)

    # create videowidget object
    self.videowidget = QVideoWidget()

    # create open button
    self.openbtn = QPushButton('Open Video', self)  
    self.openbtn.setFocusPolicy(Qt.NoFocus)
    self.openbtn.setIcon(QIcon('icons/open.png'))
    self.openbtn.setFixedHeight(25);
    self.openbtn.setMaximumWidth(100);
    self.openbtn.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Minimum)
    self.openbtn.setStyleSheet('background-color : black ; color : white')
    self.openbtn.clicked.connect(self.open_file)

    # media Menu

    self.mediabtn = QMenuBar()
    actionFile = self.mediabtn.addMenu(QIcon('icons/media.png'),'Media')
    self.mediabtn.setStyleSheet('background-color : black; color : white')
    
    actionFile.addSeparator()

    PlaybackMenu = QMenu('Playback', self)
    Forward10 = QAction(QIcon('icons/forward.png'),'Forward 10sec', self)
    PlaybackMenu.addAction(Forward10)
    Forward10.triggered.connect(self.forwardSlider)
    Forward1 = QAction(QIcon('icons/forward.png'),'Forward 1min', self)
    PlaybackMenu.addAction(Forward1)
    Forward1.triggered.connect(self.forwardSlider10)    
    Backward10 = QAction(QIcon('icons/backward.png'),'Backward 10sec', self)
    PlaybackMenu.addAction(Backward10)
    Backward10.triggered.connect(self.backSlider)
    Backward1 = QAction(QIcon('icons/backward.png'),'Backward 1min', self)
    PlaybackMenu.addAction(Backward1)
    Backward1.triggered.connect(self.backSlider10)

    VolumeIncrease = QAction(QIcon('icons/max.png'),'Volume Increase', self)
    actionFile.addAction(VolumeIncrease)
    VolumeIncrease.triggered.connect(self.volumeUp)
    VolumeDecrease = QAction(QIcon('icons/min.png'),'Volume Decrease', self)
    actionFile.addAction(VolumeDecrease)
    VolumeDecrease.triggered.connect(self.volumeDown)
    VolumeMute = QAction(QIcon('icons/mute.png'),'Volume Mute', self)
    actionFile.addAction(VolumeMute)
    VolumeMute.triggered.connect(self.volumeMute)

    self.Play = QAction(QIcon('icons/play.png'),'Play/Pause', self)
    actionFile.addAction(self.Play)
    self.Play.triggered.connect(self.play_video)

    actionFile.addMenu(PlaybackMenu)
    PlaybackMenu.setStyleSheet('background-color : black; color : white')
    
    self.mediabtn.setFixedHeight(25)
    self.mediabtn.setMaximumWidth(200)
    self.mediabtn.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Minimum)

    # Display menu                                                         

    self.displaybtn = QMenuBar()
    actionFile = self.displaybtn.addMenu(QIcon('icons/display.png'),'Setting')
    self.displaybtn.setStyleSheet('background-color : black; color : white')
    full = QAction('Full Screen', self)
    full.triggered.connect(self.handleFullscreen)
    actionFile.addAction(full)
    actionFile.addSeparator()

    AspectMenu = QMenu('Aspect Ratio', self)
    Aspect169 = QAction('16:9', self)
    AspectMenu.addAction(Aspect169)
    Aspect169.triggered.connect(self.screen169)
    Aspect43 = QAction('4:3', self)
    AspectMenu.addAction(Aspect43)
    Aspect43.triggered.connect(self.screen43)

    actionFile.addMenu(AspectMenu)
    AspectMenu.setStyleSheet('background-color : black; color : white')
    
    self.displaybtn.setFixedHeight(25)
    self.displaybtn.setMaximumWidth(200)
    self.displaybtn.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Minimum)

    #settings menu
    
    self.settingbtn = QMenuBar()
    actionFile = self.settingbtn.addMenu(QIcon('icons/settings.png'),'Setting')
    self.settingbtn.setStyleSheet('background-color : black; color : white')
    exit = QAction(QIcon('icons/exit.png'), 'Exit', self)
    exit.setShortcut('Ctrl+Q')
    exit.triggered.connect(app.quit)
    actionFile.addAction(exit) 
    actionFile.addSeparator()
    info = QAction(QIcon('icons/info.png'), 'Info', self)
    info.setShortcut('F12')
    info.triggered.connect(self.open_info_dialog)
    actionFile.addAction(info)
    
    self.settingbtn.setFixedHeight(25)
    self.settingbtn.setMaximumWidth(200)
    self.settingbtn.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Minimum)
    
    # create button for playing
    self.playbtn = QPushButton()
    self.playbtn.setEnabled(False)
    self.playbtn.setStyleSheet('background-color : black')
    self.playbtn.setIcon(QIcon('icons/play.png'))
    self.playbtn.clicked.connect(self.play_video)
    
    # create button for backward 
    self.bbtn = QPushButton()
    self.bbtn.setEnabled(False)
    self.bbtn.setStyleSheet('background-color : black')
    self.bbtn.setIcon(QIcon('icons/backward.png'))
    self.bbtn.clicked.connect(self.backSlider)
    
    # create stop button
    self.stopbtn = QPushButton()
    self.stopbtn.setStyleSheet('background-color : black')
    self.stopbtn.setIcon(QIcon('icons/stop.png'))
    self.stopbtn.clicked.connect(self.stop_video) 

    # create button for forward 
    self.fbtn = QPushButton()
    self.fbtn.setEnabled(False)
    self.fbtn.setStyleSheet('background-color : black')
    self.fbtn.setIcon(QIcon('icons/forward.png'))
    self.fbtn.clicked.connect(self.forwardSlider)
    

    self.lbl = QLineEdit('00:00:00')
    self.lbl.setReadOnly(True)
    self.lbl.setFixedWidth(70)
    self.lbl.setUpdatesEnabled(True)
    self.lbl.setStyleSheet('background-color : black; color : white; border : none')
    self.lbl.selectionChanged.connect(lambda: self.lbl.setSelection(0, 0))


    #create content slider
    self.slider = QSlider(Qt.Horizontal)
    self.slider.setFocusPolicy(Qt.NoFocus)
    self.slider.setRange(0,0)
    self.slider.sliderMoved.connect(self.set_position)
    self.slider.setStyleSheet (self.stylesheet())

    self.elbl = QLineEdit('00:00:00')
    self.elbl.setReadOnly(True)
    self.elbl.setFixedWidth(70)
    self.elbl.setUpdatesEnabled(True)
    self.elbl.setStyleSheet('background-color : black; color : white; border : none')
    self.elbl.selectionChanged.connect(lambda: self.elbl.setSelection(0, 0))
    
    #create vol label
    self.vlabel = QPushButton(self)
    self.vlabel.setIcon(QIcon('icons/mute.png'))
    self.vlabel.setStyleSheet('background-color : black')
    self.vlabel.clicked.connect(self.volumeMute)

    #create volume slider\
    self.sld = QSlider(Qt.Horizontal, self)
    self.sld.setFocusPolicy(Qt.NoFocus)
    self.sld.setRange(0,100)
    self.sld.valueChanged.connect(self.changeValue)
    self.sld.sliderMoved.connect(self.set_volume)
    self.sld.setMaximumWidth(100);
    self.sld.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
    self.sld.setStyleSheet (self.stylesheet())
        
    # fullscreen toggle
    self.screenbtn = QPushButton()
    self.screenbtn.setEnabled(True)
    self.screenbtn.setStyleSheet('background-color : black')
    self.screenbtn.setIcon(QIcon('icons/full-screen.png'))
    self.screenbtn.clicked.connect(self.handleFullscreen)
  

    #create label
    self.label = QLabel()
    self.label.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)
    
    # topbox
    tboxLayout=QHBoxLayout()
    tboxLayout.setAlignment(Qt.AlignLeft)
    tboxLayout.addWidget(self.openbtn)
    tboxLayout.addWidget(self.mediabtn)
    tboxLayout.addWidget(self.displaybtn)
    tboxLayout.addWidget(self.settingbtn)
   
    # create hbox layout
    hboxLayout = QHBoxLayout()

    # set widgets to the hbox layout
    hboxLayout.addWidget(self.playbtn)
    hboxLayout.addWidget(self.bbtn)
    hboxLayout.addWidget(self.stopbtn)
    hboxLayout.addWidget(self.fbtn)
    hboxLayout.addWidget(self.lbl)
    hboxLayout.addWidget(self.slider)
    hboxLayout.addWidget(self.elbl)
    hboxLayout.addWidget(self.vlabel)
    hboxLayout.addWidget(self.sld)
    hboxLayout.addWidget(self.screenbtn) 
  
    #create vbox layout
    vboxlayout = QVBoxLayout()
    vboxlayout.addLayout(tboxLayout)
    vboxlayout.addWidget(self.videowidget)
    vboxlayout.addLayout(hboxLayout)
    vboxlayout.addWidget(self.label)
    self.setLayout (vboxlayout)
    self.mediaPlayer.setVideoOutput(self.videowidget)

    # media player signals
    self.mediaPlayer.stateChanged.connect(self.mediastate_changed)
    self.mediaPlayer.positionChanged.connect(self.position_changed)
    self.mediaPlayer.durationChanged.connect(self.duration_changed) 
    self.videowidget = True
      
    #shortcuts
    self.openbtnshortcut = QShortcut(QKeySequence('Ctrl+O'), self)
    self.openbtnshortcut.activated.connect(self.open_file)
    self.Hideshortcut = QShortcut(QKeySequence('H'), self)
    self.Hideshortcut.activated.connect(self.toggleSlider)
    self.VolumeIncreaseshortcut = QShortcut(QKeySequence(Qt.Key_Up), self)
    self.VolumeIncreaseshortcut.activated.connect(self.volumeUp)
    self.VolumeDecreaseshortcut = QShortcut(QKeySequence(Qt.Key_Down), self)
    self.VolumeDecreaseshortcut.activated.connect(self.volumeDown)
    self.VolumeMuteshortcut = QShortcut(QKeySequence('Ctrl+M'), self)
    self.VolumeMuteshortcut.activated.connect(self.volumeMute)
    self.Forward10shortcut = QShortcut(QKeySequence(Qt.Key_Right), self)
    self.Forward10shortcut.activated.connect(self.forwardSlider)
    self.Backward10shortcut = QShortcut(QKeySequence(Qt.Key_Left), self)
    self.Backward10shortcut.activated.connect(self.backSlider)
    self.Forward1shortcut = QShortcut(QKeySequence(Qt.ShiftModifier +  Qt.Key_Right) , self)
    self.Forward1shortcut.activated.connect(self.forwardSlider10)
    self.Backward1shortcut = QShortcut(QKeySequence(Qt.ShiftModifier +  Qt.Key_Left) , self)
    self.Backward1shortcut.activated.connect(self.backSlider10)
    self.fullshortcut = QShortcut(QKeySequence('F'), self)
    self.fullshortcut.activated.connect(self.handleFullscreen)
    self.Playshortcut = QShortcut(QKeySequence('Space'), self)
    self.Playshortcut.activated.connect(self.play_video)
    

  # function section   

  def stop_video(self):
    if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
      self.mediaPlayer.stop() 
  
  def open_info_dialog(self):

    info = InfoDialog()
    info.exec_()
  
  def mouseDoubleClickEvent(self, event):
    self.handleFullscreen()

  def open_file(self):
    filename, _ =QFileDialog.getOpenFileName(self, "Open Good Files ") 

    if filename != '':   
      self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(filename)))
      self.playbtn.setEnabled(True)
      self.fbtn.setEnabled(True)
      self.bbtn.setEnabled(True)
      self.mediaPlayer.play()

  def play_video(self):
    if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
      self.mediaPlayer.pause()
    else:
      self.mediaPlayer.play()

  def mediastate_changed(self,state):
    if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
      self.playbtn.setIcon(
        QIcon('icons/pause.png')
      )
      self.Play.setIcon(
        QIcon('icons/pause.png')
      )
    else:
      self.playbtn.setIcon(
        QIcon('icons/play.png')
      )
      self.Play.setIcon(
        QIcon('icons/play.png')
      )

  def position_changed(self, position):
    self.slider.setValue(position)
    mtime = QTime(0,0,0,0)
    mtime = mtime.addMSecs(self.mediaPlayer.position())
    self.lbl.setText(mtime.toString())

  def duration_changed(self, duration):
    self.slider.setRange(0, duration)
    mtime = QTime(0,0,0,0)
    mtime = mtime.addMSecs(self.mediaPlayer.duration())
    self.elbl.setText(mtime.toString())


  def set_position(self, position):
    self.mediaPlayer.setPosition(position)
  
  def handle_errors(self):
    self.playbtn.setEnabled(False)
    self.label.setText("Error: " + self.mediaPlayer.errorString())

  def set_volume(self, position):
    self.mediaPlayer.setVolume(position)
    
  def changeValue(self, value):
    if self.mediaPlayer.isMuted():
      self.vlabel.setIcon(QIcon('icons/mute.png'))
    else:
      self.volume = value
      if self.volume == 0:
        self.vlabel.setIcon(QIcon('icons/mute.png'))
      elif 0 < self.volume <= 30:
        self.vlabel.setIcon(QIcon('icons/min.png'))
      elif 30 < self.volume < 80:
        self.vlabel.setIcon(QIcon('icons/med.png'))
      else:
        self.vlabel.setIcon(QIcon('icons/max.png'))

  def volumeMute(self):
    vol=self.mediaPlayer.volume()
    if self.mediaPlayer.isMuted():
      self.mediaPlayer.setMuted(False)
      self.sld.setSliderPosition(int(self.mediaPlayer.volume()))
      self.volume = vol
      if self.volume == 0:
        self.vlabel.setIcon(QIcon('icons/mute.png'))
      elif 0 < self.volume <= 30:
        self.vlabel.setIcon(QIcon('icons/min.png'))
      elif 30 < self.volume < 80:
        self.vlabel.setIcon(QIcon('icons/med.png'))
      else:
        self.vlabel.setIcon(QIcon('icons/max.png'))
    else:
      self.mediaPlayer.setMuted(True)
      self.vlabel.setIcon(QIcon('icons/mute.png'))

  def volumeUp(self):
    self.mediaPlayer.setVolume(self.mediaPlayer.volume() + 10)
    self.sld.setSliderPosition(int(self.mediaPlayer.volume()))
    print("Volume: " + str(self.mediaPlayer.volume()))
    
  def volumeDown(self):
    self.mediaPlayer.setVolume(self.mediaPlayer.volume() - 10)
    self.sld.setSliderPosition(int(self.mediaPlayer.volume()))  
    print("Volume: " + str(self.mediaPlayer.volume()))

  def forwardSlider(self):
    if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
      self.mediaPlayer.setPosition(self.mediaPlayer.position() + 1000*10)

  def forwardSlider10(self):
    if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
      self.mediaPlayer.setPosition(self.mediaPlayer.position() + 1000*60)

  def backSlider(self):
    if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
      self.mediaPlayer.setPosition(self.mediaPlayer.position() - 1000*10)

  def backSlider10(self):
    if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
      self.mediaPlayer.setPosition(self.mediaPlayer.position() - 1000*60)
  
  # full screen on double click & button
  def handleFullscreen(self):
    if self.windowState() & Qt.WindowFullScreen:
      QApplication.setOverrideCursor(Qt.ArrowCursor)
      self.screenbtn.setIcon(QIcon('icons/full-screen.png'))
      self.showNormal()
      print("no Fullscreen")
    else:
      self.showFullScreen()
      QApplication.setOverrideCursor(Qt.ArrowCursor)
      self.screenbtn.setIcon(QIcon('icons/full-screen-exit.png'))
      print("Fullscreen entered")

  def screen169(self):
    self.videowidget = True
    mwidth = self.frameGeometry().width()
    mheight = self.frameGeometry().height()
    mleft = self.frameGeometry().left()
    mtop = self.frameGeometry().top()
    mratio = 1.778
    self.setGeometry(mleft, mtop, mwidth, round(mwidth / mratio))

  def screen43(self):
    self.videowidget = False
    mwidth = self.frameGeometry().width()
    mheight = self.frameGeometry().height()
    mleft = self.frameGeometry().left()
    mtop = self.frameGeometry().top()
    mratio = 1.33
    self.setGeometry(mleft, mtop, mwidth, round(mwidth / mratio))

  def toggleSlider(self):    
    if self.slider.isVisible():
      self.hideSlider()
    else:
      self.showSlider()
    
  def hideSlider(self):
    self.openbtn.hide()
    self.mediabtn.hide()
    self.displaybtn.hide()
    self.settingbtn.hide()
    self.playbtn.hide()
    self.bbtn.hide()
    self.stopbtn.hide()
    self.fbtn.hide()
    self.lbl.hide()
    self.slider.hide()
    self.elbl.hide()
    self.vlabel.hide()  
    self.sld.hide()
    self.screenbtn.hide()
         
    self.label.hide()  
  
  def showSlider(self):
    self.openbtn.show()
    self.mediabtn.show()
    self.displaybtn.show()
    self.settingbtn.show()
    self.playbtn.show()
    self.bbtn.show()
    self.stopbtn.show()
    self.fbtn.show()
    self.lbl.show()
    self.slider.show()
    self.elbl.show()
    self.vlabel.show()
    self.sld.show()
    self.screenbtn.show()
    
    self.label.show()
     
  
  def stylesheet(self):
    return """
            QSlider::handle:horizontal 
            {
            background: transparent;
            width: 8px;
            }

            QSlider::groove:horizontal {
            border: 1px solid #444444;
            height: 8px;
              background: qlineargradient(y1: 0, y2: 1,
                            stop: 0 #2e3436, stop: 1.0 #000000);
            }

            QSlider::sub-page:horizontal {
            background: qlineargradient( y1: 0, y2: 1,
                stop: 0 #729fcf, stop: 1 #2a82da);
            border: 1px solid #777;
            height: 8px;
            }

            QSlider::handle:horizontal:hover {
            background: #2a82da;
            height: 8px;
            width: 18px;
            border: 1px solid #2e3436;
            }

            QSlider::sub-page:horizontal:disabled {
            background: #bbbbbb;
            border-color: #999999;
            }

            QSlider::add-page:horizontal:disabled {
            background: #2a82da;
            border-color: #999999;
            }

            QSlider::handle:horizontal:disabled {
            background: #2a82da;
            }

            QLineEdit
            {
            background: black;
            color: #585858;
            border: 0px solid #076100;
            font-size: 8pt;
            font-weight: bold;
            }
            QAction QIcon{
              size:15px;
            }
          """

app = QApplication(sys.argv)
window = Window()
sys.exit(app.exec_())