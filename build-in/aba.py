class Solution(object):
    def longestPalindrome(self, s):
        """
        :type s: str
        :rtype: str
        """
        m = {}

        if len(s) <= 1:
            return s
        def check(s, l, h):
            if l >= h:
                return True
            if s[l] != s[h]:
                return False
            if check(s, l + 1, h - 1):
                return True
            else:
                return False

        p = []
        for i, v in enumerate(s):
            if m.get(v) is None:
                m[v] = []
            for j in m.get(v):
                # vif v in m:
                if check(s, j, i):
                    p.append(s[j:i+1])
            m[v].append(i)

        l = [len(x) for x in p]
        if len(l) > 0:
            return p[l.index(max(l))]
        else:
            return s[0]

s='abababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababababa'
print(Solution().longestPalindrome(s))
s='a'
print(Solution().longestPalindrome(s))
s = "babad"
print(Solution().longestPalindrome(s))
s='ac'
print(Solution().longestPalindrome(s))
s=''
print(Solution().longestPalindrome(s))
