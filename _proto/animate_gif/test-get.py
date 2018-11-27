from PIL import Image
import requests
import matplotlib.pyplot as plt
import time
import io

url = 'http://bishopweather.com/netcamxla2.jpg'
#url = 'https://lowell.edu/skycamftp/dct_allsky.jpg'
#url = 'http://dct-allsky.lowell.edu/allsky/dct_allsky.jpg'

image_number = 1

while True:
  while True:
    try:
      img = Image.open(requests.get(url, stream=True).raw)
    except:
      print("Oops, that didn't work, try again")
      continue
    break

  img.save("bishop" + format(image_number, '05d') + ".jpg")
  image_number = image_number + 1
  time.sleep(10)
