#sunflower_url = "https://storage.googleapis.com/download.tensorflow.org/example_images/592px-Red_sunflower.jpg"
import tensorflow as tf
from tensorflow import keras
import numpy as np
import cv2
img_height = 180
img_width = 180
signImg = r"C:\Users\stonewow\Desktop\1.webp"
im = cv2.imread(signImg)
cv2.imshow("yes",im)
cv2.waitKey(0)

img = keras.preprocessing.image.load_img(
    signImg, target_size=(img_height, img_width)
)
img_array = keras.preprocessing.image.img_to_array(img)
img_array = tf.expand_dims(img_array, 0) # Create a batch
model = tf.keras.models.load_model("model.h5")
predictions = model.predict(img_array)
score = tf.nn.softmax(predictions[0])
sign = np.argmax(score)
print(
    "{:.2f} percent confidence."
    .format(100 * np.max(score))
)
print(sign)
startingUrl = r"C:\Users\stonewow\Desktop\magshimim\archive\my Meta\ "[:-1]
im = cv2.imread(startingUrl + str(sign) + ".png", cv2.IMREAD_UNCHANGED)
cv2.imshow("yes",im)
cv2.waitKey(0)