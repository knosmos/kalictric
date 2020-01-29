import os
from multiprocessing import Pool

def main():
    processes = ('minecraft-pi','python minecraft.py')
    pool = Pool(processes = 3)
    pool.map(run_process,processes)

def run_process(process):
    os.system(process)

if __name__ == '__main__':
    main()
