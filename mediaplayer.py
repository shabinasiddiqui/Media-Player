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
    Forward10 = QAction('Forward 10sec', self)
    PlaybackMenu.addAction(Forward10)
    Forward10.triggered.connect(self.forwardSlider)
    Forward1 = QAction('Forward 1min', self)
    PlaybackMenu.addAction(Forward1)
    Forward1.triggered.connect(self.forwardSlider10)    
    Backward10 = QAction('Backward 10sec', self)
    PlaybackMenu.addAction(Backward10)
    Backward10.triggered.connect(self.backSlider)
    Backward1 = QAction('Backward 1min', self)
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

    while self.mediabtn.is_pressed():
      if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
        Play = QAction(QIcon('icons/pause.png'),'Pause', self)
        actionFile.addAction(Play)
        Play.triggered.connect(self.play_video)
      else:
        Pause = QAction(QIcon('icons/play.png'),'Play', self)
        actionFile.addAction(Pause)
        Pause.triggered.connect(self.play_video)

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

    #create settings button dropdown
    
    self.settingbtn = QMenuBar()
    actionFile = self.settingbtn.addMenu(QIcon('icons/settings.png'),'Setting')
    self.settingbtn.setStyleSheet('background-color : black; color : white')
    actionFile.addAction("New")
    actionFile.addSeparator()
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

    # create button for forward 
    self.fbtn = QPushButton()
    self.fbtn.setStyleSheet('background-color : black')
    self.fbtn.setIcon(QIcon('icons/forward.png'))
    self.fbtn.clicked.connect(self.forwardSlider)

    # create button for backward 
    self.bbtn = QPushButton()
    self.bbtn.setStyleSheet('background-color : black')
    self.bbtn.setIcon(QIcon('icons/backward.png'))
    self.bbtn.clicked.connect(self.backSlider)


    #create content slider
    self.slider = QSlider(Qt.Horizontal)
    self.slider.setFocusPolicy(Qt.NoFocus)
    self.slider.setRange(0,0)
    self.slider.sliderMoved.connect(self.set_position)

    self.lbl = QLineEdit('00:00:00')
    
    self.lbl.setReadOnly(True)
    self.lbl.setFixedWidth(70)
    self.lbl.setUpdatesEnabled(True)
    self.lbl.setStyleSheet('background-color : black; color : white; border : none')
    self.lbl.selectionChanged.connect(lambda: self.lbl.setSelection(0, 0))
    
    self.elbl = QLineEdit('00:00:00')
  
    self.elbl.setReadOnly(True)
    self.elbl.setFixedWidth(70)
    self.elbl.setUpdatesEnabled(True)
    self.elbl.setStyleSheet('background-color : black; color : white; border : none')
    self.elbl.selectionChanged.connect(lambda: self.elbl.setSelection(0, 0))

    #create volume slider
    
    self.sld = QSlider(Qt.Horizontal, self)
    self.sld.setFocusPolicy(Qt.NoFocus)
    self.sld.setRange(0,100)
    self.sld.valueChanged.connect(self.changeValue)
    self.sld.sliderMoved.connect(self.set_volume)
    self.sld.setMaximumWidth(100);
    self.sld.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        
    # fullscreen toggle
    self.screenbtn = QPushButton()
    self.screenbtn.setEnabled(True)
    self.screenbtn.setStyleSheet('background-color : black')
    self.screenbtn.setIcon(QIcon('icons/full-screen.png'))
    self.screenbtn.clicked.connect(self.handleFullscreen)
  

    #create label
    self.label = QLabel()
    self.label.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)

    #create vol label
    self.vlabel = QPushButton(self)
    self.vlabel.setIcon(QIcon('icons/mute.png'))
    self.vlabel.setStyleSheet('background-color : black')
    self.vlabel.clicked.connect(self.volumeMute)

    # create hbox layout
    hboxLayout = QHBoxLayout()

    # set widgets to the hbox layout
    hboxLayout.addWidget(self.bbtn)
    hboxLayout.addWidget(self.playbtn)
    hboxLayout.addWidget(self.fbtn)
    hboxLayout.addWidget(self.lbl)
    hboxLayout.addWidget(self.slider)
    hboxLayout.addWidget(self.elbl)
    hboxLayout.addWidget(self.vlabel)
    hboxLayout.addWidget(self.sld)
    hboxLayout.addWidget(self.screenbtn)

    # topbox

    tboxLayout=QHBoxLayout()
    tboxLayout.setAlignment(Qt.AlignLeft)
    tboxLayout.addWidget(self.openbtn)
    tboxLayout.addWidget(self.mediabtn)
    tboxLayout.addWidget(self.displaybtn)
    tboxLayout.addWidget(self.settingbtn)
  
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
    # self.mediaPlayer.positionChanged.connect(self.volume_changed)  

    self.videowidget = True
      
    #shortcuts
    self.shortcut = QShortcut(QKeySequence('Ctrl+O'), self)
    self.shortcut.activated.connect(self.open_file)
    self.shortcut = QShortcut(QKeySequence('h'), self)
    self.shortcut.activated.connect(self.toggleSlider)
    self.shortcut = QShortcut(QKeySequence(Qt.Key_Up), self)
    self.shortcut.activated.connect(self.volumeUp)
    self.shortcut = QShortcut(QKeySequence(Qt.Key_Down), self)
    self.shortcut.activated.connect(self.volumeDown)
    self.shortcut = QShortcut(QKeySequence(Qt.Key_Right), self)
    self.shortcut.activated.connect(self.forwardSlider)
    self.shortcut = QShortcut(QKeySequence(Qt.Key_Left), self)
    self.shortcut.activated.connect(self.backSlider)
    self.shortcut = QShortcut(QKeySequence(Qt.ShiftModifier +  Qt.Key_Right) , self)
    self.shortcut.activated.connect(self.forwardSlider10)
    self.shortcut = QShortcut(QKeySequence(Qt.ShiftModifier +  Qt.Key_Left) , self)
    self.shortcut.activated.connect(self.backSlider10)


  # function section    
  
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
    else:
      self.playbtn.setIcon(
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
  
  # def volume_changed(self, position):
  #   self.sld.setValue(position)

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
    if self.mediaPlayer.isMuted():
      self.mediaPlayer.setMuted(False)
      self.mediaPlayer.setVolume(100)
      self.vlabel.setIcon(QIcon('icons/max.png'))
    else:
      self.mediaPlayer.setMuted(True)
      self.vlabel.setIcon(QIcon('icons/mute.png'))

  def volumeUp(self):
    self.mediaPlayer.setVolume(self.mediaPlayer.volume() + 10)
    print("Volume: " + str(self.mediaPlayer.volume()))
    
  def volumeDown(self):
    self.mediaPlayer.setVolume(self.mediaPlayer.volume() - 10)  
    print("Volume: " + str(self.mediaPlayer.volume()))

  def forwardSlider(self):
    self.mediaPlayer.setPosition(self.mediaPlayer.position() + 1000*10)

  def forwardSlider10(self):
    self.mediaPlayer.setPosition(self.mediaPlayer.position() + 1000*60)

  def backSlider(self):
    self.mediaPlayer.setPosition(self.mediaPlayer.position() - 1000*10)

  def backSlider10(self):
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
    self.settingbtn.hide()
    self.displaybtn.hide()
    self.bbtn.hide()
    self.playbtn.hide()
    self.fbtn.hide()
    self.label.hide()
    self.vlabel.hide()
    self.slider.hide()
    self.sld.hide()
    self.screenbtn.hide()
    self.lbl.hide()
    self.elbl.hide()    
  
  def showSlider(self):
    self.openbtn.show()
    self.settingbtn.show()
    self.displaybtn.show()
    self.bbtn.show()
    self.playbtn.show()
    self.fbtn.show()
    self.label.show()
    self.vlabel.show()
    self.slider.show()
    self.sld.show()
    self.screenbtn.show()
    self.lbl.show()
    self.elbl.show() 

app = QApplication(sys.argv)
window = Window()
sys.exit(app.exec_())