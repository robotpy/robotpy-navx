robotpy-navx
============

Python bindings for StudicaLib 2027.0.0-alpha-1, supporting Studica NavX3
sensors over CAN and USB.

.. note:: The RobotPy project is not associated with or endorsed by kauailabs or Studica Robotics.

Documentation
=============

* `Installation <https://robotpy.readthedocs.io/en/stable/install/navx.html>`_
* `Python API Documentation <https://robotpy.readthedocs.io/projects/navx/en/stable/api.html>`_
* `Examples <https://github.com/robotpy/robotpy-navx/tree/main/examples>`_

Quick start
===========

.. code-block:: python

    import navx

    imu = navx.Navx.usb()  # Discover a NavX3 on any USB port
    # Alternatively, select a SystemCore USB port:
    # imu = navx.Navx.usb(navx.UsbPort.USB1)
    # Or open CAN device ID 0 on CAN_S0:
    # imu = navx.Navx(0)

    yaw = imu.getYaw()  # degrees, or None if unavailable
    if yaw is not None:
        print(yaw)

Getters return ``None`` when readings are unavailable, stale, or not enabled
for streaming. Commands return ``navx.Status``; compare with ``navx.Status.OK``.
See the `USB example <examples/navx3-usb/robot.py>`_ for a complete robot program.

This release requires RobotPy 2027 and replaces the legacy sensor API. Older
SPI/I2C sensor interfaces and their simulation examples are no longer included.

License
=======

The original NavX software is available under the MIT license, as is this.
