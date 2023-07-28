import sys
import zipfile
import os

directory_zip = os.fsencode('./data/zip/')

print(os.listdir(directory_zip))
    
for file in os.listdir(directory_zip):
  filename = os.fsdecode(file)
  print('Here', filename)
  if filename.endswith('.zip'):
    with zipfile.ZipFile('./data/zip/' + filename, 'r') as zip_ref:
      zip_ref.extractall('./data/txt/')
