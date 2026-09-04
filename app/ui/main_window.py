from core.expert_system import ExpertSystem
from PyQt6 import QtWidgets
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import (QComboBox, QHBoxLayout, QLabel, QMainWindow,
                             QSlider, QTableWidget, QTableWidgetItem,
                             QVBoxLayout, QWidget)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.logic = ExpertSystem()

        self.setWindowTitle("Expert System")
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QHBoxLayout()
        central_widget.setLayout(main_layout)

        left_layout = QVBoxLayout()

        # right field ----------------------------------------------------------------
        self.user_input = {
            "name": "",
            "market": "",
            "risk": "",
            "asset": "",
            "parameter": "",
            "liquidity": "",
            "horizon": "",
            "investor_qualification": ""
        }

        self.user_input_null = {
            "name": "",
            "market": "",
            "risk": "",
            "asset": "",
            "parameter": 0.0,
            "liquidity": "",
            "horizon": "",
            "investor_qualification": ""
        }

        market_label = QLabel("Биржа")
        self.market_combo = QComboBox()
        markets = self.logic.return_markets()
        markets.append("")
        self.market_combo.addItems(sorted(markets))

        risk_label = QLabel("Риск")
        self.risk_combo = QComboBox()
        self.risk_combo.addItems(["", "Низкорисковый", "Среднерисковый", "Высокорисковый"])

        asset_label = QLabel("Тип актива")
        self.asset_combo = QComboBox()
        assets = self.logic.return_assets()
        assets.append("")
        self.asset_combo.addItems(sorted(assets))

        self.slider_parameter = QSlider(Qt.Orientation.Horizontal)
        self.slider_parameter.setVisible(False)
        self.slider_parameter.setMinimum(0)
        self.slider_parameter.setMaximum(2000)
        self.slider_parameter.setSingleStep(1)
        self.parameter_label = QLabel("Параметр: 0.00%")
        self.parameter_label.setVisible(False)
        self.slider_parameter.valueChanged.connect(self.update_label)

        liquidity_label = QLabel("Ликвидность")
        self.liquidity_combo = QComboBox()
        self.liquidity_combo.addItems(["", "Низкая", "Средняя", "Высокая"])

        horizon_label = QLabel("Горизонт инвестирования")
        self.horizon_combo = QComboBox()
        self.horizon_combo.addItems(["", "Краткосрочный", "Среднесрочный", "Долгосрочный"])

        investor_qualification_label = QLabel("Квалификация инвестора")
        self.investor_qualification_combo = QComboBox()
        self.investor_qualification_combo.addItems(["", "да", "нет"])

        self.market_combo.currentTextChanged.connect(self.update_results)
        self.risk_combo.currentTextChanged.connect(self.update_results)
        self.asset_combo.currentTextChanged.connect(self.update_results)
        self.liquidity_combo.currentTextChanged.connect(self.update_results)
        self.horizon_combo.currentTextChanged.connect(self.update_results)
        self.investor_qualification_combo.currentTextChanged.connect(self.update_results)

        self.asset_combo.currentTextChanged.connect(self.on_combo_changed)
        self.slider_parameter.valueChanged.connect(self.update_results)

        self.table = QTableWidget()
        self.table.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)

        self.print_table()

        #Add on window ----------------------------------------------------------------------

        main_layout.addLayout(left_layout, 2)
        main_layout.addWidget(self.table, 1)

        self.table.setMinimumWidth(200)

        left_layout.addWidget(market_label)
        left_layout.addWidget(self.market_combo)
        left_layout.addWidget(risk_label)
        left_layout.addWidget(self.risk_combo)
        left_layout.addWidget(asset_label)
        left_layout.addWidget(self.asset_combo)
        left_layout.addWidget(self.parameter_label)
        left_layout.addWidget(self.slider_parameter)
        left_layout.addWidget(liquidity_label)
        left_layout.addWidget(self.liquidity_combo)
        left_layout.addWidget(horizon_label)
        left_layout.addWidget(self.horizon_combo)
        left_layout.addWidget(investor_qualification_label)
        left_layout.addWidget(self.investor_qualification_combo)
        # left_layout.addWidget(self.rating_label)
        # left_layout.addWidget(self.rating_slider)
        # left_layout.addWidget(self.info_rating_label)
        left_layout.addStretch()


    def print_table(self):
        asset_names = self.logic.return_names()

        self.table.setRowCount(len(asset_names))
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["Активы", "% совпадения"])
        self.table.setColumnWidth(0, 300)
        self.table.setColumnWidth(1, 150)

        for i in range(len(asset_names)):
            asset_name = asset_names[i]
            asset_item = QTableWidgetItem(str(asset_name))
            # asset_item.setBackground(QColor(39, 230, 144, 50))
            self.table.setItem(i, 0, asset_item)
            self.table.setItem(i, 1, QTableWidgetItem(""))


    def on_combo_changed(self, text):
        if text == "Акция" or text == "Облигация":
            self.slider_parameter.setVisible(True)
            self.parameter_label.setVisible(True)
        else:
            self.slider_parameter.setVisible(False)
            self.parameter_label.setVisible(False)


    def update_label(self, value):
        self.parameter_label.setText(f"Параметр: {value / 100:.2f}%")


    def update_results(self):
        self.user_input = {
            'name': '',
            'market': self.market_combo.currentText(),
            'risk': self.risk_combo.currentText(),
            'asset': self.asset_combo.currentText(),
            'parameter': self.slider_parameter.value() / 100,
            'liquidity': self.liquidity_combo.currentText(),
            'horizon': self.horizon_combo.currentText(),
            'investor_qualification': self.investor_qualification_combo.currentText(),
        }


        print(self.user_input)
        print(self.user_input_null)

        if (self.user_input == self.user_input_null):
            self.print_table()
        else:
            new_asset_names, max_match = self.logic.evaluate(self.user_input)
            self.update_table(new_asset_names, max_match)
        return 0


    def update_table(self, new_asset_names, match):
        count = 0
        i = 0

        for asset_info in new_asset_names.values():
            if i >= 20:
                break
            i += 1

            rate = asset_info[1]
            if match != 0:
                match_percent = rate * 100 / match
            else:
                match_percent = 0

            if match_percent >= 30:
                count += 1

        self.table.setRowCount(count)

        i = 0
        for asset_name, asset_info in new_asset_names.items():
            if i >= 20:
                break

            asset, rate = asset_name, asset_info[1]

            if match != 0:
                match_percent = rate * 100 / match
            else:
                match_percent = 0

            if match_percent > 100:
                match_percent = 100

            asset_item = QTableWidgetItem(str(asset))
            asset_rate = QTableWidgetItem(str(round(match_percent, 1)))
            if match_percent > 80:
                asset_item.setBackground(QColor(39, 230, 144, 50))
                print("GREEN", asset, rate)
            elif match_percent < 30:
                asset_item.setBackground(QColor(255, 34, 0, 50))
                print("RED", asset, rate)
            else:
                asset_item.setBackground(QColor(247, 234, 0, 50))
                print("YELLOW", asset, rate)
            self.table.setItem(i, 0, asset_item)
            self.table.setItem(i, 1, asset_rate)
            i += 1
        print('---------------')
        return 0
