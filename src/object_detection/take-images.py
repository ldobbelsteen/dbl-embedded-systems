from uuid import uuid4
from time import sleep
from pathlib import Path
from picamera import PiCamera

output_directory = "./images/black_disk/"
Path(output_directory).mkdir(parents=True, exist_ok=True)

camera = PiCamera(resolution=(480, 480), framerate=30)
camera.start_preview()
sleep(2)

image_count = 100
total_time = 5
for i in range(image_count):
    print(str(round(100 * i / image_count, 2)) + "%")
    camera.capture(output_directory + str(uuid4()) + ".jpg")
    sleep(total_time / image_count)
