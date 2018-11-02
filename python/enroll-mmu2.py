##-----------------------------------------------------------------------------
##  Author      : Thuy Nguyen-Chinh
##  Date        : Nov 27, 2017
##
##  Interpreter : Python 3.5
##  Description : Enroll accounts for the whole of database
##-----------------------------------------------------------------------------


##-----------------------------------------------------------------------------
##  Import
##-----------------------------------------------------------------------------
import argparse, os
from glob import glob
from tqdm import tqdm
from time import time
from scipy.io import savemat
from multiprocessing import cpu_count

from fnc.extractFeature import extractFeature


#------------------------------------------------------------------------------
#	Argument parsing
#------------------------------------------------------------------------------
parser = argparse.ArgumentParser()

parser.add_argument("--data_dir", type=str, default="../MMU2/",
					help="Path to the directory containing MMU2 images.")

parser.add_argument("--temp_dir", type=str, default="./templates/MMU2/",
					help="Path to the directory containing templates.")

parser.add_argument("--n_cores", type=int, default=cpu_count(),
					help="Number of cores used for enrolling template.")

args = parser.parse_args()


##-----------------------------------------------------------------------------
##  Execution
##-----------------------------------------------------------------------------
start = time()

# Get list of files for enrolling template, just "*010*.jpg" files are selected
files = glob(os.path.join(args.data_dir, "*010*.bmp"))
n_files = len(files)
print("Number of files for enrolling:", n_files)

# Enroll
print("Start enrolling...")
for file in tqdm(files, total=n_files):
	template, mask, filename = extractFeature(file)
	basename = os.path.basename(file)
	out_file = os.path.join(args.temp_dir, "%s.mat" % (basename))
	savemat(out_file, mdict={'template': template, 'mask': mask})

end = time()
print('\n>>> Enrollment time: {} [s]\n'.format(end-start))