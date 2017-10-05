from skimage.measure import compare_ssim
import configparser
import cv2
import time
from urllib.request import urlopen
import numpy as np
import datetime
import sys


class Stream(object):
  def __init__(self, config_file):
    print("Reading config from ", config_file)
    config = configparser.ConfigParser()
    config.read(config_file)
    stream = config['stream']
    self.url = stream['Url']
    self.stream_type = stream['Type']
    self.params = config['params']
    self.options = config['options']
    self.previous_img = None
    self.current_img = None
    print("Streaming from ", self.url)

  def url_to_image(self):
    url_stream = urlopen(self.url)
    stream_type = self.stream_type
    if stream_type == 'jpeg':
      image = url_stream.read()
      #bytes_ = bytearray(url_stream.read())
      #image = np.asarray(bytes_, dtype=np.uint8)
    elif stream_type == 'mjpeg':
      image = self.url_mjpeg_to_image(url_stream)
    else:
      print('The utils format {} is not implemented.'.format(stream_type))
      sys.exit(1)
    cvt_color = self.params.getboolean('BGR2RGB')
    if cvt_color:
       image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    self.current_img = cv2.imdecode(np.fromstring(image, dtype=np.uint8),
                                    cv2.IMREAD_COLOR)
    return image

  def url_mjpeg_to_image(self, url_stream):
    bytes_ = bytes()
    while True:
      bytes_ += url_stream.read(1024)
      a = bytes_.find(b'\xff\xd8')
      b = bytes_.find(b'\xff\xd9')
      if a != -1 and b != -1:
        jpg = bytes_[a:b+2]
        return np.array(jpg)
        #return np.fromstring(jpg, dtype=np.uint8)

  def next_frame(self):
    timestamp = time.time()
    current_time = datetime.datetime.fromtimestamp(timestamp)
    time_str = current_time.strftime('%Y-%m-%d_%H:%M:%S')

    image = self.url_to_image()
    is_display = self.options.getboolean('Display')
    if is_display:
        cv2.imshow(time_str, self.current_img)
        cv2.moveWindow(time_str, 100, 100)
        cv2.waitKey(100)
        cv2.destroyAllWindows()

    print("=" * 40)
    print("Current time is ", time_str)
    score_threshold = self.params.getfloat('SimThreshold')
    sim_score = self.similarity_score(self.previous_img, self.current_img)
    self.previous_img = self.current_img
    if sim_score > score_threshold:
      print("Nothing new detected (similarity score = {})".format(sim_score))
      self.next_frame()
    else:
      print("Detected something! (similarity score = {})".format(sim_score))
      return image

  def similarity_score(self, img1, img2):
    if (img1 is None) or (img2 is None):
        return -1
    (score, diff) = compare_ssim(img1, img2, multichannel=True, full=True)
    return score


if __name__ == "__main__":
  config_file = './config.ini'
  s = Stream(config_file)
  while True:
      image = s.next_frame()