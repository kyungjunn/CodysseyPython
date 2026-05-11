import zipfile
import itertools
import time
import string
import multiprocessing
import sys
import zlib  # zlib 오류 처리를 위해 추가

def check_password_chunk(first_char, zip_file_path):
    '''지정된 첫 글자로 시작하는 모든 6자리 비밀번호 조합을 테스트합니다.'''
    characters = string.ascii_lowercase + string.digits
    
    try:
        zip_file = zipfile.ZipFile(zip_file_path)
    except Exception:
        return None
        
    # 첫 글자를 고정하고 나머지 5자리에 대한 조합 생성 (총 36^5 번 반복)
    for password_tuple in itertools.product(characters, repeat=5):
        password = first_char + ''.join(password_tuple)
        
        try:
            zip_file.extractall(pwd=password.encode('utf-8'))
            zip_file.close()
            return password  # 성공 시 비밀번호 반환
            
        except (RuntimeError, zipfile.BadZipFile, zlib.error):
            # 비밀번호가 틀렸을 때 발생하는 예외들을 무시하고 다음 조합 시도
            continue
        except Exception:
            # 기타 치명적인 오류 발생 시 건너뜀
            continue
            
    zip_file.close()
    return None

def unlock_zip_fast():
    zip_file_path = 'emergency_storage_key.zip'
    characters = string.ascii_lowercase + string.digits
    
    start_time = time.time()
    start_time_str = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(start_time))
    
    print(f'고속 해킹 시작 시간: {start_time_str}')
    print(f'사용 가능한 CPU 코어 수: {multiprocessing.cpu_count()}개')

    # 멀티프로세스 풀 생성 (가능한 모든 CPU 코어 사용)
    pool = multiprocessing.Pool(processes=multiprocessing.cpu_count())
    
    # 각 프로세스에 첫 번째 문자를 할당하여 비동기 실행 (총 36개의 작업 생성)
    results = []
    for char in characters:
        result = pool.apply_async(check_password_chunk, (char, zip_file_path))
        results.append(result)
        
    found_password = None
    
    # 결과 대기 및 확인
    while not found_password:
        # 진행 중인 작업 확인
        for r in results:
            if r.ready():
                res = r.get()
                if res is not None:
                    found_password = res
                    break
        
        # 암호를 아직 찾지 못했다면 1초마다 진행 시간 갱신
        if not found_password:
            elapsed_time = time.time() - start_time
            # 터미널 한 줄에 덮어쓰며 출력하여 화면이 지저분해지는 것을 방지
            sys.stdout.write(f'\r 비밀번호 찾는 중. 현재 진행 시간: {elapsed_time:.2f}초')
            sys.stdout.flush()
            time.sleep(1)

    # 암호를 찾았으므로 나머지 프로세스 강제 종료
    pool.terminate()
    pool.join()
    
    elapsed_time = time.time() - start_time
    print('\n\n[ 잠금 해제 성공! ]')
    print(f'찾아낸 비밀번호: {found_password}')
    print(f'총 진행 시간: {elapsed_time:.2f}초')
    
    # 파일로 저장
    try:
        with open('password.txt', 'w', encoding='utf-8') as f:
            f.write(found_password)
        print('비밀번호가 password.txt 파일에 안전하게 저장되었습니다.')
    except IOError:
        print('경고: 비밀번호를 찾았으나 저장하는 데 실패했습니다.')

if __name__ == '__main__':
    # 윈도우 환경 등에서의 멀티프로세싱 안전성을 위한 보호 구문
    multiprocessing.freeze_support()
    unlock_zip_fast()