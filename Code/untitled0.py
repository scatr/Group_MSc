#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 12 17:55:00 2020

@author: scatr
"""
########################VERSION REQUIREMENTS##################################
'''
Python v3.6
Numpy 1.14.3
Pandas 0.23.0
'''
##############################################################################

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

### ways to break code
'''
    >> the arrays rely on the number of measurements taken on each probe to be equal
    >> the directory is specified in a linux format
    >> requires the file to be saved in a specific format
    >> measurements must be specified in mm
'''

########################GLOBAL USER SPECIFIED PARAMETERS#######################
#Number of probes
probe_num=4
path='~/Documents/Group_MSc/Experiment/All_probes_calibration/'
#files of the format ***mm.csv. Specify the numbers
folder=np.array([50,101,200,305,400,500,600,700,799,900,950])


###############################################################################

no_probes=range(probe_num)
folder_length=len(folder)
#Results array
results=np.zeros((folder_length,probe_num))
maxs=np.zeros((folder_length,probe_num))
mins=np.zeros((folder_length,probe_num))
percentage_error=np.zeros((folder_length,probe_num))


def access_folder(results, maxs, mins, percentage_error):
    
    V_anticipated=anticipated_Vout(folder)
    for j in range(len(folder)):
        time_series=pd.read_csv(path+str(folder[j]) +'mm.csv')
        np_time=time_series.values
    
    
        for i in no_probes:
           data_points=len(np_time[:,i])
           probe_ave=sum(np_time[:,i])/data_points
           results[j,i]=probe_ave
           maxs[j,i]=max(np_time[:,i])
           mins[j,i]=min(np_time[:,i])      
           percentage_error[j,i]=100*abs(probe_ave-V_anticipated[j])/probe_ave
        
    return results, maxs, mins, percentage_error


    
def anticipated_Vout(folder):
    V_anticipated=np.zeros(len(folder))
    for q in range(len(folder)):
        V_anticipated[q]=5*(0.09*(folder[q]*9.81/1000)+0.04)   
    
    return V_anticipated



def plot_results(no_probes, results, folder):
    best_fit_probes=np.zeros((len(results[:,0]),len(no_probes)))
    V_anticipated=anticipated_Vout(folder)
    
    for p in no_probes:
        plt.figure(p)
        y_axis=results[:,p]
        
        #find the line of best fit
        m, c = np.polyfit(folder, y_axis,1)
        best_fit=c+m*folder
       
     
        plt.plot(folder, y_axis,'rx', folder, best_fit, '--k',folder, V_anticipated, 'b')
        plt.title('Probe '+ str(p+1))
        plt.xlabel('Distance, (mm)')
        plt.ylabel('Voltage Output, (V)')
        
        best_fit_probes[:,p]=best_fit
    return best_fit_probes
        
    
#Creates a dictionary format and converts to dataframe in pandas, saving the
#resulting csv file to a specific directory
def create_csv(no_probes, results, folder, maxs, mins, percentage_error):
    V_anticipated=anticipated_Vout(folder)
    best_fit_probes=plot_results(no_probes, results, folder)
    output={}
    output['Height,(mm)']=folder

    for p in no_probes:
        output['Probe ' +str(p)]=(results[:,p])

    output[""]=""

    for p in no_probes:
        output['Probe ' +str(p) + ' best fit']=best_fit_probes[:,p]
    
    #cant fit the empty columns
    output[""]=""
    
    output['Anticipated V_out']=(V_anticipated)
    
    output[""]=""
    
    for p in no_probes:
        output["P"+str(p) +" max"]=maxs[:,p]
    output[""]=""
    
    for p in no_probes:
        output["P"+str(p) +" min"]=mins[:,p]
    output[""]=""
    
    for p in no_probes:
        output["P"+str(p) +" error"]=percentage_error[:,p]
    output[""]=""
    
    df=pd.DataFrame(data=output)
    print(df)
    
    #Need to write a part of code which checks if this exists
    df.to_csv('~/Documents/Group_MSc/Experiment/'+'Calibration_results.csv', index=False)


results, maxs, mins, percentage_error=access_folder(results, maxs, mins, percentage_error)
    
best_fit_probes=plot_results(no_probes, results, folder)

create_csv(no_probes, results, folder, maxs, mins, percentage_error)


