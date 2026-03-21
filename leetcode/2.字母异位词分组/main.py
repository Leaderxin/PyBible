# 给你一个字符串数组，请你将 字母异位词 组合在一起。可以按任意顺序返回结果列表。

 

# 示例 1:

# 输入: strs = ["eat", "tea", "tan", "ate", "nat", "bat"]

# 输出: [["bat"],["nat","tan"],["ate","eat","tea"]]

# 解释：

# 在 strs 中没有字符串可以通过重新排列来形成 "bat"。
# 字符串 "nat" 和 "tan" 是字母异位词，因为它们可以重新排列以形成彼此。
# 字符串 "ate" ，"eat" 和 "tea" 是字母异位词，因为它们可以重新排列以形成彼此。
from collections import defaultdict

def groupAnagrams(strs):
    anagram_map = defaultdict(list)
    
    for s in strs:
        # 对字符串进行排序，作为键
        sorted_str = ''.join(sorted(s))
        anagram_map[sorted_str].append(s)
    
    # 返回所有分组的值
    return list(anagram_map.values())
# 测试示例
strs = ["eat", "tea", "tan", "ate", "nat", "bat"]
print(groupAnagrams(strs))
strs = ["",""]
print(groupAnagrams(strs))