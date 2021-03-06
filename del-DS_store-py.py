#!/bin/python

# delete-dssstore.py
#
# A simple python script to delete .DS_Store files
#
# 3zbumban
# 2019

import os
import sys
import argparse
import time
from hurry.filesize import size

CWD = os.getcwd()

to_delete = ".DS_Store"

argumetnparser = argparse.ArgumentParser(description="Usage: delete-dsstore.py -p/--path <PATH> or:  delete-dsstore.py -c/--cwd/--current-dir \nExample: delete-dsstore.py -p /Users/angelito")
argumetnparser.add_argument("-p", "--path", dest="target_path", type=str, required=False, help="the path you want to start from as a string \"C:\\example\\dir\\...\\...\"")
argumetnparser.add_argument("-c", "--current-dir", "--cwd", dest="use_cwd", action="store_true", help="add this flag to use the scripts dir as the starting point")
argumetnparser.add_argument("-v", "--verbose", dest="v", action="store_true", help="outputs every file that gets checked for debug purpose, slows down the script")

args, unknowns = argumetnparser.parse_known_args()

def welcome():
	print("\n" * 5)
	print("""
       /$$           /$$       /$$$$$$$   /$$$$$$                    /$$                                  
      | $$          | $$      | $$__  $$ /$$__  $$                  | $$                                  
  /$$$$$$$  /$$$$$$ | $$      | $$  \ $$| $$  \__/        /$$$$$$$ /$$$$$$    /$$$$$$   /$$$$$$   /$$$$$$ 
 /$$__  $$ /$$__  $$| $$      | $$  | $$|  $$$$$$        /$$_____/|_  $$_/   /$$__  $$ /$$__  $$ /$$__  $$
| $$  | $$| $$$$$$$$| $$      | $$  | $$ \____  $$      |  $$$$$$   | $$    | $$  \ $$| $$  \__/| $$$$$$$$
| $$  | $$| $$_____/| $$      | $$  | $$ /$$  \ $$       \____  $$  | $$ /$$| $$  | $$| $$      | $$_____/
|  $$$$$$$|  $$$$$$$| $$      | $$$$$$$/|  $$$$$$/       /$$$$$$$/  |  $$$$/|  $$$$$$/| $$      |  $$$$$$$
 \_______/ \_______/|__/     .|_______/  \______//$$$$$$|_______/    \___/   \______/ |__/       \_______/
                                                |______/                       

												by 3zbumban
""")

def main():
	welcome()
	try:
		if(args.use_cwd):
			path  = CWD
			print("[i] using scripts dir: {}".format(path))
		elif(args.target_path):
			if(os.path.isdir(args.target_path)):
				path = args.target_path
			else:
				print("[e] given path is not a dir\n[i] did you use a backslash (\"\\\") to much?")
				sys.exit(-1)
		else:
			print("[i] exit no path given...")
			sys.exit(0)
		
		if input("[i] your path to clean: {} \n[?] do you want to start? (y/n)   ".format(path)) == "y":
			start = time.time()
			# 1. Check if parameter is a dir
			if os.path.isdir(path):

				# 2. Clear file counter
				i = 0
				acc_f_size = 0
				# 3. walks all files in the directory
				for root, sub, files in os.walk(path):
						
					for file in files:
						if(args.v):
							print("[i] checking: {}".format(os.path.abspath(os.path.join(root, file))))
						# 4. Checks if exists .DS_Store file
						if file == to_delete:

							# 5. Get full path of current .DS_Store file
							fullpath = os.path.abspath(os.path.join(root, file))
							# get file size
							acc_f_size += os.path.getsize(fullpath)

							print("[i] Deleting: \"{}\" \n[i] deleted: {}".format(fullpath, size(acc_f_size)))

							# 6. Remove file
							os.remove(fullpath)
							i += 1
				# 7. print result
				end = time.time()
				print("\n\n\n[i] number of deleted files: {} \n[i] total filesize: {} \n[i] time elapsed: {:4.4f}sec".format(i, size(acc_f_size), (end - start) % 60))
			else:
				sys.exit(0)
		else:
			print("[i] you choose to abort the script...")
			sys.exit(0)
	except KeyboardInterrupt:
		end = time.time()
		print("[i] KeyboardINterrupt, aborting")
		print("\n\n\n[i] number of deleted files: {} \n[i] total filesize: {} \n[i] time elapsed: {:4.4f}sec".format(i, size(acc_f_size), (end - start) % 60))

if __name__ == "__main__":
	main()
