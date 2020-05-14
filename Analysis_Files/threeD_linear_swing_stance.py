import scipy
from scipy.signal import find_peaks
import os
import csv
import matplotlib.pyplot as plt
import numpy as np

def swing_stance(l_x_pos, r_x_pos, nlegs, amp_leg, fig_num, save_plots, fig_rep_dir, fig_type, swing_stance_fig_type, dpi_value):
    
    #extract leg positions
    l1_x = l_x_pos[0]
    l2_x = l_x_pos[1]
    l3_x = l_x_pos[2]
    
    r1_x = r_x_pos[0]
    r2_x = r_x_pos[1]
    r3_x = r_x_pos[2]
    
    # create empty matrix
    swing_stance_mat=np.zeros([nlegs,len(l1_x)])
    frames=np.arange(0,len(l1_x))
    
    # find peaks parameters
    prom=0.18
    w=0
    dist=1
    
    # find the indices of local maximums (stance start)
    l1_max_pks, l1_max_properties = scipy.signal.find_peaks(l1_x, prominence=prom, width=w, distance=dist)
    l2_max_pks, l2_max_properties = scipy.signal.find_peaks(l2_x, prominence=prom, width=w, distance=dist)
    l3_max_pks, l3_max_properties = scipy.signal.find_peaks(l3_x, prominence=prom, width=w, distance=dist)
    
    r1_max_pks, r1_max_properties = scipy.signal.find_peaks(r1_x, prominence=prom, width=w, distance=dist)
    r2_max_pks, r2_max_properties = scipy.signal.find_peaks(r2_x, prominence=prom, width=w, distance=dist)
    r3_max_pks, r3_max_properties = scipy.signal.find_peaks(r3_x, prominence=prom, width=w, distance=dist)
    
    stance_start=[l1_max_pks, l2_max_pks, l3_max_pks, r1_max_pks, r2_max_pks, r3_max_pks]

    
    # find the indices of local maximums (swing start)
    l1_min_pks, l1_min_properties = scipy.signal.find_peaks(-l1_x, prominence=prom, width=w, distance=dist)
    l2_min_pks, l2_min_properties = scipy.signal.find_peaks(-l2_x, prominence=prom, width=w, distance=dist)
    l3_min_pks, l3_min_properties = scipy.signal.find_peaks(-l3_x, prominence=prom, width=w, distance=dist)
    
    r1_min_pks, r1_min_properties = scipy.signal.find_peaks(-r1_x, prominence=prom, width=w, distance=dist)
    r2_min_pks, r2_min_properties = scipy.signal.find_peaks(-r2_x, prominence=prom, width=w, distance=dist)
    r3_min_pks, r3_min_properties = scipy.signal.find_peaks(-r3_x, prominence=prom, width=w, distance=dist)
    
    stance_end=[l1_min_pks, l2_min_pks, l3_min_pks, r1_min_pks, r2_min_pks, r3_min_pks]
    
    no_steps = False
    for leg in range (0, len(stance_start)):
        if len(stance_start[leg]) == 0:
            no_steps = True
        if len(stance_end[leg]) == 0:
            no_steps = True
    
    if no_steps:
        return [0], stance_start, stance_end, fig_num

#     # plot l1 with peaks
#     plt1=plt.figure(fig_num, figsize=[10,5])
#     plt.plot(frames, l1_x, color='black', linewidth=1.25)
#     plt.plot(l1_max_pks,l1_x[l1_max_pks], "o", color='red')
#     plt.plot(l1_min_pks,l1_x[l1_min_pks], "o", color='blue')
#     plt.xlabel('Frame (#)', fontsize=18)
#     plt.ylabel('x position (mm)', fontsize=18)
#     plt.title('l1 peaks')
#     plt.legend(['x position', 'stance start', 'swing start'])
#     fig_num=fig_num+1
#     fig_name= fig_rep_dir+'/l1 peaks'+fig_type
#     plt1.savefig(fig_name, dpi=dpi_value)
    
#     # plot l2 with peaks
#     plt2=plt.figure(fig_num, figsize=[10,5])
#     plt.plot(frames, l2_x, color='black', linewidth=1.25)
#     plt.plot(l2_max_pks,l2_x[l2_max_pks], "o", color='red')
#     plt.plot(l2_min_pks,l2_x[l2_min_pks], "o", color='blue')
#     plt.xlabel('Frame (#)', fontsize=18)
#     plt.ylabel('x position (mm)', fontsize=18)
#     plt.title('l2 peaks')
#     plt.legend(['x position', 'stance start', 'swing start'])
#     fig_num=fig_num+1
#     fig_name= fig_rep_dir+'/l2 peaks'+fig_type
#     plt2.savefig(fig_name, dpi=dpi_value)
    
#     # plot l3 with peaks
#     plt3=plt.figure(fig_num, figsize=[10,5])
#     plt.plot(frames, l3_x, color='black', linewidth=1.25)
#     plt.plot(l3_max_pks,l3_x[l3_max_pks], "o", color='red')
#     plt.plot(l3_min_pks,l3_x[l3_min_pks], "o", color='blue')
#     plt.xlabel('Frame (#)', fontsize=18)
#     plt.ylabel('x position (mm)', fontsize=18)
#     plt.title('l3 peaks')
#     plt.legend(['x position', 'stance start', 'swing start'])
#     fig_num=fig_num+1
#     fig_name= fig_rep_dir+'/l3 peaks'+fig_type
#     plt3.savefig(fig_name, dpi=dpi_value)
    
#     # plot r1 with peaks
#     plt4=plt.figure(fig_num, figsize=[10,5])
#     plt.plot(frames, r1_x, color='black', linewidth=1.25)
#     plt.plot(r1_max_pks,r1_x[r1_max_pks], "o", color='red')
#     plt.plot(r1_min_pks,r1_x[r1_min_pks], "o", color='blue')
#     plt.xlabel('Frame (#)', fontsize=18)
#     plt.ylabel('x position (mm)', fontsize=18)
#     plt.title('r1 peaks')
#     plt.legend(['x position', 'stance start', 'swing start'])
#     fig_num=fig_num+1
#     fig_name= fig_rep_dir+'/r1 peaks'+fig_type
#     plt4.savefig(fig_name, dpi=dpi_value)
    
#     # plot r2 with peaks
#     plt5=plt.figure(fig_num, figsize=[10,5])
#     plt.plot(frames, r2_x, color='black', linewidth=1.25)
#     plt.plot(r2_max_pks,r2_x[r2_max_pks], "o", color='red')
#     plt.plot(r2_min_pks,r2_x[r2_min_pks], "o", color='blue')
#     plt.xlabel('Frame (#)', fontsize=18)
#     plt.ylabel('x position (mm)', fontsize=18)
#     plt.title('r2 peaks')
#     plt.legend(['x position', 'stance start', 'swing start'])
#     fig_num=fig_num+1
#     fig_name= fig_rep_dir+'/r2 peaks'+fig_type
#     plt5.savefig(fig_name, dpi=dpi_value)
    
#     # plot r3 with peaks
#     plt6=plt.figure(fig_num, figsize=[10,5])
#     plt.plot(frames, r3_x, color='black', linewidth=1.25)
#     plt.plot(r3_max_pks,r3_x[r3_max_pks], "o", color='red')
#     plt.plot(r3_min_pks,r3_x[r3_min_pks], "o", color='blue')
#     plt.xlabel('Frame (#)', fontsize=18)
#     plt.ylabel('x position (mm)', fontsize=18)
#     plt.title('r3 peaks')
#     plt.legend(['x position', 'stance start', 'swing start'])
#     fig_num=fig_num+1
#     fig_name= fig_rep_dir+'/r3 peaks'+fig_type
#     plt6.savefig(fig_name, dpi=dpi_value)
    
    # compute swing stance
    swing_stance_mat=find_stance(stance_start, stance_end, swing_stance_mat)

    # amputated leg is always in swing. 
    if amp_leg >= 0:
        # amputated leg (L1=0, L2=1, L3=2)
        swing_stance_mat[amp_leg]=np.zeros(len(swing_stance_mat[amp_leg])).tolist()
 
    
        # plot swing stance
    plt8=plt.figure(fig_num, figsize=[15,2])
#     plt.rc('xtick', labelsize = 60)
#     plt.rc('ytick', labelsize = 60)
#     plt.xlim(3000, 4000)
    title = 'Swing Stance Plot (stance = white; swing = black)'
    plt.title(title, fontsize = 18)
    plt.xlabel('frame number (#)', fontsize = 18)
    plt.ylabel('leg', fontsize = 18)
    labels = ['L1', 'L2', 'L3', 'R1', 'R2', 'R3']
    axes = plt.gca()
    axes.set_yticks(np.arange(0, nlegs, 1))
    axes.set_yticklabels(labels)
    plt.imshow(swing_stance_mat, interpolation = 'none', cmap = 'gray',aspect='auto')
    fig_num=fig_num+1
    fig_name= fig_rep_dir+'/swing stance'+swing_stance_fig_type
    plt8.savefig(fig_name, dpi=dpi_value)
        
    
    return swing_stance_mat, stance_start, stance_end, fig_num



def find_stance(stance_start, stance_end, swing_stance_mat):
    for leg in range(0,len(stance_start)):
        # use each stance start as a point of reference and find the next stance end point
        for stance in range(0,len(stance_start[leg])):
            itr=0
            # go until the next stance is found
            end_idx=0
            while stance_end[leg][itr] < stance_start [leg][stance]:
                itr=itr+1 # iterate through to find next end
                if itr > len(stance_end[leg])-1: # deals with boundary condition
                    break
            if itr > len(stance_end[leg])-1:
                swing_stance_mat[leg][stance_start [leg][stance]::]=1
            else:
                swing_stance_mat[leg][stance_start [leg][stance]:stance_end[leg][itr]]=1
            
    return(swing_stance_mat)
              
    

 