import zipfile
import itertools
import time
import string
import zlib  # zlib 모듈을 추가로 불러옵니다.

def unlock_zip():
    zip_file_path = 'emergency_storage_key.zip'
    # 소문자 알파벳과 숫자로 구성된 문자열 
    characters = string.ascii_lowercase + string.digits
    
    # 파일 존재 여부 예외 처리
    try:
        zip_file = zipfile.ZipFile(zip_file_path)
    except FileNotFoundError:
        print(f'오류: {zip_file_path} 파일을 찾을 수 없습니다.')
        return
    except zipfile.BadZipFile:
        print('오류: 손상되었거나 올바르지 않은 zip 파일입니다.')
        return
        
    start_time = time.time()
    start_time_str = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(start_time))
    print(f'해킹 시작 시간: {start_time_str}')
    print('비밀번호 해독을 시작합니다...')
    
    attempt_count = 0
    is_found = False
    
    # 6자리 중복 순열 생성 (문자 + 숫자)
    for password_tuple in itertools.product(characters, repeat=6):
        attempt_count += 1
        password = ''.join(password_tuple)
        
        # 출력으로 인한 속도 저하를 막기 위해 100만 번마다 진행 상황 출력
        if attempt_count % 1000000 == 0:
            elapsed_time = time.time() - start_time
            print(f'반복 횟수: {attempt_count}회, 진행 시간: {elapsed_time:.2f}초, 현재 시도 암호: {password}')
            
        try:
            # 암호 해제 시도
            zip_file.extractall(pwd=password.encode('utf-8'))
            is_found = True
            
            # 성공 시 결과 출력
            elapsed_time = time.time() - start_time
            print('\n[ 잠금 해제 성공! ]')
            print(f'찾아낸 비밀번호: {password}')
            print(f'총 반복 횟수: {attempt_count}회')
            print(f'총 진행 시간: {elapsed_time:.2f}초')
            
            # 비밀번호를 파일로 저장 (예외 처리 포함)
            try:
                with open('password.txt', 'w', encoding='utf-8') as f:
                    f.write(password)
                print('비밀번호가 password.txt 파일에 저장되었습니다.')
            except IOError:
                print('경고: 비밀번호를 찾았으나 password.txt에 저장하는 데 실패했습니다.')
                
            break
            
        except (RuntimeError, zipfile.BadZipFile, zlib.error):
            # zlib.error를 추가하여 비밀번호가 틀렸을 때 발생하는 예외를 무시하고 계속 진행합니다.
            continue
        except Exception as e:
            # 예상치 못한 다른 오류에 대한 예외 처리
            print(f'예기치 못한 오류 발생: {type(e).__name__}: {e}')
            break
            
    if not is_found:
        print('모든 조합을 시도했지만 비밀번호를 찾지 못했습니다.')
        
    zip_file.close()

if __name__ == '__main__':
    unlock_zip()