import argparse
import time
import shutil
import sys
import os
import re
def check_build_full(build_path):
    for target in ["Development","Shipping"]:
        if not os.path.isdir(os.path.join(build_path, target)):
            return False
        for fullbuild in ["ATC","DXT","ETC1","ETC2"]:
            if not os.path.isdir(os.path.join(build_path, target, fullbuild)):
                return False
    return True
def check_build_full2(build_path):
    for target in ["Development2","Shipping2"]:
        if not os.path.isdir(os.path.join(build_path, target)):
            return False
        for fullbuild in ["ATC2","DXT2","ETC12","ETC22"]:
            if not os.path.isdir(os.path.join(build_path, target, fullbuild)):
                return False
    return True

def remove_outdated_builds(root_folder_path, validity_period):
    delta_time = 24*60*60*validity_period   #validity_period in days
    current_time = time.time()
    directory = os.path.join(root_folder_path)
    print("Processing ", directory)
    for build in os.listdir(directory):
        print("Found build ", build)

        timestamp = os.path.getmtime(os.path.join(root_folder_path, build))
        print(os.path.join(root_folder_path, build),current_time,delta_time) #debag
        if (current_time - delta_time > timestamp):
            if check_build_full(os.path.join(root_folder_path, build)) or check_build_full2(os.path.join(root_folder_path, build)):
                print("Skipped build is full")
                continue
            try:
                print("Removing ", os.path.join(root_folder_path, build))

                #shutil.rmtree(os.path.join(root_folder_path, build))  #uncomment to use----del
            except Exception as ex:
                print("Unable to remove", build)
                print(ex)
                pass
            else:
                print("Removed", build)
        else:
            print("Skipped modification time")

def main():
    parser = argparse.ArgumentParser(description="Clean Build Artifacts")
    args = parser.parse_args() #can del

    for project in ["INJ2","MKM"]:
        for platform in ["IOS","Android"]:
            for dir in os.listdir("D:\chi-file01\INJ2Mobile\MobileBuilds\\"+project+"\Automated\\"+platform):
                print("Processing release " + dir)
                remove_outdated_builds("D:\chi-file01\INJ2Mobile\MobileBuilds\\"+project+"\Automated\\"+platform+"\\"+dir, 0)

if __name__ == "__main__":
    main()


--------------------------------------


import os
import subprocess

def convert_size(size):
    for x in ['bytes', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024.0:
            return "%3.1f %s" % (size, x)
        size /= 1024.0

def main():
    path1 = "C:\\Users\\wetal\\Documents\\Size"
    path = "D:\\chi-file01\\INJ2Mobile\\MobileBuilds\\"+project+"\\Automated\\"+platform"
    if os.path.isfile(path):
        try:
            size = os.path.getsize(path)
        except Exception as err:
            print(err)
    else:
        size = 0
        for dirpath, dirnames, filenames in os.walk(path):
            for file in filenames:
                filepath = os.path.join(dirpath, file)
                try:
                    size += os.path.getsize(filepath)
                except Exception as err:
                    print (err)
    print (size, "bytes")
    print (convert_size(size))

if __name__ == "__main__":
    main()
