call conda activate Voice
call nuitka --onefile --standalone --include-package=uvicorn --include-package=fastapi --nofollow-import-to=*.test --nofollow-import-to=numba --noinclude-default-mode=error --enable-plugin=upx --jobs=16 --output-dir=build --windows-icon-from-ico=./resource/logo.ico --output-filename=VoiceServer .\main.py
exit 0