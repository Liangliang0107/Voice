#!/usr/bin/env python3
# encoding: utf-8
"""
@author: liangliang
@license: (C) Copyright 2023-2024, Personal exclusive right.
@contact: 2035776757@qq.com
@file: voice_app.py
@time: 2024/3/21
@desc:
"""
import os
import re
import time
import uuid

import numpy as np
from funasr_onnx import CT_Transformer
from sherpa_onnx import OfflineRecognizer

from Core.config import cli_args
from Core.format import chinese_to_num, adjust_space
from Core.logger import logger
from Core.utlis import findPath, Audio2Float32

VoiceModel_Zh = None
VoiceModel_En = None
PuncModel = None


def format_text(text, punc_model):
    if cli_args.ForMatSpell:
        text = adjust_space(text)  # 调空格
    if cli_args.ForMatPunc and punc_model and text:
        text = punc_model(text)[0]  # 加标点
    if cli_args.ForMatNum:
        text = chinese_to_num(text)  # 转数字
    if cli_args.ForMatSpell:
        text = adjust_space(text)  # 调空格
    return text


def Load_Model():
    global VoiceModel_Zh, VoiceModel_En, PuncModel

    ModelPath = cli_args.ModelPath
    if not ModelPath:
        ModelPath = findPath('models')
    if not ModelPath.endswith('models'):
        os.path.join(ModelPath, 'models')

    t1 = time.time()
    logger.info(f'当前模型目录: {ModelPath}')
    if os.path.exists(cli_args.ParaFormerPath_Zh):
        logger.info(f'[中文]语音模型载入中...')
        VoiceModel_Zh = OfflineRecognizer.from_paraformer(paraformer=cli_args.ParaFormerPath_Zh,
                                                          tokens=cli_args.TokensPath_Zh,
                                                          num_threads=6,
                                                          sample_rate=16000,
                                                          feature_dim=80,
                                                          decoding_method='greedy_search',
                                                          debug=False
                                                          )
        logger.info(f'[中文]语音模型载入完成')
    if os.path.exists(cli_args.ParaFormerPath_En):
        logger.info(f'[英文]语音模型载入中...')
        VoiceModel_En = OfflineRecognizer.from_paraformer(paraformer=cli_args.ParaFormerPath_En,
                                                          tokens=cli_args.TokensPath_En,
                                                          num_threads=6,
                                                          sample_rate=16000,
                                                          feature_dim=80,
                                                          decoding_method='greedy_search',
                                                          debug=False
                                                          )
        logger.info(f'[英文]语音模型载入完成')

    if not VoiceModel_Zh and not VoiceModel_En:
        logger.error(f'没有找到模型文件,请下载模型文件并复制到{cli_args.ModelPath}文件夹')
    if cli_args.ForMatPunc:
        logger.info('标点模型载入中(加载过程漫长,请耐心等待)...')
        PuncModel = CT_Transformer(cli_args.PuncModelPath, quantize=True)
        logger.info(f'标点模型载入完成')
    logger.info(f'模型加载耗时 {time.time() - t1 :.2f}s')


def Voice_Test(AudioPath, Language='zh'):
    global VoiceModel_Zh, VoiceModel_En, PuncModel

    if Language == 'zh':
        VoiceModel = VoiceModel_Zh
    elif Language == 'en':
        VoiceModel = VoiceModel_En
    else:
        logger.error(f'未加载模型文件{Language},请先加载模型文件后进行识别')
        return

    # 生成一个任务ID 用于日志显示
    TaskID = uuid.uuid4()

    AudioData = Audio2Float32(AudioPath)
    Audio_Duration = len(AudioData) / 4 / 16000

    logger.info(f'任务标识: {TaskID} 音频时长: {Audio_Duration}s')

    # 将语音数据转换成np数据
    samples = np.frombuffer(AudioData, dtype=np.float32)
    # 片段识别
    stream = VoiceModel.create_stream()
    stream.accept_waveform(16000, samples)
    VoiceModel.decode_stream(stream)

    timestamps = stream.result.timestamps
    tokens = stream.result.tokens

    # token 合并为文本
    text = ' '.join(tokens).replace('@@ ', '')
    text = re.sub('([^a-zA-Z0-9]) (?![a-zA-Z0-9])', r'\1', text)

    # 调整文本格式
    text = format_text(text, PuncModel)

    # 删除末尾标点符号
    text.strip('，。,.')

    logger.info(f'任务标识: {TaskID} 识别结果: {text}')

    return {
        'timestamps': timestamps,
        'tokens': tokens,
        'duration': Audio_Duration,
        'text': text
    }
