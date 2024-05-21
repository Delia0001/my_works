from PyQt5.QtWidgets import *
from PyQt5.QtCore import *


# Создаем класс главного окна
class MainWindow(QMainWindow):
    lst = []

    def __init__(self):
        super().__init__()

        # Создаем таблицу для записей наблюдений
        self.observation_table = QTableWidget()
        self.observation_table.setColumnCount(4)
        self.observation_table.setHorizontalHeaderLabels(
            ["Дата и время", "Наименование объекта", "Комментарий", "Состояние"])
        self.observation_table.setEditTriggers(QTableWidget.NoEditTriggers)  # Запрещаем редактирование таблицы

        # Создаем кнопку для добавления записи наблюдения
        self.add_button = QPushButton("Добавить запись")
        self.add_button.clicked.connect(self.add_observation)

        # Создаем вертикальный макет для таблицы наблюдений и кнопки
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Таблица записей наблюдений:"))
        layout.addWidget(self.observation_table)
        layout.addWidget(self.add_button)

        # Создаем виджет и устанавливаем макет
        widget = QWidget()
        widget.setLayout(layout)

        # Устанавливаем виджет в главное окно
        self.setCentralWidget(widget)

        # Устанавливаем размеры главного окна
        self.resize(800, 600)

        # Устанавливаем размеры столбцов в таблице
        self.observation_table.setColumnWidth(0, 200)  # Устанавливаем ширину первого столбца в 200 пикселей
        self.observation_table.setColumnWidth(1, 200)  # Устанавливаем ширину второго столбца в 200 пикселей
        self.observation_table.setColumnWidth(2, 200)  # Устанавливаем ширину третьего столбца в 200 пикселей
        self.observation_table.setColumnWidth(3, 200)  # Устанавливаем ширину четвертого столбца в 200 пикселей

        # Устанавливаем заголовок главного окна
        self.setWindowTitle("Таблица записей наблюдений")

    def add_observation(self):
        # Получаем данные для новой записи
        date = QDateTime.currentDateTime()
        date_str = date.toString("yyyy-MM-dd HH:mm:ss")
        object_name, ok1 = QInputDialog.getItem(self, "Введите наименование объекта", "Список ФИО пациентов", self.lst, 0, True)
        if not ok1:
            return
        comment, ok2 = QInputDialog.getText(self, "Введите комментарий", "Введите симптомы болезни:")
        if not ok2:
            return
        state, ok3 = QInputDialog.getItem(self, "Выберите состояние", "Выберите статус пациента: alive/dead/healthy",
                                          ["alive", "dead", "healthy"])
        if not ok3:
            return
        # Проверяем, что пользователь ввел значения для всех полей
        if ok1 and ok2 and ok3:
            # Проверяем, есть ли уже строка с таким же объектом и статусом "dead"
            for row in range(self.observation_table.rowCount()):
                if self.observation_table.item(row, 1).text() == object_name and self.observation_table.item(row,
                                                                                                             3).text() == "dead":
                    QMessageBox.warning(self, "Ошибка",
                                        "Уже есть запись для мертвого пациента с таким же ФИО.")
                    return

            # Добавляем новую строку
            row_count = self.observation_table.rowCount()
            self.observation_table.insertRow(row_count)

            # Заполняем данными
            self.observation_table.setItem(row_count, 0, QTableWidgetItem(date_str))
            self.observation_table.setItem(row_count, 1, QTableWidgetItem(object_name))
            if object_name not in self.lst:  # Проверяем, что такого пациента еще нет в списке lst
                self.lst.append(object_name)
            # Если статус "dead", удаляем object_name из списка lst
            if state == "dead" and object_name in self.lst:
                self.lst.remove(object_name)
            self.observation_table.setItem(row_count, 2, QTableWidgetItem(comment))
            item = QTableWidgetItem(state)
            if state == "alive":
                item.setForeground(Qt.green)  # Зеленый цвет для "alive"
            elif state == "dead":
                item.setForeground(Qt.red)  # Красный цвет для "dead"
            else:
                item.setForeground(Qt.blue)  # Синий цвет для "healthy"
            self.observation_table.setItem(row_count, 3, item)

            # Обновляем размер таблицы
            self.observation_table.resizeRowsToContents()
            self.observation_table.resizeColumnsToContents()

            # Получаем значение столбца "Наименование объекта"
            name = object_name

            # Получаем значение столбца "Состояние"
            state = state

            # Проверяем, есть ли уже строка с таким же объектом в таблице object_table
            for row in range(object_window.object_table.rowCount()):
                if object_window.object_table.item(row, 0).text() == name:
                    # Обновляем значение столбца "Последнее состояние"
                    object_window.object_table.setItem(row, 1, QTableWidgetItem(state))
                    break
            else:
                # Добавляем новую строку в таблицу object_table
                row_count = object_window.object_table.rowCount()
                object_window.object_table.insertRow(row_count)
                object_window.object_table.setItem(row_count, 0, QTableWidgetItem(name))
                object_window.object_table.setItem(row_count, 1, QTableWidgetItem(state))

            # Если статус "dead", удаляем строку с таким же объектом из таблицы object_table
            if state == "dead":
                for row in range(object_window.object_table.rowCount()):
                    if object_window.object_table.item(row, 0).text() == name:
                        object_window.object_table.removeRow(row)
                        break


# Создаем класс окна для таблицы объектов наблюдений
class ObjectWindow(QWidget):
    def __init__(self):
        super().__init__()

        # Создаем таблицу для объектов наблюдений
        self.object_table = QTableWidget()
        self.object_table.setColumnCount(2)
        self.object_table.setHorizontalHeaderLabels(["Наименование", "Последнее состояние"])
        self.object_table.setEditTriggers(QTableWidget.NoEditTriggers)  # Запрещаем редактирование таблицы

        # Создаем вертикальный макет для таблицы объектов наблюдений
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Таблица объектов наблюдений:"))
        layout.addWidget(self.object_table)

        # Устанавливаем макет в окно
        self.setLayout(layout)

        # Устанавливаем размеры окна
        self.resize(800, 600)

        # Устанавливаем размеры столбцов в таблице
        self.object_table.setColumnWidth(0, 400)  # Устанавливаем ширину первого столбца в 400 пикселей
        self.object_table.setColumnWidth(1, 400)  # Устанавливаем ширину второго столбца в 400 пикселей

        # Устанавливаем заголовок окна
        self.setWindowTitle("Таблица объектов наблюдений")


# Создаем экземпляр приложения Qt
app = QApplication([])

# Создаем экземпляр окна для таблицы объектов наблюдений
object_window = ObjectWindow()

# Создаем экземпляр главного окна
main_window = MainWindow()

# Отображаем оба окна
object_window.show()
main_window.show()

# Запускаем главный цикл приложения Qt
app.exec_()
