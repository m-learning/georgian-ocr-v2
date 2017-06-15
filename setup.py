from setuptools import setup

setup(name='geo_ocr',
      version='2',
      description='Georgian ocr',
      url='https://github.com/m-learning/georgian-ocr-v2',
      packages=['v2'],
      install_requires=[
        'numpy',
        'matplotlib',
        'tensorflow',
        'keras',
        'cairocffi',
        'editdistance',
        'nose2',
        'h5py',
        'pillow',
        'opencv-python',
        'scikit-image'
      ])

