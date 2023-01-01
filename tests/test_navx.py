import navx


def test_get_angle():
    imu = navx.AHRS.create_spi()
    imu.getAngle()


def test_get_rotation2d():
    imu = navx.AHRS.create_spi()
    imu.getRotation2d()
