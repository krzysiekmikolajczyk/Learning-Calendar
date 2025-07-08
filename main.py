from PySide6 import QtWidgets, QtCore
import sys
import calendar
from datetime import datetime, timedelta
import json
import os

class CalendarApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Calendar')
        self.setGeometry(200,200, 300,300)

        self.data = {}

        if os.path.exists("data.json"):
            try:
                with open('data.json', 'r', encoding='utf-8') as file:
                    self.data = json.load(file)
            except json.JSONDecodeError:
                self.data = {}
        else:
            with open('data.json', 'w', encoding='utf-8') as file:
                json.dump({}, file)


        self.showingyear = False
        self.showingmonth = False
        self.showingweek = False

        self.today = datetime.today()
        self.year = self.today.year
        self.month = self.today.month 
        
        layout_main = QtWidgets.QVBoxLayout()

        layout_head = QtWidgets.QHBoxLayout()

        self.layout_calendar = QtWidgets.QGridLayout()
        self.layout_calendar.setContentsMargins(0,20,0,20)
        self.layout_calendar.setSpacing(2)

        layout_bottom = QtWidgets.QHBoxLayout()
        
        label_changeview = QtWidgets.QLabel('Change view')
        layout_head.addWidget(label_changeview)

        button_yearview = QtWidgets.QPushButton('Year')
        button_yearview.clicked.connect(self.showyear)
        layout_head.addWidget(button_yearview)

        button_monthview = QtWidgets.QPushButton('Month')
        button_monthview.clicked.connect(self.showmonth)
        layout_head.addWidget(button_monthview)

        button_weekview = QtWidgets.QPushButton('Week')
        button_weekview.clicked.connect(self.showweek)
        layout_head.addWidget(button_weekview)

        button_previous = QtWidgets.QPushButton('<')
        button_previous.clicked.connect(self.previous)
        layout_bottom.addWidget(button_previous)

        button_next = QtWidgets.QPushButton('>')
        button_next.clicked.connect(self.nexxt)
        layout_bottom.addWidget(button_next)

        layout_main.addLayout(layout_head)
        layout_main.addLayout(self.layout_calendar)
        layout_main.addLayout(layout_bottom)   
        self.setLayout(layout_main)

    def day_clicked(self, day,  month, year):
        date_str = f'{year:04d}-{month:02d}-{day:02d}'

        current_value = str(self.data.get(date_str, ''))
        
        text , ok = QtWidgets.QInputDialog.getText(self,
                                                       'Learning hours',
                                                       'Enter learning hours:',
                                                       QtWidgets.QLineEdit.Normal,
                                                       current_value)
            
        if ok:
            try: 
                    hours = float(text)
                    self.data[date_str] = hours

                    with open('data.json', 'w', encoding='utf-8') as file:
                        json.dump(self.data, file, ensure_ascii=False, indent=4)

            except ValueError:
                    QtWidgets.QMessageBox.warning(self, "Error", "Enter correct number.")

    def clear_calendar(self):
        while self.layout_calendar.count():
            item = self.layout_calendar.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()
        self.showingyear = False
        self.showingmonth = False
        self.showingweek = False

    def showyear(self):
        self.clear_calendar()
        self.showingyear = True

        days = []
        start_day = self.today - timedelta(days=370)
        current = start_day
        while current <= self.today:
            days.append(current)
            current += timedelta(days=1)
        weekday = start_day.weekday()


        monlabel = QtWidgets.QLabel('Mon')
        wedlabel = QtWidgets.QLabel('Wed')
        frilabel = QtWidgets.QLabel('Fri')
        sunlabel = QtWidgets.QLabel('Sun')
        self.layout_calendar.addWidget(monlabel, 0, 0)
        self.layout_calendar.addWidget(wedlabel, 2, 0)
        self.layout_calendar.addWidget(frilabel, 4, 0)
        self.layout_calendar.addWidget(sunlabel, 6, 0)
        
        k = 370
        i = 53
        
        while i > 0:
            j = 7
            while j >= 0:
                button = QtWidgets.QPushButton(' ')
                button.setFixedSize(15,15)
                button.setStyleSheet("""
                                        QPushButton {
                                            border-radius: 0px;
                                            border: 1px solid #1e1e1e;
                                            margin: 0px;
                                            padding: 0px;
                                            background-color: #2b2b2b;
                                        }
                                        QPushButton:hover {
                                            background-color: #3f3f3f;
                                        }
                                        QPushButton:pressed {
                                            background-color: #a0a0a0;
                                        }
                                    """)

                self.layout_calendar.setSpacing(1)
                day = days[k]
                k -= 1
                date_str = day.strftime('%Y-%m-%d')
                hours = self.data.get(date_str, 0)

                if hours >= 7:
                    color = "#b4f57a" 
                elif hours >= 6:
                    color = "#92e265"  
                elif hours >= 5:
                    color = "#6fd84f"  
                elif hours >= 3.75:
                    color = "#4c9a2a"  
                elif hours >= 2.25:
                    color = "#357218"  
                elif hours >= 1:
                    color = "#234d11" 
                elif hours > 0:
                    color = "#122b07"  
                else:
                    color = "#2b2b2b"  

                if color:
                    button.setStyleSheet(f'QPushButton {{background-color: {color}; }} QPushButton:hover {{background-color: #3f3f3f;}}')

                    button.clicked.connect(lambda checked, d=day.day: self.day_clicked(d, self.month, self.year))
                
                if i < 1:
                    break
                self.layout_calendar.addWidget(button, weekday-1, i)
                if weekday > 1:
                    weekday -= 1
                else:
                    weekday = 7
                    i -= 1
                    j = 7
                j -= 1
            i -= 1 
            

        self.setMinimumSize(900, 300)
        self.setMaximumSize(900, 300)


    def showmonth(self):
        self.clear_calendar()
        self.showingmonth = True

        self.label_abovecalendar = QtWidgets.QLabel()
        self.label_abovecalendar.setAlignment(QtCore.Qt.AlignCenter)
        self.layout_calendar.addWidget(self.label_abovecalendar,0,2,1,3)

        self.label_abovecalendar.setText(f'{self.month}. {self.year}')
        weekdays = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        for col, weekday in enumerate(weekdays):
            label = QtWidgets.QLabel(weekday)
            self.layout_calendar.addWidget(label, 1, col)


        cal = calendar.Calendar(0)
        month_days = cal.monthdayscalendar(self.year, self.month)

        for row_index, week in enumerate(month_days, 2):
            for col_index, day in enumerate(week):
                if day != 0:
                    button = QtWidgets.QPushButton(str(day))

                    date_str = f'{self.year:04d}-{self.month:02d}-{day:02d}'
                    hours = self.data.get(date_str, 0)

                    if hours >= 7:
                        color = "#b4f57a" 
                    elif hours >= 6:
                        color = "#92e265"  
                    elif hours >= 5:
                        color = "#6fd84f"  
                    elif hours >= 3.75:
                        color = "#4c9a2a"  
                    elif hours >= 2.25:
                        color = "#357218"  
                    elif hours >= 1:
                        color = "#234d11" 
                    elif hours > 0:
                        color = "#122b07"  
                    else:
                        color = "#2b2b2b"  

                    if color:
                        button.setStyleSheet(f'QPushButton {{background-color: {color}; }} QPushButton:hover {{background-color: #3f3f3f;}}')

                    button.setFixedSize(40,40)
                    button.clicked.connect(lambda checked, d=day: self.day_clicked(d, self.month, self.year))
                    self.layout_calendar.addWidget(button, row_index, col_index)
        
        self.setMinimumSize(300,400)
        self.setMaximumSize(300,400)

    def showweek(self):
        self.clear_calendar()
        self.showingweek = True

        self.label_abovecalendar = QtWidgets.QLabel()
        self.label_abovecalendar.setAlignment(QtCore.Qt.AlignCenter)
        self.layout_calendar.addWidget(self.label_abovecalendar,0,2,1,3)

        if not hasattr(self, 'current_week_start'):
            today = datetime.today().date()
            self.current_week_start = today - timedelta(days=today.weekday())

        week_dates = [self.current_week_start + timedelta(days=i) for i in range(7)]

        weekdays = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        for col, weekday in enumerate(weekdays):
            label = QtWidgets.QLabel(weekday)
            self.layout_calendar.addWidget(label, 1, col)

        for col_index, day in enumerate(week_dates):
            button = QtWidgets.QPushButton(day.strftime('%d-%m'))
            date_str = day.strftime('%Y-%m-%d')
            hours = self.data.get(date_str, 0)

            if hours >= 7:
                color = "#b4f57a" 
            elif hours >= 6:
                color = "#92e265"  
            elif hours >= 5:
                color = "#6fd84f"  
            elif hours >= 3.75:
                color = "#4c9a2a"  
            elif hours >= 2.25:
                color = "#357218"  
            elif hours >= 1:
                color = "#234d11" 
            elif hours > 0:
                color = "#122b07"  
            else:
                color = "#2b2b2b"  

            if color:
                button.setStyleSheet(f'QPushButton {{background-color: {color}; }} QPushButton:hover {{background-color: #3f3f3f;}}')
                
            button.clicked.connect(lambda checked, d=day.day: self.day_clicked(d, self.month, self.year))
            button.setFixedSize(50,40)
            self.layout_calendar.addWidget(button, 2, col_index)

        start_str = self.current_week_start.strftime('%d-%m')
        end_str = (self.current_week_start + timedelta(days=6)).strftime('%d-%m')
        self.label_abovecalendar.setText(f'{start_str} - {end_str}')

        self.setMinimumSize(400,250)
        self.setMaximumSize(400,250)
        

    def previous(self):
        if self.showingyear:
            pass
        elif self.showingmonth:
            if self.month > 1:
                self.month -= 1
            else:
                self.year -= 1
                self.month = 12
            self.showmonth()
        elif self.showingweek:
            self.current_week_start -= timedelta(days=7)
            self.showweek()
            
            
    def nexxt(self):
        if self.showingyear:
            pass
        elif self.showingmonth:
            if self.month < 12:
                self.month += 1
            else:
                self.year += 1
                self.month = 1
            self.showmonth()
        elif self.showingweek:
            self.current_week_start += timedelta(days=7)
            self.showweek()


app = QtWidgets.QApplication(sys.argv)
window = CalendarApp()
window.show()
window.showweek()
sys.exit(app.exec())
