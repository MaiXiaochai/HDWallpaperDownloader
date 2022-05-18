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


def find_and_move_4k(src_dir_path, to_dir_path, vertical=False):
    four_k = 3840 * 2160
    four_k_tuple = (3840, 2160)
    bad_ext = ['rar', 'zip', 'chm', 'jpg', 'png']

    moved = 0
    for i in list_paths(src_dir_path, 4):
        try:
            ext = i.split('.')[-1].lower()
            if ext in bad_ext:
                continue

            # info demo: ('video', 2160, 3840)
            info = get_video_info(i)

            if info[0] != 'video':
                continue

            if info[1] * info[2] != four_k:
                continue

            if vertical and info[1] != four_k_tuple[1]:
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


def find_vertical_video_4k():
    """找到 4k竖屏视频，移动到目标文件夹"""
    src_dir_path = r"G:\videos\bilibili"
    to_dir_path = r"G:\videos\b站高清舞蹈\4K竖屏"
    find_and_move_4k(src_dir_path, to_dir_path, True)


if __name__ == '__main__':
    # find_and_move_4k()
    find_vertical_video_4k()
    # del_empty_dirs()
