# main.py>
# Main of scriptgen4HPC - utility for customizing the UASOS experiment
# Set your parameters where requested hereafter
# Author: Vincenzo Maria VITALE - DCAS - MS TAS AERO - FTE
###################################################################

from scriptgen import *
from datetime import datetime
from numpy import *
import multiprocessing as mp
import os
import sys
import csv
maxInt = sys.maxsize

while True:
    # decrease the maxInt value by factor 10
    # as long as the OverflowError occurs.
    try:
        csv.field_size_limit(maxInt)
        break
    except OverflowError:
        maxInt = int(maxInt/10)

global num_threads
num_threads = mp.cpu_count()  # Number of CPU Cores, put mp.cpu_count()-1 if you are running it on a standard PC

global phase_gen, exp_time_main, exp_time_train, it_time, jitter, treshold, treshold_train
global max_size_dset,max_perthread, max_time
global main_filename, train_filename_src, train_filename_navi
min2ms = 60*1000
main_filename = 'scripts_dset.csv'
train_filename_src = 'scripts_SRC_train.csv'
train_filename_navi = 'scripts_NAVI_train.csv'

# Change parameters here!--------
max_size_dset = 1000  # indicative, pc needs to do a round number of scripts
max_time = 167  # Max time allowable to run, useful to cut before HPC cuts the allocation time
# Related to the script_dset.csv gen
phase_gen = 'MAIN'  # choose between 'MAIN', 'SRC_TRAIN', 'NAVI_TRAIN'
exp_time_main = 2*60*min2ms
exp_time_train = 3*min2ms
it_time = 7000
jitter = 1000
treshold = 0.03  # Default <3% for convergence in 2hrs 7 (+/-1) sec
treshold_train = 0.5  # Stay large, it's just training
# --------------------------------
max_perthread = round(max_size_dset/num_threads)

global scripts
scripts = []
for _ in range(num_threads):
    scripts.append(ScriptGen())

def cleanup_folder(folder_path, exclude_file=None):
    # Check folder existence
    if not os.path.exists(folder_path):
        return

    for filename in os.listdir(folder_path):
        if exclude_file is not None:
            if filename != exclude_file:
                file_path = os.path.join(folder_path, filename)
                # remove each file from the folder
                if os.path.isfile(file_path):
                    os.remove(file_path)
        else:
            file_path = os.path.join(folder_path, filename)
            # remove each file from the folder
            if os.path.isfile(file_path):
                os.remove(file_path)

    return


def check_dev(vec, thr):
    arr = array(vec)
    if (arr < thr).sum() == arr.size:
        return True
    else:
        return False


def merge_csv(n_threads):
    file_s = []
    out_h = None
    if phase_gen == 'MAIN':
        out_h = main_filename
    elif phase_gen == 'SRC_TRAIN':
        out_h = train_filename_src
    elif phase_gen == 'NAVI_TRAIN':
        out_h = train_filename_navi
    folder = './out'
    folderf = './final'

    for i in range(n_threads):
        file_h = 'scripts_thr' + str(i) + '.csv'
        file_s.append(os.path.join(folder, file_h))

    out_s = os.path.join(folderf, out_h)
    with open(out_s, "a", newline="") as outfile:
        writer = csv.writer(outfile)

        for i, csv_file in enumerate(file_s):
            if os.path.exists(csv_file):
                with open(csv_file, "r") as infile:
                    reader = csv.reader(infile)

                    for row in reader:
                        writer.writerow(row)

                infile.close()

    outfile.close()


def launch_gen(args):
    watchdog = 0.0
    n_thread, script = args
    print('Start the generation of the Scripts on Thread ', n_thread)  # Add No of thread
    folder = './out'
    file_s = 'scripts_thr'+str(n_thread)+'.csv'  # Holder of the scripts
    report_dev = 'report_dev'+str(n_thread)+'.txt'  # Report of the deviations

    try:
        # generate path files
        file_ps = os.path.join(folder, file_s)
        report_pdev = os.path.join(folder, report_dev)
        filetxt = open(report_pdev, 'w', newline='')

        k = 0
        max_size = max_perthread
        PANDO_Time = max_time  #23.5  # In hrs: 23.5h -> 23h30m00s
        start = datetime.now().timestamp()

        filetxt.write(f'Script Report for Thread {n_thread} \n')
        while k != max_size and watchdog < (PANDO_Time*60*60):  # It checks max size of
            script = ScriptGen(phase=phase_gen)
            if phase_gen == 'MAIN':
                script.exp_time = exp_time_main
                script.it_time = it_time
                script.jitter = jitter
                script.threshold = treshold
            elif phase_gen == 'SRC_TRAIN' or phase_gen == 'NAVI_TRAIN':
                script.exp_time = exp_time_train
                script.it_time = it_time
                script.jitter = jitter
                script.threshold = treshold_train

            valid = script.generate_batch(n_thread)
            if valid:
                if script.dev_per <= script.threshold:
                    with open(file_ps, 'a', newline='') as csvfile:
                        writer_s = csv.writer(csvfile, delimiter='\t')
                        writer_s.writerow(script.TIME)
                        writer_s.writerow(script.SWITCH)
                        writer_s.writerow(script.TASK)

                    filetxt = open(report_pdev, 'a', newline='')
                    filetxt.write(f'Script No. {k+1} deviation: {"{:.3f}".format(script.dev_per*100)}% \n')

                    # safe closing
                    csvfile.close()
                    filetxt.close()
                    k += 1
                    del script
                else: del script
            else: del script
            watchdog = datetime.now().timestamp() - start  # Task time in sec

        return 0
    except Exception as e_thr:
        print(f"Exception in execution: {e_thr}")
        return -1

if __name__ == "__main__":
    print('########## EXECUTION OF THE SCRIPT GEN ##########')  # Add No of thread
    # cleanup event if necessary
    folder = "./out"
    folderf = "./final"
    cleanup_folder(folder)
    cleanup_folder(folderf)
    # Start of the execution in parallel
    start_gen = datetime.now().timestamp()
    # execution of the folder generation
    if not os.path.exists(folder):
        os.makedirs(folder)
    if not os.path.exists(folderf):
        os.makedirs(folderf)
    # Multiprocessing execution now
    pool = mp.Pool(processes=num_threads)
    data = zip(list(range(0, num_threads)), scripts)
    # results vector will return correct/incorrect execution of the thread
    results = pool.map(launch_gen, data)

    pool.close()
    pool.join()
    ares = array(results)
    if (ares == 0).sum() == ares.size:
        merge_csv(n_threads=num_threads)
        print('Correct Execution!')
        print('End of generation. Start writing the final .csv dataset.')
        print('Total Duration: ', "{:.3f}".format((datetime.now().timestamp() - start_gen)/60), ' min')
    else:
        for i_thread, v_thread in enumerate(results):
            if v_thread != 0:
                print('Error in Thread ', i_thread)
            else:
                pass

