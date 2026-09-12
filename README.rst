robotpy-navx
============

This is a python implementation of the kauailabs NavX library.

.. note:: The RobotPy project is not associated with or endorsed by kauailabs

Documentation
=============

* `Installation <http://robotpy.readthedocs.io/en/stable/install/navx.html>`_
* `Python API Documentation <http://robotpy.readthedocs.io/projects/navx/en/stable/api.html>`_
* `Examples <https://github.com/robotpy/robotpy-navx/tree/main/examples>`_

NavX3 over USB
==============

Studica NavX3 sensors use ``navx.Navx`` rather than the older ``navx.AHRS`` API.
This project includes StudicaLib 2026.0.2, with USB support:

.. code-block:: python

    import navx

    imu = navx.Navx(navx.Navx.Port.kUSB1)  # or kUSB2
    yaw = imu.getYaw()

Use the ``Port`` enum for USB; passing an integer selects a CAN device ID.
See the `USB example <examples/navx3-usb/robot.py>`_ for a complete robot program.

License
=======

The original NavX software is available under the MIT license, as is this.
