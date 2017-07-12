# Georgian OCR

## Requierments

### Ubuntu

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

### Arch Linux

```bash
pacman -Sy opencv

pip2 install tensorflow
pip2 install keras
pip2 install cairocffi
pip2 install matplotlib
pip2 install image
pip2 install h5py

mkdir -f ~/.fonts
cp bulk_fonts/latin/* ~/.fonts/
cp bulk_fonts/utf-8/* ~/.fonts/
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
