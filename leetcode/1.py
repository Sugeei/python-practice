class Solution(object):
    def threeSumClosest(self, nums, target):
        """
        :type nums: List[int]
        :type target: int
        :rtype: int
        """
        s = 0
        # nums.sort()
        i=0
        gap = nums[i]+nums[i+1]+nums[i+2]
        res = gap
        gap = abs(gap-target)
        for i in range(0,len(nums)-2):
            s= nums[i]+nums[i+1]+nums[i+2]
            # s1 =

            if abs(target - s) < gap:
                gap = abs(target - s)
                res = s
            print("gap ,s,res")
            print(gap, s,res)
        return res

input = [-1,2,1,-4]
# input = [0,1,2]
input = [1,1,-1,-1,3]
# 3
print(Solution().threeSumClosest(input, 3))