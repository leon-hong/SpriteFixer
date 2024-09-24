from collections import Counter
from PIL import Image
from typing import List, Tuple
import os

"""
주어진 폴더의 모든 파일을 가져오는 함수

:param folder_path: 파일을 가져올 폴더의 경로
:return: 폴더 내의 모든 파일 경로 리스트
"""
def get_all_files(folder_path: str) -> List[str]:

    files: List[str] = []
    
    # 폴더 내의 모든 항목 가져오기
    for item in os.listdir(folder_path):
        item_path: str = os.path.join(folder_path, item)
        
        # 항목이 파일인지 확인
        if os.path.isfile(item_path):
            files.append(item_path)    
    
    return files

"""
가장 많이 등장한 색상 찾기
반환값: (가장 많이 등장한 색상, 등장 횟수)
"""
def findMostColor(image: Image.Image) -> Tuple[Tuple[int, int, int], int]:
    # 픽셀 데이터 가져오기
    pixels: List[Tuple[int, int, int]] = list(image.getdata())

    # 각 픽셀의 색상 카운트
    color_counts: Counter = Counter(pixels)

    # 가장 많이 등장한 색상 찾기
    most_common_color: Tuple[Tuple[int, int, int], int] = color_counts.most_common(1)[0]

    return most_common_color

"""
주어진 이미지 파일들 중 가장 큰 너비와 높이를 구하는 함수

:param image_paths: 이미지 파일 경로 리스트
:return: 가장 큰 너비와 높이
"""
def get_max_dimensions(images: List[Image.Image]) -> Tuple[int, int]:
    max_width: int = 0
    max_height: int = 0
    
    for img in images:        
        width, height = img.size
        if width > max_width:
            max_width = width
        if height > max_height:
            max_height = height

    return max_width, max_height


"""
주어진 너비와 높이로 빈 이미지를 생성하는 함수

:param width: 이미지의 너비
:param height: 이미지의 높이
:param color: 이미지의 배경색 (기본값은 흰색)
:return: 생성된 빈 이미지
"""
def create_blank_image(width: int, height: int, color: Tuple[int, int, int] = (255, 255, 255)) -> Image.Image:
    return Image.new('RGB', (width, height), color)


"""
빈 이미지에 주어진 이미지를 왼쪽 하단을 기준으로 붙여넣는 함수

:param dest_image: 복사될 이미지
:param image_src: 붙여넣을 이미지 파일 경로
:return: 이미지가 붙여넣어진 이미지
"""
def copy_image_LB(dest: Image.Image, src: Image.Image) -> Image.Image:
    width, height = src.size
    # 왼쪽 하단을 기준으로 위치 계산
    position = (0, dest.height - height)
    dest.paste(src, position)
    
    return dest


"""
Main 함수
"""
if __name__ == "__main__":

    print("Start.")

    # 이미지 폴더 경로
    dir_src: str = 'D:/temp/img_src'
    dir_dest: str = 'D:/temp/img_dest2'

    # 이미지 원본 폴더가 없으면 오류
    if not os.path.exists(dir_src):
        print("Error : " + dir_src + " does not exist.")
        exit()

    # 출력 폴더가 없으면 생성
    if not os.path.exists(dir_dest):
        os.makedirs(dir_dest)

    # 이미지들 경로
    all_files: List[str] = get_all_files(dir_src)    

    # 이미지들
    images: List[Image.Image] = [Image.open(image_path) for image_path in all_files]
    
    # 가장 많이 등장한 색상 찾기
    most_common_color: Tuple[Tuple[int, int, int], int]  = findMostColor(images[0])
    print(f"가장 많이 등장한 색상: {most_common_color[0]}, 등장 횟수: {most_common_color[1]}")
    
    # 이미지 파일들 중 가장 큰 너비와 높이 구하기
    dim:Tuple[int, int] = get_max_dimensions(images)
    print(f"가장 큰 너비: {dim[0]}, 가장 큰 높이: {dim[1]}")
    
    # 가장 큰 사이즈의 빈 이미지 생성
    for img in images:        
        blank_image: Image.Image = create_blank_image(dim[0], dim[1], most_common_color[0])
        copy_image_LB(blank_image, img)
        output_path = dir_dest + '/' + os.path.basename(img.filename)
        blank_image.save(output_path)
        print(f"Complete : {output_path}")
        
    print("End.")
