from App.Helpers import *
import multiprocessing as mp
import os
from App.database.models import Settings
l = getLogging("younes", "temp/logs/younes.log")
m = importlib.import_module("temp.test2")
m.funcman()
"""
### Explanation:

### Args:

### return:

"""

# def info(title):
#     print(title)
#     print('module name:', __name__)
#     print('parent process:', os.getppid())
#     print('process id:', os.getpid())
    
    

# def f(n):
#     add2memory(**{f"test{n}":f"Hello World {n}"})
#     info(f'function f {n}')
#     print("global mem ", memory().get(f"test{n}"))
#     print("===============================")

# if __name__ == '__main__':
#     print("===============================")
#     # add2memory(test="Hello World")
    
#     # ctx = mp.get_context('fork')
#     # p = ctx.Process(target=f, args=("1",))
#     # p2 = ctx.Process(target=f, args=("2",))
 
#     p = mp.Process(target=f, args=("1",))
#     p2 = mp.Process(target=f, args=("2",))


#     p.start()
#     p2.start()

#     p.join()
#     p2.join()

#     print(memory().get("test"))