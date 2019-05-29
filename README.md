# TikTag

TikTag is music file tagger with automatic aproach.

## Installation

All required dependencies are in setup.py file.

```bash
python setup.py install
```

## Fingerprinting

To enable fingerprinting you should install AcoustID too.

```bash
sudo apt install ffmpeg acoustid-fingerprinter
```

For Windows fpcalc.exe library is highly recommended. 
When downloaded, make sure it's in system PATH. (eg. C:\Windows\fpcalc.exe))
https://acoustid.org/chromaprint

## Run

To open app run /TikTag/main.py with Python interpret.

```bash
python main.py
```
