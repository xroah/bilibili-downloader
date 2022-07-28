from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput
from PySide6.QtCore import QUrl
import os


def play_ring():
    player = QMediaPlayer()
    output = QAudioOutput()
    ring_file = os.path.join(os.getcwd(), "resources/ring.mp3")
    player.setSource(QUrl.fromLocalFile(ring_file))
    player.setAudioOutput(output)
    output.setVolume(50)
    player.play()
