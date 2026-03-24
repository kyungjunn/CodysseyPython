import random
import datetime


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

        #파일에 로그 남기기
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
        import os
        file_exists = os.path.isfile('sensor_log.csv')
        with open('sensor_log.csv', 'a', encoding='utf-8') as log_file:
            if not file_exists:
                log_file.write(header)
            log_file.write(log_line)

        return self.env_values

# DummySensor 인스턴스 생성
ds = DummySensor()

# 랜덤 데이터 생성
ds.set_env()

# 데이터 확인 및 로그 저장
env = ds.get_env()

# 결과 출력 테스트
print('=== 화성 기지 환경 데이터 ===')
print(f"화성 기지 내부 온도       : {env['mars_base_internal_temperature']} °C")
print(f"화성 기지 외부 온도       : {env['mars_base_external_temperature']} °C")
print(f"화성 기지 내부 습도       : {env['mars_base_internal_humidity']} %")
print(f"화성 기지 외부 광량       : {env['mars_base_external_illuminance']} W/m²")
print(f"화성 기지 내부 CO₂ 농도   : {env['mars_base_internal_co2']} %")
print(f"화성 기지 내부 산소 농도  : {env['mars_base_internal_oxygen']} %")