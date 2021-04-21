import airsim
import numpy as np
import time
import os
import laneDetect
import cv2
#zuck you mom

client = airsim.CarClient()
client.confirmConnection()
client.enableApiControl(True)
car_controls = airsim.CarControls()
# client.reset()
#client.simSetVehiclePose(airsim.Pose(airsim.Vector3r(183, -198, 1), airsim.utils.to_quaternion(0, 0, np.pi * 3 / 2)), True)
print("API Control enabled: %s" % client.isApiControlEnabled())
client.enableApiControl(False)

while True:
	car_state = client.getCarState().kinematics_estimated.position
	print(car_state)
while False:
	rawImage = client.simGetImage("0", airsim.ImageType.Scene)
	rawImage = cv2.imdecode(airsim.string_to_uint8_array(rawImage), cv2.IMREAD_UNCHANGED)
	a = laneDetect.detectLaneCoordiantes(rawImage)
	
	if (type(a) != bool):
		print("well done!")
		filename = np.array2string(a).replace('\n', '')
		cv2.imwrite(filename + ".png", rawImage)
#os.system('cls')