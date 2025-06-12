from keras.applications.vgg19 import VGG19
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.vgg16 import preprocess_input,decode_predictions
from PIL import Image
import numpy as np
print('Imports complete')

img_path = "/home/armaan/Downloads/tf-project/cat.jpg"
print('image path set')


model = VGG19(weights = 'imagenet')
print('Model/Weights initiated')

img = image.load_img(img_path,color_mode = 'rgb', target_size = (224,224))
x = image.img_to_array(img)
x = np.expand_dims(x, axis=0)
print('Image Altered Successfully')

x = preprocess_input(x)
features = model.predict(x)
print('Predictions finished')
p = decode_predictions(features)
print(p[0][0][1])
