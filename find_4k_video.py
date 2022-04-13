"""
------------------------------------------
@File       : find_4k_video.py
@CreatedOn  : 2022/4/13 21:17
------------------------------------------
"""
from os import listdir, rmdir
from shutil import move as file_move
from os.path import join as path_join, isfile, isdir
import json

from pymediainfo import MediaInfo
from public_tools import list_paths


def get_video_info(v_path):
    media_info = MediaInfo.parse(v_path)
    data = media_info.to_json()
    data = json.loads(data).get('tracks')[1]

    file_type = data.get('track_type').lower()
    width = data.get('width')
    height = data.get('height')

    return file_type, width, height


def main():
    src_dir_path = r"I:\videos\博弈论\未整理"
    to_dir_path = r"I:\videos\博弈论\4K"

    four_k = 3840 * 2160
    bad_ext = ['rar', 'zip', 'chm', 'jpg', 'png']

    moved = 0
    for i in list_paths(src_dir_path, 4):
        try:
            ext = i.split('.')[-1].lower()
            if ext in bad_ext:
                continue

            info = get_video_info(i)

            if info[0] != 'video':
                continue

            if info[1] * info[2] != four_k:
                continue

            file_move(i, to_dir_path)
            moved += 1
            print(f"NO.{moved} | {i}")

        except Exception as err:
            pass


def remove_empty_dir(dir_path, total=0):
    """
        删除空文件夹
    """
    for i in listdir(dir_path):
        full_path = path_join(dir_path, i)

        if isfile(full_path):
            continue

        else:
            if len(listdir(full_path)) == 0:
                rmdir(full_path)
                total += 1

            else:
                remove_empty_dir(full_path)

    print(f"total: {total} dirs, removed.")


def del_empty_dirs():
    src_dir_path = r"I:\videos\博弈论\未整理"
    remove_empty_dir(src_dir_path)


if __name__ == '__main__':
    # main()
    del_empty_dirs()
