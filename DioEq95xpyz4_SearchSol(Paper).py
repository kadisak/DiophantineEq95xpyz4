import math,gmpy2,time,multiprocessing
from multiprocessing import Pool, current_process
def is_prime(num):
    if num==2 or num==3: return True
    if num%2==0 or num<2: return False
    r = int(num**0.5)
    for i in range(3,r+1,2):
        if num%i == 0: return False
    return True
def is_fourth_power(x):
    if x < 0: return False
    root = gmpy2.iroot(x, 4)    # returns (root, exact_bool)
    return root[1]              # True if exact 4th power
def integer_fourth_root(x):
    if x < 0: raise ValueError("x must be non-negative")
    if x == 0 or x == 1: return x
    low, high = 0, x
    while low <= high:
        mid = (low + high) // 2
        mid_pow4 = mid**4
        if mid_pow4 == x: return mid
        elif mid_pow4 < x: low = mid + 1
        else: high = mid - 1
    return high  # `high` will be the integer part of 4th root of x
def is_perfect_fourth_power(x):
    root = integer_fourth_root(x)
    return root**4 == x
def classify_solution(sol):
    x,y,z,p = sol
    if z%30 in {2,4,8,14,16,22,26,28}:
        if p%240==29 and (x-y)%4==0:    return 'A'
        elif p%240==149 and (x-y)%4!=0: return 'B'
    return None
def search_solution(p):
    x_max = 1000
    results = []
    for x in range(1,x_max+1,2):
        y_max=math.floor(math.log(9*5**x,p))
        for y in range(1,y_max+1,2):
            z_power4  = 9*5**x-p**y
            if is_perfect_fourth_power(z_power4):
                z = integer_fourth_root(z_power4)
                class_solution = classify_solution((x,y,z,p))
                results.append((x,y,z,p,class_solution))
    return results
if __name__=='__main__':
    num_cores = multiprocessing.cpu_count()
    print(f"Number of CPU cores available: {num_cores}")
    #### parameters ####
    prime_max = 10**8
    ####################
    primes = []
    for p in range(2,prime_max+1):
        if is_prime(p): primes.append(p)
    primes = [p for p in primes if p%240==29 or p%240==149]
    with Pool(processes=num_cores) as pool:
        results = pool.map(search_solution, primes)
    results = [result for result in results if len(result)>0]
    print("Results:", results)