import random
import datetime
import json
import os
import threading
import time


class DummySensor:
    def __init__(self):
        # 환경 값을 저장할 사전 객체 초기화
        self.env_values = {
            'mars_base_internal_temperature': 0,
            'mars_base_external_temperature': 0,
            'mars_base_internal_humidity': 0,
            'mars_base_external_illuminance': 0,
            'mars_base_internal_co2': 0,
            'mars_base_internal_oxygen': 0,
        }

    def set_env(self):
        # 각 환경 지표에 대해 정해진 범위 내의 랜덤 값을 생성하여 저장
        self.env_values['mars_base_internal_temperature'] = round(random.uniform(18, 30), 2)
        self.env_values['mars_base_external_temperature'] = round(random.uniform(0, 21), 2)
        self.env_values['mars_base_internal_humidity'] = round(random.uniform(50, 60), 2)
        self.env_values['mars_base_external_illuminance'] = round(random.uniform(500, 715), 2)
        self.env_values['mars_base_internal_co2'] = round(random.uniform(0.02, 0.1), 4)
        self.env_values['mars_base_internal_oxygen'] = round(random.uniform(4, 7), 2)

    def get_env(self):
        # 현재 환경 값을 반환하고, 로그 파일에 기록
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # 파일에 로그 남기기
        header = (
            'datetime,'
            'internal_temperature,'
            'external_temperature,'
            'internal_humidity,'
            'external_illuminance,'
            'internal_co2,'
            'internal_oxygen\n'
        )
        log_line = (
            f"{timestamp},"
            f"{self.env_values['mars_base_internal_temperature']},"
            f"{self.env_values['mars_base_external_temperature']},"
            f"{self.env_values['mars_base_internal_humidity']},"
            f"{self.env_values['mars_base_external_illuminance']},"
            f"{self.env_values['mars_base_internal_co2']},"
            f"{self.env_values['mars_base_internal_oxygen']}\n"
        )

        # 파일이 없을 때만 헤더 기록
        file_exists = os.path.isfile('sensor_log.csv')
        with open('sensor_log.csv', 'a', encoding='utf-8') as log_file:
            if not file_exists:
                log_file.write(header)
            log_file.write(log_line)

        return self.env_values


class MissionComputer:
    def __init__(self):
        # 화성 기지 환경값을 저장할 사전 객체
        self.env_values = {
            'mars_base_internal_temperature': 0,
            'mars_base_external_temperature': 0,
            'mars_base_internal_humidity': 0,
            'mars_base_external_illuminance': 0,
            'mars_base_internal_co2': 0,
            'mars_base_internal_oxygen': 0,
        }
        self._running = False
        # 5분 평균 계산을 위한 누적 데이터
        self._history = {key: [] for key in self.env_values}
        self._last_avg_time = None

    def get_sensor_data(self):
        self._running = True
        self._last_avg_time = time.time()

        # 별도 스레드에서 키 입력을 감지 ('q' 입력 시 종료)
        input_thread = threading.Thread(target=self._wait_for_stop, daemon=True)
        input_thread.start()

        while self._running:
            # 센서 값을 갱신하고 env_values에 저장
            ds.set_env()
            sensor_data = ds.get_env()
            for key in self.env_values:
                self.env_values[key] = sensor_data[key]

            # 5분 평균 계산을 위해 히스토리에 누적
            for key in self._history:
                self._history[key].append(self.env_values[key])

            # env_values를 JSON 형태로 출력
            print(json.dumps(self.env_values, indent=4))

            # 5분(300초)마다 평균값 출력 후 히스토리 초기화
            if time.time() - self._last_avg_time >= 300:
                self._print_averages()
                self._last_avg_time = time.time()
                self._history = {key: [] for key in self.env_values}

            # 5초 대기 (0.1초 단위로 나눠 종료 신호에 빠르게 반응)
            for _ in range(50):
                if not self._running:
                    break
                time.sleep(0.1)

        print('System stopped...')

    def _wait_for_stop(self):
        # 사용자가 'q'를 입력하면 반복 중단
        while self._running:
            try:
                user_input = input()
                if user_input.strip().lower() == 'q':
                    self._running = False
                    break
            except EOFError:
                break

    def _print_averages(self):
        # 5분 평균값을 계산해 출력
        averages = {}
        for key, values in self._history.items():
            if values:
                averages[key] = round(sum(values) / len(values), 4)
            else:
                averages[key] = None

        print('\n[5-Minute Average]')
        print(json.dumps(averages, indent=4))
        print()


if __name__ == '__main__':
    ds = DummySensor()
    RunComputer = MissionComputer()
    RunComputer.get_sensor_data()