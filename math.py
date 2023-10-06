import cupy as cp
import functools as feet
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

A = 10
B = 100000
with cp.cuda.Device(1):
    all_pot_sums = cp.arange(B-11) + 11
    calculated_sums = cp.array([])

    addition = cp.ElementwiseKernel(
        'S a, S b',
        'S c',
        'c = a + b',
        'addition')

    # combine = cp.ElementwiseKernel(
    #     'S p',
    #     'S c',
    #     '''
    #     for(int i=0;i<sizeof(p);i++){
    #           c = p;
    #         }''',
    #     'combine')

    for i in range(A, B):
            permutes = permutations([x for x in str(i)])
            list_permutes = cp.array([int("".join(p)) for p in permutes])
            #list_permutes = cp.array([''.join(map(str, p)) for p in permutes])
            #list_permutes = [int(bytes(map(ord("0").__add__,p))) for p in permutes]
            #calculated_sums = cp.append(calculated_sums, addition(i, cp.array([int("".join(p)) for p in permutes])))
            calculated_sums = cp.append(calculated_sums, addition(i, list_permutes))
            #print(list_permutes)

    impossible_sums = cp.setdiff1d(all_pot_sums, calculated_sums)
    #print(impossible_sums)
    print("{0} seconds for {1} numbers".format(round(time.time() - start_time, 5), B))

# file = open("impossibleSums.txt", "w")
# for x in impossible_sums:
#     file.write("{}\n".format(x))
file = open("impossibleSums.txt", "w")
for x in impossible_sums:
    file.write("{}\n".format(x))
