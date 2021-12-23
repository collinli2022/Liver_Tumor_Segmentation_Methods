import argparse
import shutil
 
msg = "Program to quickly sort and move files from one directory to another"
 
# Initialize parser
parser = argparse.ArgumentParser(description = msg)
parser.add_argument("-s", "--source", help = "Source directory folder", required = True)
parser.add_argument('-d', "--destination", nargs='?', default='./ISMRM_AutoLevelSet', help = "Destination directory folder")
args = parser.parse_args()

print(args)
print('TODO: need to finish this')




# os.rename("path/to/current/file.foo", "path/to/new/destination/for/file.foo")
# os.replace("path/to/current/file.foo", "path/to/new/destination/for/file.foo")
# shutil.move("path/to/current/file.foo", "path/to/new/destination/for/file.foo")