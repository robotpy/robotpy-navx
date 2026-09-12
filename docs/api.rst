
NavX API
========

This is not installed on the robot by default.

NavX3 Interface
---------------

Studica NavX3 sensors use :class:`navx.Navx`, not :class:`navx.AHRS`.

.. code-block:: python

    import navx

    # Use the Port enum for USB, not an integer CAN device ID.
    imu = navx.Navx(navx.Navx.Port.kUSB1)
    # For the other USB port:
    # imu = navx.Navx(navx.Navx.Port.kUSB2)
    # To specify the update rate (default: 100 Hz):
    # imu = navx.Navx(navx.Navx.Port.kUSB1, 50)

    yaw = imu.getYaw()      # degrees, wrapped to +/-180
    angle = imu.getAngle()  # continuous angle in degrees

For CAN, pass the configured device ID instead, for example ``navx.Navx(0)``.
USB selection uses ``navx.Navx.Port``, not ``wpilib.SerialPort.Port``.

Methods returning an error flag use ``True`` for an error and ``False`` for
success. Output parameters are returned alongside the flag, for example:

.. code-block:: python

    error, rotation = imu.getRotation2D()
    if not error:
        heading = rotation.degrees()

``getYaw()`` returns 360 on error; ``getAngle()`` returns NaN on error.

.. autoclass:: navx.Navx
    :members:
    :undoc-members:
    :show-inheritance:

NavX AHRS Interface
-------------------

.. autoclass:: navx.AHRS
    :members:
    :undoc-members:
    :show-inheritance:

    
