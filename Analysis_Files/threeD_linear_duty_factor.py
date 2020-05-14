# duty factor = stance duration / swing duration. 

import numpy as np
import matplotlib.pyplot as plt


def duty_factor(stance_start, stance_end, time, fig_num, save_plots, fig_rep_dir, fig_type, dpi_value):
    
    stance_duration=[]
    swing_duration=[]
    duty_factor=[]
    fig_num=fig_num+1
    for leg in range(0,len(stance_start)):
                
        # get times of when stance starts
        stance_start_time=time[stance_start[leg]]

        # get times of when stance ends
        stance_end_time=time[stance_end[leg]]
        
        #make stance_start and stance_end the same length. 
        #make first time stance_start and last time stance_end. 
        if stance_end_time[0] <= stance_start_time[0]:
            stance_end_time = np.delete(stance_end_time, 0)  
        if stance_start_time[-1] > stance_end_time[-1]:
            stance_start_time = np.delete(stance_start_time, -1)
        
        # calculate the difference in time for step duration 
        step_dur=np.diff(stance_start_time)

        # calculate difference between stance start and end for stance duration 
        stance_dur=np.subtract(stance_end_time, stance_start_time)

        # calculate difference between step duration and stance duration for swing duration
        # there will always be an extra stance, remove it so there's the same number as steps. 
        stance_dur = np.delete(stance_dur, -1)
        swing_dur=np.subtract(step_dur, stance_dur)
        
        #convert durations from seconds to  milliseconds
        stance_duration_ms = stance_dur*1000
        stance_duration.append(stance_duration_ms)
        
        swing_duration_ms = swing_dur*1000
        swing_duration.append(swing_duration_ms)
        
        #print and save duty factor (two tone bar graph)
        
#         plt1=plt.figure(fig_num, figsize=[10,5])
#         width = 0.35
#         p1 = plt.bar(stance_start_time[:-1], stance_duration[leg], width)
#         p2 = plt.bar(stance_start_time[:-1], swing_duration[leg], width, bottom=stance_duration[leg])
#         plt.title('Duty Factor, L' +str(leg+1), fontsize=18)
#         plt.ylabel('duration (ms)', fontsize=18)
#         plt.xlabel('time (s)', fontsize=18)
#         plt.legend((p1[0], p2[0]), ('Stance', 'Swing'), fontsize=18)
#         fig_num=fig_num+1
#         fig_name= fig_rep_dir+'/duty factor l'+str(leg+1)+fig_type
#         plt1.savefig(fig_name, dpi=dpi_value)

    return stance_duration, swing_duration, fig_num



def global_duty_factor(fly_id, global_stance_duration, global_swing_duration, nlegs, global_plots_path, global_data_path, fig_type, dpi_value, fig_num):
    
    # stance duration 
    shape = len(np.array(global_stance_duration).shape)          
    if shape == 3: #for single file analysis... the list needs to be nested once more 
        global_stance_duration = [global_stance_duration]
    
    for f in range(0, len(global_stance_duration)):
        if not isinstance(global_stance_duration[f], list):
            global_stance_duration[f] = global_stance_duration[f].tolist()
    global_stance_duration = np.array(global_stance_duration)
    
    # swing duration
    shape = len(np.array(global_swing_duration).shape)          
    if shape == 3: #for single file analysis... the list needs to be nested once more 
        global_swing_duration = [global_swing_duration]
    
    for f in range(0, len(global_swing_duration)):
        if not isinstance(global_swing_duration[f], list):
            global_swing_duration[f] = global_swing_duration[f].tolist()
    global_swing_duration = np.array(global_swing_duration)
    
    #PLOT
    line_transparency = 0.3
    mean = 0
    std = 1
    
    num_sessions = len(global_stance_duration[0])
    sessions = np.arange(1, num_sessions+1)
    
    leg_labels = ['L1', 'L2', 'L3', 'R1', 'R2', 'R3']
    
    global_swing_dur_mean_var = []
    global_stance_dur_mean_var = []
    
    #plot mean and variance of MEAN
    for leg in range(0, nlegs):
        plt1=plt.figure(fig_num, figsize=[10,5])
        width = 0.35

        stance_mean = np.nanmean(global_stance_duration[:, :, leg, mean], axis=0)
        swing_mean = np.nanmean(global_swing_duration[:, :, leg, mean], axis=0)
        
        stance_var = np.nanstd(global_stance_duration[:, :, leg, mean], axis=0)
        swing_var = np.nanstd(global_swing_duration[:, :, leg, mean], axis=0)
        
        global_swing_dur_mean_var.append([swing_mean, swing_var])
        global_stance_dur_mean_var.append([stance_mean, stance_var])
            
        p1 = plt.bar(sessions, stance_mean, width, yerr=stance_var)
        p2 = plt.bar(sessions, swing_mean, width, bottom=stance_mean, yerr=swing_var)
        
        plt.xticks(sessions, fontsize=12)
        plt.xlabel('Session', fontsize=18)
        plt.ylabel('Mean Duration (ms)', fontsize=18)
        plt.title('Mean Population Duty Factor, '+leg_labels[leg], fontsize=18)
        plt.legend((p1[0], p2[0]), ('Stance', 'Swing'), fontsize=18)
        fig_name= global_plots_path+'/mean duty factor '+leg_labels[leg]+fig_type
        plt1.savefig(fig_name, dpi=dpi_value)
        fig_num=fig_num+1
        
    global_swing_dur_mean_var = np.array(global_swing_dur_mean_var)  
    global_stance_dur_mean_var = np.array(global_stance_dur_mean_var)  
        
    #plot mean and variance of VARIANCE
    for leg in range(0, nlegs):
        plt1=plt.figure(fig_num, figsize=[10,5])
        width = 0.35

        stance_mean = np.nanmean(global_stance_duration[:, :, leg, std], axis=0)
        swing_mean = np.nanmean(global_swing_duration[:, :, leg, std], axis=0)
        
        stance_var = np.nanstd(global_stance_duration[:, :, leg, std], axis=0)
        swing_var = np.nanstd(global_swing_duration[:, :, leg, std], axis=0)
        
        p1 = plt.bar(sessions, stance_mean, width, yerr=stance_var)
        p2 = plt.bar(sessions, swing_mean, width, bottom=stance_mean, yerr=swing_var)
        
        plt.xticks(sessions, fontsize=12)
        plt.xlabel('Session', fontsize=18)
        plt.ylabel('Variance Duration (ms)', fontsize=18)
        plt.title('Variance Population Duty Factor, '+leg_labels[leg], fontsize=18)
        plt.legend((p1[0], p2[0]), ('Stance', 'Swing'), fontsize=18)
        fig_name= global_plots_path+'/variance duty factor '+leg_labels[leg]+fig_type
        plt1.savefig(fig_name, dpi=dpi_value)
        fig_num=fig_num+1
          
    return global_swing_dur_mean_var, global_stance_dur_mean_var, fig_num



def global_duty_factor_reps(fly_id, global_stance_duration, global_swing_duration, nlegs, global_plots_path, global_data_path, fig_type, dpi_value, fig_num):
    
    # stance duration 
    shape = len(np.array(global_stance_duration).shape)          
    if shape == 3: #for single file analysis... the list needs to be nested once more 
        global_stance_duration = [global_stance_duration]
    
    for f in range(0, len(global_stance_duration)):
        if not isinstance(global_stance_duration[f], list):
            global_stance_duration[f] = global_stance_duration[f].tolist()
    global_stance_duration = np.array(global_stance_duration)
    
    # swing duration
    shape = len(np.array(global_swing_duration).shape)          
    if shape == 3: #for single file analysis... the list needs to be nested once more 
        global_swing_duration = [global_swing_duration]
    
    for f in range(0, len(global_swing_duration)):
        if not isinstance(global_swing_duration[f], list):
            global_swing_duration[f] = global_swing_duration[f].tolist()
    global_swing_duration = np.array(global_swing_duration)
    
    #PLOT
    line_transparency = 0.3
    mean = 0
    std = 1
    
    num_reps = len(global_stance_duration[0])
    repeats = np.arange(1, num_reps+1)
    
    leg_labels = ['L1', 'L2', 'L3', 'R1', 'R2', 'R3']
    
    global_swing_dur_mean_var = []
    global_stance_dur_mean_var = []
    
    #plot mean and variance of MEAN
    for leg in range(0, nlegs):
        plt1=plt.figure(fig_num, figsize=[10,5])
        width = 0.35

        stance_mean = np.nanmean(global_stance_duration[:, :, leg, mean], axis=0)
        swing_mean = np.nanmean(global_swing_duration[:, :, leg, mean], axis=0)
        
        stance_var = np.nanstd(global_stance_duration[:, :, leg, mean], axis=0)
        swing_var = np.nanstd(global_swing_duration[:, :, leg, mean], axis=0)
        
        global_swing_dur_mean_var.append([swing_mean, swing_var])
        global_stance_dur_mean_var.append([stance_mean, stance_var])
            
        p1 = plt.bar(repeats, stance_mean, width, yerr=stance_var)
        p2 = plt.bar(repeats, swing_mean, width, bottom=stance_mean, yerr=swing_var)
        
        plt.xticks(repeats, fontsize=12)
        plt.xlabel('Repeat', fontsize=18)
        plt.ylabel('Mean Duration (ms)', fontsize=18)
        plt.title('Mean Population Duty Factor, '+leg_labels[leg], fontsize=18)
        plt.legend((p1[0], p2[0]), ('Stance', 'Swing'), fontsize=18)
        fig_name= global_plots_path+'/mean duty factor '+leg_labels[leg]+fig_type
        plt1.savefig(fig_name, dpi=dpi_value)
        fig_num=fig_num+1
        
    global_swing_dur_mean_var = np.array(global_swing_dur_mean_var)  
    global_stance_dur_mean_var = np.array(global_stance_dur_mean_var)    
        
    #plot mean and variance of VARIANCE
    for leg in range(0, nlegs):
        plt1=plt.figure(fig_num, figsize=[10,5])
        width = 0.35

        stance_mean = np.nanmean(global_stance_duration[:, :, leg, std], axis=0)
        swing_mean = np.nanmean(global_swing_duration[:, :, leg, std], axis=0)
        
        stance_var = np.nanstd(global_stance_duration[:, :, leg, std], axis=0)
        swing_var = np.nanstd(global_swing_duration[:, :, leg, std], axis=0)
            
        p1 = plt.bar(repeats, stance_mean, width, yerr=stance_var)
        p2 = plt.bar(repeats, swing_mean, width, bottom=stance_mean, yerr=swing_var)
        
        plt.xticks(repeats, fontsize=12)
        plt.xlabel('Repeat', fontsize=18)
        plt.ylabel('Variance Duration (ms)', fontsize=18)
        plt.title('Variance Population Duty Factor, '+leg_labels[leg], fontsize=18)
        plt.legend((p1[0], p2[0]), ('Stance', 'Swing'), fontsize=18)
        fig_name= global_plots_path+'/variance duty factor '+leg_labels[leg]+fig_type
        plt1.savefig(fig_name, dpi=dpi_value)
        fig_num=fig_num+1
          
    return fig_num