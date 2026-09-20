#!/usr/bin/env python3

import navx
import wpilib


class MyRobot(wpilib.TimedRobot):
    def robotInit(self):
        # NavX3 uses Navx; AHRS is for older navX sensors.
        # Use kUSB2 for the other USB port. An integer selects CAN instead.
        self.imu = navx.Navx(navx.Navx.Port.kUSB1)
        # Optional update rate in Hz (default: 100):
        # self.imu = navx.Navx(navx.Navx.Port.kUSB1, 50)

    def robotPeriodic(self):
        # Yaw is wrapped to +/-180 degrees; angle is continuous.
        # On a read error, yaw is 360 and angle is NaN.
        wpilib.SmartDashboard.putNumber("NavX3/Yaw", self.imu.getYaw())
        wpilib.SmartDashboard.putNumber("NavX3/Angle", self.imu.getAngle())


if __name__ == "__main__":
    wpilib.run(MyRobot)
