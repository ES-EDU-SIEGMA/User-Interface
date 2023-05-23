import PyQt5.QtWidgets as PyQtWidgets
import PyQt5.QtCore as PyQtCore
import time
import runtime_data as RuntimeData
import css as Css
import mock_serial as SerialCommunication
import scale as Scale


# window to start and view the mixing progress
#
class MixingProgressWindow(PyQtWidgets.QWidget):
    beverage_to_mix: RuntimeData.Beverage  # can also be None
    mix_drink_to_mix: RuntimeData.MixDrinkInformation  # can also be None
    # either beverage_to_mix or mix_drink_to_mix is None
    mix_drink_mode: bool
    # mix_drink_mode true means we are mixing a mix drink
    # mix_drink_mode false means we are dispensing a beverage
    is_mixing: bool
    # is_mixing acts as a lock to hinder further mixing commands

    def __init__(
            self,
            __parent_window: PyQtWidgets.QWidget,
            __beverage: RuntimeData.Beverage,
            __mix_drink: RuntimeData.MixDrinkInformation, ):

        super().__init__()
        self.parentWidget: PyQtWidgets.QWidget = __parent_window
        self.setWindowTitle("Mixing ProgressWindow")
        self.setStyleSheet(f"background-color: {Css.m_main_background_color};")
        self.is_mixing: bool = False
        self.beverage_to_mix: RuntimeData.Beverage = __beverage
        self.mix_drink_to_mix: RuntimeData.MixDrinkInformation = __mix_drink
        self.mix_drink_mode: bool = self.beverage_to_mix is None
        self.standard_activation_time: int = 5  # former globals variable with the value 5
        self.showFullScreen()

        ##############################################################################
        #       Labels
        ##############################################################################
        self.drinkSizeLabel: PyQtWidgets.QLabel = PyQtWidgets.QLabel("Select the Size of your Drink:", self)
        self.drinkSizeLabel.setStyleSheet(
            f"color: {Css.m_standard_text_color}; font-size: 11pt;")

        self.headerLabel: PyQtWidgets.QLabel = PyQtWidgets.QLabel(f"", self)
        if self.mix_drink_mode:
            self.headerLabel.setText(f"Mixing {self.mix_drink_to_mix.mix_drink_name}")
        else:
            self.headerLabel.setText(f"Mixing {self.beverage_to_mix.beverage_name}")
        self.headerLabel.setStyleSheet(
            f"color: {Css.m_standard_text_color}; font-size: 14pt;")
        self.headerLabel.setAlignment(PyQtCore.Qt.AlignCenter)

        self.informationLabel: PyQtWidgets.QLabel = PyQtWidgets.QLabel("", self)
        self.informationLabel.setStyleSheet(f"color: {Css.m_standard_text_color};")

        ##############################################################################
        #       Buttons
        ##############################################################################
        self.back_button: PyQtWidgets.QPushButton = PyQtWidgets.QPushButton("Back to Main Menu", self)
        self.back_button.clicked.connect(lambda: self.back_button_on_click())
        self.back_button.setStyleSheet(
            f"background-color: {Css.m_button_background_color};"
            f"padding-top: 30%; padding-bottom: 30%; padding-left: 40%; padding-right: 40%;"
            f"color: {Css.m_standard_text_color}; margin: 5%; border: 1px solid #ffffff;")

        self.start_mixing_button: PyQtWidgets.QPushButton = PyQtWidgets.QPushButton("Start Mixing", self)
        self.start_mixing_button.clicked.connect(lambda: self.start_mixing_button_on_click())
        self.start_mixing_button.setStyleSheet(
            f"background-color: {Css.m_button_background_color};"
            f"padding-top: 30%; padding-bottom: 30%; padding-left: 40%; padding-right: 40%;"
            f"color: {Css.m_standard_text_color}; margin: 5%; border: 1px solid #ffffff;")

        ##############################################################################
        #       Combobox
        ##############################################################################
        self.drink_size_select: PyQtWidgets.QComboBox = PyQtWidgets.QComboBox(self)
        self.drink_size_select.insertItem(0, "0.1 L")
        self.drink_size_select.insertItem(1, "0.2 L")
        self.drink_size_select.insertItem(2, "0.3 L")
        self.drink_size_select.insertItem(3, "0.4 L")
        self.drink_size_select.insertItem(4, "0.5 L")
        self.drink_size_select.setStyleSheet(
            f"color: {Css.m_standard_text_color};"
            f"background-color: {Css.m_button_background_color};border: 1px solid {Css.m_border_color};"
            f"padding-top: 25%; padding-bottom: 25%; padding-left: 40%; padding-right: 40%; font-size: 14pt;")

        ##############################################################################
        #       Progressbar
        ##############################################################################
        self.mixing_progress: PyQtWidgets.QProgressBar = PyQtWidgets.QProgressBar(self)
        self.mixing_progress.setStyleSheet(f"color: {Css.m_standard_text_color};")
        self.mixing_progress.setMinimum(0)
        self.mixing_progress.setMaximum(100)
        self.mixing_progress.setValue(0)

        ##############################################################################
        #       Layout
        ##############################################################################
        self.main_layout: PyQtWidgets.QGridLayout = PyQtWidgets.QGridLayout(self)
        self.main_layout.addWidget(self.headerLabel, 0, 0, 1, 2)
        self.main_layout.addWidget(self.drinkSizeLabel, 1, 0)
        self.main_layout.addWidget(self.drink_size_select, 1, 1)
        self.main_layout.addWidget(self.mixing_progress, 2, 0, 2, 2)
        self.main_layout.addWidget(self.informationLabel, 3, 0, 1, 2)
        self.main_layout.addWidget(self.back_button, 4, 1)
        self.main_layout.addWidget(self.start_mixing_button, 4, 0)

    # gets triggered when the start mixing button gets clicked
    # starts either the Beverage or the mix_drink mixing progress
    def start_mixing_button_on_click(self):
        self.back_button.setEnabled(False)
        self.start_mixing_button.setEnabled(False)
        self.drink_size_select.setEnabled(False)
        expected_weight = 0
        empty_drink_weight: int = Scale.get_current_weight()
        current_drink_size_index: int = self.drink_size_select.currentIndex()
        deci_liter: float = (1 + current_drink_size_index) / 10

        current_drink_name: str = ""
        if self.mix_drink_mode:
            current_drink_name: str = self.mix_drink_to_mix.mix_drink_name
        else:
            current_drink_name: str = self.beverage_to_mix.beverage_name

        self.informationLabel.setText(
            f"Mixing {current_drink_name}, {deci_liter} L. Please do not touch the display or the machine!")
        self.is_mixing: bool = True  # activates the lock is_mixing to stop other mixing commands

        if self.mix_drink_mode:
            expected_weight: int = self.mix_mix_drink(self.mix_drink_to_mix, deci_liter)
        else:
            expected_weight: int = self.mix_beverage(self.beverage_to_mix, deci_liter)

        expected_weight_full: int = expected_weight + empty_drink_weight
        self.wait_for_drink_finish(expected_weight, expected_weight_full, empty_drink_weight)
        self.is_mixing: bool = False

        self.back_button.setEnabled(True)
        self.start_mixing_button.setEnabled(True)
        self.drink_size_select.setEnabled(True)
        self.informationLabel.setText(
            "The Drink is finished. Please remove your drink from the machine.")

    # reads out the scale and sets the value of the progressbar accordingly - if the value
    # hasn't changed in 8 secs -> quit
    def wait_for_drink_finish(
            self, expected_weight: int, expected_weight_full: int, empty_drink_weight: int):

        current_weight: int = Scale.get_current_weight()
        timeval: float = time.time()
        current_weight_comp: int = current_weight
        while (current_weight not in range(expected_weight_full - 5, expected_weight_full + 5)
               and self.is_mixing):  # a little bit of breathing room

            if time.time() - timeval >= 8:  # check every 8 seconds if the value has changed

                if current_weight_comp == current_weight:  # if the value is the same -> quit
                    break

                else:
                    timeval = time.time()
                    current_weight_comp = current_weight

            self.mixing_progress.setValue(
                int(((current_weight - empty_drink_weight) / expected_weight) * 100))
            current_weight = Scale.get_current_weight()
            time.sleep(0.5)
        self.mixing_progress.setValue(100)

    # calculates and sends the timings which are needed to mix the given Beverage for the given drinksize
    def mix_beverage(self, __beverage_to_mix: RuntimeData.Beverage, __deci_liter: float):
        cup_size: int = int(__deci_liter * 1000)
        hopper_size: int = 30
        pico_id: int = 0
        str_to_send: str = ""

        if __beverage_to_mix.beverage_hopper_id > 8:
            hopper_size: int = 40

        hopper_timings: list[int] = [0, 0, 0, 0]

        pico_id: int = self.get_pico_id_to_hopper_id(__beverage_to_mix.beverage_hopper_id)

        res: list[int] = self.calc_time_for_activation(__beverage_to_mix, cup_size, 100, hopper_size)

        for i in range(len(res) - 1):
            hopper_timings[__beverage_to_mix.beverage_hopper_id % 4]: int = res[i + 1]
            str_to_send: str = f"{hopper_timings[0]};{hopper_timings[1]};{hopper_timings[2]};{hopper_timings[3]};\n"
            SerialCommunication.send_msg(pico_id, str_to_send)

        return (len(res) - 1) * hopper_size

    # calculates the time and iteration amounts needed to mix a given beverages
    def calc_time_for_activation(
            self, __bvg: RuntimeData.Beverage, cup_size: int, __fill_perc: int, hopper_size: int
    ):
        activation_amount_full = int((cup_size * (__fill_perc / 100)) // hopper_size)
        activation_time_full = int(self.standard_activation_time * __bvg.beverage_flow_speed * 1000)
        temp = []

        if activation_amount_full == 0:
            activation_time_full = 0
        # if activationAmountRest > 0:
        #     activationAmountRest = 1

        temp.append(__bvg.beverage_hopper_id)
        for _ in range(activation_amount_full):
            temp.append(activation_time_full)

        # if activationAmountRest > 0:
        #     temp.append(activationTimeRest)
        return temp

    # calculates all the information needed to mix the given mix_drink and sends them to the corresponding picos
    def mix_mix_drink(self, __mix_drink_to_mix: RuntimeData.MixDrinkInformation, __deci_liter: float):
        cup_size: int = int(__deci_liter * 1000)
        hopper_size: int = 30
        time_list = []
        pico_id: int = 0

        # calculate the time, each bvg needs and add them to the list
        for i in range(len(__mix_drink_to_mix.mix_drink_needed_beverages)):
            if __mix_drink_to_mix.mix_drink_needed_beverages[i].beverage_hopper_id > 8:
                hopper_size = 40
            time_list.append(
                self.calc_time_for_activation(
                    __mix_drink_to_mix.mix_drink_needed_beverages[i],
                    cup_size,
                    __mix_drink_to_mix.get_fill_perc(
                        __mix_drink_to_mix.mix_drink_needed_beverages[i].beverage_id
                    ),
                    hopper_size,
                )
            )
            hopper_size = 30

        cmd_list = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]

        iter_counter = 1
        timings = self.get_timings_to_pico(time_list)
        longest_list_len = self.get_longest_list_length(timings)

        expected_weight = self.get_estimated_weight(time_list)

        # runs through the list and puts the timings into the corresponding hopper cmdS
        while not (iter_counter == longest_list_len):
            for pico_id in range(3):  # run through each pico entry
                for i in range(
                        len(timings[pico_id])
                ):  # run through each timing and place in the corresponding list entry
                    temp = timings[pico_id]
                    hopper_id = temp[i][0] % 4

                    if iter_counter < len(temp[i]):
                        cmd_list[pico_id][hopper_id] = temp[i][iter_counter]
                    else:
                        cmd_list[pico_id][hopper_id] = 0

            pico0_cmd = (
                f"{cmd_list[0][0]};{cmd_list[0][1]};{cmd_list[0][2]};{cmd_list[0][3]};\n")
            pico1_cmd = (
                f"{cmd_list[1][0]};{cmd_list[1][1]};{cmd_list[1][2]};{cmd_list[1][3]};\n")
            pico2_cmd = (
                f"{cmd_list[2][0]};{cmd_list[2][1]};{cmd_list[2][2]};{cmd_list[2][3]};\n")

            SerialCommunication.send_msg(0, pico0_cmd)
            SerialCommunication.send_msg(1, pico1_cmd)
            SerialCommunication.send_msg(2, pico2_cmd)
            print(f"left {pico0_cmd}right {pico1_cmd}rondell {pico2_cmd}")
            iter_counter += 1
        return expected_weight

    # returns the length of the longest list
    def get_longest_list_length(self, __timings_list):
        longest_list_length = 0
        for i in range(len(__timings_list)):
            for y in range(len(__timings_list[i])):
                current_list_length = len(__timings_list[i][y])
                if current_list_length > longest_list_length:
                    longest_list_length = current_list_length
        return longest_list_length

    # separates the Beverage timings to their corresponding pico
    def get_timings_to_pico(self, __timings_list):
        res = [[], [], []]
        for i in range(len(__timings_list)):
            pico_id = self.get_pico_id_to_hopper_id(__timings_list[i][0])
            res[pico_id].append(__timings_list[i])
        return res

    # returns the drink_to_add_id of the pico which is responsible for the hopper
    def get_pico_id_to_hopper_id(self, __hopper_id: int):
        pico_id = 0
        if __hopper_id < 4:
            pico_id = 1
        elif 4 <= __hopper_id < 8:
            pico_id = 0
        else:
            pico_id = 2
        return pico_id

    # returns the estimated weight of the drink after its mixed -> 1ml = 1g
    def get_estimated_weight(self, __time_list):
        result = 0
        for i in range(len(__time_list)):
            hopper_size = 30
            if __time_list[i][0] > 8:
                hopper_size = 40
            for y in range(len(__time_list[i]) - 1):
                result += hopper_size
        return result

    def back_button_on_click(self):
        if not self.is_mixing:
            self.close()
