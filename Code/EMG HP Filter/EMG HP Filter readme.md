
**_EMG HP Filter_**

A simple high pass filter for EMG data

EMG signals collected in the gait lab are often affected by low frequency noise, such as movement artefact. This high pass (HP) filter has been implemented to remove low frequency artefacts and baseline offsets while preserving the EMG signal.

The filter routine has been implemented in Python, using the Vicon Nexus Python module to handle reading and writing of the c3d file, with other standard Python modules for signal processing used for the filter. 

**_Instructions_**

The plugin is designed to be called from within Nexus as a custom pipeline, and can be run on an individual trial, or as a batch process. A c3d file must have been created for each trial prior to running the pipeline. The cut off frequency is set using an integer value in the Nexus pipeline options. The code searches for the EMG devices by name, as defined in Nexus when data are collected. Default names are ‘Delsys Digital EMG’ and 'Delsys Digital IMU EMG’, and these will need to be changed in the code to match local naming conventions. Filtering will not be applied to any other devices, or if the EMG devices are not named.

**Caution!** The original EMG data in the c3d file are overwritten with the filtered data. To revert back to unfiltered data you will need to recreate the c3d file.


**_Requirements_** 

Vicon Nexus 2.x & Anaconda (Python 2.7 32 bit version)
Works with a combination of Vicon and Delsys systems, but could be modified for other EMG systems.

**_Contact_**
neil.postans@nhs.net
