from pathos.multiprocessing import ProcessingPool
import time
import sys
import datetime


class tester:
    def __init__(self):
        self.pool=ProcessingPool(2)

    def func(self,msg):
        print(str(datetime.datetime.now()))
        for i in range(1):
            print(msg)
            sys.stdout.flush()
        time.sleep(2)    

#----------------------------------------------------------------------
    def worker(self):
        """"""
        pool=self.pool
        for i in range(10):
               msg = "hello %d" %(i)
               pool.map(self.func,[i])
        pool.close()
        pool.join()
        time.sleep(40)



if __name__ == "__main__":
    print(datetime.datetime.now())
    t=tester()
    t.worker()
    time.sleep(60)
    print("Sub-process(es) done.")
