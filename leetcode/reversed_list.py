# Definition for singly-linked list.
class ListNode(object):
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next
class Solution(object):
    def reverseList(self, head):
        """
        :type head: ListNode
        :rtype: ListNode
        """
        newhead = ListNode()
        newhead.val=head.val
        newhead.next = None

        newtail = newhead
        head = head.next
        # newtail.next = None
        # cur = head
        while head:
            newhead = head
            # newhead.next

            head = head.next
            newhead.next = newtail
            newtail = newhead

        return newhead

    def reverseList2(self, head):
        if not head or not head.next:
            return head

        p = self.reverseList2(head.next)
        head.next.next = head
        head.next = None

        return p

head = ListNode(1)
head.next= ListNode(2)
head.next.next= ListNode(3)
head.next.next.next= ListNode(4)
head.next.next.next.next= ListNode(5)
r = Solution().reverseList2(head)
# r = Solution().reverseList(head)

while r:
    print(r.val)
    r = r.next