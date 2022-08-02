import os

from PySide6.QtMultimedia import (
    QMediaPlayer,
    QAudioOutput,
    QMediaDevices
)
from PySide6.QtCore import QUrl, QObject


def play_ring(parent: QObject):
    player = QMediaPlayer(parent)
    output = QAudioOutput(parent)
    ring_file = os.path.join(os.getcwd(), "resources/ring.mp3")
    ring_file = os.path.normpath(ring_file)
    output.setDevice(QMediaDevices.defaultAudioOutput())
    output.setVolume(50)
    player.setSource(QUrl.fromLocalFile(ring_file))
    player.setAudioOutput(output)
    player.play()
