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

save model file model.h5 to results/data from release page
then
```
python geo_ocr/read.py -i tests/mnatobi-lines.png --debug
```

## Model and Test files

see releases page

## Use as module

```bash
pip install .
```

```python
import geo_ocr
geo_ocr.train()
geo_ocr.read(path)
```
