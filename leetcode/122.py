class Solution(object):
    def maxProfit(self, prices):
        """
        :type prices: List[int]
        :rtype: int
        """
        l = prices[0]
        h = l

        s = 0
        for p in prices[1:]:
            if p < l:
                l = p
                h = p
            elif p > h:
                h = p

            if h >= l:
                s += h - l
                l = h
        return s

prices = [7,1,5,3,6,4]
prices = [1,2,3,4,5]
prices = [7,6,4,3,1]
print(Solution().maxProfit(prices))