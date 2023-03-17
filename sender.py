import multiprocessing as mp
import download_text, send_text
from os import listdir, rmdir
from os.path import isfile, join, exists
import time
import sys
import utils

def main():
    args = sys.argv
    assert len(args) == 2, "Incorrect number of args"

    N_PROCS = int(args[1])

    
    download_text.main(N_PROCS)

    files = utils.get_filename("./sent_texts")
    pool = mp.Pool(len(files))

    for i, f in enumerate(files):
        pool.apply_async(send_text.main, args=(f,))
    pool.close()
    pool.join()
    print("done")

    if exists("sent_texts"):
        rmdir("sent_texts")

if __name__ == '__main__':
    main()