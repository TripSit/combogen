import mimetypes
import base64
import os

def file_to_dataURI(path):
  if not os.path.exists(path):
      raise FileNotFoundError

  mime, _ = mimetypes.guess_type(path)

  with open(path, 'rb') as f:
      data = f.read()
      data64 = base64.b64encode(data)
      return 'data:{};base64,{}'.format(mime, data64.decode('UTF-8'))