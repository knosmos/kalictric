import os
from multiprocessing import Pool

processes = ('timidity -iAqq','python Mainmenu.py')

def run_process(process):
        os.system(process)

pool = Pool(processes = 3)
pool.map(run_process,processes)

