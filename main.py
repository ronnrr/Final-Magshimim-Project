import airsim
import cv2
import numpy as np
import os
import time
import laneDetect


class remote:
    def __init__(self):
        # connect to the AirSim simulator
        self.stopLoop = False
        self.client = airsim.CarClient()
        self.client.confirmConnection()
        self.client.enableApiControl(True)
        self.car_controls = airsim.CarControls()
        self.car_controls.brake = 0
        self.car_controls.throttle = 0
        # self.client.reset()
        self.lastDist = 40
        self.objectFound = False
        self.car_state = self.client.getCarState()
        #{   'x_val': -27.714330673217773,
        #'y_val': -8.967389106750488,
        #'z_val': 0.22875159978866577}
        self.client.simSetVehiclePose(airsim.Pose(airsim.Vector3r(183, -198, 1), airsim.utils.to_quaternion(0, 0, np.pi * 3 / 2)), True)
        print("API Control enabled: %s" % self.client.isApiControlEnabled())

    def __del__(self):
        self.client.enableApiControl(False)

    def stopLooper(self):
        return self.stopLoop

    def drive(self): # main loop
        #print(self.car_controls)

        #a = laneDetect.detectLaneCoordiantes(self.takePicture())

        #if (type(a) != bool): # lane detected!
            #print("hi")
        self.car_state = self.client.getCarState()
        #os.system('cls')
        #print("dist", (pow(3.6 * self.car_state.speed, 2)) / (254 * 0.7))
        #print("distance", self.client.getDistanceSensorData().distance)
        if (self.objectFound):
            #print("found")
            if (self.car_state.speed > 0): # slowing to full stop, not moving forward check
                self.brake = 1
                self.lastDist = self.client.getDistanceSensorData().distance # updating
            else:
                if (self.lastDist < self.client.getDistanceSensorData().distance): # increasing distance
                    objectFound = False

        elif (self.car_state.speed > 15):
            #print("too fast boi")
            self.car_controls.brake = 1 # go back
            self.car_controls.throttle = 0
        elif (self.client.getDistanceSensorData().distance > (pow(3.6 * self.car_state.speed, 2)) / (254 * 0.4)):
            self.car_controls.throttle = 1 # drive
            self.car_controls.brake = 0
            #print("full speed")

        else:
            self.objectFound = True
            self.lastDist = self.client.getDistanceSensorData().distance
            #print("slowing down")
            self.car_controls.brake = 1 # go back
            self.car_controls.throttle = 0
            

        if (self.isRightTurn(183, -473)): # x y
            #print("right turn")
            self.car_controls.steering = 1
        if (self.isBetween(-490, -480)): # x x y= 195
            #print("not right turn")
            self.car_controls.steering = 0
        self.client.setCarControls(self.car_controls)
        #print(self.checkDistance())

    def checkDistance(self):
        dist = self.client.getDistanceSensorData()
        #self.client.simPrintLogMessage(f"distance {dist.distance}")
        return dist.distance

    def isRightTurn(self, x, y):
        a = abs(abs(x) - abs(self.car_state.kinematics_estimated.position.x_val)) < 1
        b = abs(abs(y) - abs(self.car_state.kinematics_estimated.position.y_val)) < 1 # increase for longer ride
        #a = abs(abs(1) - abs(self.car_state.kinematics_estimated.position.z_val)) < 1
        return a and b

    def isBetween(self, x, x1):
        #return abs(abs(x) - abs(x)) > 
        car = self.car_state.kinematics_estimated.position
       
        return x < car.y_val and x1 > car.y_val and abs(car.x_val - 196.5) < 5
            # 200
            # 202 


    def takePicture(self):
        # get camera images from the car
        rawImage = self.client.simGetImage("0", airsim.ImageType.Scene)
        return cv2.imdecode(airsim.string_to_uint8_array(rawImage), cv2.IMREAD_UNCHANGED)


def main():
    myRemote = remote()
    while (not myRemote.stopLooper()):
        myRemote.drive()

if __name__ == '__main__':
    main()
