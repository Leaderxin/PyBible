from typing import List
# 给定一个整数数组 nums 和一个整数目标值 target，请你在该数组中找出 和为目标值 target  的那 两个 整数，并返回它们的数组下标。

# 你可以假设每种输入只会对应一个答案，并且你不能使用两次相同的元素。

# 你可以按任意顺序返回答案。

def two_sum(nums: List[int], target: int) -> List[int]:
    """
    在数组中找出和为目标值的两个整数的下标
    
    Args:
        nums: 整数数组
        target: 目标值
    
    Returns:
        两个整数在数组中的下标
    """
    # 从数组末尾开始向前遍历，这样可以保证找到的第一个解就是正确的
    # range(len(nums)-1, -1, -1) 生成从最后一个索引到0的序列
    for i in range(len(nums)-1,-1,-1):
        # 计算补数：目标值减去当前元素的值
        # 如果 nums[i] + complement = target，那么 complement 就是我们要找的另一个数
        complement = target - nums[i]
        
        # 在当前元素之前的所有元素中查找补数
        # nums[:len(nums)-1] 表示从数组开头到倒数第二个元素的所有元素
        # 这样可以避免重复使用同一个元素
        if(complement in nums[:len(nums)-1]):
            # 找到补数后，返回当前元素的下标和补数的下标
            # nums.index(complement) 返回补数在数组中第一次出现的下标
            return [i,nums.index(complement)]    
    # 如果没有找到答案（题目保证有答案，所以这里不会执行到这里）
    raise ValueError("No two sum solution")


# 测试用例
if __name__ == "__main__":
    # 示例 1
    nums1 = [2, 7, 11, 15]
    target1 = 9
    result1 = two_sum(nums1, target1)
    print(f"示例 1: nums = {nums1}, target = {target1}")
    print(f"输出: {result1}")  # 预期输出: [0, 1]
    
    # 示例 2
    nums2 = [3, 2, 4]
    target2 = 6
    result2 = two_sum(nums2, target2)
    print(f"\n示例 2: nums = {nums2}, target = {target2}")
    print(f"输出: {result2}")  # 预期输出: [1, 2]
    
    # 示例 3
    nums3 = [3, 3]
    target3 = 6
    result3 = two_sum(nums3, target3)
    print(f"\n示例 3: nums = {nums3}, target = {target3}")
    print(f"输出: {result3}")  # 预期输出: [0, 1]
