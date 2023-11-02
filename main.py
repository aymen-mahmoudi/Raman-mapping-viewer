import os
import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow,  QApplication,  QFileDialog,  \
    QMessageBox

import matplotlib
import pandas as pd
import numpy as np

Ui_MainWindow,  _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__),  'gui.ui'))


class DrawChart(QMainWindow):
    def __init__(self):
        super(QMainWindow,  self).__init__(parent=None)
        self.ui = Ui_MainWindow()  # setup gui
        self.ui.setupUi(self)  # connect gui to window

        self.file = ''  # path to file with data
        self.data = ''  # data for heatmap
        self.cmaps = [
            'Blues', 'viridis', 'plasma',  'inferno',  'magma',
            'cividis', 'Greys',  'Purples',  'Greens',  'Oranges',
            'Reds',  'YlOrBr',  'YlOrRd',  'OrRd',  'PuRd',  'RdPu',  'BuPu',
            'GnBu',  'PuBu',  'YlGnBu',  'PuBuGn',  'BuGn',  'YlGn', 'binary',
            'gist_yarg',  'gist_gray',  'gray',  'bone',
            'pink',  'spring',  'summer',  'autumn',  'winter',  'cool',
            'Wistia',  'hot',  'afmhot',  'gist_heat',  'copper',  'PiYG',
            'PRGn', 'BrBG',  'PuOr',  'RdGy',  'RdBu',  'RdYlBu',
            'RdYlGn',  'Spectral',  'coolwarm',  'bwr',  'seismic',
            'twilight',  'twilight_shifted',  'hsv',  'Pastel1',  'Pastel2',
            'Paired',  'Accent',  'Dark2',
            'Set1',  'Set2',  'Set3',  'tab10',  'tab20',  'tab20b',
            'tab20c',  'flag',  'prism',  'ocean',  'gist_earth',  'terrain',
            'gist_stern',  'gnuplot',  'gnuplot2',  'CMRmap',
            'cubehelix',  'brg',  'gist_rainbow',  'rainbow',  'jet',
            'turbo',  'nipy_spectral',  'gist_ncar', 'Blues_r',
            'viridis_r', 'plasma_r', 'inferno_r', 'magma_r', 'cividis_r',
            'Greys_r', 'Purples_r', 'Greens_r', 'Oranges_r', 'Reds_r',
            'YlOrBr_r', 'YlOrRd_r', 'OrRd_r',
            'PuRd_r',  'RdPu_r',  'BuPu_r', 'GnBu_r', 'PuBu_r',  'YlGnBu_r',
            'PuBuGn_r', 'BuGn_r', 'YlGn_r', 'binary_r',  'gist_yarg_r',
            'gist_gray_r',  'gray_r', 'bone_r', 'pink_r', 'spring_r',
            'summer_r', 'autumn_r',  'winter_r',  'cool_r', 'Wistia_r',
            'hot_r', 'afmhot_r', 'gist_heat_r', 'copper_r',  'PiYG_r',
            'PRGn_r',  'BrBG_r',  'PuOr_r',
            'RdGy_r', 'RdBu_r',  'RdYlBu_r', 'RdYlGn_r', 'Spectral_r',
            'coolwarm_r',  'bwr_r',  'seismic_r',  'twilight_r',
            'twilight_shifted_r',  'hsv_r',  'Pastel1_r',  'Pastel2_r',
            'Paired_r',  'Accent_r',  'Dark2_r',  'Set1_r',  'Set2_r',
            'Set3_r', 'tab10_r',  'tab20_r',  'tab20b_r', 'tab20c_r',
            'flag_r',  'prism_r', 'ocean_r', 'gist_earth_r',  'terrain_r',
            'gist_stern_r', 'gnuplot_r', 'gnuplot2_r', 'CMRmap_r',
            'cubehelix_r', 'brg_r',  'gist_rainbow_r', 'rainbow_r',
            'jet_r', 'turbo_r',  'nipy_spectral_r',  'gist_ncar_r'
        ]
        self.ui.comboBox_cmap.addItems(self.cmaps)
        self.cb = False  # handle for colorbar
        self.signals()  # connect signals in program

    def signals(self):
        self.ui.pushButton_open.clicked.connect(self.process)
        self.ui.pushButton_close.clicked.connect(self.close)
        self.ui.pushButton_redraw.clicked.connect(self.redraw)

    def process(self):
        if not self.point_file():
            return
        self.read_data()
        self.draw_chart()

    def redraw(self):
        if not os.path.isfile(self.file):
            msgBox = QMessageBox()
            msgBox.setText('File does not exist')
            msgBox.exec_()
            return False
        self.draw_chart()

    def point_file(self):
        dial = QFileDialog()  # get path from user
        path,  filters = dial.getOpenFileName(
            self,  'Open Files',  '',  'Supported (*.txt)'
        )
        if path == '':  # check if user give some output
            return False
        if not os.path.isfile(path):  # check if file exists
            msgBox = QMessageBox()
            msgBox.setText('File does not exist')
            msgBox.exec_()
            return False

        self.file = path
        return True

    def read_data(self):
        # your code,  didnt messing around
        data = pd.read_csv(self.file,  header = None,  sep='\t')
        data=data.fillna(0)
        da=data.to_numpy()
        data1=pd.DataFrame(da, index=da[:, 0],  columns=da[0, :])
        data_new=data1.drop(index=0.00000,  columns=0.0000)
        df=data_new[::-1].iloc[:, ::-1]
        col1=df.index.to_numpy()
        x1=[]
        c=np.linspace(0, col1.max()-col1.min(), len(col1))
        for i in c:
            x1.append(round(i, 2))

        row1=df.columns.to_numpy()
        r=np.linspace(0, row1.max()-row1.min(), len(row1))
        f1=[]
        for i in r:
            f1.append(round(i, 2))
        s=df.to_numpy()
        data2=pd.DataFrame(s, index=x1,  columns=f1)
        self.data = data2.iloc[::-1]
        self.ui.doubleSpinBox_min.setValue(self.data.min().min())
        self.ui.doubleSpinBox_max.setValue(self.data.max().max())

    def draw_chart(self):
        self.ui.widget.canvas.ax.clear()  # clean widet
        if self.cb:
            self.cb.remove()

        pc = self.ui.widget.canvas.ax.pcolormesh(
            self.data,  cmap=self.ui.comboBox_cmap.currentText())
        self.cb = self.ui.widget.canvas.ax.figure.colorbar(
            pc,  ax=self.ui.widget.canvas.ax)
        pc.set_clim(
            vmin=self.ui.doubleSpinBox_min.value(),
            vmax=self.ui.doubleSpinBox_max.value()
        )  # we need this to be accesible for remove it on redraw

        # format plot and axes
        cols = [col for col in self.data]
        rows = list(self.data.index)
        self.ui.widget.canvas.ax.set_xticks([i for i in range(len(cols))])
        self.ui.widget.canvas.ax.set_yticks([j for j in range(len(rows))])
        self.ui.widget.canvas.ax.set_xticklabels(cols)
        self.ui.widget.canvas.ax.set_yticklabels(rows)
        self.ui.widget.canvas.ax.axes.xaxis.set_major_locator(
            matplotlib.ticker.MultipleLocator(20))
        self.ui.widget.canvas.ax.axes.yaxis.set_major_locator(
            matplotlib.ticker.MultipleLocator(20))
        self.ui.widget.canvas.ax.set_title(self.ui.lineEdit.text())
        self.ui.widget.canvas.ax.set_xlabel('X (μm)')
        self.ui.widget.canvas.ax.set_ylabel('Y (μm)')
        self.ui.widget.canvas.ax.get_figure().tight_layout()
        self.ui.widget.canvas.draw()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    form = DrawChart()
    form.show()
    app.exec_()
    sys.exit(0)
