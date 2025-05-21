Setup
=====

.. argparse::
    :module: geocompy.apps.setmeasurement.setup
    :func: cli

    The targets first must be defined in a JSON format, providing the point
    IDs, prism types and their 3D coordinates in an arbitrary coordinate
    system. This command can be used to create such a definition.

    .. note::

        A station setup and orientation must be in the same system as the
        targets. If there is no predefined coordinate system, an arbitrary
        local, station centered setup can be used as well.

    The program will give instructions in the terminal at each step. For
    each point an ID is requested, then the target must be aimed at.

    .. caution::
        :class: warning

        The appropriate prism type needs to be set on the instrument before
        recording each target point. The program will automatically request
        the type from the instrument after the point is measured.
