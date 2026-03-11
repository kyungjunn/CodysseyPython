def read_log(filename):
    """로그 파일을 읽고 전체 내용을 출력하는 함수."""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        return lines
    except FileNotFoundError:
        print(f'[오류] 파일을 찾을 수 없습니다: {filename}')
        return None
    except PermissionError:
        print(f'[오류] 파일 접근 권한이 없습니다: {filename}')
        return None
    except UnicodeDecodeError:
        print(f'[오류] 파일 인코딩을 읽을d 수 없습니다: {filename}')
        return None
    except OSError as e:
        print(f'[오류] 파일을 여는 중 문제가 발생했습니다: {e}')
        return None


def parse_log(lines):
    """로그 라인을 파싱하여 딕셔너리 리스트로 반환하는 함수."""
    entries = []
    header = True
    for line in lines:
        line = line.strip()
        if not line:
            continue
        if header:
            header = False
            continue
        parts = line.split(',', 2)
        if len(parts) == 3:
            entries.append({
                'timestamp': parts[0],
                'event': parts[1],
                'message': parts[2],
            })
    return entries


def print_log(lines):
    """로그 전체 내용을 화면에 출력하는 함수."""
    print('=' * 60)
    print('       mission_computer_main.log 전체 내용')
    print('=' * 60)
    for line in lines:
        print(line, end='')
    print('=' * 60)


def analyze_and_write_report(entries, report_filename):
    """로그를 분석하고 Markdown 보고서를 작성하는 함수."""
    critical_events = [e for e in entries if 'unstable' in e['message'].lower()
                       or 'explosion' in e['message'].lower()]

    normal_end_events = [e for e in entries if 'mission completed' in e['message'].lower()]
    shutdown_events = [e for e in entries if 'powered down' in e['message'].lower()]

    report_lines = [
        '# 미션 컴퓨터 로그 분석 보고서\n',
        '\n',
        '## 1. 개요\n',
        '\n',
        '본 보고서는 `mission_computer_main.log` 파일을 분석하여 ',
        '화성 기지 사고의 원인을 규명하기 위해 작성되었습니다.\n',
        '\n',
        '---\n',
        '\n',
        '## 2. 로그 요약\n',
        '\n',
        f'- **총 로그 항목 수:** {len(entries)}건\n',
        f'- **기록 시작:** {entries[0]["timestamp"]}\n',
        f'- **기록 종료:** {entries[-1]["timestamp"]}\n',
        '\n',
        '---\n',
        '\n',
        '## 3. 미션 타임라인\n',
        '\n',
        '| 시각 | 이벤트 | 내용 |\n',
        '|------|--------|------|\n',
    ]

    for e in entries:
        report_lines.append(f'| {e["timestamp"]} | {e["event"]} | {e["message"]} |\n')

    report_lines += [
        '\n',
        '---\n',
        '\n',
        '## 4. 사고 원인 분석\n',
        '\n',
        '### 4-1. 정상 미션 완료\n',
        '\n',
    ]

    if normal_end_events:
        for e in normal_end_events:
            report_lines.append(f'- `{e["timestamp"]}` : {e["message"]}\n')
        report_lines.append('\n로켓의 발사, 위성 배치, 착륙까지의 주요 미션은 **정상적으로 완료**되었습니다.\n')
    else:
        report_lines.append('- 정상 완료 이벤트를 찾을 수 없습니다.\n')

    report_lines += [
        '\n',
        '### 4-2. 이상 징후 및 사고 이벤트\n',
        '\n',
    ]

    if critical_events:
        for e in critical_events:
            report_lines.append(f'- `{e["timestamp"]}` : **{e["message"]}**\n')
    else:
        report_lines.append('- 이상 이벤트가 감지되지 않았습니다.\n')

    report_lines += [
        '\n',
        '### 4-3. 시스템 종료\n',
        '\n',
    ]

    if shutdown_events:
        for e in shutdown_events:
            report_lines.append(f'- `{e["timestamp"]}` : {e["message"]}\n')

    report_lines += [
        '\n',
        '---\n',
        '\n',
        '## 5. 결론 및 원인 규명\n',
        '\n',
        '로그 분석 결과, 사고의 원인은 다음과 같이 정리됩니다:\n',
        '\n',
        '1. **미션 자체는 성공적으로 완료되었습니다.**  \n',
        '   로켓 발사 → 위성 배치 → 재진입 → 착륙까지 모든 단계가 정상적으로 수행되었습니다.\n',
        '\n',
        '2. **미션 완료 직후 산소 탱크 이상이 감지되었습니다.**  \n',
        '   `2023-08-27 11:35:00` 시각에 `Oxygen tank unstable` 경고가 기록되었으며,\n',
        '   이는 구조적 결함 또는 착륙 충격으로 인한 탱크 손상을 시사합니다.\n',
        '\n',
        '3. **5분 후 산소 탱크 폭발이 발생하였습니다.**  \n',
        '   `2023-08-27 11:40:00`에 `Oxygen tank explosion` 이벤트가 기록되었습니다.  \n',
        '   불안정 감지 후 어떠한 대응 조치도 로그에 남아 있지 않아,\n',
        '   경보 시스템의 미작동 또는 대응 절차 부재가 피해를 키운 것으로 판단됩니다.\n',
        '\n',
        '4. **폭발 이후 시스템이 전면 중단되었습니다.**  \n',
        '   `2023-08-27 12:00:00`에 미션 컨트롤 시스템이 강제 종료되었습니다.\n',
        '\n',
        '### 핵심 원인 요약\n',
        '\n',
        '> **산소 탱크의 구조적 불안정으로 인한 폭발**이 이번 사고의 직접적 원인이며,  \n',
        '> 이상 감지 후 경보·대응 체계의 부재가 피해를 확대시킨 간접 원인으로 판단됩니다.\n',
        '\n',
        '---\n',
        '\n',
        '## 6. 권고 사항\n',
        '\n',
        '- 산소 탱크에 대한 실시간 압력·온도 모니터링 센서 추가 설치\n',
        '- 이상 감지 시 자동 경보 및 긴급 차단 시스템 구축\n',
        '- 착륙 후 기체 구조 점검 프로토콜 의무화\n',
        '- 비상 대응 매뉴얼 수립 및 정기 훈련 실시\n',
        '\n',
        '---\n',
        '\n',
        '*본 보고서는 mission_computer_main.log 데이터를 기반으로 자동 생성되었습니다.*\n',
    ]

    try:
        with open(report_filename, 'w', encoding='utf-8') as f:
            f.writelines(report_lines)
        print(f'\n[완료] 보고서가 저장되었습니다: {report_filename}')
    except PermissionError:
        print(f'[오류] 보고서 파일 쓰기 권한이 없습니다: {report_filename}')
    except OSError as e:
        print(f'[오류] 보고서 저장 중 문제가 발생했습니다: {e}')


if __name__ == '__main__':
    log_filename = 'mission_computer_main.log'
    report_filename = 'log_analysis.md'

    print('Hello Mars')
    print()

    lines = read_log(log_filename)
    if lines is not None:
        print_log(lines)
        entries = parse_log(lines)
        analyze_and_write_report(entries, report_filename)
