import sys

# PyQt5 UI 관련 클래스 import
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QApplication,
    QGridLayout,
    QLineEdit,
    QPushButton,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)


class CalculatorWindow(QWidget):
    def __init__(self):
        super().__init__()

        # 현재 화면에 표시되는 값 (문자열로 관리)
        self.current_input = '0'

        # 계산을 위한 변수들
        self.left_operand = None            # 왼쪽 값
        self.pending_operator = None        # 연산자 (+, -, ×, ÷)
        self.waiting_for_new_input = False  # 다음 숫자 입력 대기 상태
        self.last_right_operand = None      # '=' 연속 입력 시 사용할 값

        # UI 설정
        self._setup_window()
        self._setup_ui()
        self._update_display()

    # 윈도우 기본 설정
    def _setup_window(self):
        self.setWindowTitle('Calculator')
        self.setFixedSize(360, 620)

    # UI 구성 (버튼 + 디스플레이)
    def _setup_ui(self):
        main_layout = QVBoxLayout()

        # 여백 및 간격 설정
        main_layout.setContentsMargins(12, 12, 12, 12)
        main_layout.setSpacing(12)

        # 계산 결과 표시 창
        self.display = QLineEdit()
        self.display.setReadOnly(True)            # 입력 불가능 (출력 전용)
        self.display.setAlignment(Qt.AlignRight)  # 오른쪽 정렬
        self.display.setFixedHeight(110)

        # 스타일 설정 (검정 배경 + 흰 글씨)
        self.display.setStyleSheet(
            '''
            QLineEdit {
                background-color: #000000;
                color: #ffffff;
                border: none;
                padding: 12px;
                font-size: 40px;
            }
            '''
        )

        main_layout.addWidget(self.display)

        # 버튼 배치용 Grid Layout
        grid = QGridLayout()
        grid.setSpacing(10)

        # 아이폰 계산기와 동일한 버튼 배열
        buttons = [
            [('AC', 'function'), ('+/-', 'function'), ('%', 'function'), ('÷', 'operator')],
            [('7', 'number'), ('8', 'number'), ('9', 'number'), ('×', 'operator')],
            [('4', 'number'), ('5', 'number'), ('6', 'number'), ('-', 'operator')],
            [('1', 'number'), ('2', 'number'), ('3', 'number'), ('+', 'operator')],
            [('0', 'number_wide'), ('.', 'number'), ('=', 'operator')],
        ]

        # 버튼 생성 및 배치
        for row_index, row in enumerate(buttons):
            column_index = 0

            for text, button_type in row:
                button = QPushButton(text)

                # 버튼 스타일 및 크기 설정
                button.setFocusPolicy(Qt.NoFocus)
                button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
                button.setMinimumHeight(90)

                # 클릭 이벤트 연결
                button.clicked.connect(self._handle_button_click)

                # 버튼 색상 적용
                button.setStyleSheet(self._button_style(button_type))

                # '0' 버튼은 가로 2칸 차지
                if button_type == 'number_wide':
                    grid.addWidget(button, row_index, column_index, 1, 2)
                    column_index += 2
                else:
                    grid.addWidget(button, row_index, column_index)
                    column_index += 1

        main_layout.addLayout(grid)
        self.setLayout(main_layout)

    # 버튼 스타일 설정
    @staticmethod
    def _button_style(button_type):
        base_style = '''
            QPushButton {
                border: none;
                border-radius: 45px;
                font-size: 26px;
            }
        '''

        # 기능 버튼 (AC, +/- , %)
        if button_type == 'function':
            return base_style + '''
                QPushButton {
                    background-color: #a5a5a5;
                    color: #000000;
                }
            '''

        # 연산자 버튼
        if button_type == 'operator':
            return base_style + '''
                QPushButton {
                    background-color: #f1a33c;
                    color: #ffffff;
                }
            '''

        # 숫자 버튼
        return base_style + '''
            QPushButton {
                background-color: #333333;
                color: #ffffff;
            }
        '''

    # 버튼 클릭 이벤트 처리
    def _handle_button_click(self):
        button = self.sender()
        text = button.text()

        # 숫자 입력
        if text.isdigit():
            self._input_digit(text)
            return

        # 소수점
        if text == '.':
            self._input_decimal()
            return

        # 연산자
        if text in ('+', '-', '×', '÷'):
            self._set_operator(text)
            return

        # 결과 계산
        if text == '=':
            self._calculate_result()
            return

        # 초기화
        if text == 'AC':
            self._clear_all()
            return

        # 부호 변경
        if text == '+/-':
            self._toggle_sign()
            return

        # 퍼센트
        if text == '%':
            self._apply_percent()

    # 숫자 입력 처리
    def _input_digit(self, digit):
        if self.waiting_for_new_input:
            self.current_input = digit
            self.waiting_for_new_input = False
        elif self.current_input == '0':
            self.current_input = digit
        else:
            self.current_input += digit

        self._update_display()

    # 소수점 입력
    def _input_decimal(self):
        if self.waiting_for_new_input:
            self.current_input = '0.'
            self.waiting_for_new_input = False
        elif '.' not in self.current_input:
            self.current_input += '.'

        self._update_display()

    # 연산자 설정
    def _set_operator(self, operator):
        current_value = float(self.current_input)

        # 이전 연산이 있으면 먼저 계산
        if self.pending_operator and not self.waiting_for_new_input:
            result = self._perform_operation(
                self.left_operand,
                current_value,
                self.pending_operator
            )
            self.left_operand = result
            self.current_input = str(result)
        else:
            self.left_operand = current_value

        self.pending_operator = operator
        self.waiting_for_new_input = True

    # 결과 계산 (=)
    def _calculate_result(self):
        if not self.pending_operator:
            return

        right_operand = float(self.current_input)

        result = self._perform_operation(
            self.left_operand,
            right_operand,
            self.pending_operator
        )

        self.current_input = str(result)
        self.left_operand = result
        self.waiting_for_new_input = True

        self._update_display()

    # 초기화 (AC)
    def _clear_all(self):
        self.current_input = '0'
        self.left_operand = None
        self.pending_operator = None
        self.waiting_for_new_input = False
        self._update_display()

    # 부호 변경
    def _toggle_sign(self):
        if self.current_input.startswith('-'):
            self.current_input = self.current_input[1:]
        else:
            self.current_input = '-' + self.current_input

        self._update_display()

    # 퍼센트 계산
    def _apply_percent(self):
        value = float(self.current_input) / 100
        self.current_input = str(value)
        self._update_display()

    # 실제 연산 처리
    def _perform_operation(self, left, right, operator):
        if operator == '+':
            return left + right
        if operator == '-':
            return left - right
        if operator == '×':
            return left * right
        if operator == '÷':
            if right == 0:
                return 0
            return left / right

    # 화면 업데이트
    def _update_display(self):
        self.display.setText(self.current_input)


# 프로그램 시작 지점
def main():
    app = QApplication(sys.argv)
    window = CalculatorWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()