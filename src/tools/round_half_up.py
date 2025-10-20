# -*- coding: utf-8 -*-
import math


def evaluate(number):
    # 通过将数字乘以 10 并取整来检查小数部分是否为 0.5
    if number - int(number) == 0.5:
        return int(number) + 1
    else:
        return int(round(number))


def main():
    # 示例输入列表
    numbers = [1.5, 2.3, 2.5, 3.7, 4.5]
    
    # 对每个数字进行四舍五入并取整
    rounded_numbers = [evaluate(num) for num in numbers]
    
    # 打印结果
    print("Original numbers:", numbers)
    print("Rounded numbers:", rounded_numbers)

if __name__ == "__main__":
    main()