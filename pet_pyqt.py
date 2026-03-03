import sys, random, math
from PyQt5 import QtWidgets, QtCore, QtGui
from PIL import Image, ImageDraw


class PetPetWidget(QtWidgets.QWidget):
    def __init__(self, config):
        self.MainImagePath = config["MainImagePath"]
        self.ScreenWitdh = config["ScreenWidth"]
        self.ScreenHeight = config["ScreenHeight"]
        self.Speed = config["Speed"]
        super().__init__()
        self.setWindowFlags(
            QtCore.Qt.FramelessWindowHint | # 移除标题栏和边框
            QtCore.Qt.WindowStaysOnTopHint | # 窗口始终在其他窗口之上
            QtCore.Qt.Tool # 隐藏在任务栏上
        )
        self.setWindowTitle("PetPet")
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground) # 启用每像素透明度

        self.unit = self.width = self.height = round(min(config["ScreenWidth"], config["ScreenHeight"]) * config["Scale"])

        self.resize(self.width, self.height)

        self.DragPos = None
        self.MainImage = None
        
        
        self.PosX = (config["ScreenWidth"] - self.width) / 2
        self.PosY = (config["ScreenHeight"] - self.height) / 2

        self.VelocityX = random.uniform(-self.unit * self.Speed, self.unit * self.Speed)
        self.VelocityY = random.uniform(-self.unit * self.Speed, self.unit * self.Speed)

        self.Speed *= self.unit
        self.AccelRange = self.Speed * 0.1

        self.AccelerationX = random.uniform(-self.AccelRange, self.AccelRange)
        self.AccelerationY = random.uniform(-self.AccelRange, self.AccelRange)

        self.DesTime = 0

        self._last_time = QtCore.QElapsedTimer()
        self._last_time.start()
        self.DestinationX, self.DestinationY = random.randint(0, self.ScreenWitdh - self.width), random.randint(0, self.ScreenHeight - self.height)
        
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.animate)
        self.timer.start(30) # 30ms interval (~33 FPS)

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        pix = QtGui.QPixmap.fromImage(self.make_image())
        painter.drawPixmap(0, 0, pix)
        painter.end()

    def make_image(self):
        if self.MainImage is None:
            pil_img = Image.open(self.MainImagePath)
            pil_img = pil_img.convert("RGBA")
            pil_img = pil_img.resize((self.width, self.height), Image.LANCZOS)
            data = pil_img.tobytes('raw', 'RGBA')
            self.MainImage = QtGui.QImage(data, self.width, self.height, QtGui.QImage.Format_RGBA8888)
        return self.MainImage

    def animate(self):
        # compute elapsed time in seconds
        Elapsed_ms = self._last_time.elapsed()
        # if timer hasn't advanced, skip
        if Elapsed_ms <= 0:
            return
        self._last_time.restart()
        dt = Elapsed_ms / 1000

        # 更新追随点
        self.DesTime += Elapsed_ms
        if self.DesTime >= 30000:
            self.DesTime = 0
            self.DestinationX, self.DestinationY = random.randint(0, self.ScreenWitdh - self.width), random.randint(0, self.ScreenHeight - self.height)
        
        
        print(self.DestinationX, self.DestinationY)
        
        if self.DragPos is None:
            
            self.AccelerationX = self.AccelerationX * 0.1 + 0.9 * (0.1 * random.uniform(-self.AccelRange, self.AccelRange) + 0.9 * (self.DestinationX - self.PosX) / self.ScreenWitdh * self.AccelRange)
            self.AccelerationY = self.AccelerationY * 0.1 + 0.9 * (0.1 * random.uniform(-self.AccelRange, self.AccelRange) + 0.9 * (self.DestinationY - self.PosY) / self.ScreenHeight * self.AccelRange)

            self.VelocityX += self.AccelerationX
            self.VelocityY += self.AccelerationY
            
            self.VelocityX = max(-self.Speed, min(self.VelocityX, self.Speed))
            self.VelocityY = max(-self.Speed, min(self.VelocityY, self.Speed))
            self.PosX += self.VelocityX * dt
            self.PosY += self.VelocityY * dt

            RightLimit = self.ScreenWitdh - self.width
            BottomLimit = self.ScreenHeight - self.height
            if self.PosX < 0:
                self.PosX = 1
                self.VelocityX = -self.VelocityX
            elif self.PosX > RightLimit:
                self.PosX = RightLimit
                self.VelocityX = -self.VelocityX
            if self.PosY < 0:
                self.PosY = 1
                self.VelocityY = -self.VelocityY
            elif self.PosY > BottomLimit:
                self.PosY = BottomLimit - 1
                self.VelocityY = -self.VelocityY
        if self.DragPos or True: self.move(round(self.PosX), round(self.PosY))
        self.update()

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.RightButton:
            QtWidgets.qApp.quit()
        elif event.button() == QtCore.Qt.LeftButton:
            self.DragPos = event.globalPos() - self.frameGeometry().topLeft()

    def mouseMoveEvent(self, event):
        if self.DragPos is not None and event.buttons() & QtCore.Qt.LeftButton:
            Pos = event.globalPos() - self.DragPos
            self.PosX, self.PosY = Pos.x(), Pos.y()

    def mouseReleaseEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.DragPos = None

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    
    config = {
        "Scale" : 0.05,
        "ScreenWidth" : app.primaryScreen().size().width(),
        "ScreenHeight" : app.primaryScreen().size().height(),
        "MainImagePath" : ".\\Resources\\1.bmp",
        "Speed" : 3
    }
    Pet = PetPetWidget(config)
    Pet.show()
    sys.exit(app.exec_())
