# -*- coding: utf-8 -*-
from django.http import HttpResponse , HttpResponseRedirect
from django.shortcuts import render
import os
import subprocess
import tempfile

work_dir = os.path.dirname(os.path.realpath(__file__))

def upload(request):
  image_file = tempfile.NamedTemporaryFile(delete=False)
  image_path = image_file.name
  for chunk in request.FILES['file'].chunks():
      image_file.write(chunk)
  image_file.close()

  ocr_executable = os.path.join(work_dir, '../../bin/ocr.sh')
  export_executable = os.path.join(work_dir, '../../bin/export_words.sh')
  print ocr_executable
  print export_executable
  subprocess.check_output([ocr_executable, image_path])
  recognized_text = subprocess.check_output([export_executable, image_path])

  os.remove(image_path)

  return HttpResponse(recognized_text)
