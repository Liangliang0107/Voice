import base64
import logging
import os
import random
import string

import uvicorn
from fastapi import Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from Core.HotWords import Update_HotWords, Replace_HotWords
from Core.config import cli_args, SYSTEM
from Core.logger import logger
from Core.utlis import avoid_suspension, empty_current_working_set
from fastapi_app import app
from voice_app import Load_Model, Voice_Test


def info(x, *args, **kwargs):  # 关闭输出
    # return logger.info(x % args, **kwargs)
    pass


class RequestBody(BaseModel):
    HotWords: str = None
    Language: str = 'zh'
    UpFile_B64: str


@app.post('/api/asr')
async def api_asr(request: Request, body: RequestBody):
    Update_HotWords(body.HotWords.replace(',', '\n\r') if body.HotWords else '')

    AudioData = base64.b64decode(body.UpFile_B64)
    FileName = "".join(random.choice(string.ascii_letters + string.digits) for _ in range(8))
    AudioPath = f'./cache/{FileName}.mp3'
    with open(AudioPath, 'wb') as f:
        f.write(AudioData)

    result = Voice_Test(AudioPath, body.Language)
    if not cli_args.SaveCache:
        os.unlink(AudioPath)

    result['text'] = Replace_HotWords(result['text'])

    return JSONResponse(status_code=200, content={'code': 200,
                                                  'result': result,
                                                  'message': 'success'})


if __name__ == '__main__':
    # 屏蔽 uvicorn 的信息
    logging.getLogger('uvicorn.error').info = info
    # 屏蔽jieba 调试信息
    logging.getLogger('jieba').setLevel(logging.INFO)

    logger.info(f'服务器已启动监听 http://{cli_args.host}:{cli_args.port}')
    logger.info(f'调用地址 http://127.0.0.1:{cli_args.port}/api/asr')

    if SYSTEM == 'Windows':
        empty_current_working_set()
        avoid_suspension()
        os.system(f'title {cli_args.title}')

    # 加载模型信息
    Load_Model()

    if not os.path.exists('./cache'):
        os.mkdir('./cache')

    uvicorn.run(app=app, host=cli_args.host, port=cli_args.port, log_level='info',
                access_log=False, interface='asgi3', server_header=False, date_header=False)
