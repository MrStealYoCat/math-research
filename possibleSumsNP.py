#!/usr/bin/env python3
import numpy as np
import math
import sys
import time
start_time = time.time()

def permutations(iterable):
    n = len(iterable)
    indices = list(range(n))
    cycles = list(range(n, 0, -1))
    yield iterable
    while True:
        for i in reversed(range(n)):
            cycles[i] -= 1
            if cycles[i] == 0:
                indices[i:] = indices[i+1:] + indices[i:i+1]
                cycles[i] = n - i
            else:
                j = cycles[i]
                indices[i], indices[-j] = indices[-j], indices[i]
                yield [iterable[i] for i in indices]
                break
        else:
            return
A = 200
B = 300
if (len(sys.argv) > 1):
    print(sys.argv[1], sys.argv[2])
    A = int(sys.argv[1])
    B = int(sys.argv[2])
max_digits = int(math.log10(B))+1
max_perms = math.factorial(max_digits)
all_pot_sums = np.arange(B-A, dtype=int) + A
sums = np.zeros(max_perms, dtype=int)
# [[permuted number, sums...]]
calculated_sums = np.zeros(shape=(B-A, max_perms), dtype=int)

for i in range(A, B):
    digits = int(math.log10(i))+1
    num_sums = math.factorial(digits)
    permutes = permutations([x for x in str(i)])
    list_permutes = np.zeros(max_perms, dtype=int)
    list_permutes[0:num_sums] = [int("".join(p)) for p in permutes]
    list_permutes[0:num_sums] += i
    calculated_sums[i-A] = list_permutes
print(calculated_sums.flatten())
print(all_pot_sums)
impossible_sums = np.setdiff1d(all_pot_sums, calculated_sums.flatten())

#possible_sums = np.setdiff1d(all_pot_sums, impossible_sums)
#for arr in calculated_sums:
#    print(arr)
#for sum in impossible_sums:
#    print(sum)
print(impossible_sums)
#print(calculated_sums)
print("{0} seconds for {1} numbers".format(round(time.time() - start_time, 5), B))
# possible_sums = cp.setdiff1d(all_pot_sums, impossible_sums)
# file = open("impossibleSums.txt", "w")
# for x in impossible_sums:
#     file.write("{}\n".format(x))
#file = open("possibleSums.txt", "w")
#for x in calculated_sums:
#    file.write("{}\n".format(x))
