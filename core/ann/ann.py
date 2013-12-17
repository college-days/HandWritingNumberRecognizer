from annacc import mainprocess
import multiprocessing

if __name__ == '__main__':
    pool = multiprocessing.Pool(processes=10)
    for i in xrange(10):
        pool.apply_async(mainprocess, (i, ))
    pool.close()
    pool.join()
    print 'train ann is done'
