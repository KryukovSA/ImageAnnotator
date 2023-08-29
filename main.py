import sys

from PyQt5 import QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, QLabel, QGraphicsView, QGraphicsScene, \
    QGraphicsPixmapItem, QVBoxLayout, QWidget, QFileDialog, QGraphicsEllipseItem, QTableWidget, \
    QTableWidgetItem


class ImageAnnotator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Image Annotator")
        self.setGeometry(100, 100, 2500, 1600)

        self.initUI()

    def initUI(self):
        self.image_label = QLabel()
        self.scene = QGraphicsScene()
        self.graphics_view = QGraphicsView(self.scene)
        layout = QVBoxLayout()
        layout.addWidget(self.graphics_view)
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        open_action = QAction("Open Image", self)
        open_action.triggered.connect(self.openImage)
        zoom_in_action = QAction("Zoom In", self)
        zoom_in_action.triggered.connect(self.zoomIn)
        zoom_out_action = QAction("Zoom Out", self)
        zoom_out_action.triggered.connect(self.zoomOut)

        self.toolbar = self.addToolBar("Toolbar")
        self.toolbar.addAction(open_action)
        self.toolbar.addAction(zoom_in_action)
        self.toolbar.addAction(zoom_out_action)

        self.zoom_factor = 1.0
        self.points = []

        # Создаем виджет для отображения списка точек
        self.points_table = QTableWidget()
        self.points_table.setColumnCount(3)
        self.points_table.setHorizontalHeaderLabels(["Number", "X", "Y"])

        layout.addWidget(self.points_table)

    def openImage(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        file_name, _ = QFileDialog.getOpenFileName(self, "Open Image", "", "Images (*.png *.jpg *.bmp);;All Files (*)",
                                                   options=options)
        if file_name:
            self.scene.clear()
            pixmap = QPixmap(file_name)
            self.original_pixmap = pixmap
            pixmap_item = QGraphicsPixmapItem(pixmap)
            self.scene.addItem(pixmap_item)
            self.graphics_view.setScene(self.scene)

    def zoomIn(self):
        self.zoom(1.2)

    def zoomOut(self):
        self.zoom(1 / 1.2)

    def zoom(self, factor):
        self.zoom_factor *= factor
        self.graphics_view.setTransform(QtGui.QTransform().scale(self.zoom_factor, self.zoom_factor))

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton and self.original_pixmap:
            view_pos = event.pos()
            scene_pos = self.graphics_view.mapToScene(view_pos)
            self.addPoint(scene_pos)

    def addPoint(self, pos):
        x = round(pos.x(), 1)
        y = round(pos.y(), 1)
        marker_size = 4 / self.zoom_factor
        point_item = QGraphicsEllipseItem(pos.x() - marker_size / 2, pos.y() - marker_size / 2, marker_size,
                                          marker_size)
        point_item.setPen(Qt.red)
        self.scene.addItem(point_item)

        self.points.append((len(self.points) + 1, x, y))
        self.updatePointsTable()

    def updatePointsTable(self):
        self.points_table.setRowCount(len(self.points))
        for row, point in enumerate(self.points):
            for col, value in enumerate(point):
                self.points_table.setItem(row, col, QTableWidgetItem(str(value)))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    annotator = ImageAnnotator()
    annotator.show()
    sys.exit(app.exec_())
