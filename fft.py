import sys
import numpy as np
import scipy.fftpack
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt, QTimer, QRect
from PyQt5.QtWidgets import QWidget, QApplication, QPushButton, QGridLayout, QHBoxLayout, QSpinBox
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt
import random

class math():
    
    def mm(self):
        global ew, N, Fs, xf, yf1, yf2, yy12
        r = 0
        yy12 = np.array([])
        N = int(m.spin.value())
        Fs = int(m.spin1.value())
        u = int(m.spin3.value())
        T = 1.0 / Fs
        x = np.linspace(0.0, N * T, N)
        # y1=np.sin(random.randint(1,1000)*np.pi*x*x)
        y1 = np.random.normal(0, x, N)
        y2 = np.cos(int(m.spin2.value()) * 1.6 * np.pi * x * x * x * (random.randint(2, 3) / random.randint(3, 6)))
        yf1 = scipy.fftpack.fft(y1)
        yf2 = scipy.fftpack.fft(y2)
        xf = np.linspace(0.0, 1.0 / (2.0 * T), N / 2)  # Nyquist–Shannon sampling
        for i in range(int(N)):
            if abs(yf1[i]) > abs(yf2[i]):
                r = abs(yf2[i])
            elif yf1[i] == yf2[i]:
                r = abs(yf1[i])
            else:
                r = abs(yf1[i])
            yy12 = np.append(yy12, r)
            if u > abs(yy12[i]):
                r = 0
            else:
                r = abs(yy12[i])
            yy12 = np.append(yy12, r)
            # print(abs(yy12)) #debug
            # print(abs(yf1[i]),abs(yf2[i]))
            # print(abs(r))

class W(QWidget):
    
    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        self.setWindowFlags(QtCore.Qt.CustomizeWindowHint)
        self.setMinimumSize(1000, 900)
        self.setMaximumSize(1000, 900)
        self.f = plt.figure()
        plt.subplots_adjust(0.09, 0.05, 0.87, 0.98)
        self.canvas = FigureCanvas(self.f)
        layout = QHBoxLayout(self)
        layout.addStretch(0)
        layout.addWidget(self.canvas)
        grid = QGridLayout(self)
        grid.addWidget(self.canvas)
        self.button1 = QtWidgets.QPushButton('Пуск', self)
        self.button2 = QtWidgets.QPushButton('Стоп', self)
        self.button3 = QtWidgets.QPushButton('Выход', self)
        self.lbl1 = QtWidgets.QLabel('Параметры \nотображаемых сигналов:', self)
        self.lbl2 = QtWidgets.QLabel('Длины \nсигналов:', self)
        self.lbl3 = QtWidgets.QLabel('Размер \nвыборки \nсигналов:', self)
        self.lbl4 = QtWidgets.QLabel('Ширина \nрозового \nшума:', self)
        self.lbl5 = QtWidgets.QLabel('Ширина\nинтервала\nсовпадения:', self)
        self.lbl6 = QtWidgets.QLabel(' БПФ (FFT) - быстрое \nпреобразование Фурье.\n\n log - логарифмический\nмасштаб.\n\n Программа отображает:\n два БПФ сигнала -\n белый шум розовый\n шум, и диаграмму\n совпадения этих\n сигналов.', self)
        self.lbl7 = QtWidgets.QLabel('НАЖМИТЕ "ПУСК"', self)
        self.spin = QtWidgets.QSpinBox(self)
        self.spin.setRange(1, 2000)
        self.spin.setValue(500)
        # print(int(self.spin.value()))  #debug
        self.spin1 = QtWidgets.QSpinBox(self)
        self.spin1.setRange(1, 2000)
        self.spin1.setValue(1000)
        self.spin2 = QtWidgets.QSpinBox(self)
        self.spin2.setRange(1, 2000)
        self.spin2.setValue(400)
        self.spin3 = QtWidgets.QSpinBox(self)
        self.spin3.setRange(0, 100)
        self.spin3.setValue(100)
        self.canvas.setGeometry(0, 0, 1000, 900)
        self.button1.setGeometry(885, 605, 100, 30)
        self.button2.setGeometry(885, 635, 100, 30)
        self.button3.setGeometry(885, 830, 100, 27)
        self.lbl1.setGeometry(870, 270, 130, 50)
        self.lbl2.setGeometry(883, 320, 50, 35)
        self.lbl3.setGeometry(883, 360, 50, 35)
        self.lbl4.setGeometry(883, 400, 50, 40)
        self.lbl5.setGeometry(883, 445, 64, 40)
        self.lbl6.setGeometry(875, 20, 200, 200)
        self.lbl7.setGeometry(430, 360, 150, 150)
        self.spin.setGeometry(942, 330, 45, 23)
        self.spin1.setGeometry(942, 370, 45, 23)
        self.spin2.setGeometry(942, 413, 45, 23)
        self.spin3.setGeometry(947, 458, 40, 23)
        self.button1.clicked.connect(self.start)
        self.button2.clicked.connect(self.stop)
        self.button3.clicked.connect(self.exit)
        W.show(self)
        
    def gt(self):
        m_math = math()
        m_math.mm()
        self.f.clear()
        ax1 = self.f.add_subplot(321)
        ax2 = self.f.add_subplot(323)
        ax3 = self.f.add_subplot(322)
        ax4 = self.f.add_subplot(324)
        ax5 = self.f.add_subplot(313)
        ax1.bar(xf, 2.0 / N * np.abs(yf1[:N // 2]), color='g')
        ax2.semilogy(xf, 2.0 / N * np.abs(yf1[:N // 2]), color='g')
        ax3.bar(xf, 2.0 / N * np.abs(yf2[:N // 2]), color='b')
        ax4.semilogy(xf, 2.0 / N * np.abs(yf2[:N // 2]), color='b')
        ax5.semilogy(xf, 2.0 / N * np.abs(yy12[:N // 2]), color='r')
        ax1.grid()
        ax2.grid()
        ax3.grid()
        ax4.grid()
        ax5.grid()
        ax1.set_title('Диаграммы БПФ Первого сигнала - Белый шум', fontsize=9, fontweight="bold")
        ax3.set_title('Диаграммы БПФ Второго сигнала - Розовый шум', fontsize=9, fontweight="bold")
        ax5.set_title('Наиболее похожие участки \nпервого и второго сигналов - log', fontsize=7, fontweight="bold")
        ax1.set_ylabel('Интенсивность БПФ сигнала', fontsize=7)
        ax2.set_ylabel('Интенсивность БПФ сигнала - log', fontsize=7)
        ax3.set_ylabel('Интенсивность БПФ сигнала', fontsize=7)
        ax4.set_ylabel('Интенсивность БПФ сигнала - log', fontsize=7)
        ax5.set_ylabel('Интенсивность БПФ сигнала - log', fontsize=7)
        ax1.set_xlabel('Частота сигнала (Гц)', fontsize=7)
        ax2.set_xlabel('Частота сигнала (Гц)', fontsize=7)
        ax3.set_xlabel('Частота сигнала (Гц)', fontsize=7)
        ax4.set_xlabel('Частота сигнала (Гц)', fontsize=7)
        ax5.set_xlabel('Частота сигнала (Гц)', fontsize=7)
        self.canvas.draw()
        # print(int(self.spin.value())) #debug
        
    def start(self):
        self.lbl7.setText('')
        timer.start(150)
    def stop(self):
        timer.stop()
    def exit(self):
        m.close()
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    m = W()
    m.show()
    global timer
    timer = QTimer()
    timer.timeout.connect(m.gt)
    sys.exit(app.exec_())
