# Georgian OCR

## Requierments

```bash
apt install python-tk
apt install libffi-dev
apt install python-opencv

pip install tensorflow
pip install keras
pip install cairocffi
pip install editdistance
pip install matplotlib
pip install nose2
pip install h5py

cp fonts/* /usr/share/fonts/truetype
```

## Learn

```
bin/learn.sh
```

## Predict

```
bin/ocr.sh tests/mnatobi-line.png
```

