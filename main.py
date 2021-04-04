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
        # self.client.reset()
        self.car_state = self.client.getCarState()
        self.client.simSetVehiclePose(airsim.Pose(airsim.Vector3r(183, -198, 1), airsim.utils.to_quaternion(0, 0, np.pi * 3 / 2)), True)
        print("API Control enabled: %s" % self.client.isApiControlEnabled())

    def __del__(self):
        self.client.enableApiControl(False)

    def drive(self):
        # a = laneDetect.detectLaneCoordiantes(self.takePicture())
        # if (a != 0): # lane detected!
        #    print("prnting")
        self.car_state = self.client.getCarState()
        if (self.car_state.speed > 15):
            self.car_controls.throttle = -1
            self.car_controls.is_manual_gear = True
            self.car_controls.manual_gear = -1
        elif (self.checkDistance() > 20):
            self.car_controls.throttle = 1
            self.car_controls.is_manual_gear = False
            self.car_controls.manual_gear = 0
        else:
            self.car_controls.throttle = 0
            self.car_controls.is_manual_gear = False
            self.car_controls
        self.client.setCarControls(self.car_controls)

    def checkDistance(self):
        dist = self.client.getDistanceSensorData()
        self.client.simPrintLogMessage(f"distance {dist.distance}")
        return dist.distance

    def takePicture(self):
        # get camera images from the car
        rawImage = self.client.simGetImage("0", airsim.ImageType.Scene)
        return cv2.imdecode(airsim.string_to_uint8_array(rawImage), cv2.IMREAD_UNCHANGED)


def main():
    myRemote = remote()
    while True:
        myRemote.drive()

if __name__ == '__main__':
    main()
