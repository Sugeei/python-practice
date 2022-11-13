# Trapping Rain Water
# coding=utf-8

# 未完成
def get_max_index(input_list, low, high):
    sublist = input_list[low:high + 1]
    # maxindex = sublist.find(max(sublist))
    maxindex = sublist.index(max(sublist))
    return low + maxindex


def trap_rain(input_list, i, low, high):
    # left
    left = 0
    right = 0

    if i == 0:
        left = 0
    else:

        max_left = get_max_index(input_list, low, i - 1)
        if max_left <= 1:
            left = 0
        else:

            left = trap_rain(input_list, max_left, low, i - 1)

    if i == len(input_list) - 1:
        right = 0

    else:

        max_right = get_max_index(input_list, i+1, high)
        if max_right >= len(input_list) - 2:
            right = 0
        else:
            right = trap_rain(input_list, max_right, i+1, high)

    return left + right

if __name__ == "__main__":
    a = [0,1,0,2,1,0,1,3,2,1,2,1]

    # print trap_rain(a, 7, 0, len(a)-1)
