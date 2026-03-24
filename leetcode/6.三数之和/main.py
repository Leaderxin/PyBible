# 给你一个整数数组 nums ，判断是否存在三元组 [nums[i], nums[j], nums[k]] 满足 i != j、i != k 且 j != k ，
# 同时还满足 nums[i] + nums[j] + nums[k] == 0 。请你返回所有和为 0 且不重复的三元组。

# 注意：答案中不可以包含重复的三元组。

def threeSum(nums):
    """
    :type nums: List[int]
    :rtype: List[List[int]]
    """
    # 如果数组长度小于3，直接返回空列表
    if len(nums) < 3:
        return []
    
    # 对数组进行排序，这是双指针法的前提
    nums.sort()
    result = []
    
    # 遍历数组，将当前元素作为第一个数
    for i in range(len(nums) - 2):
        # 跳过重复的第一个数
        if i > 0 and nums[i] == nums[i - 1]:
            continue
        
        # 如果当前数大于0，由于数组已排序，后面的数都大于0，不可能找到和为0的三元组
        if nums[i] > 0:
            break
        
        # 使用双指针寻找另外两个数
        left = i + 1
        right = len(nums) - 1
        
        while left < right:
            total = nums[i] + nums[left] + nums[right]
            
            if total == 0:
                # 找到一个满足条件的三元组
                result.append([nums[i], nums[left], nums[right]])
                
                # 跳过重复的左指针元素
                while left < right and nums[left] == nums[left + 1]:
                    left += 1
                # 跳过重复的右指针元素
                while left < right and nums[right] == nums[right - 1]:
                    right -= 1
                
                # 移动指针到下一个不同的元素
                left += 1
                right -= 1
            elif total < 0:
                # 和小于0，需要增大左指针的值
                left += 1
            else:
                # 和大于0，需要减小右指针的值
                right -= 1
    
    return result


# 测试用例
if __name__ == "__main__":
    # 测试用例1
    nums1 = [-1, 0, 1, 2, -1, -4]
    print(f"输入: {nums1}")
    print(f"输出: {threeSum(nums1)}")
    print()
    
    # 测试用例2
    nums2 = [0, 1, 1]
    print(f"输入: {nums2}")
    print(f"输出: {threeSum(nums2)}")
    print()
    
    # 测试用例3
    nums3 = [0, 0, 0]
    print(f"输入: {nums3}")
    print(f"输出: {threeSum(nums3)}")
    print()
    
    # 测试用例4
    nums4 = [-2, 0, 1, 1, 2]
    print(f"输入: {nums4}")
    print(f"输出: {threeSum(nums4)}")
    print()
    
    # 测试用例5
    nums5 = []
    print(f"输入: {nums5}")
    print(f"输出: {threeSum(nums5)}")
