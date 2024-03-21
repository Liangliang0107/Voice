#!/usr/bin/env python3
# encoding: utf-8
"""
@author: liangliang
@license: (C) Copyright 2023-2024, Personal exclusive right.
@contact: 2035776757@qq.com
@file: test.py
@time: 2024/3/21
@desc:
"""

import base64

import requests

AudioFile = b''

result = requests.post('http://127.0.0.1/api/asr', json={
    'Language': 'zh',
    'HotWords': '',
    'UpFile_B64': base64.b64encode(AudioFile).decode()
}, headers={
    'Content-Type': 'application/json'
})
print(result)
