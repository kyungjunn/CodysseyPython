
# 보너스 과제: 텍스트 사전 (3글자 이상 영어 단어만 등록하여 오탐지 방지)
WORD_DICTIONARY = [
    'the', 'and', 'that', 'have', 'for', 'not', 'with',
    'you', 'this', 'but', 'his', 'from', 'they', 'say',
    'she', 'will', 'one', 'all', 'would', 'there', 'their',
    'what', 'out', 'about', 'who', 'get', 'which', 'when',
    'make', 'can', 'like', 'time', 'just', 'him', 'know',
    'take', 'into', 'your', 'good', 'some', 'could', 'them',
    'see', 'other', 'than', 'then', 'now', 'look', 'only',
    'come', 'its', 'over', 'think', 'also', 'back', 'after',
    'use', 'two', 'how', 'our', 'work', 'well', 'way', 'even',
    'new', 'want', 'because', 'any', 'these', 'give', 'day',
    'most', 'base', 'mars', 'password', 'secret', 'open',
    'door', 'emergency', 'access', 'key', 'code', 'storage',
    'unlock', 'hello', 'world', 'love', 'life', 'blue', 'red',
    'green', 'black', 'white', 'here', 'there', 'where',
    'very', 'much', 'more', 'less', 'high', 'low', 'big',
    'small', 'long', 'short', 'old', 'young', 'next',
    'last', 'first', 'right', 'left', 'same', 'different'
]


def read_password_file(file_path):
    """password.txt 파일을 읽어 내용을 반환한다."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read().strip()
        print(f'[파일 읽기 성공] "{file_path}" -> 내용: "{content}"')
        return content
    except FileNotFoundError:
        print(f'[오류] 파일을 찾을 수 없습니다: {file_path}')
        return None
    except PermissionError:
        print(f'[오류] 파일 접근 권한이 없습니다: {file_path}')
        return None
    except OSError as e:
        print(f'[오류] 파일을 읽는 중 문제가 발생했습니다: {e}')
        return None


def save_result_file(file_path, shift, decoded_text):
    """해독된 결과를 result.txt 파일로 저장한다."""
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write('[카이사르 암호 해독 결과]\n')
            f.write(f'이동 자리수 (Shift): {shift}\n')
            f.write(f'최종 해독 암호: {decoded_text}\n')
        print(f'\n[저장 완료] 결과가 "{file_path}"에 저장되었습니다.')
    except PermissionError:
        print(f'[오류] 파일 쓰기 권한이 없습니다: {file_path}')
    except OSError as e:
        print(f'[오류] 파일을 저장하는 중 문제가 발생했습니다: {e}')


def contains_dictionary_word(text):
    """
    텍스트 내에 사전 단어(3글자 이상)가 포함되어 있는지 확인한다.
    공백으로 분리된 단어 단위로만 비교하여 오탐지를 방지한다.
    (보너스 과제)
    """
    words_in_text = text.lower().split()
    for word in WORD_DICTIONARY:
        if word in words_in_text:
            return True, word
    return False, None


def caesar_cipher_decode(target_text):
    """
    카이사르 암호를 해독한다.

    알파벳 26자리 각각에 대해 이동(shift)을 적용하여
    가능한 모든 해독 결과를 출력한다.
    공백, 숫자, 기타 문자는 그대로 유지한다.
    사전 단어가 발견되면 해당 줄에 표시하지만 반복은 26까지 계속한다.

    파라메터:
        target_text (str): 해독할 암호 문자열

    반환값:
        list: (shift, decoded_text) 튜플의 리스트
    """
    alphabet_count = 26
    results = []
    auto_found_shift = None

    print('\n' + '=' * 55)
    print('  카이사르 암호 해독 시작')
    print(f'  원문 암호: "{target_text}"')
    print('=' * 55)

    for shift in range(1, alphabet_count + 1):
        decoded_chars = []

        for char in target_text:
            if char.isalpha():
                base = ord('A') if char.isupper() else ord('a')
                decoded_char = chr(
                    (ord(char) - base - shift) % alphabet_count + base
                )
                decoded_chars.append(decoded_char)
            else:
                # 공백, 숫자, 기타 문자는 그대로 유지
                decoded_chars.append(char)

        decoded_text = ''.join(decoded_chars)
        results.append((shift, decoded_text))

        # 보너스: 사전 단어 감지 - 표시만 하고 반복은 계속
        found, matched_word = contains_dictionary_word(decoded_text)

        if found and auto_found_shift is None:
            auto_found_shift = shift
            marker = f'  ★ 사전 단어 발견: "{matched_word}" <- 추천'
        elif found:
            marker = f'  ★ 사전 단어 발견: "{matched_word}"'
        else:
            marker = ''

        print(f'  Shift {shift:>2}자리 -> {decoded_text}{marker}')

    print('=' * 55)

    if auto_found_shift is not None:
        print(f'\n  [자동 감지] Shift {auto_found_shift}에서 의미 있는 단어를 발견했습니다.')

    return results


def get_valid_shift_input(max_shift):
    """사용자로부터 유효한 자리수를 입력받는다."""
    while True:
        try:
            user_input = input(
                f'\n몇 번째 자리수가 올바른 암호인가요? (1~{max_shift}): '
            )
            shift_num = int(user_input)
            if 1 <= shift_num <= max_shift:
                return shift_num
            print(f'  [입력 오류] 1~{max_shift} 사이의 숫자를 입력해 주세요.')
        except ValueError:
            print('  [입력 오류] 숫자만 입력해 주세요.')


def main():
    """메인 실행 함수."""
    print('\n' + '★' * 55)
    print('  화성 기지 비상 저장소 암호 해독 시스템')
    print('★' * 55)

    # 1단계: password.txt 파일 읽기
    password_file = 'password.txt'
    target_text = read_password_file(password_file)

    if target_text is None:
        print('\n프로그램을 종료합니다.')
        return

    # 2~5단계: 카이사르 암호 해독 및 전체 26자리 결과 출력
    results = caesar_cipher_decode(target_text)

    # 6단계: 사용자로부터 정답 자리수 입력 받기
    correct_shift = get_valid_shift_input(len(results))

    # 해당 자리수의 해독 결과 추출
    final_decoded = results[correct_shift - 1][1]
    print(
        f'\n  [선택 결과] Shift {correct_shift}자리 -> '
        f'최종 해독 암호: "{final_decoded}"'
    )

    # result.txt로 저장
    save_result_file('result.txt', correct_shift, final_decoded)


if __name__ == '__main__':
    main()