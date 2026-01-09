import navx


def test_get_angle():
    imu = navx.AHRS.create_spi()
    imu.getAngle()


def test_get_rotation2d():
    imu = navx.AHRS.create_spi()
    imu.getRotation2d()


def test_get_board_yaw_axis():
    imu = navx.AHRS.create_spi()
    imu.getBoardYawAxis()


def test_get_velocity_x():
    imu = navx.AHRS.create_spi()
    imu.getVelocityX()


def test_navx_get_yaw():
    imu = navx.Navx(0)
    imu.getYaw()
