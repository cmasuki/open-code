
#!
# coding=utf-8

"""
GPS version 1.4

Created on Tue Mar 26 11:39:28 2019

@author: npostans
Code to extract kinematics is based on GaitKinematics_1.2.py example code available @vicon.com


Version includes handling of exceptions
Detects is Nexus is open, and calls executable if not
Will run on 32 and 64 bit Windows
Includes full server path names to avoid drive map mismatches
More detailed comments added!

"""

import sys

# ******** Change this path if Anaconda is installed elsewhere ********
sys.path.append( 'C:\\Anaconda32\\Lib\\site-packages')                          

#Add paths for installed versions of Vicon Nexus. ******** Make sure your Nexus version is referenced here *******
#Win64
sys.path.append( 'C:\\Program Files (x86)\\Vicon\\Nexus2.6\\SDK\\Python')
sys.path.append( 'C:\\Program Files (x86)\\Vicon\\Nexus2.6\\SDK\\Win32')
sys.path.append( 'C:\\Program Files (x86)\\Vicon\\Nexus2.3\\SDK\\Python')
sys.path.append( 'C:\\Program Files (x86)\\Vicon\\Nexus2.3\\SDK\\Win32')
#Win32
sys.path.append( 'C:\\Program Files\\Vicon\\Nexus2.6\\SDK\\Python')
sys.path.append( 'C:\\Program Files\\Vicon\\Nexus2.6\\SDK\\Win32')
sys.path.append( 'C:\\Program Files\\Vicon\\Nexus2.3\\SDK\\Python')
sys.path.append( 'C:\\Program Files\\Vicon\\Nexus2.3\\SDK\\Win32')

#Import all required modules

import ViconNexus
import numpy as np
import webbrowser
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import Tkinter as tk
import ttk
import tkFileDialog
import tkMessageBox
from os.path import splitext, normpath
import os
import subprocess

vicon = ViconNexus.ViconNexus()

print   ('Gait Profile Score v1.4')


#Search for Nexus.exe 
if 'PROGRAMFILES(X86)' in os.environ:
    for root, dirs, files in os.walk('C:\\Program Files (x86)\\Vicon\\'):
        for name in files:
            if name == 'Nexus.exe':
                Nexus_Path = os.path.abspath(os.path.join(root, name))

else:
    for root, dirs, files in os.walk('C:\\Program Files\\Vicon\\'):
        for name in files:
            if name == 'Nexus.exe':
                Nexus_Path = os.path.abspath(os.path.join(root, name))

root = tk.Tk()
root.withdraw()

#Check if Nexus is running and if not then start it, user is prompted to acknowledge when Nexus is running
s = subprocess.check_output('tasklist', shell=True)
if "Nexus.exe" not in s:
       
    os.startfile(Nexus_Path)
    root.lift()
    root.wm_attributes("-topmost", 1)
    tkMessageBox.showinfo('Info', 'Click OK when Nexus has opened')
    vicon = ViconNexus.ViconNexus()

#Select patient data. any number of valid c3d files can be opened

root.lift()
root.wm_attributes("-topmost", 1)

# ********Change 'intialdir = ...' as required ********
trials = tkFileDialog.askopenfilenames(parent=root, initialdir= "\\\\rjah\\dfs\\orlau-clinical\\clinical\\Vicon 612\\Network Clinical",
                            filetypes =[("c3d File", "*.c3d")],
                            title = "Gait Profile Score: Select Trial Data")




#Select control data. Must be in a csv file, with kinematic variables in columns, and normal means & SDs in final 2 columns

# ********Change 'intialdir = ...' as required ********
controlfile = tkFileDialog.askopenfilename(parent=root, initialdir= "\\\\rjah\\dfs\\orlau-clinical\\clinical\\GPS\\Control Data",
                           filetypes =[("csv File", "*.csv")],
                           title = "Gait Profile Score: Select Control Data")




#Read and format control data
temp_data = np.genfromtxt(controlfile, delimiter=',')

control_data = temp_data[:,0:15]

# Get normal values for MAP & GPS for controls for plotting graph
norm = temp_data[:,15]
normSD = temp_data[:,16]

#Set up arrays for patient data
patient_data = np.empty([51,15])
MAP = np.empty([18,len(trials)])
aMAP = np.empty([18])
sdMAP = np.empty([18])

#Trial progress box

root = tk.Tk()
root.withdraw()


popup = tk.Toplevel()
popup.title('Gait Profile Score')

progress = 0
progress_var = tk.DoubleVar()
progress_bar = ttk.Progressbar(popup, length = 600, variable=progress_var, maximum=100)
progress_bar.grid(row=1, column=0)#.pack(fill=tk.X, expand=1, side=tk.BOTTOM)
popup.pack_slaves()

progress_step = float(100.0/len(trials))

root.lift()
root.wm_attributes("-topmost", 1)


#Open trials
for t in range (0,len(trials)):
    
    tk.Label(popup, text="Processing " + trials[t]).grid(row=0,column=0)
    
    popup.update()     
    
    
    try:
        vicon.OpenTrial(normpath(splitext(trials[t])[0]),10)
    except:
        tkMessageBox.showerror('Error', 'Cannot open trial')
        popup.destroy()
        sys.exit(1)  
        
        
        
    # Extract information from active trial  
    # Check if there is a valid subject    
    try:
        SubjectName = vicon.GetSubjectNames()[0]
    except IndexError:
        tkMessageBox.showerror('Error', 'No subject in trial\n' + trials[t])
        popup.destroy()
        sys.exit(1)  
        
    
    # Extract Plug-in Gait Lower Body Model Outputs using numpy
    # Check if the kinematics are present in file
    
    modelOutputs = vicon.GetModelOutputNames(SubjectName)
    
    if not ('LPelvisAngles' in modelOutputs): 
        tkMessageBox.showerror('Error', 'No kinematics in trial\n' + trials[t]  )
        popup.destroy()
        sys.exit(1) 
        
        
        
    LPelvisA = np.array([vicon.GetModelOutput(SubjectName, 'LPelvisAngles')])
    RPelvisA = np.array([vicon.GetModelOutput(SubjectName, 'RPelvisAngles')])
    LHipA = np.array([vicon.GetModelOutput(SubjectName, 'LHipAngles')])
    RHipA = np.array([vicon.GetModelOutput(SubjectName, 'RHipAngles')])
    LKneeA = np.array([vicon.GetModelOutput(SubjectName, 'LKneeAngles')])
    RKneeA = np.array([vicon.GetModelOutput(SubjectName, 'RKneeAngles')])
    LAnkA = np.array([vicon.GetModelOutput(SubjectName, 'LAnkleAngles')])
    RAnkA = np.array([vicon.GetModelOutput(SubjectName, 'RAnkleAngles')])
    LFootPro = np.array([vicon.GetModelOutput(SubjectName, 'LFootProgressAngles')])
    RFootPro = np.array([vicon.GetModelOutput(SubjectName, 'RFootProgressAngles')])
   
    
    # Extract Events from Vicon Data
    LFStrike = vicon.GetEvents(SubjectName, "Left", "Foot Strike")[0]
    RFStrike = vicon.GetEvents(SubjectName, "Right", "Foot Strike")[0]
    lenLFS = len(LFStrike)
    lenRFS = len(RFStrike)

    #Check that sufficient event markers are present
    if (lenLFS < 2):
        tkMessageBox.showerror('Error', 'Left event marker(s) missing\n' + trials[t])
        popup.destroy()
        sys.exit(1) 
        
    
    if (lenRFS < 2):
        tkMessageBox.showerror('Error', 'Right event marker(s) missing\n' + trials[t])
        popup.destroy()
        sys.exit(1) 
        

    tn = np.linspace(0, 50, 51)

    if lenLFS and lenRFS >= 2:
        # Calculate Left Gait Cycles
        # Extracting Left Strikes
        LFStrike1 = LFStrike[:1]
        LFStrike2 = LFStrike[1:2]

        # Left Gait Cycle 1
        LGCycle1 = []
        LGCycle1 += LFStrike1
        LGCycle1 += LFStrike2
        LGC1Start = min(LGCycle1)
        LGC1End = max(LGCycle1)

        # Calculate Right Gait Cycles
        # Extract Right Gait Cycles
        RFStrike1 = RFStrike[:1]
        RFStrike2 = RFStrike[1:2]

        # Right Gait Cycle 1
        RGCycle1 = []
        RGCycle1 += RFStrike1
        RGCycle1 += RFStrike2
        RGC1Start = min(RGCycle1)
        RGC1End = max(RGCycle1)

        # Crop data to Gait Cycles
        # Left Gait Cycle 1 X
        LGC1LPelvisX = LPelvisA[0][0][0][LGC1Start:LGC1End]
        LGC1LHipX = LHipA[0][0][0][LGC1Start:LGC1End]
        LGC1LKneeX = LKneeA[0][0][0][LGC1Start:LGC1End]
        LGC1LAnkX = LAnkA[0][0][0][LGC1Start:LGC1End]
        # Left Gait Cycle 1 Y
        LGC1LPelvisY = LPelvisA[0][0][1][LGC1Start:LGC1End]
        LGC1LHipY = LHipA[0][0][1][LGC1Start:LGC1End]
        # Left Gait Cycle 1 Z
        LGC1LPelvisZ = LPelvisA[0][0][2][LGC1Start:LGC1End]
        LGC1LHipZ = LHipA[0][0][2][LGC1Start:LGC1End]
        LGC1LFootProZ = LFootPro[0][0][2][LGC1Start:LGC1End]

        # Right Gait Cycle 1 X
        RGC1RPelvisX = RPelvisA[0][0][0][RGC1Start:RGC1End]
        RGC1RHipX = RHipA[0][0][0][RGC1Start:RGC1End]
        RGC1RKneeX = RKneeA[0][0][0][RGC1Start:RGC1End]
        RGC1RAnkX = RAnkA[0][0][0][RGC1Start:RGC1End]
        # Right Right Gait Cycle 1 Y
        RGC1RPelvisY = RPelvisA[0][0][1][RGC1Start:RGC1End]
        RGC1RHipY = RHipA[0][0][1][RGC1Start:RGC1End]
        # Right Gait Cycle 1 Z
        RGC1RPelvisZ = RPelvisA[0][0][2][RGC1Start:RGC1End]
        RGC1RHipZ = RHipA[0][0][2][RGC1Start:RGC1End]
        RGC1RFootProZ = RFootPro[0][0][2][RGC1Start:RGC1End]
        
        # Set timebase for normalisation
        LGC1t = np.linspace(0, 50, len(LGC1LKneeX))
        RGC1t = np.linspace(0, 50, len(RGC1RKneeX))

        # Arrange and time normalise kinematic data for GPS calculation
        patient_data[:,0] = np.interp(tn, RGC1t, RGC1RPelvisX)
        patient_data[:,1] = np.interp(tn, LGC1t, LGC1LHipX)
        patient_data[:,2] = np.interp(tn, RGC1t, RGC1RHipX)
        patient_data[:,3] = np.interp(tn, LGC1t, LGC1LKneeX)
        patient_data[:,4] = np.interp(tn, RGC1t, RGC1RKneeX)
        patient_data[:,5] = np.interp(tn, LGC1t, LGC1LAnkX)
        patient_data[:,6] = np.interp(tn, RGC1t, RGC1RAnkX)
        patient_data[:,7] = np.interp(tn, RGC1t, RGC1RPelvisY)
        patient_data[:,8] = np.interp(tn, LGC1t, LGC1LHipY)
        patient_data[:,9] = np.interp(tn, RGC1t, RGC1RHipY)
        patient_data[:,10] = np.interp(tn, RGC1t, RGC1RPelvisZ)
        patient_data[:,11] = np.interp(tn, LGC1t, LGC1LHipZ)
        patient_data[:,12] = np.interp(tn, RGC1t, RGC1RHipZ)
        patient_data[:,13] = np.interp(tn, LGC1t, LGC1LFootProZ)
        patient_data[:,14] = np.interp(tn, RGC1t, RGC1RFootProZ)

        #Calculate MAP
        for n in range(0,15):
            MAP[n,t] = np.sqrt(np.mean( (control_data[:,n] - patient_data[:,n])**2) )

        # MAP 15, 16, 17 are Left, Right & Overall GPS
        MAP[15,t] = np.sqrt( (MAP[0,t]**2+MAP[1,t]**2+MAP[3,t]**2+MAP[5,t]**2+MAP[7,t]**2+MAP[8,t]**2+MAP[10,t]**2+MAP[11,t]**2+MAP[13,t]**2)/9 ) 
        MAP[16,t] = np.sqrt( (MAP[0,t]**2+MAP[2,t]**2+MAP[4,t]**2+MAP[6,t]**2+MAP[7,t]**2+MAP[9,t]**2+MAP[10,t]**2+MAP[12,t]**2+MAP[14,t]**2)/9 ) 
        MAP[17,t] = np.sqrt(np.mean(MAP[0:15,t]**2))

    progress += progress_step
    progress_var.set(progress) 
    
root.destroy()
popup.destroy()



# Calculate mean & SD of MAP & GPS across all trials
for n in range(0,18):

    aMAP[n] = np.mean(MAP[n,:])
    sdMAP[n] = np.std(MAP[n,:])


#Get patient details from dialog box
root = tk.Tk()
text = tk.Text(root, relief=tk.GROOVE, height=10, width = 40, borderwidth=1)
text.pack()

root.title('Enter patient details')
root.geometry("300x200")

def getInfo():
    global patientDetails
    patientDetails = (text.get(1.0, tk.END))
    root.quit()
    return patientDetails
  
submit = tk.Button(root, text = "OK", width = 10, command = getInfo)
submit.pack()
submit.place(x=110, y=170)

root.mainloop()
root.destroy()


# Create the file name and graph title
# GPS_PDF_Name = "F:\GPS\\" + SubjectName + " " + vicon.GetTrialName()[1] [0:5]+ " GPS.pdf"


# ******** Change pathname as required ******** 
GPS_PDF_Name = "\\\\rjah\\dfs\\orlau-clinical\\clinical\\GPS\\" + SubjectName + " " + vicon.GetTrialName()[1] [0:5]+ " GPS.pdf"

GPSTitle = "GPS for "  + SubjectName + " " + vicon.GetTrialName()[1][0:5]




# Create Graphs from extracted data and save to pdf

plt.style.use('seaborn-pastel')

with PdfPages(GPS_PDF_Name) as pdf:

        LMAP = (0,aMAP[1],aMAP[3],aMAP[5],0,aMAP[8],0,aMAP[11],aMAP[13],aMAP[15])
        RMAP = (aMAP[0],aMAP[2],aMAP[4],aMAP[6],aMAP[7],aMAP[9],aMAP[10],aMAP[12],aMAP[14],aMAP[16])
        GPS = (0,0,0,0,0,0,0,0,0,aMAP[17])

        sdLMAP = (0,sdMAP[1],sdMAP[3],sdMAP[5],0,sdMAP[8],0,sdMAP[11],sdMAP[13],sdMAP[15])
        sdRMAP = (sdMAP[0],sdMAP[2],sdMAP[4],sdMAP[6],sdMAP[7],sdMAP[9],sdMAP[10],sdMAP[12],sdMAP[14],sdMAP[16])
        sdGPS = (0,0,0,0,0,0,0,0,0,sdMAP[17])
        
        LNorm = (0,norm[1],norm[3],norm[5],0,norm[8],0,norm[11],norm[13],norm[15])
        RNorm = (norm[0],norm[2],norm[4],norm[6],norm[7],norm[9],norm[10],norm[12],norm[14],norm[16])
        GNorm = (0,0,0,0,0,0,0,0,0,norm[17])
            
        index=np.arange(10)
        bar_width = 0.29
        opacity = 1

        xlabels = ["Pelvic Tilt","Hip Flex","Knee Flex","Ankle Df","Pelvic Obl","Hip Abd","Pelvic Rotn","Hip Rotn","Foot Prog","GPS"]

        plt.figure(figsize=(8.26,11.69))
        plt.subplot(2,1,1)
        plt.suptitle(GPSTitle, fontsize=14, fontweight="bold")

        LMAPbar = plt.bar(index, LMAP, bar_width,
                                      alpha=opacity,
                                      label = 'Left',
                                      linewidth = 0,
                                      color='tomato',
                                      yerr=sdLMAP,
                                      error_kw=dict(ecolor='black', lw=1, capsize=5, capthick=1))

        RMAPbar = plt.bar(index + bar_width + 0.043, RMAP, bar_width,
                                      alpha=opacity,
                                      label = 'Right',
                                      linewidth = 0,
                                      color='lightgreen',
                                      yerr=sdRMAP,
                                      error_kw=dict(ecolor='black', lw=1, capsize=5, capthick=1))

        GPSbar = plt.bar(index + (bar_width+0.043)*2, GPS, bar_width,
                                      alpha=opacity,
                                      label = 'Overall',
                                      linewidth = 0,
                                      color='lightblue',
                                      yerr=sdGPS,
                                      error_kw=dict(ecolor='black', lw=1, capsize=5, capthick=1))

        LNormbar = plt.bar(index, LNorm, bar_width,
                                      label = 'Control Data',
                                      linewidth = 0,
                                      color='silver')

        RNormbar = plt.bar(index + bar_width + 0.043, RNorm, bar_width,
                                      linewidth = 0,
                                      color='silver')
    
        GNormbar = plt.bar(index + (bar_width + 0.043)*2, GNorm, bar_width,
                                      linewidth = 0,
                                      color='silver')    


        plt.legend(loc='upper center', bbox_to_anchor=(0.5, 1.0),
          ncol=4, frameon=False, fontsize = 'small')
        plt.title('MAP & GPS', fontsize=14)
        plt.subplot(2,1,1).xaxis.set_ticks_position('bottom')
        plt.subplot(2,1,1).yaxis.set_ticks_position('left')
        
        plt.annotate('Gait Profile Score (GPS)', (0,0), (0, -100), xycoords='axes fraction', textcoords='offset points', va='top', fontsize=20)
        plt.annotate('Control Group', (0,0), (300, -100), xycoords='axes fraction', textcoords='offset points', va='top', fontsize=20)
        plt.annotate('Mean       SD', (0,0), (100, -130), xycoords='axes fraction', textcoords='offset points', va='top', fontsize=20)
        plt.annotate('Mean       SD', (0,0), (300, -130), xycoords='axes fraction', textcoords='offset points', va='top', fontsize=20)

        plt.annotate('Left', (0,0), (0, -160), xycoords='axes fraction', textcoords='offset points', va='top', fontsize=20, color='r')
        plt.annotate("{0:.2f}".format(aMAP[15]), (0,0), (100, -160), xycoords='axes fraction', textcoords='offset points', va='top', fontsize=20, color='r')
        plt.annotate("{0:.2f}".format(sdMAP[15]), (0,0), (200, -160), xycoords='axes fraction', textcoords='offset points', va='top', fontsize=20, color='r')

        plt.annotate('Right', (0,0), (0, -190), xycoords='axes fraction', textcoords='offset points', va='top', fontsize=20, color='g')
        plt.annotate("{0:.2f}".format(aMAP[16]), (0,0), (100, -190), xycoords='axes fraction', textcoords='offset points', va='top', fontsize=20, color='g')
        plt.annotate("{0:.2f}".format(sdMAP[16]), (0,0), (200, -190), xycoords='axes fraction', textcoords='offset points', va='top', fontsize=20, color='g')

        plt.annotate('Overall', (0,0), (0, -220), xycoords='axes fraction', textcoords='offset points', va='top', fontsize=20, color='b')
        plt.annotate("{0:.2f}".format(aMAP[17]), (0,0), (100, -220), xycoords='axes fraction', textcoords='offset points', va='top', fontsize=20, color='b')
        plt.annotate("{0:.2f}".format(sdMAP[17]), (0,0), (200, -220), xycoords='axes fraction', textcoords='offset points', va='top', fontsize=20, color='b')

        plt.annotate("{0:.2f}".format(norm[15]), (0,0), (300, -160), xycoords='axes fraction', textcoords='offset points', va='top', fontsize=20)
        plt.annotate("{0:.2f}".format(normSD[15]), (0,0), (400, -160), xycoords='axes fraction', textcoords='offset points', va='top', fontsize=20)
        
        plt.annotate("{0:.2f}".format(norm[16]), (0,0), (300, -190), xycoords='axes fraction', textcoords='offset points', va='top', fontsize=20)
        plt.annotate("{0:.2f}".format(normSD[16]), (0,0), (400, -190), xycoords='axes fraction', textcoords='offset points', va='top', fontsize=20)

        plt.annotate("{0:.2f}".format(norm[17]), (0,0), (300, -220), xycoords='axes fraction', textcoords='offset points', va='top', fontsize=20)
        plt.annotate("{0:.2f}".format(normSD[17]), (0,0), (400, -220), xycoords='axes fraction', textcoords='offset points', va='top', fontsize=20)

        plt.annotate(patientDetails, (0,0), (100, -300), xycoords='axes fraction', textcoords='offset points', va='top', fontsize=15)

        
        plt.xticks(index + bar_width,xlabels, rotation="vertical")
        plt.ylabel('Deg.')
        
        if max(aMAP) < 40:
            ymax = 40
        else:
            ymax = max(aMAP) + 10        
            
        plt.ylim(0, np.ceil(ymax))

        plt.xlim(-0.2,10.2)
        pdf.savefig()
        plt.close()

        print('PDF File Created in: ' + GPS_PDF_Name)
        print("Completed: GPS Calculation")
        
        tkMessageBox.showinfo('Completed GPS Calculation\n\n','PDF File Created in: ' + GPS_PDF_Name)
   
webbrowser.open_new(GPS_PDF_Name)




