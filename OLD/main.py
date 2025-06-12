from gpiozero import Button
from time import sleep
from picamera2 import Picamera2
from keras.applications.vgg19 import VGG19
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.vgg16 import preprocess_input, decode_predictions
from PIL import Image
import numpy as np
import subprocess

#Define Button
button = Button(21, pull_up=True)

#initialize espeak process through shell
def espeak(text: str, pitch: int=50) -> int:
    """ Use espeak to convert text to speech. """
    return subprocess.run(['espeak', f'-p {pitch}', text]).returncode

while True:
    if button.is_pressed:
        picam2 = Picamera2()
        picam2.start()
        picam2.capture_file('image2.jpg')
        
        print('Image taken')
        
        
        img_path = "/home/armaan/Downloads/tf-project/image2.jpg"
        print('image path set')
        
        
        
        model = VGG19(weights = 'imagenet')
        print('Model/Weights initiated')
        #here 
        original_img = image.load_img(img_path,color_mode = 'rgb', target_size = (224,224))
        img = original_img.transpose(method=Image.FLIP_TOP_BOTTOM)
        x = image.img_to_array(img)
        x = np.expand_dims(x, axis=0)
        print('Image Altered Successfully')
        
        x = preprocess_input(x)
        features = model.predict(x)
        print('Predictions finished')
        p = decode_predictions(features)
        print(p[0][0][1])
        espeak(p[0][0][1])
