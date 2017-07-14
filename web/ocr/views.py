# -*- coding: utf-8 -*-
from django.http import HttpResponse , HttpResponseRedirect
from django.shortcuts import render
import os
import subprocess
import tempfile
import geo_ocr

work_dir = os.path.dirname(os.path.realpath(__file__))

def index(request):
  return HttpResponseRedirect("/static/index.html")

def upload(request):
  image_file = tempfile.NamedTemporaryFile(delete=False)
  image_path = image_file.name
  for chunk in request.FILES['file'].chunks():
      image_file.write(chunk)
  image_file.close()

  recognized_text = geo_ocr.read(image_path,
      correct_words = True,
      debug=True)

  os.remove(image_path)

  return HttpResponse(recognized_text)
