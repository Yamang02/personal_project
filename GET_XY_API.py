import requests
import json
import os

# 설정 파일 읽기
with open('app_settings.json', 'r') as settings_file:
    settings = json.load(settings_file)

rest_api_key = settings['rest_api_key']
url = settings['urls']['GET_XY']
domain = settings['domain']

# 검색할 장소 이름을 입력하세요
query = '박달 우성아파트'

# 결과 JSON 파일 경로
json_file_path = 'XY_RESULT.json'

# 기존 JSON 파일 읽기 또는 새로 생성
if os.path.exists(json_file_path):
    with open(json_file_path, 'r') as json_file:
        existing_data = json.load(json_file)
else:
    existing_data = {}

# 기존 데이터에 쿼리가 있는지 확인
if query in existing_data:
    print(f'쿼리 "{query}"에 대한 데이터가 이미 존재합니다: {existing_data[query]}')
else:
    # API 호출 URL 생성
    full_url = f'{url}{query}'

    # 요청 헤더에 API 키와 도메인 추가
    headers = {
        'Authorization': f'KakaoAK {rest_api_key}',
        'Referer': domain
    }

    # API 호출
    response = requests.get(full_url, headers=headers)

    # 응답 데이터 확인
    if response.status_code == 200:
        data = response.json()
        if data['documents']:
            # 첫 번째 결과의 x, y 값 가져오기
            x = data['documents'][0]['x']
            y = data['documents'][0]['y']
            
            # JSON 데이터 생성
            json_data = {
                'x': x,
                'y': y
            }
            
            # 새로운 데이터 추가
            existing_data[query] = json_data
            
            # JSON 파일로 저장
            with open(json_file_path, 'w') as json_file:
                json.dump(existing_data, json_file, indent=4, ensure_ascii=False)
            
            print(f'쿼리 "{query}"에 대한 데이터가 저장되었습니다: {json_data}')
        else:
            print('검색 결과가 없습니다.')
    else:
        print(f'API 호출 실패: {response.status_code}')