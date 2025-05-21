Measure
=======

.. code-block:: shell
    :caption: Invoking the application

    python -m geocompy.apps.setmeasurement.measure -h

Once the target definition JSON is created, the measurement sets can
be started. In each measurement session the time, internal temperature
and battery level are recorded at start and again at finish. For each
target the polar coordinates, as well as the cartesian coordinates are
recorded.

.. argparse::
    :module: geocompy.apps.setmeasurement.measure
    :func: cli
