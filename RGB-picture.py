import numpy as np
from PIL import Image
import pytesseract
import argparse
import colorama
import os
from pathlib import Path
import shutil
colorama.init()

parser = argparse.ArgumentParser()
parser.add_argument('-f', type=str, default=None, required=True,
                    help='输入文件名称')
parser.add_argument('-min', type=int, default=1,
                    help='指定宽高最小尺寸，默认为1')
parser.add_argument('-cut', type=str, default=',',
                    help='指定rgb值分割符，默认为","')
parser.add_argument('--ocr',action='store_true',
                    help='对生成图片进行OCR')

args = parser.parse_args()

file_path = Path(args.f)
dir_path = os.path.dirname(os.path.abspath(file_path))
min=args.min
ocr=args.ocr
cut=args.cut

output_path=os.path.join(dir_path,'output')
if os.path.exists(output_path):
    shutil.rmtree(output_path, ignore_errors=True)
os.makedirs(output_path)


#获取所有公因数
def get_factors(num,min):
    factors = []
    for i in range(min, num + 1):
        if num % i == 0:
            factors.append(i)
    return factors

with open(file_path, 'r') as file:
    lines = file.readlines()
num_lines = len(lines)

factors = get_factors(num_lines,min)
num_factors = len(factors)

print('正在生成图片请稍等...')
for i in range(num_factors):
    width = factors[i]
    height = num_lines // width

    # 构造像素矩阵
    pixels = np.zeros((height, width, 3), dtype=np.uint8)
    for j in range(num_lines):
        row = j // width
        col = j % width
        pixel = lines[j].strip().strip('(').strip(')').split(cut)
        pixels[row, col] = [int(p) for p in pixel]

    # 创建图像对象并保存
    image = Image.fromarray(pixels, 'RGB')
    image.save(f'{output_path}/{width}x{height}.png')
print('生成图片已保存在output目录下！')


#OCR
if ocr:
    flag_results = []
    for i in range(num_factors):
        width = factors[i]
        height = num_lines // width
        image_path = f'output/{width}x{height}.png'

        try:
            result = pytesseract.image_to_string(image_path).strip('\r\n')
            if result:
                if 'flag' in result.lower():
                    flag_results.append(result)
                    print(f'{image_path}: \033[31m{result}\033[0m')
                else:
                    print(f'{image_path}: {result}')
        except pytesseract.TesseractError:
            pass
    if flag_results:
        print('--------------------------')
        print('找到的包含flag字段：')
        for flag in flag_results:
            print(f'\033[31m{flag}\033[0m')
os.system("pause")
