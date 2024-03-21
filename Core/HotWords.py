#!/usr/bin/env python3
# encoding: utf-8
"""
@author: liangliang
@license: (C) Copyright 2023-2024, Personal exclusive right.
@contact: 2035776757@qq.com
@file: HotWords.py
@time: 2024/3/21
@desc:
"""

from pypinyin import pinyin

from Core.logger import logger

__all__ = ['Update_HotWords', 'Replace_HotWords', 'Polyphonic', 'Tone']

# ================全局配置=======================


HotWords = {}
Polyphonic = True
Tone = False  # 是否要求匹配声调

# ===========================================


Style = 1 if Tone else 0  # 依据是否需要声调，设置拼音风格


def Update_HotWords(HotWordStr: str):
    global HotWords
    HotWords.clear()
    for HotW in HotWordStr.splitlines():
        HotW = HotW.strip()  # 给热词去掉多余的空格
        if not HotW or HotW.startswith('#'): continue  # 过滤掉注释
        WordPinYin = pinyin(HotW, Style, Polyphonic)  # 得到拼音

        if len(WordPinYin) != len(HotW):
            logger.info(f'热词「{HotW}」得到的拼音数量与字数不符，抛弃')
            continue

        PinYinList = [[], ]
        for DuoYin in WordPinYin:
            YinShu = len(DuoYin)
            if YinShu > 1:
                OrgList, PinYinList = PinYinList, []
                for Yin in DuoYin:
                    PinYinList.extend([x.copy() + [Yin] for x in OrgList])
            else:
                for x in PinYinList: x.append(DuoYin[0])

        HotWords[HotW] = PinYinList
    return len(HotWords)


def Match_HotWords(Sent: str):
    """
    将全局「热词词典」中的热词按照拼音依次与句子匹配，将所有匹配到的「热词、拼音」以元组放到列表
    将列表返回
    """
    global HotWords

    AllMatch = []
    JuZiPinYin = ''.join([x[0] for x in pinyin(Sent, Style, Polyphonic)])  # 字符串形式的句子拼音
    for Ci in HotWords.keys():
        for PinYinSeq in HotWords[Ci]:
            if ''.join(PinYinSeq) in JuZiPinYin:
                AllMatch.append((Ci, PinYinSeq))
            else:
                continue
    return AllMatch


def GetPinYinIndex(Sent: str):
    """
    输入句子字符串，获取一个列表，列表内是字典，字典包含了拼音和索引

    例如，输入 '撒贝宁' ，输出：
    [
        {'pinyin': 'sǎ', 'index': 0 },
        {'pinyin': 'bèi', 'index': 1 },
        {'pinyin': 'nìng', 'index': 2 },
    ]
    """
    PinYinTapeIndex = [{'pinyin': x[0], 'index': None} for x in pinyin(Sent, Style, Polyphonic)]
    PinYinTapeIndex_ = iter(PinYinTapeIndex)
    PinYin = next(PinYinTapeIndex_)
    for i, Zi in enumerate(Sent):
        if PinYin['pinyin'] in pinyin(Zi, Style, Polyphonic)[0] or PinYin['pinyin'].startswith(Zi):
            PinYin['index'] = i
            try:
                PinYin = next(PinYinTapeIndex_)
            except:
                ...
    return PinYinTapeIndex


def Replace_HotWords(JuZi):
    """
    从热词词典中查找匹配的热词，替换句子

    句子：       被查找和替换的句子
    """
    AllMatch = Match_HotWords(JuZi)
    for Item in AllMatch:
        Hw, PinYinSeq = Item  # 从字典中找到可以替换的热词和对应的拼音

        SentTabIndex = GetPinYinIndex(JuZi)
        RepRange = []
        for i, item in enumerate(SentTabIndex):
            for j, Yin in enumerate(PinYinSeq):
                if i + j >= len(SentTabIndex): break
                if Yin != SentTabIndex[i + j]['pinyin']: break
            else:
                RepRange.append([SentTabIndex[i]['index'], SentTabIndex[i + j]['index']])

        for Range in RepRange:
            JuZi = JuZi[:Range[0]] + Hw + JuZi[Range[1] + 1:]

    return JuZi
