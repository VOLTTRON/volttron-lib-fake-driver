.. _Fake-Driver:

===========
Fake Driver
===========

The FakeDriver is included as a way to quickly see data published to the message bus in a format
that mimics what a true Driver would produce.  This is an extremely simple implementation of the
:ref:`VOLTTRON Driver Framework <Driver-Framework>`.


Fake Device Driver Configuration
================================

This driver does not connect to any actual device and instead produces random and or pre-configured values.


Driver Config
-------------

There are no arguments for the `driver_config` section of the device configuration file. The `driver_config` entry must
still be present and should be left blank.

Here is an example device configuration file:

.. code-block:: json

    {
        "driver_type": "fake",
        "driver_config": {},
        "registry_config":"config://registry_configs/fake.csv",
        "interval": 5,
        "timezone": "US/Pacific",
        "heart_beat_point": "Heartbeat",
        "publish_breadth_first_all": false,
        "publish_depth_first": false,
        "publish_breadth_first": false
    }

This sample fake device configuration file can also be found in the volttron-lib-fake-driver repository as
`fake.config <https://raw.githubusercontent.com/eclipse-volttron/volttron-lib-fake-driver/main/fake.config>`_

Fake Device Registry Configuration File
---------------------------------------

The registry configuration file is a `CSV <https://en.wikipedia.org/wiki/Comma-separated_values>`_ file. Each row
configures a point on the device.

The following columns are required for each row:

    - **Volttron Point Name** - The name by which the platform and agents running on the platform will refer to this
      point.  For instance, if the `Volttron Point Name` is `HeatCall1` and the device configuration is stored as
      `devices/pnnl/isb2/hvac1`, then an agent would use `pnnl/isb2/hvac1/HeatCall1` to refer to the point when using
      the RPC interface of the driver or actuator agents.
    - **Units** - Used for meta data when creating point information on the historian.
    - **Writable** - Either `TRUE` or `FALSE`. Determines if the point can be written to.  Only points labeled `TRUE`
      can be written.  Writing to points labeled `FALSE` will cause an error to be returned when an agent attempts to
      write to the point.


The following columns are optional:

    - **Starting Value** - Initial value for the point.  If the point is reverted it will change back to this value.  By
      default, points will start with a random value (1-100).
    - **Type** - Value type for the point.  Defaults to "string".  Valid types are:

        * string
        * integer
        * float
        * boolean

Any additional columns will be ignored.  It is common practice to include a `Point Name` or `Reference Point Name` to
include the device documentation's name for the point and `Notes` and `Unit Details` for additional information
about a point.  Please note that there is nothing in the driver that will enforce anything specified in the
`Unit Details` column.

.. csv-table:: BACnet
        :header: Volttron Point Name,Units,Units Details,Writable,Starting Value,Type,Notes

        Heartbeat,On/Off,On/Off,TRUE,0,boolean,Point for heartbeat toggle
        OutsideAirTemperature1,F,-100 to 300,FALSE,50,float,CO2 Reading 0.00-2000.0 ppm
        SampleWritableFloat1,PPM,10.00 (default),TRUE,10,float,Setpoint to enable demand control ventilation
        SampleLong1,Enumeration,1 through 13,FALSE,50,int,Status indicator of service switch
        SampleWritableShort1,%,0.00 to 100.00 (20 default),TRUE,20,int,Minimum damper position during the standard mode
        SampleBool1,On / Off,on/off,FALSE,TRUE,boolean,Status indicator of cooling stage 1
        SampleWritableBool1,On / Off,on/off,TRUE,TRUE,boolean,Status indicator

A sample fake registry configuration file can be found in the volttron-lib-fake-driver repository as
`fake.csv <https://raw.githubusercontent.com/eclipse-volttron/volttron-lib-fake-driver/main/fake.csv>`_.


.. _Fake-Driver-Install:

Installation
============

Installing a Fake driver in the :ref:`Platform Driver Agent <Platform-Driver-Agent>` requires adding copies of the device
configuration and registry configuration files to the Platform Driver's :ref:`configuration store <Configuration-Store>`

- Create a local directory for editing config files (if one doesn't already exist):

.. code-block:: bash

    mkdir myconfig

- Save copies, in myconfig, of the example
  `device config file <https://raw.githubusercontent.com/eclipse-volttron/volttron-lib-fake-driver/main/fake.config>`_
  and `registry file <https://raw.githubusercontent.com/eclipse-volttron/volttron-lib-fake-driver/main/fake.csv>`_
  from the volttron-lib-fake-driver repository.

- Edit the fake.config and fake.csv files, if desired.

- Add fake.csv and fake.config to the :ref:`configuration store <Configuration-Store>`:

.. code-block:: bash

    vctl config store platform.driver devices/campus/building/fake1 myconfig/fake.config
    vctl config store platform.driver registry_configs/fake.csv myconfig/fake.csv --csv

- If it is not already installed, install the Platform Driver agent:

.. code-block:: bash

    vctl install volttron-platform-driver --vip-identity platform.driver --tag driver

- Install the volttron fake driver library:

.. code-block:: bash

    pip install volttron-lib-fake-driver

- If you have a :ref:`Listener Agent<Listener-Agent>` already installed, you should start seeing data being published to
  the bus as soon as the driver agent is started.
