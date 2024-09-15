# import datetime
#
#
# n = 100000000
# lst = list(range(n))
#
# start = datetime.datetime.now().time()
# lst[len(lst) - 1]
# end = datetime.datetime.now().time()
# print(end - start
import time
from functools import wraps

# append -> O(n)
# pop() с конца O(1)
# pop(index) -> O(n)
# for - быстрее всего напрямую работает с последовательностью
# enumerate принцип как у for + index > for
# range while  самые медленные
# compr - хорош не для сильно больших последовательностях (преобразование формы списка в другую)


def measure_time(f):
    wraps(f)

    def wrapper(*args, **kwargs):
        start = time.time() * 1000
        result = f(*args, **kwargs)
        end = time.time() * 1000
        print(f"{f.__name__} => {end - start}")

    return wrapper


n = 100
lst = list(range(n))

#
# @measure_time
# def for_loop():
#     for el in lst:
#         el += 1
#
#
# @measure_time
# def lst_compr():
#     [x + 1 for x in lst]
#
#
# @measure_time
# def enumerate_loop():
#     for index, element in enumerate(lst):
#         element += 1
#
#
# @measure_time
# def for_with_range():
#     for i in range(len(lst)):
#         lst[i] += 1
#
#
# @measure_time
# def while_loop():
#     counter = 0
#     while counter < len(lst):
#         lst[counter] += 1
#         counter += 1
#
#
# for_loop()
# lst_compr()
# enumerate_loop()
# for_with_range()
# while_loop()


min_elem = sorted(lst)[0]
print(min_elem)
p = float("inf")
print(p)

with open("my.txt", "w") as file:
    file.write("mmmm")
    print(file.fileno(), "file")
