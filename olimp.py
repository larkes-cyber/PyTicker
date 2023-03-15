from functools import lru_cache


n = int(input())


@lru_cache(maxsize=2*n)
def find_best(value):
    global massive

    left, right = indexes[value]

    max_ = 0
    for i in range(left+1, right):
        if rl[i] == -1 and indexes[massive[i]][1] > right:
            max_ = max(max_, find_best(massive[i]))

    return 1 + max_


massive = list(map(int, input().split()))
rl = [0 for i in range(n*2)]
indexes = {}
for i in range(1, n+1):
    left = massive.index(i)
    right = massive[left+1:].index(i) + left + 1
    indexes[i] = [left, right]
    rl[left] = -1
    rl[right] = 1
maxi = 0
for i in range(1, n+1):
    maxi = max(maxi, find_best(i))
print(maxi)
