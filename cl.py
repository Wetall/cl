#!/bin/env python3

import time
import shutil
import os
import argparse

parser = argparse.ArgumentParser(description='Prune outdated builds')
parser.add_argument('--maximum-size', type=int, default=2 **
                    40, help='Max sum of left builds ( bytes )')
parser.add_argument('--keep-all-duration', type=int,
                    default=30, help='Days to keep builds')
parser.add_argument('--release', type=str,
                    default=None, help='Release name ( default ALL releases )')

args = parser.parse_args()


def remove_outdated_builds(directory, validity_days=30):
    current_time = time.time()
    valid_seconds = 24*60*60*validity_days
    candidates = []
    candidates_sum_size = 0
    print("Processing directory %s" % directory)
    # search candidates on removing
    for build in os.listdir(directory):
        build_path = '%s\\\%s' % (directory, build)
        mtime = os.path.getmtime(build_path)
        build_age = current_time - mtime
        print("Found build %s, mtime: %s, build_age: %s" %
              (build_path, mtime, build_age))
        if (build_age < valid_seconds):
            print("Skipped build because %s < %s" % (build_age, valid_seconds))
            continue
        print("Found candidate for removing: %s" % build_path)
        candidate_size = folder_size(build_path)
        candidates.append({
            "path": build_path,
            "size": candidate_size
        })
        candidates_sum_size += candidate_size
    if len(candidates) == 0:
        return  # no candidates - go away
    # sort candidates by size
    candidates = sorted(candidates, key=lambda x: x["size"])
    print('Candidates sorted by size:')
    [print(x["path"], convert_size(x["size"])) for x in candidates]
    # safe biggest build
    safed_build = candidates.pop(-1)
    print('Safe biggest build %s ' % safed_build["path"])
    candidates_sum_size = candidates_sum_size-safed_build['size']

    # remove other builds
    while candidates_sum_size > args.maximum_size and len(candidates) > 0:
        remove_candidate = candidates.pop(0)
        print('Removing build %s' % remove_candidate["path"])
        candidates_sum_size = candidates_sum_size-remove_candidate["size"]
        # shutil.rmtree('%s\\\%s' % (root_folder_path, remove_candidate) )  #uncomment to use----del


def folder_size(path='.'):
    total = 0
    for entry in os.scandir(path):
        if entry.is_file():
            total += entry.stat().st_size
        elif entry.is_dir():
            total += folder_size(entry.path)
    return total


def convert_size(size):
    for x in ['bytes', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024.0:
            return "%3.1f %s" % (size, x)
        size /= 1024.0


def main():
    for project in ["INJ2", "MKM"]:
        for platform in ["IOS", "Android"]:
            platform_dir = 'D:\\\chi-file01\\\INJ2Mobile\\\MobileBuilds\\\%s\\\Automated\\\%s' % (
                project, platform)
            if args.release:
                remove_outdated_builds(
                    '%s\\\%s' % (platform_dir, args.release), validity_days=args.keep_all_duration)
            else:
                for release_name in os.listdir(platform_dir):
                    print("Processing release %s" % release_name)
                    remove_outdated_builds(
                        '%s\\\%s' % (platform_dir, release_name), validity_days=args.keep_all_duration)


if __name__ == "__main__":
    main()
