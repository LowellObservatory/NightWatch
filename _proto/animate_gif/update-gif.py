import imageio
import glob
import os
import time

while True:
  files_path = os.path.join('.', '*')
  files = sorted(
      glob.iglob(files_path), key=os.path.getctime, reverse=True)
  for fl in files[:]:
      if not(fl.endswith(".jpg")):
          files.remove(fl)

  filenames = files[0:30]
  filenames.reverse()
  print(filenames)
  images = []
  for filename in filenames:
      images.append(imageio.imread(filename))
  imageio.mimsave('updateMovie.gif', images, duration=0.066)
  time.sleep(60)
