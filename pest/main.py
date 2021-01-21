


if __name__ == '__main__':
    pool = multiprocessing.Pool()
    pool.map(worker, range(5))