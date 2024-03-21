#!/usr/bin/env python3
# encoding: utf-8
"""
@author: liangliang
@license: (C) Copyright 2023-2024, Personal exclusive right.
@contact: 2035776757@qq.com
@file: fastapi_app.py
@time: 2024/3/21
@desc: logger templating
"""
import sys
from pathlib import Path

from loguru import logger

logger.remove()
log_directory = "logs"
filename = f'{Path(__file__).stem}-script.log'
Path(log_directory).mkdir(parents=True, exist_ok=True)
custom_format = ("<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level:^8}</level> | <cyan>{name}</cyan>:<cyan>{"
                 "function}</cyan>:<cyan>{line}</cyan> - "
                 "<level>{message}</level>")
logger.add(
    sink=(Path(log_directory) / filename),
    enqueue=True,
    level="WARNING",
    rotation="15 MB",
    retention="2 days",
    encoding="utf-8",
    backtrace=True,
    diagnose=True,
    compression="zip",
    format=custom_format,
)

logger.add(
    sink=sys.stderr,
    format=custom_format,
    level="DEBUG"
)
