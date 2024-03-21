#!/usr/bin/env python3
# encoding: utf-8
"""
@author: liangliang
@license: (C) Copyright 2023-2024, Personal exclusive right.
@contact: 2035776757@qq.com
@file: fastapi_app.py
@time: 2024/3/21
@desc: fastapi templating
"""

from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError, HTTPException
from fastapi.responses import JSONResponse

from Core.logger import logger

app = FastAPI()


# 添加HTTP异常处理函数
def HTTPExceptHandel(request: Request, Except: HTTPException):
    content = {
        'code': Except.status_code,
        'method': request.method,
        'url': request.url.path,
        'msg': Except.detail
    }
    logger.warning(content)  # 日志输出不一定需要
    return JSONResponse(status_code=Except.status_code, content=content)


# 除HTTP_422 其他错误统一处理
@app.exception_handler(RequestValidationError)
def HTTP_422_UNPROCESSABLE_ENTITY(request: Request, Except: Exception):
    return HTTPExceptHandel(request, HTTPException(status_code=422, detail='Unprocessable Entity'))


for Property in [attr for attr in status.__dict__.keys() if 'HTTP' in attr]:
    app.add_exception_handler(getattr(status, Property), HTTPExceptHandel)
