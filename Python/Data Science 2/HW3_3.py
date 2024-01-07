def get_index_sorted_non_unique(arr,elem):
    n = len(arr)
    f = 0
    while n - f > 1:
        mid = (n + f) // 2
        if arr[mid] < elem:
            f = mid + 1
            if arr[f] == elem:
                return f
        else:
            n = mid
    return -1

testarray = [([-17, -10, -3, -3, -3, -3, -3, 10, 15],-3),([-17, -10, -3, -3, -3, -3, -3, 10, 15],7),([-17, -10, -3, 0, 0, 3, 5, 5, 10, 15],5),([],5),([-17, -10, -3, 0, 0, 3, 5, 5, 10, 15],0)]

for i in testarray:
    print(get_index_sorted_non_unique(*i))
