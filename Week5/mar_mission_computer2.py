import random
import datetime
import json
import os
import threading
import time
import platform
import multiprocessing


def create_default_setting():
    """출력 항목 설정을 위한 setting.txt 파일을 생성합니다."""
    settings = {
        'show_os_info': 'True',
        'show_cpu_load': 'True',
        'show_sensor_data': 'True'
    }
    # 파일이 없을 경우에만 기본 설정값으로 생성
    if not os.path.exists('setting.txt'):
        with open('setting.txt', 'w', encoding='utf-8') as f:
            for key, value in settings.items():
                f.write(f'{key}={value}\n')


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
        # 보너스 과제: 설정 로드
        self.settings = self._load_settings()

    def _load_settings(self):
        """setting.txt 파일을 읽어 출력 항목 설정 딕셔너리를 반환합니다."""
        conf = {}
        try:
            if os.path.exists('setting.txt'):
                with open('setting.txt', 'r', encoding='utf-8') as f:
                    for line in f:
                        if '=' in line:
                            key, value = line.strip().split('=')
                            # 'True' 문자열을 실제 Boolean 값으로 변환
                            conf[key] = value.strip().lower() == 'true'
            else:
                # 파일이 없을 경우 기본값 반환
                return {
                    'show_os_info': True,
                    'show_cpu_load': True,
                    'show_sensor_data': True
                }
        except Exception as e:
            print(f'Error loading settings: {e}')
        return conf

    def get_mission_computer_info(self):
        """미션 컴퓨터의 시스템 정보를 가져와 JSON 형식으로 출력합니다."""
        # 설정 확인
        if not self.settings.get('show_os_info', True):
            return

        try:
            info = {
                'os': platform.system(),
                'os_version': platform.version(),
                'cpu_type': platform.processor(),
                'cpu_cores': multiprocessing.cpu_count(),
                'memory_size': self._get_total_memory()
            }
            print('\n[Mission Computer System Information]')
            print(json.dumps(info, indent=4))
            return info
        except Exception as e:
            print(f'Error retrieving system info: {e}')
            return None

    def _get_total_memory(self):
        """시스템의 총 메모리 크기를 가져옵니다."""
        try:
            if platform.system() == 'Windows':
                return 'N/A (Windows platform limitation)'
            else:
                # 리눅스 환경의 메모리 정보 읽기
                with open('/proc/meminfo', 'r') as f:
                    for line in f:
                        if 'MemTotal' in line:
                            return line.split(':')[1].strip()
        except Exception:
            return 'Unknown'

    def get_mission_computer_load(self):
        """CPU 및 메모리의 실시간 사용량을 가져와 JSON 형식으로 출력합니다."""
        # 설정 확인
        if not self.settings.get('show_cpu_load', True):
            return

        try:
            load_info = {
                'cpu_usage_percent': self._get_cpu_load(),
                'memory_usage_percent': self._get_mem_load()
            }
            print('\n[Mission Computer Real-time Load]')
            print(json.dumps(load_info, indent=4))
            return load_info
        except Exception as e:
            print(f'Error retrieving load info: {e}')
            return None

    def _get_cpu_load(self):
        """CPU 부하 상태를 확인합니다."""
        try:
            if platform.system() == 'Linux':
                with open('/proc/loadavg', 'r') as f:
                    return f.read().split()[0]
            return 'Load info access limited'
        except Exception:
            return 'Error'

    def _get_mem_load(self):
        """메모리 사용량 비율을 계산합니다."""
        try:
            if platform.system() == 'Linux':
                with open('/proc/meminfo', 'r') as f:
                    lines = f.readlines()
                    mem = {}
                    for line in lines[:3]:
                        parts = line.split(':')
                        mem[parts[0]] = int(parts[1].split()[0])
                used = mem['MemTotal'] - mem['MemFree']
                return f"{round((used / mem['MemTotal']) * 100, 2)}%"
            return 'Memory info access limited'
        except Exception:
            return 'Error'

    def get_sensor_data(self):
        """센서 데이터를 수집하고 설정에 따라 출력합니다."""
        # 설정 확인
        if not self.settings.get('show_sensor_data', True):
            print('\nSensor data display is disabled in setting.txt')
            return

        self._running = True
        self._last_avg_time = time.time()

        # 스레드를 사용하여 사용자 입력(종료) 대기
        input_thread = threading.Thread(target=self._wait_for_stop, daemon=True)
        input_thread.start()

        print("\nStarting sensor data collection... (Press 'q' and Enter to stop)")

        while self._running:
            # 센서 데이터 업데이트
            ds.set_env()
            sensor_data = ds.get_env()
            for key in self.env_values:
                self.env_values[key] = sensor_data[key]
                self._history[key].append(sensor_data[key])

            # 실시간 데이터 출력
            print(json.dumps(self.env_values, indent=4))

            # 5분(300초) 주기 평균 출력
            if time.time() - self._last_avg_time >= 300:
                self._print_averages()
                self._last_avg_time = time.time()
                self._history = {key: [] for key in self.env_values}

            # 5초 대기 (0.1초 단위로 종료 신호 체크)
            for _ in range(50):
                if not self._running:
                    break
                time.sleep(0.1)

        print('System data collection stopped.')

    def _wait_for_stop(self):
        """사용자의 'q' 입력을 감지하여 시스템을 정지시킵니다."""
        while self._running:
            try:
                user_input = input()
                if user_input.strip().lower() == 'q':
                    self._running = False
                    break
            except EOFError:
                break

    def _print_averages(self):
        """누적된 히스토리 데이터의 평균을 계산하여 출력합니다."""
        averages = {}
        for key, values in self._history.items():
            if values:
                averages[key] = round(sum(values) / len(values), 4)
            else:
                averages[key] = None

        print('\n' + '=' * 30)
        print('[5-Minute Average Report]')
        print(json.dumps(averages, indent=4))
        print('=' * 30 + '\n')


if __name__ == '__main__':
    # 0. 설정 파일 생성 (최초 실행 시)
    create_default_setting()

    # 1. 센서 및 미션 컴퓨터 인스턴스화
    ds = DummySensor()
    runComputer = MissionComputer()

    # 2. 시스템 정보 출력 (설정값 기반)
    runComputer.get_mission_computer_info()

    # 3. 실시간 부하 정보 출력 (설정값 기반)
    runComputer.get_mission_computer_load()

    # 4. 센서 데이터 수집 시작 (설정값 기반)
    runComputer.get_sensor_data()