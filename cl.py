import time
import shutil
import os
import argparse
import datetime
import Defines

def convert(seconds):
    return time.strftime("%b %d %Y %H:%M:%S", time.gmtime(seconds))

def convertDelta(build_age):
    return str(datetime.timedelta(seconds=build_age))

def remove_outdated_builds(directory, args):
    validity_days = args.keep_all_duration
    current_time = time.time()
    valid_seconds = 24*60*60*validity_days
    candidates = []
    candidates_total_size = 0
    print("Processing directory %s" % directory)
    # search candidates on removing
    for build in os.listdir(directory):
        build_path = '%s\\\%s' % (directory, build)
        mtime = os.path.getmtime(build_path)
        build_age = current_time - mtime
        print("Found build %s, mtime: %s, build_age: %s" %
              (build_path, convert(mtime), convertDelta(build_age)))
        if (build.endswith('_CERT')):
            print("Skipped build due to name ends on _CERT")
            continue
        if (build_age < valid_seconds):
            print("Skipped build because %s < %s days" % (convertDelta(build_age), validity_days))
            continue
        print("Found candidate for removing: %s" % build_path)
        candidate_size = folder_size(build_path)
        candidates.append({
            "path": build_path,
            "size": candidate_size
        })
        candidates_total_size += candidate_size
    if len(candidates) == 0:
        return  # no candidates - go away
    # sort candidates by size
    candidates = sorted(candidates, key=lambda x: x["size"])
    print('Candidates total size: %s' % (candidates_total_size))
    print('Candidates sorted by size:')
    [print(x["path"], convert_size(x["size"])) for x in candidates]
    # safe biggest build
    safed_build = candidates.pop(-1)
    print('Safe biggest build %s ' % safed_build["path"])
    candidates_total_size = candidates_total_size-safed_build['size']

    # remove other builds
    while candidates_total_size > args.maximum_size and len(candidates) > 0:
        remove_candidate = candidates.pop(0)
        print('Removing build %s ( %s )' %
              (remove_candidate["path"], convert_size(remove_candidate["size"])))
        candidates_total_size = candidates_total_size-remove_candidate["size"]
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

def select_folder(args):
    for project in [Defines.GAME_INJ2 , Defines.GAME_MKM]:
        for platform in [Defines.PLATFORM_IOS, Defines.PLATFORM_ANDROID]:
            platform_dir = os.path.join('\\\\' + Defines.SHARE_DRIVE, 'Automated', project, platform )
            if args.release:
                remove_outdated_builds(
                    '%s\\\%s' % (platform_dir, args.release), args=args)
            else:
                for release_name in os.listdir(platform_dir):
                    print("Processing release %s" % release_name)
                    remove_outdated_builds(
                        '%s\\\%s' % (platform_dir, release_name), args=args)

def main():
    parser = argparse.ArgumentParser(description='Prune outdated builds')
    parser.set_defaults(cmd=select_folder)
    parser.add_argument('--maximum-size', type=int, default=2 **
                        40, help='Max sum of left builds ( bytes )')
    parser.add_argument('--keep_all_duration', type=int,
                        default=30, help='Days to keep builds')
    parser.add_argument('--release', type=str,
                        default=None, help='Release name ( default ALL releases )')

    args = parser.parse_args()
    result = args.cmd(args)

if __name__ == "__main__":
    main()
