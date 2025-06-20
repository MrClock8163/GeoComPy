Process
=======

.. code-block:: shell
    :caption: Invoking the application

    python -m geocompy.apps.setmeasurement.process -h

After set measurements are done, the results need to be processed. Thanks
to the easily usable JSON format, this can be done with custom scripts if
needed. For more general use cases, a few processing commands are available
here.

Merging
-------

The results of every set measurement session are saved to a separate file.
When multiple sessions are measured using the same targets from the same
station, the data files need to be merged to process them together.

.. note::

    The merge will be refused if the station information, or the target
    points do not match between the targeted sessions.

Validation
----------

After the measurement sessions are finished, it might be useful to validate,
that each session succeeded, no points were skipped.

Calculation
-----------

The most common calculation needed after set measurements is the determination
of the target coordinates, from results of multiple measurement sessions and/or
cycles. The resulting coordinates (as well as their deviations) are saved
to a simple CSV file.

Usage
-----

.. argparse::
    :module: geocompy.apps.setmeasurement.process
    :func: cli
