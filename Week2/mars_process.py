import pickle

def process_mars_inventory():
    project_file = 'Mars_Base_Inventory_List.csv'
    danger_project_file = 'Mars_Base_Inventory_danger.csv'
    bin_project_file = 'Mars_Base_Inventory_List.bin'
    
    inventory_list = []
    
    try:
        # 1. 파일 읽기 및 원본 내용 출력
        with open(project_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            
            if not lines:
                print('파일 내용이 비어 있습니다.')
                return
            
            print('--- [1] Mars_Base_Inventory_List.csv 원본 내용 출력 ---')
            for line in lines:
                print(line.strip())
            
            # 2. Python 리스트 객체로 변환
            header_str = lines[0].strip()
            for line in lines[1:]:
                if line.strip():
                    row = line.strip().split(',')
                    # 인화성 지수(인덱스 4)를 정렬을 위해 float으로 변환
                    try:
                        row[4] = float(row[4])
                    except ValueError:
                        row[4] = 0.0
                    inventory_list.append(row)
        
        print('\n[2] 리스트 객체 변환 완료.')

        # 3. 인화성 지수 기준 내림차순 정렬
        inventory_list.sort(key=lambda x: x[4], reverse=True)

        # 4. 인화성 지수 0.7 이상 추출 및 출력
        danger_list = [item for item in inventory_list if item[4] >= 0.7]
        
        print('\n--- [3, 4] 인화성 0.7 이상 위험 물질 목록 (정렬됨) ---')
        print(header_str)
        for item in danger_list:
            print(','.join(map(str, item)))

        # 5. 위험 물질 목록을 CSV 파일로 저장
        try:
            with open(danger_project_file, 'w', encoding='utf-8') as f:
                f.write(header_str + '\n')
                for item in danger_list:
                    f.write(','.join(map(str, item)) + '\n')
            print(f'\n[5] {danger_project_file} 저장 완료.')
        except IOError as e:
            print(f'CSV 쓰기 중 오류 발생: {e}')

        # 보너스 과제: 이진 파일 저장 및 읽기
        try:
            # 이진 파일로 저장
            with open(bin_project_file, 'wb') as f:
                pickle.dump(inventory_list, f)
            print(f'\n[Bonus] {bin_project_file} 이진 파일 저장 완료.')

            # 이진 파일 읽기
            with open(bin_project_file, 'rb') as f:
                loaded_data = pickle.load(f)
            
            print('\n--- [Bonus] 이진 파일(bin)로부터 로드된 내용 (상위 5개) ---')
            for row in loaded_data[:5]:
                print(row)
        except (IOError, pickle.PickleError) as e:
            print(f'이진 파일 처리 중 오류 발생: {e}')

    except FileNotFoundError:
        print(f'오류: {project_file} 파일을 찾을 수 없습니다.')
    except Exception as e:
        print(f'예상치 못한 예외 발생: {e}')

if __name__ == '__main__':
    process_mars_inventory()