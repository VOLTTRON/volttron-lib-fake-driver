# VOLTTRON Fake Driver Interface

![Python 3.10](https://img.shields.io/badge/python-3.10-blue.svg)
![Passing?](https://github.com/eclipse-volttron/volttron-lib-fake-driver/actions/workflows/run-tests.yml/badge.svg)
[![pypi version](https://img.shields.io/pypi/v/volttron-lib-fake-driver.svg)](https://pypi.org/project/volttron-lib-fake-driver/)

The FakeDriver is a way to quickly see data published to the message bus in a format that mimics
what a true Driver would produce. This is an extremely simple implementation of the 
[VOLTTRON Driver Framework](https://eclipse-volttron.readthedocs.io/en/latest/external-docs/volttron-platform-driver/index.html). 
This driver does not connect to any actual device and instead produces random and or pre-configured values.

# Requires

* python >= 3.10
* volttron-core >= 2.0.0rc0
* volttron-lib-base-driver >= 2.0.0rc0


# Documentation
More detailed documentation can be found on [ReadTheDocs](https://eclipse-volttron.readthedocs.io/en/latest/external-docs/volttron-lib-fake-driver_docs_root/docs/source/index.html#fake-driver). The RST source
of the documentation for this component is located in the "docs" directory of this repository.


# Installation

Before installing, VOLTTRON should be installed and running.  Its virtual environment should be active.
Information on how to install of the VOLTTRON platform can be found
[here](https://github.com/eclipse-volttron/volttron-core).

1. If it is not already, install the VOLTTRON Platform Driver Agent:

    ```shell
    vctl install volttron-platform-driver --vip-identity platform.driver
    ```

2. Install the volttron fake driver library:

   ```shell
   poetry add --directory $VOLTTRON_HOME volttron-lib-fake-driver
   ```

3. Create configurations for a fake device:

   * Create a file called `fake.config` and add the following JSON to it:

      ```json
      {
          "driver_config": {},
          "registry_config": "config://fake.csv",
          "interval": 5,
          "timezone": "US/Pacific",
          "heart_beat_point": "Heartbeat",
          "driver_type": "fake",
          "publish_breadth_first_all": false,
          "publish_depth_first": false,
          "publish_breadth_first": false
          }
      ```

   * Create another file called `fake.csv` and add the following contents to it:

      ```csv
      Point Name,Volttron Point Name,Units,Units Details,Writable,Starting Value,Type,Notes
      EKG,EKG,waveform,waveform,TRUE,sin,float,Sine wave for baseline output
      Heartbeat,Heartbeat,On/Off,On/Off,TRUE,0,boolean,Point for heartbeat toggle
      OutsideAirTemperature1,OutsideAirTemperature1,F,-100 to 300,FALSE,50,float,CO2 Reading 0.00-2000.0 ppm
      SampleWritableFloat1,SampleWritableFloat1,PPM,1000.00 (default),TRUE,10,float,Setpoint to enable demand control ventilation
      SampleLong1,SampleLong1,Enumeration,1 through 13,FALSE,50,int,Status indicator of service switch
      SampleWritableShort1,SampleWritableShort1,%,0.00 to 100.00 (20 default),TRUE,20,int,Minimum damper position during the standard mode
      SampleBool1,SampleBool1,On / Off,on/off,FALSE,TRUE,boolean,Status indidcator of cooling stage 1
      SampleWritableBool1,SampleWritableBool1,On / Off,on/off,TRUE,TRUE,boolean,Status indicator
      OutsideAirTemperature2,OutsideAirTemperature2,F,-100 to 300,FALSE,50,float,CO2 Reading 0.00-2000.0 ppm
      SampleWritableFloat2,SampleWritableFloat2,PPM,1000.00 (default),TRUE,10,float,Setpoint to enable demand control ventilation
      SampleLong2,SampleLong2,Enumeration,1 through 13,FALSE,50,int,Status indicator of service switch
      SampleWritableShort2,SampleWritableShort2,%,0.00 to 100.00 (20 default),TRUE,20,int,Minimum damper position during the standard mode
      SampleBool2,SampleBool2,On / Off,on/off,FALSE,TRUE,boolean,Status indidcator of cooling stage 1
      SampleWritableBool2,SampleWritableBool2,On / Off,on/off,TRUE,TRUE,boolean,Status indicator
      OutsideAirTemperature3,OutsideAirTemperature3,F,-100 to 300,FALSE,50,float,CO2 Reading 0.00-2000.0 ppm
      SampleWritableFloat3,SampleWritableFloat3,PPM,1000.00 (default),TRUE,10,float,Setpoint to enable demand control ventilation
      SampleLong3,SampleLong3,Enumeration,1 through 13,FALSE,50,int,Status indicator of service switch
      SampleWritableShort3,SampleWritableShort3,%,0.00 to 100.00 (20 default),TRUE,20,int,Minimum damper position during the standard mode
      SampleBool3,SampleBool3,On / Off,on/off,FALSE,TRUE,boolean,Status indidcator of cooling stage 1
      SampleWritableBool3,SampleWritableBool3,On / Off,on/off,TRUE,TRUE,boolean,Status indicator
      HPWH_Phy0_PowerState,PowerState,1/0,1/0,TRUE,0,int,Power on off status
      ERWH_Phy0_ValveState,ValveState,1/0,1/0,TRUE,0,int,power on off status
      EKG_Sin,EKG_Sin,1-0,SIN Wave,TRUE,sin,float,SIN wave
      EKG_Cos,EKG_Cos,1-0,COS Wave,TRUE,sin,float,COS wave
      ```

   * Add fake.csv and fake.config to the configuration store:

      ```
      vctl config store platform.driver devices/campus/building/fake fake.config
      vctl config store platform.driver fake.csv fake.csv --csv
      ```

4. Observe Data

   To see data being published to the bus, install a [Listener Agent](https://github.com/eclipse-volttron/volttron-listener):
   
   ```
   vctl install volttron-listener --start
   ```
   
   Once installed, you should see the data being published by viewing the Volttron logs file that was created in step 2.
   To watch the logs, open a separate terminal and run the following command:
   
   ```
   tail -f <path to folder containing volttron.log>/volttron.log
   ```

# Development

Please see the following for contributing guidelines [contributing](https://github.com/eclipse-volttron/volttron-core/blob/develop/CONTRIBUTING.md).

Please see the following helpful guide about [developing modular VOLTTRON agents](https://eclipse-volttron.readthedocs.io/en/latest/developing-volttron/developing-agents/agent-development.html)


# Disclaimer Notice

This material was prepared as an account of work sponsored by an agency of the
United States Government.  Neither the United States Government nor the United
States Department of Energy, nor Battelle, nor any of their employees, nor any
jurisdiction or organization that has cooperated in the development of these
materials, makes any warranty, express or implied, or assumes any legal
liability or responsibility for the accuracy, completeness, or usefulness or any
information, apparatus, product, software, or process disclosed, or represents
that its use would not infringe privately owned rights.

Reference herein to any specific commercial product, process, or service by
trade name, trademark, manufacturer, or otherwise does not necessarily
constitute or imply its endorsement, recommendation, or favoring by the United
States Government or any agency thereof, or Battelle Memorial Institute. The
views and opinions of authors expressed herein do not necessarily state or
reflect those of the United States Government or any agency thereof.
