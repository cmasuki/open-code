#!
# coding=utf-8

"""
EMG high pass filter v1.0 - written by Neil - 24/08/2016
Applies high pass filter to all digital EMG channels. Uses cut off frequency given in script arguments
Requires SciPy library for filter functions, imported from Anaconda in this instance
"""
import sys

sys.path.append( 'C:\\Anaconda32\\Lib\\site-packages')

from ViconNexus import *
from scipy.signal import butter, filtfilt

def EMGHPFilter(vicon, fc):

# Define filter functions
    def butter_highpass(cutoff, fs, order):
        nyq = 0.5 * fs
        normal_cutoff = cutoff / nyq
        b, a = butter(order, normal_cutoff, btype='high', analog=False)
        return b, a

    def butter_highpass_filter(data, cutoff, fs, order):
        b, a = butter_highpass(cutoff, fs, order)
        y = filtfilt(b, a, data)
        return y

# Get video frame rate and number of frames in trial
    frameRate = vicon.GetFrameRate()
    frameCount = vicon.GetFrameCount()

# Loop through devices to find EMG devices. EMG is channelID 1, deviceOutputID for EMG 1 to 16

    deviceIDs = vicon.GetDeviceIDs();
    if( len(deviceIDs) > 0 ):
        for deviceID in deviceIDs:
            deviceName = vicon.GetDeviceDetails( deviceID )[0]
            if deviceName in ('Delsys Digital EMG', 'Delsys Digital IMU EMG'):  #Specify any number of device names here as required              
                channelID = int((vicon.GetDeviceOutputDetails(deviceID,1)[5])[0])
                deviceRate = vicon.GetDeviceDetails(deviceID)[2]
                SamplesPerFrame = 1
                if deviceRate > frameRate:
                    SamplesPerFrame = deviceRate / frameRate

#Set up arrays for EMG data; No of samples * 16 channels
                EMGData = [0]*(frameCount * int(SamplesPerFrame))
                EMGDataFilt = [0]*(frameCount * int(SamplesPerFrame))

#Read in EMG data, filter and write out to same channel
                for deviceOutputID in range (1,17):
                    print deviceOutputID                    
                    EMGData = vicon.GetDeviceChannel(deviceID, deviceOutputID, channelID)[0]
                    EMGDataFilt = (butter_highpass_filter(EMGData, int(fc), int(deviceRate), 2))
                    vicon.SetDeviceChannel(deviceID, deviceOutputID, channelID, EMGDataFilt)

#Call function upon running pipeline
if __name__ == "__main__":    
    vicon = ViconNexus()
    EMGHPFilter(vicon, sys.argv[1])



