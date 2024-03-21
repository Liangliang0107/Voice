%~d0
cd %~dp0

if exist "model.onnx" (
    02-01-sherpa-onnx-offline-websocket-server.exe --paraformer=model.onnx --tokens=tokens.txt --port=6007 --num-threads=8
) else if exist "model.int8.onnx" (
    02-01-sherpa-onnx-offline-websocket-server.exe --paraformer=model.int8.onnx --tokens=tokens.txt --port=6007 --num-threads=8
) else if exist "model_quant.onnx" (
    02-01-sherpa-onnx-offline-websocket-server.exe --paraformer=model_quant.onnx --tokens=tokens.txt --port=6007 --num-threads=8
) 