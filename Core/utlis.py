#!/usr/bin/env python3
# encoding: utf-8
"""
@author: liangliang
@license: (C) Copyright 2023-2024, Personal exclusive right.
@contact: 2035776757@qq.com
@file: utlis.py
@time: 2024/3/21
@desc:
"""
import ctypes
import os
import subprocess

from Core.logger import logger


def findPath(PathName):
    current_dir = os.getcwd()
    while True:
        if PathName in os.listdir(current_dir):
            return os.path.join(current_dir, PathName)
        parent_dir = os.path.dirname(current_dir)
        if current_dir == parent_dir:
            break
        current_dir = parent_dir
    return None


def Audio2Float32(AudioPath):
    # 获取音频数据，ffmpeg 输出采样率 16000，单声道，float32 格式
    ffmpegPath = os.path.join(findPath('runtime'), 'ffmpeg')
    ffmpeg_cmd = [
        ffmpegPath,
        "-i", AudioPath,
        "-f", "f32le",
        "-ac", "1",
        "-ar", "16000",
        "-",
    ]
    process = subprocess.Popen(ffmpeg_cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
    AudioData = process.stdout.read()
    process.stdout.close()
    return AudioData


def avoid_suspension():
    """
    禁用快速编辑模式，防止误操作
    :return:
    """
    try:
        import ctypes
        kernel32 = ctypes.windll.kernel32
        kernel32.SetConsoleMode(kernel32.GetStdHandle(-10), (0x4 | 0x80 | 0x20 | 0x2 | 0x10 | 0x1 | 0x00 | 0x100))
        logger.info('禁用快速编辑模式')
    except:
        logger.warning(
            f'禁用快速编辑模式失败, 请勿误选择黑框内容导致程序暂停'
        )


def empty_working_set(pid: int):
    # 获取 pid 的句柄
    handle = ctypes.windll.kernel32.OpenProcess(0x1F0FFF, False, pid)

    # 清空工作集
    ctypes.windll.psapi.EmptyWorkingSet(handle)

    # 关闭进程句柄
    ctypes.windll.kernel32.CloseHandle(handle)


def empty_current_working_set():
    # 获取当前进程ID
    pid = ctypes.windll.kernel32.GetCurrentProcessId()
    empty_working_set(pid)

if __name__ == '__main__':
    Audio2Float32('./1.mp3')
