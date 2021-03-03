from PyQt5.QtGui import QIcon, QPalette,QKeySequence
from PyQt5.QtWidgets import QApplication,QWidget,QHBoxLayout,QPushButton,QVBoxLayout,QLabel,QSlider,QStyle, QSizePolicy,QFileDialog,QShortcut,QMenu, QAction,QMenuBar,QLineEdit
import sys 
from PyQt5.QtMultimedia import QMediaPlayer,QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt,QUrl,QPoint,QTime

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
    videowidget = QVideoWidget()

    # create open button
    self.openbtn = QPushButton('Open Video', self)  
    self.openbtn.setIcon(QIcon('icons/open.png'))
    self.openbtn.setFixedHeight(30);
    self.openbtn.setMaximumWidth(100);
    self.openbtn.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Minimum)
    self.openbtn.setStyleSheet('background-color : black ; color : white')
    self.openbtn.clicked.connect(self.open_file)

    #create settings button dropdown
    
    settingbtn = QMenuBar()
    actionFile = settingbtn.addMenu(QIcon('icons/settings.png'),'&Setting')
    settingbtn.setStyleSheet('background-color : black; color : white')
    actionFile.addAction("New")
    actionFile.addAction("Open")
    actionFile.addAction("Save")
    actionFile.addSeparator()
    exit = QAction(QIcon('icons/exit.png'), 'Exit', self)
    exit.setShortcut('Ctrl+Q')
    exit.setStatusTip('Exit application')
    exit.triggered.connect(app.quit)
    actionFile.addAction(exit) 

    settingbtn.setFixedHeight(30)
    settingbtn.setMaximumWidth(200)
    settingbtn.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Minimum)

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
        

    #create label
    self.label = QLabel()
    self.label.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)

    #create vol label
    self.vlabel = QLabel(self)
    self.vlabel.setPixmap(QPixmap('icons/mute.png'))

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
    hboxLayout.addWidget(self.sld )

    # topbox

    tboxLayout=QHBoxLayout()
    tboxLayout.setAlignment(Qt.AlignLeft)
    tboxLayout.addWidget(self.openbtn)
    tboxLayout.addWidget(settingbtn)



    #create vbox layout 
    vboxlayout = QVBoxLayout()
    vboxlayout.addLayout(tboxLayout)
    vboxlayout.addWidget(videowidget)
    vboxlayout.addLayout(hboxLayout)
    vboxlayout.addWidget(self.label)
    self.setLayout (vboxlayout)
    self.mediaPlayer.setVideoOutput(videowidget)

    # media player signals

    self.mediaPlayer.stateChanged.connect(self.mediastate_changed)
    self.mediaPlayer.positionChanged.connect(self.position_changed)
    self.mediaPlayer.durationChanged.connect(self.duration_changed)
    self.mediaPlayer.positionChanged.connect(self.volume_changed)  

    self.widescreen = True
      
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
  
  def volume_changed(self, position):
    self.sld.setValue(position)

  def changeValue(self, value):

    self.volume = value
    if self.volume == 0:
      self.vlabel.setPixmap(QPixmap('icons/mute.png'))
    elif 0 < self.volume <= 30:
      self.vlabel.setPixmap(QPixmap('icons/min.png'))
    elif 30 < self.volume < 80:
      self.vlabel.setPixmap(QPixmap('icons/med.png'))
    else:
      self.vlabel.setPixmap(QPixmap('icons/max.png'))


  def volumeUp(self):
    vol= self.mediaPlayer.setVolume(self.mediaPlayer.volume() + 10)
    print("Volume: " + str(self.mediaPlayer.volume()))
    
  def volumeDown(self):
    vol=self.mediaPlayer.setVolume(self.mediaPlayer.volume() - 10)    
    print("Volume: " + str(self.mediaPlayer.volume()))

  def forwardSlider(self):
    self.mediaPlayer.setPosition(self.mediaPlayer.position() + 1000*10)

  def forwardSlider10(self):
    self.mediaPlayer.setPosition(self.mediaPlayer.position() + 1000*60)

  def backSlider(self):
    self.mediaPlayer.setPosition(self.mediaPlayer.position() - 1000*10)

  def backSlider10(self):
    self.mediaPlayer.setPosition(self.mediaPlayer.position() - 1000*60)
  
  # full screen on double click
  def handleFullscreen(self):
    if self.windowState() & Qt.WindowFullScreen:
      QApplication.setOverrideCursor(Qt.ArrowCursor)
      self.showNormal()
      print("no Fullscreen")
    else:
      self.showFullScreen()
      QApplication.setOverrideCursor(Qt.BlankCursor)
      print("Fullscreen entered")

  def toggleSlider(self):    
    if self.slider.isVisible():
      self.hideSlider()
    else:
      self.showSlider()
    
  def hideSlider(self):
    self.openbtn.hide()
    self.settingbtn.hide()
    self.bbtn.hide()
    self.playbtn.hide()
    self.fbtn.hide()
    self.label.hide()
    self.vlabel.hide()
    self.slider.hide()
    self.sld.hide()
  
  def showSlider(self):
    self.openbtn.show()
    self.settingbtn.show()
    self.bbtn.show()
    self.playbtn.show()
    self.fbtn.show()
    self.label.show()
    self.vlabel.show()
    self.slider.show()
    self.sld.show()


app = QApplication(sys.argv)
window = Window()
sys.exit(app.exec_())