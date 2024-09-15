# asyncio.get_event_loop().run_until_complete(run())
# def func():
#     p = 6
#
#
# if func() is None:
#     print("func is None")
#
# p = 4
# print(id(p))
# import asyncpg
# from asyncpg.ex
# import asyncio
#
#
# async def create_connection():
#     conn = await asyncpg.connect(
#         "postgresql://postgres:postgres@localhost:5432/testing"
#     )
#     await conn.execute("""DROP TABLE products;""")
#     await conn.close()
#
#
# asyncio.run(create_connection())


# import bcrypt
#
# hashed = bcrypt.hashpw(
#     b"very sycret",
#     bcrypt.gensalt(),
# )
# print(hashed)
# if bcrypt.checkpw(b"very sycret", hashed):
#     print("fdsffdsf")
# p = {}
# p.update({"f": "f"})
# print(p)
# l = {"f": {"d", 0}}

import time


n = 100_000_000
lst = list(range(n))
start = time.time()
lst[len(lst) - 1]
end = time.time()
print(end - start)
