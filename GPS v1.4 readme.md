**_GPS v1.4_**  
Calculates MAP and GPS for any number of trials.  
Outputs mean & SD in pdf format. 

**_Requirements_**  
Anaconda (Python 2.7 32 bit version) & Vicon Nexus 2.x  
Kinematic data for a control group in csv format.

**_Instructions_**  
There are some default pathnames specified in the code that can be altered to suit local requirements. These are highlighted in the code with asterisks.  
Nexus must be running for the code to work. The code will check if Nexus is running and, if not, it will automatically start Nexus and prompt the user to confirm when Nexus is fully open, before continuing.  
Upon running the code, an open file dialog box will prompt you to open the c3d files for which you want to calculate the GPS.  
Each c3d file must contain valid lower body kinematic data from PiG and event markers for at least one gait cycle for each limb.  
You will then be prompted to open the csv file containing the control data.  
The MAP and GPS are calculated for one gait cycle in each trial, being the first cycle in the trial for each limb. Right sided pelvic data is used by default.  
Once all the trials are processed, a free text box allows you to enter patient data etc. This will be pasted on to the bottom of the output pdf file.  
The pdf is automatically named using the subject and trial name extracted from the c3d file(s). It is automatically saved to the path specified in the code, so you will probably want to change this. The pdf filed will open once finished.   

**_Control Data_**  
Example control data is supplied, but you should really use control data from your own lab. The kinematic data need to be normalised to give 51 points in the gait cycle.  
The final 2 columns of the control data are the mean and SDs of the control group MAP and GPS values. These are only used for plotting the control data with the results.  
If this is not required then values in the final 2 columns can be set to zero.

Data are arranged in columns in the following order: Pelvic Tilt, Hip Flex, Hip Flex, Knee Flex, Knee Flex, Ankle DF, Ankle DF, Pelvic Obl, Hip Abd, Hip Abd, Pelvic Rotn, Hip Rotn, Hip Rotn, Foot Prog, Foot Prog, Mean MAP, SD MAP.  

Note that columns are duplicated (with the exception of the pelvic data) for convenience so that patient and control data are in matrices of equal dimensions, which facilitates the calculation. The example control data are from the right limb. 

**_Validation_**  
Results for a sample trial have been checked against gdi-gps-calculator-v-3-2.xlsx (available at https://wwrichard.net/resources/gps-map-and-gdi-calculators/). Carrying out your own validation is still recommended though.

**_Contact_**  
neil.postans@nhs.net



