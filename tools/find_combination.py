#!/usr/bin/env python3

def find_combinations_to_target(numbers, target):
    """
    找到数值组合，通过加减运算得到目标值
    """
    from itertools import combinations, product
    
    results = []
    n = len(numbers)
    
    # 尝试不同数量的数字组合
    for r in range(1, min(n + 1, 8)):  # 限制组合数量，避免计算量过大
        for combo in combinations(range(n), r):
            # 对于每个组合，尝试所有可能的加减号组合
            for signs in product([1, -1], repeat=len(combo)):
                total = sum(numbers[i] * sign for i, sign in zip(combo, signs))
                if total == target:
                    result_items = []
                    for i, sign in zip(combo, signs):
                        if sign == 1:
                            result_items.append(f"+{numbers[i]}")
                        else:
                            result_items.append(f"-{numbers[i]}")
                    
                    # 格式化输出
                    expression = " ".join(result_items)
                    if expression.startswith("+"):
                        expression = expression[1:]  # 去掉开头的加号
                    
                    results.append({
                        'expression': expression,
                        'numbers': [numbers[i] for i in combo],
                        'signs': list(signs),
                        'total': total
                    })
    
    return results

# 给定的数值
numbers = [536, 346, 55, 910716, 145563, 16, 340715, 14585, 2829, 101, 4900222, 2314, 784172, 34684117, 86, 370, 22345]
target = 2062

print(f"寻找组合得到目标值: {target}")
print(f"可用数值: {numbers}")
print(f"数值总数: {len(numbers)}")
print("-" * 50)

# 查找组合
results = find_combinations_to_target(numbers, target)

if results:
    print(f"找到 {len(results)} 个可能的组合:")
    print()
    
    for i, result in enumerate(results[:10], 1):  # 只显示前10个结果
        print(f"方案 {i}:")
        print(f"  表达式: {result['expression']} = {result['total']}")
        print(f"  使用数值: {result['numbers']}")
        print()
        
    if len(results) > 10:
        print(f"... 还有 {len(results) - 10} 个组合未显示")
else:
    print("未找到任何组合能够得到目标值 2062")
    
    # 显示一些接近的结果
    print("\n尝试寻找最接近的组合...")
    close_results = []
    
    # 简化搜索，只尝试较少的组合
    for r in range(1, min(len(numbers) + 1, 6)):
        for combo in combinations(range(len(numbers)), r):
            for signs in product([1, -1], repeat=len(combo)):
                total = sum(numbers[i] * sign for i, sign in zip(combo, signs))
                diff = abs(total - target)
                if diff < 1000:  # 差值小于1000的认为是接近的
                    close_results.append({
                        'total': total,
                        'diff': diff,
                        'combo': combo,
                        'signs': signs
                    })
    
    # 按差值排序，显示最接近的几个
    close_results.sort(key=lambda x: x['diff'])
    
    if close_results:
        print("最接近的几个组合:")
        for i, result in enumerate(close_results[:5], 1):
            expression_parts = []
            for j, sign in zip(result['combo'], result['signs']):
                if sign == 1:
                    expression_parts.append(f"+{numbers[j]}")
                else:
                    expression_parts.append(f"-{numbers[j]}")
            
            expression = " ".join(expression_parts)
            if expression.startswith("+"):
                expression = expression[1:]
                
            print(f"  {expression} = {result['total']} (差值: {result['diff']})")