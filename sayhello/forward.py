# -*- coding: utf-8 -*-
"""
    :author: (Yega)
    :copyright: © 2021 yega
    :license: MIT, see LICENSE for more details.
"""
import subprocess
import time
import os


def live(source, target):
    cmd = 'ffmpeg -re -i {} -vcodec copy -acodec aac -f flv "{}"'.format(source, target)
    with open(os.devnull, 'w') as devnull:
        process = subprocess.Popen(
            cmd,
            shell=True,
            stdout=devnull,
            stderr=devnull,
            encoding='utf-8',
        )
    res = subprocess.Popen.poll(process)
    while res is not None:
        time.sleep(1)
        process.terminate()
        with open(os.devnull, 'w') as devnull:
            process = subprocess.Popen(
                cmd,
                shell=True,
                stdout=devnull,
                stderr=devnull,
                encoding='utf-8',
            )
        res = subprocess.Popen.poll(process)
    return process.pid


def stop_live(pid):
    cmd = 'kill -9 {}'.format(pid)
    with open(os.devnull, 'w') as devnull:
        process = subprocess.Popen(
            cmd,
            shell=True,
            stdout=devnull,
            stderr=devnull,
            encoding='utf-8',
        )
    res = subprocess.Popen.poll(process)
    return res
