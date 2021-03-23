import uuid
import time
import picamera
from pathlib import Path

output_directory = "./images/black_disk/"
Path(output_directory).mkdir(parents=True, exist_ok=True)

camera = picamera.PiCamera(resolution = (480, 480), framerate = 30)
camera.start_preview()
time.sleep(2)

image_count = 100
total_time = 5
for i in range(image_count):
	print(str(round(100 * i / image_count, 2)) + "%")
	camera.capture(output_directory + str(uuid.uuid4()) + ".jpg")
	time.sleep(time / image_count)
