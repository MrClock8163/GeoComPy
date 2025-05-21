Setup
=====

.. code-block:: shell
    :caption: Invoking the application

    python -m geocompy.apps.setmeasurement.setup -h

The targets first must be defined in a JSON format, providing the point
IDs, prism types and their 3D coordinates in an arbitrary coordinate
system. This module can be used to create such a definition.

.. note::

    A station setup and orientation must be in the same system as the
    targets. If there is no predefined coordinate system, an arbitrary
    local, station centered setup can be used as well.

.. argparse::
    :module: geocompy.apps.setmeasurement.setup
    :func: cli

    measure : @replace
        The program will give instructions in the terminal at each step. For
        each point an ID is requested, then the target must be aimed at.

        .. caution::
            :class: warning

            The appropriate prism type needs to be set on the instrument before
            recording each target point. The program will automatically request
            the type from the instrument after the point is measured.
    
    import : @replace
        If a coordinate list already exists with the target points, it can
        be imported from CSV format.

        As a CSV file may contain any number and types of columns, the
        mapping to the relevant columns can be given with a column spec.
        A column spec is a string, with each character representing a
        column type.

        - ``P``: point ID
        - ``E``: easting
        - ``N``: northing
        - ``Z``: up/height
        - ``_``: ignore/skip column

        Every column spec must specify the ``PENZ`` fields in the appropriate
        order.

        Examples:

        - ``PENZ``: standard column order
        - ``P_ENZ``: skipping 2nd column containing point codes
        - ``EN_Z_P``: mixed column order and skipping
