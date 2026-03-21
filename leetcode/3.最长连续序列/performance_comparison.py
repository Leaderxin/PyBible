"""
性能对比：set vs list 在查找操作上的差异
"""

import time
from typing import List

def longestConsecutive_with_list(nums: List[int]) -> int:
    """使用 list 查找 - 时间复杂度 O(n²)"""
    if not nums:
        return 0
    
    max_length = 0
    
    # 遍历列表中的每个数字
    for num in nums:
        # 只有当 num 是序列的起点时（即 num-1 不在列表中），才开始计算序列长度
        if num - 1 not in nums:  # list 查找：O(n)
            current_num = num
            current_length = 1
            
            # 向后查找连续的数字
            while current_num + 1 in nums:  # list 查找：O(n)
                current_num += 1
                current_length += 1
            
            # 更新最大长度
            max_length = max(max_length, current_length)
    
    return max_length

def longestConsecutive_with_set(nums: List[int]) -> int:
    """使用 set 查找 - 时间复杂度 O(n)"""
    if not nums:
        return 0
    
    # 将数组转换为集合，实现 O(1) 的查找
    num_set = set(nums)
    max_length = 0
    
    # 遍历集合中的每个数字
    for num in num_set:
        # 只有当 num 是序列的起点时（即 num-1 不在集合中），才开始计算序列长度
        if num - 1 not in num_set:  # set 查找：O(1)
            current_num = num
            current_length = 1
            
            # 向后查找连续的数字
            while current_num + 1 in num_set:  # set 查找：O(1)
                current_num += 1
                current_length += 1
            
            # 更新最大长度
            max_length = max(max_length, current_length)
    
    return max_length

# 测试数据
test_data = list(range(1, 10001))  # 1 到 10000 的连续序列

print("=" * 60)
print("性能对比测试")
print("=" * 60)
print(f"测试数据大小: {len(test_data)} 个元素")
print()

# 测试 list 版本
print("使用 list 查找...")
start_time = time.time()
result_list = longestConsecutive_with_list(test_data)
end_time = time.time()
time_list = end_time - start_time
print(f"结果: {result_list}")
print(f"耗时: {time_list:.4f} 秒")
print()

# 测试 set 版本
print("使用 set 查找...")
start_time = time.time()
result_set = longestConsecutive_with_set(test_data)
end_time = time.time()
time_set = end_time - start_time
print(f"结果: {result_set}")
print(f"耗时: {time_set:.4f} 秒")
print()

# 性能对比
print("=" * 60)
print("性能对比结果")
print("=" * 60)
print(f"set 比 list 快 {time_list / time_set:.2f} 倍")
print(f"set 节省了 {(time_list - time_set) / time_list * 100:.2f}% 的时间")
print()

# 理论分析
print("=" * 60)
print("理论分析")
print("=" * 60)
print("list 查找操作:")
print("  - 时间复杂度: O(n)")
print("  - 需要逐个遍历元素进行比较")
print()
print("set 查找操作:")
print("  - 时间复杂度: O(1)")
print("  - 通过哈希表直接定位元素")
print()
print("在这个问题中:")
print("  - list 版本总复杂度: O(n²)")
print("  - set 版本总复杂度: O(n)")
print("  - 当 n = 10000 时，set 版本理论上快 10000 倍")