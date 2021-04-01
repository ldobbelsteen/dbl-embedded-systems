from io import BytesIO
from PIL import Image
from numpy import squeeze
from picamera import PiCamera
from tflite_runtime.interpreter import Interpreter
from constants import Constants


class Detect:
    __interpreter = None
    __camera = None

    def __init__(self, model_file: str = ""):
        self.__loaded = (model_file != "")
        if self.__loaded:
            self.__interpreter = Interpreter(model_file)
            self.__interpreter.allocate_tensors()
            self.__camera = PiCamera(resolution=(480, 480), framerate=30)

    def __set_input_tensor(self, interpreter, image):
        tensor_index = interpreter.get_input_details()[0]['index']
        input_tensor = interpreter.tensor(tensor_index)()[0]
        input_tensor[:, :] = image

    def detect(self):
        # Take picture
        stream = BytesIO()
        self.__camera.capture(stream, format='jpeg', use_video_port=True)
        stream.seek(0)
        _, input_height, input_width, _ = self.__interpreter.get_input_details()[
            0]['shape']
        image = Image.open(stream).convert('RGB').resize(
            (input_width, input_height), Image.ANTIALIAS)

        # Run detection
        self.__set_input_tensor(self.__interpreter, image)
        self.__interpreter.invoke()
        output_details = self.__interpreter.get_output_details()[0]
        tensor = squeeze(
            self.__interpreter.get_tensor(output_details["index"]))

        # Get confidences from tensor
        black_disk_confidence = (tensor[0] / 255)
        white_disk_confidence = (tensor[1] / 255)
        no_disk_confidence = (tensor[2] / 255)

        # Determine image class with highest confidence
        if no_disk_confidence >= Constants.OBJECT_DETECTION_NONE_THRESHOLD.value:
            return "none"
        if white_disk_confidence >= Constants.OBJECT_DETECTION_WHITE_THRESHOLD.value:
            return "white"
        if black_disk_confidence >= Constants.OBJECT_DETECTION_BLACK_THRESHOLD.value:
            return "black"
        return "unknown"
