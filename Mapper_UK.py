import sys
import numpy as np
from Main_Window import Ui_MainWindow
from Options_Page_1 import Ui_MainWindow as Ui_Options_Page_1
from Options_Page_2 import Ui_MainWindow as Ui_Options_Page_2
from Open_Page import Window
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc
from PyQt5 import QtGui as qtg

import  matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

import Cartopy_Britain_OOP
from matplotlib.transforms import offset_copy
import cartopy.crs as ccrs
import cartopy.io.img_tiles as cimgt


## Note - Need to remember to turn the experience weightings to decimals by dividing by 100.

class Main_Window(qtw.QMainWindow):


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.scrollArea.hide()
        self.ui.pushButton.clicked.connect(self.button_clicked)
        self.ui.data_output1.hide()
        self.ui.data_output2.hide()


    def button_clicked(self):
        self.Open_Window = Window()
        self.Open_Window.show()
        self.Open_Window.btn1.clicked.connect(self.country_clicked)
        self.Open_Window.country_selected.connect(self.country_clicked_slot)

    def country_clicked(self):
        self.options_window1 = Options_Page_1()
        self.options_window1.industries.connect(self.industry_checked_slot)
        self.options_window1.done_clicked.connect(self.make_options_page_2)
        self.Open_Window.hide()
        self.options_window1.show()

    def initUI(self, dict_):
        print("PRINT 1: ", dict_)
        self.figure = Canvas(dict_)
        self.figure.map_defining(self, width = 4, height = 5)
        self.figure.move(450, 50)
        self.figure.show()

    @qtc.pyqtSlot()
    def make_options_page_2(self):
        self.options_window2 = Options_Page_2()
        self.options_window2.experience.connect(self.experience_selected_slot)
        self.options_window1.hide()
        self.options_window2.show()

    @qtc.pyqtSlot(str)
    def country_clicked_slot(self, country):
        self.ui.data_output1.setText('The country selected is: {}.'.format(country))

    @qtc.pyqtSlot(list)
    def industry_checked_slot(self, list_):
        self.current_str = '\n'
        self.list_reference = list_
        for item in list_:
            self.current_str += (item + ', ')

        if self.current_str[-2] == ',':
            replacement = self.current_str[:-2]
            self.current_str = replacement

        self.ui.data_output2.setText('The industries selected are: {}.'.format(self.current_str))

    @qtc.pyqtSlot(dict)
    def experience_selected_slot(self, dict_):
        print(dict_)

        self.dict_ = dict_
        self.current_str = ''
        for item in self.list_reference:
            self.current_str += (item + ': ' + '{}'.format(dict_[item]) + '\n')

        self.ui.data_output3.setText('The relevant experience entered is: \n' + self.current_str)
        print('Received')
        self.options_window2.hide()
        self.mapping = Cartopy_Britain_OOP.MapAssembler(dict_)

        self.current_str2 = ''
        for key in self.mapping.Ratings_done:
            self.current_str2 += (key + ': ' + '{}'.format(np.round(self.mapping.Ratings_done[key],2)) + '\n')

        self.ui.data_output4.setText('The relevant ratings found are: \n' + self.current_str2)
        self.ui.scrollArea.show()
        self.initUI(dict_)
        self.ui.data_output1.show()
        self.ui.data_output2.show()








class Options_Page_1(qtw.QMainWindow):

    industries = qtc.pyqtSignal(list)
    done_clicked = qtc.pyqtSignal()
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.ui = Ui_Options_Page_1()
        self.ui.setupUi(self)
        self.ui.pushButton_2.clicked.connect(self.button_clicked)

    def button_clicked(self):
        self.industries.emit(self.list_constructor())
        self.done_clicked.emit()


    def list_constructor(self):
        self.checkbox_list = [self.ui.checkBox, self.ui.checkBox_2, self.ui.checkBox_3, self.ui.checkBox_4, self.ui.checkBox_5]
        self.industry_list = []

        for checkbox in self.checkbox_list:
            if checkbox.isChecked():
                self.industry_list.append(checkbox.text())

        if self.industry_list == []:
            self.industry_list.append('WARNING: No industry has been selected!')

        return (self.industry_list)


class Options_Page_2(qtw.QMainWindow):

    experience = qtc.pyqtSignal(dict)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.ui = Ui_Options_Page_2()
        self.ui.setupUi(self)

        self.ui.pushButton_2.clicked.connect(self.button_clicked)
        self.current_val_1 = 0
        self.current_val_2 = 0
        self.current_val_3 = 0
        self.current_val_4 = 0
        self.current_val_5 = 0
        self.ui.horizontalSlider_1.valueChanged[int].connect(self.changed_value_handling_1)
        self.ui.horizontalSlider_2.valueChanged[int].connect(self.changed_value_handling_2)
        self.ui.horizontalSlider_3.valueChanged[int].connect(self.changed_value_handling_3)
        #self.ui.horizontalSlider_4.valueChanged[int].connect(self.changed_value_handling_4)
        #self.ui.horizontalSlider_5.valueChanged[int].connect(self.changed_value_handling_5)

        self.slider_vals = {'Academic': self.current_val_1,
                            'Aerospace': self.current_val_2,
                            'Automotive': self.current_val_3,
                            'Nuclear': 'NULL',
                            'Software': 'NULL'}


#There has to be a way to iterate through these Qt widgets
    def changed_value_handling_1(self, value):
        self.slider_vals['Academic'] = value
    def changed_value_handling_2(self, value):
        self.slider_vals['Aerospace'] = value
    def changed_value_handling_3(self, value):
        self.slider_vals['Automotive'] = value
    def changed_value_handling_4(self, value):
        self.slider_vals['Nuclear'] = value
    def changed_value_handling_5(self, value):
        self.slider_vals['Software'] = value


    def button_clicked(self):
        for item in self.slider_vals:
            if self.slider_vals[item] == 0:
                self.slider_vals[item] = 50

        for item in self.slider_vals:
            if self.slider_vals[item] is not 'NULL':
                self.slider_vals[item] = self.slider_vals[item]/100

        self.experience.emit(self.slider_vals)
        print('Clicked 1')



class Canvas(FigureCanvas):
    def __init__(self, dict_):
        self.mapper_input = dict_
        pass


    def map_defining(self, parent=None, width=2, height=1.5, dpi=100):
        print("PRINT 2: ")
        self.mapper = Cartopy_Britain_OOP.MapAssembler(self.mapper_input)
        stamen_terrain = cimgt.Stamen('terrain-background')
        self.fig = plt.figure(figsize=(4,5))
        self.ax = self.fig.add_subplot(1, 1, 1, projection=stamen_terrain.crs)
        self.ax.set_extent([2.3, -11.5, 49.2, 60], crs=ccrs.Geodetic())
        self.ax.add_image(stamen_terrain, 6)
        self.map_handling(self.mapper.latlons_done, self.mapper.Ratings_done)


        FigureCanvas.__init__(self, self.fig)
        self.setParent(parent)

    def map_handling(self, latlons, Ratings):
        for key in latlons:
            self.ax.plot(latlons[key][1], latlons[key][0], marker='.', color='k',
                    markersize=Ratings[key] * 8,
                    alpha=1, transform=ccrs.Geodetic())
            geodetic_transform = ccrs.Geodetic()._as_mpl_transform(self.ax)
            text_transform = offset_copy(geodetic_transform, units='dots', x=0)
            self.ax.text(latlons[key][1], latlons[key][0], u"{}".format(Ratings[key]),
                    verticalalignment='center', horizontalalignment='center',
                    transform=text_transform,
                    fontsize=Ratings[key] * 2.5, color='white')
            text_transform2 = offset_copy(geodetic_transform, units='dots', x=-15)

            for item in self.mapper.cities_above_pop:
                if item == key:
                    self.ax.text(latlons[key][1], latlons[key][0], u"{}".format(key),
                        verticalalignment='center', horizontalalignment='right',
                        transform=text_transform2,
                        fontsize=5,
                        bbox=dict(facecolor='sandybrown', alpha=0.3, boxstyle='round'))

        print("YES I'M BEING RUN")



if __name__ == '__main__':
    app = qtw.QApplication([])

    widget = Main_Window()
    widget.show()


    app.exec()