@echo off
setlocal enabledelayedexpansion
:: ����ű����� 01-01-transcribe-core.py Ϊһ�������ļ����� txt json srt ��Ļ�ļ�

:: ����ű�����Ŀ¼
%~d0
cd %~dp0

:: ת¼
if exist "model.onnx" (
    python 01-01-transcribe-core.py --paraformer ./model.onnx  --tokens ./tokens.txt %1
   ) else if exist "model.int8.onnx" (
    python 01-01-transcribe-core.py --paraformer ./model.int8.onnx  --tokens ./tokens.txt %1
) else if exist "model_quant.onnx" (
    python 01-01-transcribe-core.py --paraformer ./model_quant.onnx  --tokens ./tokens.txt %1
) 
pause