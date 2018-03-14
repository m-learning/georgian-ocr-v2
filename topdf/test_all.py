
import os
import glob
import subprocess

project_dir = '/home/kakha/Projects/georgian-ocr-v2'
images_dir = '/home/kakha/Projects/georgian-ocr-v2/tests/automate'
test_dir = project_dir+'/topdf/tests'

if not os.path.isdir(test_dir):
    os.mkdir(test_dir)
    os.mkdir(test_dir+'/level1')
    os.mkdir(test_dir+'/level2')

os.chdir(project_dir)
cmd = []

files = glob.glob(images_dir+'/level1/*.jpg')
files += glob.glob(images_dir+'/level1/*.png')
for f in files:
    print (f)
    i = f.split('/')[-1]
    p = i.replace('.', '_')
    p += '.pdf'
    cmd.append('python3 geo_ocr/read.py -i %s && cp %s /tmp/ && python3 topdf/lib_pdfkit/convert.py %s && sleep 2 && mv /tmp/export.pdf %s/level1/%s' % (f, f, i, test_dir, p))

files = glob.glob(images_dir+'/level2/*.jpg')
files += glob.glob(images_dir+'/level2/*.png')
for f in files:
    print (f)
    i = f.split('/')[-1]
    p = i.replace('.', '_')
    p += '.pdf'
    cmd.append('python3 geo_ocr/read.py -i %s && cp %s /tmp/ && python3 topdf/lib_pdfkit/convert.py %s && sleep 2 && mv /tmp/export.pdf %s/level2/%s' % (f, f, i, test_dir, p))

cmd = ' && '.join(cmd)
print (cmd)
subprocess.Popen(cmd, shell=True)
