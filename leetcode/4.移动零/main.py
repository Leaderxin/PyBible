# 给定一个数组 nums，编写一个函数将所有 0 移动到数组的末尾，同时保持非零元素的相对顺序。

# 请注意 ，必须在不复制数组的情况下原地对数组进行操作。
from typing import List

def moveZeroes(nums: List[int]) -> None:
    max_index = len(nums) - 1
    current_index = 0
    while current_index < max_index:
        if nums[current_index] == 0:
            nums.append(nums.pop(current_index))
            max_index -= 1
        else:
            current_index += 1
case1 = [0,1,0,3,12]
moveZeroes(case1)
print(case1)