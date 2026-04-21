# - PyQt5 기반

import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QGridLayout,
    QPushButton, QLineEdit
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt


# 계산 로직 클래스
class Calculator:
    def __init__(self):
        self.reset()

    # 초기화
    def reset(self):
        self.current = '0'         # 현재 입력 값
        self.operator = None       # 연산자
        self.operand = None        # 이전 값
        self.new_input = True      # 새 입력 여부

    # 사칙연산
    def add(self, a, b):
        return a + b

    def subtract(self, a, b):
        return a - b

    def multiply(self, a, b):
        return a * b

    def divide(self, a, b):
        if b == 0:
            raise ZeroDivisionError
        return a / b

    # 숫자 입력
    def input_number(self, num):
        if self.new_input:
            self.current = num
            self.new_input = False
        else:
            if self.current == '0':
                self.current = num
            else:
                self.current += num

    # 소수점 입력 (중복 방지)
    def input_decimal(self):
        if '.' not in self.current:
            self.current += '.'

    # 연산자 설정
    def set_operator(self, op):
        if self.operator:
            self.equal()
        self.operand = float(self.current)
        self.operator = op
        self.new_input = True

    # +/- 변환
    def negative_positive(self):
        if self.current.startswith('-'):
            self.current = self.current[1:]
        else:
            self.current = '-' + self.current

    # 퍼센트
    def percent(self):
        try:
            value = float(self.current) / 100
            self.current = str(value)
        except Exception:
            self.current = 'Error'

    # 결과 계산
    def equal(self):
        try:
            if self.operator and self.operand is not None:
                b = float(self.current)

                if self.operator == '+':
                    result = self.add(self.operand, b)
                elif self.operator == '-':
                    result = self.subtract(self.operand, b)
                elif self.operator == '*':
                    result = self.multiply(self.operand, b)
                elif self.operator == '/':
                    result = self.divide(self.operand, b)
                else:
                    return

                # 소수점 6자리 반올림
                result = round(result, 6)

                # 불필요한 0 제거 + 길이 정리
                if result.is_integer():
                    self.current = str(int(result))
                else:
                    self.current = str(result).rstrip('0').rstrip('.')
                self.operator = None
                self.operand = None
                self.new_input = True

        except ZeroDivisionError:
            self.current = 'Error'
        except Exception:
            self.current = 'Error'

    def get_display(self):
        return self.current


# UI 클래스
class CalculatorUI(QWidget):
    def __init__(self):
        super().__init__()
        self.calc = Calculator()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Calculator')
        self.setFixedSize(450, 700)
        self.setStyleSheet('background-color: black;')

        # 디스플레이 (상단 숫자 표시)
        self.display = QLineEdit()
        self.display.setText('0')
        self.display.setAlignment(Qt.AlignRight)
        self.display.setReadOnly(True)
        self.display.setStyleSheet('''
            QLineEdit {
                color: white;
                background: black;
                border: none;
                padding: 20px;
            }
        ''')

        self.display.setFont(QFont('Arial', 40))

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.display)

        grid = QGridLayout()

        # 버튼 정의 (텍스트, 행, 열, 스타일 타입)
        buttons = [
            ('AC', 0, 0, 'func'), ('+/-', 0, 1, 'func'), ('%', 0, 2, 'func'), ('/', 0, 3, 'op'),
            ('7', 1, 0, 'num'), ('8', 1, 1, 'num'), ('9', 1, 2, 'num'), ('*', 1, 3, 'op'),
            ('4', 2, 0, 'num'), ('5', 2, 1, 'num'), ('6', 2, 2, 'num'), ('-', 2, 3, 'op'),
            ('1', 3, 0, 'num'), ('2', 3, 1, 'num'), ('3', 3, 2, 'num'), ('+', 3, 3, 'op'),
            ('0', 4, 0, 'num'), ('.', 4, 2, 'num'), ('=', 4, 3, 'op')
        ]

        for text, row, col, btype in buttons:
            btn = QPushButton(text)

            # 버튼 공통 스타일
            btn.setMinimumSize(80, 80) 
            btn.setFont(QFont('Arial', 18))

            # 타입별 색상 (iOS 스타일)
            if btype == 'num':
                btn.setStyleSheet('''
                    QPushButton {
                        background-color: #333333;
                        color: white;
                        border-radius: 40px;
                    }
                ''')
            elif btype == 'func':
                btn.setStyleSheet('''
                    QPushButton {
                        background-color: #a5a5a5;
                        color: black;
                        border-radius: 40px;
                    }
                ''')
            elif btype == 'op':
                btn.setStyleSheet('''
                    QPushButton {
                        background-color: #ff9500;
                        color: white;
                        border-radius: 40px;
                    }
                ''')

            btn.clicked.connect(self.handle_button)

            # 0 버튼은 가로 2칸
            if text == '0':
                btn.setMinimumSize(170, 80)
                grid.addWidget(btn, row, col, 1, 2)
            else:
                grid.addWidget(btn, row, col)

        main_layout.addLayout(grid)
        self.setLayout(main_layout)

    # 버튼 클릭 처리
    def handle_button(self):
        text = self.sender().text()

        if text.isdigit():
            self.calc.input_number(text)
        elif text == '.':
            self.calc.input_decimal()
        elif text in ['+', '-', '*', '/']:
            self.calc.set_operator(text)
        elif text == '=':
            self.calc.equal()
        elif text == 'AC':
            self.calc.reset()
        elif text == '+/-':
            self.calc.negative_positive()
        elif text == '%':
            self.calc.percent()

        self.update_display()

    # 디스플레이 업데이트 + 폰트 자동 조절
    def update_display(self):
        text = self.calc.get_display()

        max_font = 40
        min_font = 15

        length = len(text)

        # 길이에 따라 부드럽게 줄어들게
        size = max(min_font, max_font - (length - 1) * 2)

        self.display.setFont(QFont('Arial', size))
        self.display.setText(text)


# 실행
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = CalculatorUI()
    window.show()
    sys.exit(app.exec_())
