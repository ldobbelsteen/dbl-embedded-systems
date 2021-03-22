"""Using TF Lite to detect objects with the Raspberry Pi camera."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import argparse
import io
import re
import time

# from annotation import Annotator

import numpy as np
import picamera

from PIL import Image
from tflite_runtime.interpreter import Interpreter

class ObjectDetection:
  __MODEL_DIR: str = ""
  __LABELS_DIR: str = ""
  __CAMERA_WIDTH: int = -1
  __CAMERA_HEIGHT: int = -1
  __THRESHOLD: int = -0.1


  def __init__(self, model_dir: str = "", labels_dir: str = "", camera_width: int = -1, camera_height: int = -1, threshold: float = -0.1):
        self.__loaded = (model_dir != "" and labels_dir != "" and camera_width > -1 and camera_height > -1.0 and threshold > -1.0)
        if self.__loaded:
          self.__MODEL_DIR = model_dir
          self.__LABELS_DIR = labels_dir
          self.__CAMERA_WIDTH = camera_width
          self.__CAMERA_HEIGHT = camera_height
          self.__THRESHOLD = threshold
    

  def set_input_tensor(self, interpreter, image):
    """Sets the input tensor."""
    # print( interpreter.get_input_details())
    tensor_index = interpreter.get_input_details()[0]['index']
    input_tensor = interpreter.tensor(tensor_index)()[0]
    input_tensor[:, :] = image

  def get_detected_objects(self):
    detected = []
    interpreter = Interpreter(self.__MODEL_DIR)
    interpreter.allocate_tensors()
    _, input_height, input_width, _ = interpreter.get_input_details()[0]['shape']
    fault = False
    with picamera.PiCamera(resolution=(self.__CAMERA_WIDTH, self.__CAMERA_HEIGHT), framerate=30) as camera:
      stream = io.BytesIO()
      _ = camera.capture(stream, format='jpeg', use_video_port=True)
      stream.seek(0)
      image = Image.open(stream).convert('RGB').resize(
          (input_width, input_height), Image.ANTIALIAS)

      self.set_input_tensor(interpreter, image)
      interpreter.invoke()

      tussenstap = interpreter.get_output_details()
      output_details = tussenstap[0]
      tensor = np.squeeze(interpreter.get_tensor(output_details['index']))
      #For looking which item is more prevelant.
      # index_of_maximum = np.where(tensor == max(tensor))[0][0]
      # percentage = str(round((tensor[index_of_maximum] / 255) * 100, 2)) + "%"
      # if (index_of_maximum == 0):
      #   print("Pencil: " + percentage)
      # elif (index_of_maximum == 1):
      #   print("SDCard: " + percentage)
      print("disk_black" +" " + str(round((tensor[0] / 255) * 100, 2)) + "%")
      if((tensor[0] / 255) >= self.__THRESHOLD:
        disk_black = {
          'object': "disk_black",
          'score': tensor[0] / 255,
          'readable_score': str((tensor[0] / 255) * 100) + "%"
          }
        detected.append(disk_black)


      print("disk_white" +" " + str(round((tensor[1] / 255) * 100, 2)) + "%")
      if((tensor[1] / 255) >= self.__THRESHOLD):
        disk_white = {
            'object': "disk_white",
            'score': tensor[1] / 255,
            'readable_score': str((tensor[1] / 255) * 100) + "%"
        }
        detected.append(disk_white)

      three = tensor[2]
      print("empty" +" " + str(round((three / 255) * 100, 2)) + "%")
      if((three / 255) self.__THRESHOLD):
        empty = {
            'object': "empty",
            'score': three / 255,
            'readable_score': str((three / 255) * 100) + "%"
        }
        detected.append(empty)
      
      # print("sdcard" +" " + str(tensor[2] / 255))
      # if((tensor[2] / 255) >= self.__THRESHOLD):
      #   sdcard = {
      #       'object': "sdcard",
      #       'score': str(round((tensor[2] / 255) * 100, 2)) + "%"
      #   }
      #   detected.append(sdcard)
      # print(detected)


      #         if (index_of_maximum == 0):
      #   print("Card: " + percentage)
      # elif (index_of_maximum == 1):
      #   print("Bowl: " + percentage)
      # elif (index_of_maximum == 2):
      #   print("Spray" + percentage)
      # elif (index_of_maximum == 3):
      #   print("Wood: " + percentage)

        #Check self.__TRESHOLD if they meet and then return array.
      # start
      
      #77.0 for later (IA).
      # for obj in results:
      #   if (obj['class_id'] == 33.0):
      #     detected = True
      # # end
      stream.seek(0)
      stream.truncate()
    return detected

  def is_disk_detected(self):
    detected = False
    detected_objects = self.get_detected_objects()
    for obj in detected_objects:
      if obj["object"] == "disk_black" or obj["object"] == "disk_white":
        detected = True
    #Check if detected object has disk 1 and disk 2.
    return detected

  def forbidden_object(self):
    detected = False
    detected_objects = self.get_detected_objects()
    for obj in detected_objects:
      if obj["object"] == "sdcard":
        detected = True
    #Check if detected object has disk 1 and disk 2.
    return detected


def main():
#   #oo: ObjectDetection = ObjectDetection("object_detection/modules/default/model.tflite", "object_detection/modules/default/labels.txt", 640, 480, 0.2)
#   #oo: ObjectDetection = ObjectDetection("object_detection/modules/teachablemachine/quantized/model.tflite", "object_detection/modules/teachablemachine/quantized/labels.txt", 480, 480, 0.4)
  oo: ObjectDetection = ObjectDetection("object_detection/v9/model.tflite", "object_detection/v9/labels.txt", 480, 480, 0.9)
#   print("initialized")
  while True:
    print(oo.get_detected_objects())
    time.sleep(0.5)
#   print(oo.get_detected_objects())
  # print(oo.is_disk_detected())
#   #oo.patrol()

if __name__ == '__main__':
  print("main")
  main()