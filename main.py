import airsim
import cv2
import numpy as np
import os
import time
import laneDetect

class remote:
    def __init__(self):
        # connect to the AirSim simulator
        self.client = airsim.CarClient()
        self.client.confirmConnection()
        self.client.enableApiControl(True)
        self.car_controls = airsim.CarControls()
        self.client.reset()
        print("API Control enabled: %s" % self.client.isApiControlEnabled())

    def drive(self):
        a = laneDetect.detectLaneCoordiantes(self.takePicture())
        if (a != 0): # lane detected!
            print("prnting")

    def checkDistance():
        

    def takePicture(self):
        # get camera images from the car
        response = self.client.simGetImages([airsim.ImageRequest("1", airsim.ImageType.Scene, False, False)])[0]  #scene vision image in uncompressed RGB array

        img1d = np.fromstring(response.image_data_uint8, dtype=np.uint8) # get numpy array
        img_rgb = img1d.reshape(response.height, response.width, 3) # reshape array to 3 channel image array H X W X 3
        return img_rgb


def main():
    myRemote = remote()
    myRemote.drive()
    client.enableApiControl(False)

if __name__ == '__main__':
    main()