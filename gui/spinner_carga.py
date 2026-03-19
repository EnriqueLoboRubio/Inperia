from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtCore import QRectF
from PyQt5.QtGui import QColor, QPainter
from PyQt5.QtWidgets import QWidget


class SpinnerCarga(QWidget):
    def __init__(self, parent=None, tam=30, puntos=8, color="#111111"):
        super().__init__(parent)
        self._paso = 0
        self._puntos = max(8, int(puntos))
        self._color = QColor(color)
        self._timer = QTimer(self)
        self._timer.timeout.connect(self._avanzar)
        self.setFixedSize(int(tam), int(tam))
        self.setAttribute(Qt.WA_TransparentForMouseEvents, True)
        self.setStyleSheet("background: transparent; border: none;")
        self.hide()

    def start(self):
        if not self._timer.isActive():
            self._timer.start(85)
        self.show()
        self.update()

    def stop(self):
        self._timer.stop()
        self.hide()

    def _avanzar(self):
        self._paso = (self._paso + 1) % self._puntos
        self.update()

    def paintEvent(self, _event):
        lado = min(self.width(), self.height())
        radio_orbita = (lado / 2) - 5
        radio_punto = max(2.2, lado * 0.09)
        centro = self.rect().center()

        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(Qt.NoPen)

        for i in range(self._puntos):
            color = QColor(self._color)
            alpha = int(255 * ((i + 1) / self._puntos))
            color.setAlpha(alpha)

            painter.save()
            painter.translate(centro)
            painter.rotate((360 / self._puntos) * ((i + self._paso) % self._puntos))
            painter.setBrush(color)
            painter.drawEllipse(
                QRectF(
                    -radio_punto,
                    -radio_orbita - radio_punto,
                    radio_punto * 2,
                    radio_punto * 2,
                )
            )
            painter.restore()
