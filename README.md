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
bin/ocr.sh tests/mnatobi-line.png
```

## Model and Test files

see releases page

##Using library

cd georgian-ocr-v2
pip install .


import v2
v2.learning(model_path)
v2.predict(image_path, model_path)


