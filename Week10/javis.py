# javis.py

import os
import wave
from datetime import datetime

import pyaudio


class VoiceRecorder:
    def __init__(self):
        self.chunk = 1024
        self.format_type = pyaudio.paInt16
        self.channels = 1
        self.rate = 44100
        self.record_seconds = 5
        self.records_directory = 'records'

        self.audio = pyaudio.PyAudio()

        self.create_records_directory()

    def create_records_directory(self):
        if not os.path.exists(self.records_directory):
            os.makedirs(self.records_directory)

    def show_microphones(self):
        print('사용 가능한 마이크 목록')

        device_count = self.audio.get_device_count()

        for index in range(device_count):
            device_info = self.audio.get_device_info_by_index(index)

            if device_info['maxInputChannels'] > 0:
                print(
                    f'[{index}] '
                    f'{device_info["name"]}'
                )

    def create_file_name(self):
        current_time = datetime.now()

        return current_time.strftime('%Y%m%d-%H%M%S.wav')

    def record_voice(self, device_index=None):
        file_name = self.create_file_name()

        file_path = os.path.join(
            self.records_directory,
            file_name
        )

        stream = self.audio.open(
            format=self.format_type,
            channels=self.channels,
            rate=self.rate,
            input=True,
            input_device_index=device_index,
            frames_per_buffer=self.chunk
        )

        print('녹음을 시작합니다.')

        frames = []

        total_frames = int(
            self.rate / self.chunk * self.record_seconds
        )

        for _ in range(total_frames):
            data = stream.read(self.chunk)
            frames.append(data)

        print('녹음이 완료되었습니다.')

        stream.stop_stream()
        stream.close()

        wave_file = wave.open(file_path, 'wb')

        wave_file.setnchannels(self.channels)

        wave_file.setsampwidth(
            self.audio.get_sample_size(self.format_type)
        )

        wave_file.setframerate(self.rate)

        wave_file.writeframes(b''.join(frames))

        wave_file.close()

        print(f'저장 위치: {file_path}')

    def show_records_by_date(
        self,
        start_date,
        end_date
    ):
        file_list = os.listdir(self.records_directory)

        target_files = []

        for file_name in file_list:
            if not file_name.endswith('.wav'):
                continue

            try:
                file_date = datetime.strptime(
                    file_name[:15],
                    '%Y%m%d-%H%M%S'
                )

                start_datetime = datetime.strptime(
                    start_date,
                    '%Y%m%d'
                )

                end_datetime = datetime.strptime(
                    end_date,
                    '%Y%m%d'
                )

                if start_datetime <= file_date <= end_datetime:
                    target_files.append(file_name)

            except ValueError:
                continue

        if not target_files:
            print('해당 기간의 녹음 파일이 없습니다.')
            return

        print('조회된 녹음 파일 목록')

        for file_name in sorted(target_files):
            print(file_name)

    def close(self):
        self.audio.terminate()


def main():
    recorder = VoiceRecorder()

    try:
        while True:
            print('\n===== JAVIS =====')
            print('1. 마이크 목록 보기')
            print('2. 음성 녹음')
            print('3. 날짜 범위로 녹음 파일 조회')
            print('4. 종료')

            menu = input('메뉴 선택: ')

            if menu == '1':
                recorder.show_microphones()

            elif menu == '2':
                use_device = input(
                    '마이크 번호 입력 '
                    '(기본값 사용 시 Enter): '
                )

                if use_device.strip() == '':
                    device_index = None
                else:
                    device_index = int(use_device)

                seconds = input(
                    '녹음 시간(초) 입력: '
                )

                recorder.record_seconds = int(seconds)

                recorder.record_voice(device_index)

            elif menu == '3':
                print(
                    '날짜 형식 예시: 20260526'
                )

                start_date = input(
                    '시작 날짜 입력: '
                )

                end_date = input(
                    '종료 날짜 입력: '
                )

                recorder.show_records_by_date(
                    start_date,
                    end_date
                )

            elif menu == '4':
                print('프로그램을 종료합니다.')
                break

            else:
                print('올바른 메뉴를 입력하세요.')

    finally:
        recorder.close()


if __name__ == '__main__':
    main()