#!/usr/bin/env python3
# encoding: utf-8
"""
@author: liangliang
@license: (C) Copyright 2023-2024, Personal exclusive right.
@contact: 2035776757@qq.com
@file: config.py
@time: 2024/3/21
@desc:
"""

import argparse
import multiprocessing
import os
import platform
from pathlib import Path
from string import Template

import yaml

CPU_COUNT = multiprocessing.cpu_count()
SYSTEM = platform.system()

sys_args = {
    "host": '0.0.0.0',
    "port": 4563,
    "SaveCache": False,
    "title": "VoiceServer",
    "ForMatPunc": False,
    "ForMatSpell": True,
    "ForMatNum": True,
    "ModelPath": str((Path() / 'models').resolve()),
    "ParaFormerPath_Zh": str((Path() / 'models' / 'paraformer-offline-zh' / 'model.onnx').resolve()),
    "TokensPath_Zh": str((Path() / 'models' / 'paraformer-offline-zh' / 'tokens.onnx').resolve()),
    "ParaFormerPath_En": str((Path() / 'models' / 'paraformer-offline-en' / 'model.onnx').resolve()),
    "TokensPath_En": str((Path() / 'models' / 'paraformer-offline-en' / 'tokens.onnx').resolve()),
    "PuncModelPath": str((Path() / 'models' / 'punc_ct-transformer_cn-en').resolve())
}
STARTUP_PARAM_FILE = "startup_param.yaml"

if os.path.exists(STARTUP_PARAM_FILE):
    with open(STARTUP_PARAM_FILE, 'r', encoding='utf-8') as f:
        FileBody = f.read()
        yaml_data = yaml.load(FileBody, Loader=yaml.SafeLoader)
        temTemplate = Template(FileBody).safe_substitute({'ModelPath': yaml_data['ModelPath']})
        yaml_data = yaml.load(temTemplate, Loader=yaml.SafeLoader)

        sys_args.update(yaml_data)

# cli 参数
cli_parser = argparse.ArgumentParser(description=f'VoiceServer (System: {SYSTEM})')
cli_parser.add_argument(
    '--host', dest='host', default=sys_args.get("host"), type=str,
    help='Server Listening Address (default 0.0.0.0)'
)
cli_parser.add_argument(
    '--port', dest='port', default=sys_args.get("port"), type=int,
    help='Server Listening Port (default 4563)'
)

cli_parser.add_argument('--SaveCache', dest='SaveCache', type=bool, default=sys_args.get('SaveCache'))

cli_parser.add_argument('--ForMatPunc', dest='ForMatPunc', type=bool, default=sys_args.get('ForMatPunc'))
cli_parser.add_argument('--ForMatSpell', dest='ForMatSpell', type=bool, default=sys_args.get('ForMatSpell'))
cli_parser.add_argument('--ForMatNum', dest='ForMatNum', type=bool, default=sys_args.get('ForMatNum'))

cli_parser.add_argument('--title', dest='title', type=str, default=sys_args.get('title'))

cli_parser.add_argument('--ModelPath', dest='ModelPath', type=str, default=sys_args.get('ModelPath'))

cli_parser.add_argument('--ParaFormerPath_Zh', dest='ParaFormerPath_Zh',
                        type=str, default=sys_args.get('ParaFormerPath_Zh'))
cli_parser.add_argument('--TokensPath_Zh', dest='TokensPath_Zh',
                        type=str, default=sys_args.get('TokensPath_Zh'))

cli_parser.add_argument('--ParaFormerPath_En', dest='ParaFormerPath_En',
                        type=str, default=sys_args.get('ParaFormerPath_En'))
cli_parser.add_argument('--TokensPath_En', dest='TokensPath_En',
                        type=str, default=sys_args.get('TokensPath_En'))

cli_parser.add_argument('--PuncModelPath', dest='PuncModelPath', type=str, default=sys_args.get('PuncModelPath'))

cli_args = cli_parser.parse_args()

cli_args.__dict__.update({
    "host": cli_args.host,
    "port": cli_args.port,
    "title": cli_args.title,
    "SaveCache": cli_args.SaveCache,
    "ForMatPunc": cli_args.ForMatPunc,
    "ForMatSpell": cli_args.ForMatSpell,
    "ForMatNum": cli_args.ForMatNum,
    "ModelPath": str(Path(cli_args.ModelPath).resolve()),
    "ParaFormerPath_Zh": str(Path(cli_args.ParaFormerPath_Zh).resolve()) if cli_args.ParaFormerPath_Zh else '',
    "TokensPath_Zh": str(Path(cli_args.TokensPath_Zh).resolve()) if cli_args.TokensPath_Zh else '',
    "ParaFormerPath_En": str(Path(cli_args.ParaFormerPath_En).resolve()) if cli_args.ParaFormerPath_En else '',
    "TokensPath_En": str(Path(cli_args.TokensPath_En).resolve()) if cli_args.TokensPath_En else '',
    "PuncModelPath": str(Path(cli_args.PuncModelPath).resolve())
})

__all__ = ['SYSTEM', 'cli_args', 'CPU_COUNT']
