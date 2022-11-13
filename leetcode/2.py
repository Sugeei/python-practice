# Definition for singly-linked list.
class ListNode(object):
    def __init__(self, x):
        self.val = x
        self.next = None


# Definition for singly-linked list.
# class ListNode(object):
#     def __init__(self, x):
#         self.val = x
#         self.next = None

class Solution(object):
    def addTwoNumbers(self, l1, l2):
        """
        :type l1: ListNode
        :type l2: ListNode
        :rtype: ListNode
        """
        md = 0
        l = l1
        r = []
        while l1 or l2:
            if l1 and l2:
                s = l1.val + l2.val
                d = 0
                if s > 9:
                    d = int(s / 10)
                    s = s - 10 * d
                l1.val = s + md
                r.append(s + md)
                md = d

                l1 = l1.next
                l2 = l2.next
            elif l1:
                # r.append(l1.val)
                l1.val += md
                l1 = l1.next
                # break
            elif l2:
                l1.next = l2
                l1 = l2
                l1.val+=md
                # l2 = l2.next

        if md > 0:
            el = ListNode(md)
            # r.append[md]
            while l1.next:
                l1 = l1.next
            l1.next = el
        return l

l1 = ListNode(2)
l1.next = ListNode(4)
# l1.next.next = ListNode(3)

l2 = ListNode(5)
l2.next = ListNode(6)
l2.next.next = ListNode(4)

l = Solution().addTwoNumbers(l1, l2)
while l:
    print(l.val)
    l = l.next