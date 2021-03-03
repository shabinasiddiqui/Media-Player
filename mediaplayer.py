from PyQt5.QtGui import QIcon, QPalette,QKeySequence
from PyQt5.QtWidgets import QApplication,QWidget,QHBoxLayout,QPushButton,QVBoxLayout,QLabel,QSlider,QStyle, QSizePolicy,QFileDialog,QShortcut
import sys 
from PyQt5.QtMultimedia import QMediaPlayer,QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt,QUrl,QPoint

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

    #create settings button
    self.settingbtn = QPushButton('Setting')
    self.settingbtn.setStyleSheet('background-color : black; color : white')
    self.settingbtn.setIcon(QIcon('icons/settings.png'))
    self.settingbtn.setFixedHeight(30);
    self.settingbtn.setMaximumWidth(100);
    self.settingbtn.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Minimum)
    
    # self.settingbtn.clicked.connect(self.open_file)

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
    self.slider.setRange(0,0)
    self.slider.sliderMoved.connect(self.set_position)

    #create volume slider
    
    self.sld = QSlider(Qt.Horizontal, self)
    self.sld.setFocusPolicy(Qt.NoFocus)
    self.sld.valueChanged.connect(self.changeValue)
    self.sld.sliderMoved.connect(self.set_volume)
    # self.sld.sliderMoved.connect(self.set_vposition)
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
    hboxLayout.addWidget(self.slider)
    hboxLayout.addWidget(self.vlabel)
    hboxLayout.addWidget(self.sld )

    # topbox

    tboxLayout=QHBoxLayout()
    tboxLayout.setAlignment(Qt.AlignLeft)
    tboxLayout.addWidget(self.openbtn)
    tboxLayout.addWidget(self.settingbtn)



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

  def duration_changed(self, duration):
    self.slider.setRange(0, duration)

  def set_position(self, position):
    self.mediaPlayer.setPosition(position)

  def set_vposition(self, position):
    self.mediaPlayer.setPosition(position)

  def set_volume(self, value):
    self.mediaPlayer.setVolume(value)
  
  def handle_errors(self):
    self.playbtn.setEnabled(False)
    self.label.setText("Error: " + self.mediaPlayer.errorString())

  def changeValue(self, value):
    self.volume = value
    if value == 0:
      self.vlabel.setPixmap(QPixmap('icons/mute.png'))
    elif 0 < value <= 30:
      self.vlabel.setPixmap(QPixmap('icons/min.png'))
    elif 30 < value < 80:
      self.vlabel.setPixmap(QPixmap('icons/med.png'))
    else:
      self.vlabel.setPixmap(QPixmap('icons/max.png'))

  # def changeVolume(self, value):
  #   self.volume = value

  def volumeUp(self):
    self.mediaPlayer.setVolume(self.mediaPlayer.volume() + 10)
    print("Volume: " + str(self.mediaPlayer.volume()))
    
  def volumeDown(self):
    self.mediaPlayer.setVolume(self.mediaPlayer.volume() - 10)
    print("Volume: " + str(self.mediaPlayer.volume()))


  def forwardSlider(self):
    self.mediaPlayer.setPosition(self.mediaPlayer.position() + 1000*10)

  def backSlider(self):
    self.mediaPlayer.setPosition(self.mediaPlayer.position() - 1000*10)

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