[TOC]

## Voice

![image-20240321223023658](https://cdn.jsdelivr.net/gh/Liangliang0107/image-resources/202403212312776.jpg)

基于开源项目 [CapsWriter](https://github.com/HaujetZhao/CapsWriter-Offline) 二次开发，非常感谢这位作者的无私奉献

$\color{#FF0000}{本项目仅用于研究语音验证码的识别，请勿用于非法，出问题作者不承担任何责任}$ 

$\color{#FF0000}{不支持长音频识别}$，需要使用长音频识别请使用 [CapsWriter](https://github.com/HaujetZhao/CapsWriter-Offline)

支持 ``中英`` 两张语言识别

个人建议不启用标点模型（因为太慢了,也没啥用）

## 食用方法

无论是源码方式还是懒人包都需要下载模型

默认加载所有语音模型  不需要的请修改配置文件：

```yaml
ParaFormerPath_En: Null  # 英文语音模型
TokensPath_En: Null  # 英文语音模型
```

### 1. 源码安装方式（windows + python 3.10）

```sh
pip install -r requirements.txt
```

```sh
python main.py
```

### 2. 懒人包方法

懒人包由 nuitka 编译

直接运行 VoiceServer.exe 文件

### 3. nuitka 打包教程（windows）

需要先安装 nuitka 

```sh
pip install nuitka
```

```sh
nuitka --onefile --standalone --include-package=uvicorn --include-package=fastapi --nofollow-import-to=*.test --nofollow-import-to=numba --noinclude-default-mode=error --enable-plugin=upx --jobs=16 --output-dir=build --windows-icon-from-ico=./resource/logo.ico --output-filename=VoiceServer .\main.py
```

## 配置文件说明

配置文件名：``startup_param.yaml``

```yaml
host: '0.0.0.0'  # 监听地址
port: 4563  # 监听端口
ForMatPunc: False  # 处理标点符号（开启这个会加载标点模型）
ForMatSpell: True # 处理空格
ForMatNum: True # 转换数字
ModelPath: ./models # 模型文件夹
ParaFormerPath_Zh: ${ModelPath}/paraformer-offline-zh/model.onnx  # 中文语音模型
TokensPath_Zh: ${ModelPath}/paraformer-offline-zh/tokens.txt  # 中文语音模型
ParaFormerPath_En: ${ModelPath}/paraformer-offline-en/model.onnx  # 英文语音模型
TokensPath_En: ${ModelPath}/paraformer-offline-en/tokens.txt  # 英文语音模型
PuncModelPath: ${ModelPath}/punc_ct-transformer_cn-en  # 标点模型
```

## 调用方式

```apl
POST /api/asr HTTP/1.1
Content-Type: application/json

{"Language":"zh","HotWords":"","UpFile_B64":""}
```

#### 请求地址

```apl
POST /api/asr
```

#### 请求头

|    参数名    |  类型  |       描述       | 必填 |
| :----------: | :----: | :--------------: | :--: |
| content-type | string | application/json |  是  |

#### 请求参数

|   参数名   |  类型  |           描述           | 必填 |
| :--------: | :----: | :----------------------: | :--: |
|  Language  | string |     语言类型 默认zh      |  否  |
|  HotWords  | string | 热词列表 使用逗号(,)分割 |  否  |
| UpFile_B64 | string |   音频文件的base64编码   |  是  |

#### 成功返回

| 参数名  |  类型  |            描述             | 必填 |
| :-----: | :----: | :-------------------------: | :--: |
|  code   |  int   | 错误码 正确 200 大于200失败 |  是  |
| result  |  dict  |          结果信息           |  否  |
| message | string |          错误信息           |  是  |

#### result详细

|   参数名   |  类型  |                描述                | 必填 |
| :--------: | :----: | :--------------------------------: | :--: |
| timestamps |  list  |        每个文字对应的时间点        |  是  |
|   tokens   |  list  |              文字列表              |  是  |
|  duration  | float  |            音频文件时长            |  是  |
|    text    | string | 最后的返回结果（包括热词处理后的） |  是  |

#### python 请求示例

```python
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
```

