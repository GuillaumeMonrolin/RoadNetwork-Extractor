from PyQt5 import QtWidgets, QtCore, uic
from PyQt5.QtSvg import QSvgRenderer, QSvgWidget
from PyQt5.QtWidgets import QVBoxLayout

from controllers import ViewModelController

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):

        super(MainWindow, self).__init__()

        uic.loadUi('gui/main_window.ui', self)

        self.svg_layout = QVBoxLayout(self.svgFrame)

        self.get_size = QSvgRenderer()
        self.svg_widget = QSvgWidget()
        self.wStyleComboBox.addItems(["Wood printer"])

        self.show()

    @QtCore.pyqtSlot(name="on_generateMapButton_clicked")
    def click(self):

        layers = ViewModelController.generate_layer_filter(self.motorwayCheckBox.isChecked(),
                                                           self.trunkCheckBox.isChecked(),
                                                           self.primaryCheckBox.isChecked(),
                                                           self.secondaryCheckBox.isChecked(),
                                                           self.tertiaryCheckBox.isChecked())

        exported_svg_path = ViewModelController.generate_map(self.cityInput.text(),
                                                             int(self.radiusInput.text()),
                                                             layers,
                                                             self.riverCheckBox.isChecked(),
                                                             self.lakeCheckBox.isChecked())

        self.display_svg_preview(exported_svg_path)


    def display_svg_preview(self, svg_to_render):
        self.get_size.load(svg_to_render)
        self.svg_widget.load(svg_to_render)


        self.svg_layout.addWidget(self.svg_widget)

