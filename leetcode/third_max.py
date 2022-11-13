class Solution(object):
    def thirdMax(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        res = set()
        m = None
        for i in nums:
            if len(res) < 3:
                res.add(i)
                m = min(res)

                continue
            j = 0
            print(res)
            if i>m and i not in res:
                res = list(res)
                index = res.index(m)
                del res[index]
                res.append(i)
                res = set(res)
                m = min(res)
            print(res)
        if len(res)<3:
            return max(res)
        else:
            return min(res)

print(Solution().thirdMax([1,2,2,5,3,5]))
print(Solution().thirdMax([1,2,2,5,3,5]))
print(Solution().thirdMax([1,2,2]))
print(Solution().thirdMax([1,2]))
print(Solution().thirdMax([1,2]))
print(Solution().thirdMax([2,2,3,1]))