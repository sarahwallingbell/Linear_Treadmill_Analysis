import numpy as np
import matplotlib.pyplot as plt

def step_freq_and_dur(stance_start, time, fig_num, save_plots, fig_rep_dir, fig_type, dpi_value):
    
    step_frequency=[]
    step_duration=[]
    fig_num=fig_num+1
    for leg in range(0,len(stance_start)):
        
        # get times of when stance starts
        stance_time=time[stance_start[leg]]
        
        # calculate the difference in time
        stance_dt=np.diff(stance_time)
        
        #convert duration from seconds to milliseconds
        step_duration_ms = stance_dt*1000
        step_duration.append(step_duration_ms)
        
        # compute step frequency
        freq=1/stance_dt
        
        step_frequency.append(freq)
        

        
#     # plot step FREQUENCY across time
#     # l1
#     plt1=plt.figure(fig_num, figsize=[10,5])
#     plt.plot(time[stance_start[0][1::]], step_frequency[0], color='black', linewidth=1.25)
#     plt.xlabel('time (seconds)', fontsize=18)
#     plt.ylabel('step frequency (1/s)', fontsize=18)
#     plt.title('l1 step frequency', fontsize=18)
#     fig_num=fig_num+1
#     fig_name= fig_rep_dir+'/l1 step frequency'+fig_type
#     plt1.savefig(fig_name, dpi=dpi_value)
    
#     # l2
#     plt2=plt.figure(fig_num, figsize=[10,5])
#     plt.plot(time[stance_start[1][1::]], step_frequency[1], color='black', linewidth=1.25)
#     plt.xlabel('time (seconds)', fontsize=18)
#     plt.ylabel('step frequency (1/s)', fontsize=18)
#     plt.title('l2 step frequency', fontsize=18)
#     fig_num=fig_num+1
#     fig_name= fig_rep_dir+'/l2 step frequency'+fig_type
#     plt2.savefig(fig_name, dpi=dpi_value)
    
#     # l3
#     plt3=plt.figure(fig_num, figsize=[10,5])
#     plt.plot(time[stance_start[2][1::]], step_frequency[2], color='black', linewidth=1.25)
#     plt.xlabel('time (seconds)', fontsize=18)
#     plt.ylabel('step frequency (1/s)', fontsize=18)
#     plt.title('l3 step frequency', fontsize=18)
#     fig_num=fig_num+1
#     fig_name= fig_rep_dir+'/l3 step frequency'+fig_type
#     plt3.savefig(fig_name, dpi=dpi_value)
    
#     # plot step DURATION across time
#     # l1
#     plt1=plt.figure(fig_num, figsize=[10,5])
#     plt.plot(time[stance_start[0][1::]], step_duration[0], color='black', linewidth=1.25)
#     plt.xlabel('time (seconds)', fontsize=18)
#     plt.ylabel('step duration (ms)', fontsize=18)
#     plt.title('l1 step duration', fontsize=18)
#     fig_num=fig_num+1
#     fig_name= fig_rep_dir+'/l1 step duration'+fig_type
#     plt1.savefig(fig_name, dpi=dpi_value)
    
#     # l2
#     plt2=plt.figure(fig_num, figsize=[10,5])
#     plt.plot(time[stance_start[1][1::]], step_duration[1], color='black', linewidth=1.25)
#     plt.xlabel('time (seconds)', fontsize=18)
#     plt.ylabel('step duration (ms)', fontsize=18)
#     plt.title('l2 step duration', fontsize=18)
#     fig_num=fig_num+1
#     fig_name= fig_rep_dir+'/l2 step duration'+fig_type
#     plt2.savefig(fig_name, dpi=dpi_value)
    
#     # l3
#     plt3=plt.figure(fig_num, figsize=[10,5])
#     plt.plot(time[stance_start[2][1::]], step_duration[2], color='black', linewidth=1.25)
#     plt.xlabel('time (seconds)', fontsize=18)
#     plt.ylabel('step duration (ms)', fontsize=18)
#     plt.title('l3 step duration', fontsize=18)
#     fig_num=fig_num+1
#     fig_name= fig_rep_dir+'/l3 step duration'+fig_type
#     plt3.savefig(fig_name, dpi=dpi_value)

    
    return(step_frequency, step_duration, fig_num)
      

def global_step_frequency_and_duration(fly_id, global_step_frequency, global_step_duration, nlegs, global_plots_path, global_data_path, fig_type, dpi_value, fig_num):
    
    #STEP FREQUENCY
    
    shape = len(np.array(global_step_frequency).shape)          
    if shape == 3: #for single file analysis... the list needs to be nested once more 
        global_step_frequency = [global_step_frequency]
    
    for f in range(0, len(global_step_frequency)):
        if not isinstance(global_step_frequency[f], list):
            global_step_frequency[f] = global_step_frequency[f].tolist()
    global_step_frequency = np.array(global_step_frequency)
    
    line_transparency = 0.3
    mean = 0
    std = 1
    
    num_sessions = len(global_step_frequency[0])
    sessions = np.arange(1, num_sessions+1)
    fly_labels = []
    for f in fly_id:
        fly_labels.append('fly' + str(f))
    fly_labels.append('mean + std')
    
    leg_labels = ['L1', 'L2', 'L3', 'R1', 'R2', 'R3']
    
    global_step_freq_mean_var = []

    #plot mean and variance of MEAN
    for leg in range(0, nlegs):
        plt1=plt.figure(fig_num, figsize=[10,5])
        for fly in range (0, len(global_step_frequency)):
            plt.plot(sessions, global_step_frequency[fly, :, leg, mean], marker='.', markersize=12, linewidth=0.75, alpha=line_transparency)
            
        error_array = []
        for sesh in range (0, num_sessions):
            error_array.append(global_step_frequency[:, sesh, leg, mean])

        global_step_freq_mean_var.append(np.array([np.nanmean(np.array(error_array), axis=1), np.nanstd(np.array(error_array), axis=1)])) #[mean, var]
        mean = 0
        var = 1
        plt.errorbar(sessions, global_step_freq_mean_var[leg][mean], yerr = global_step_freq_mean_var[leg][var], linewidth=1.25, color='black', marker='.', markerfacecolor='red', markersize=18)   
        plt.xticks(sessions, fontsize=12)
        plt.xlabel('Session', fontsize=18)
        plt.ylabel('Mean Step Frequency (Hz)', fontsize=18)
        plt.title('Mean Population Step Frequency, '+leg_labels[leg], fontsize=18)
        plt.legend(fly_labels ,loc='center left', bbox_to_anchor=(1, 0.5))
        fig_name= global_plots_path+'/mean step frequency '+leg_labels[leg]+fig_type
        plt1.savefig(fig_name, dpi=dpi_value)
        fig_num=fig_num+1
    
    global_step_freq_mean_var = np.array(global_step_freq_mean_var)

    #plot mean and variance of STANDARD DEVIATION
    for leg in range(0, nlegs):
        plt1=plt.figure(fig_num, figsize=[10,5])
        for fly in range (0, len(global_step_frequency)):
            plt.plot(sessions, global_step_frequency[fly, :, leg, std], marker='.', markersize=12, linewidth=0.75, alpha=line_transparency)
            
        error_array = []
        for sesh in range (0, num_sessions):
            error_array.append(global_step_frequency[:, sesh, leg, std])

        plt.errorbar(sessions, np.nanmean(np.array(error_array)), yerr = np.nanstd(np.array(error_array)), linewidth=1.25, color='black', marker='.', markerfacecolor='red', markersize=18)      
        plt.xticks(sessions, fontsize=12)
        plt.xlabel('Session', fontsize=18)
        plt.ylabel('Variance Step Frequency (Hz)', fontsize=18)
        plt.title('Variance Population Step Frequency, '+leg_labels[leg], fontsize=18)
        plt.legend(fly_labels ,loc='center left', bbox_to_anchor=(1, 0.5))
        fig_name= global_plots_path+'/variance step frequency '+leg_labels[leg]+fig_type
        plt1.savefig(fig_name, dpi=dpi_value)
        fig_num=fig_num+1
        
        
    
    #STEP DURATION    
        
    shape = len(np.array(global_step_duration).shape)          
    if shape == 3: #for single file analysis... the list needs to be nested once more 
        global_step_duration = [global_step_duration]
    
    for f in range(0, len(global_step_duration)):
        if not isinstance(global_step_duration[f], list):
            global_step_duration[f] = global_step_duration[f].tolist()
    global_step_duration = np.array(global_step_duration)
    
    line_transparency = 0.3
    mean = 0
    std = 1
    
    num_sessions = len(global_step_duration[0])
    sessions = np.arange(1, num_sessions+1)
    fly_labels = []
    for f in fly_id:
        fly_labels.append('fly' + str(f))
    fly_labels.append('mean + std')
    
    global_step_dur_mean_var = []

    #plot mean and variance of MEAN
    for leg in range(0, nlegs):
        plt1=plt.figure(fig_num, figsize=[10,5])
        for fly in range (0, len(global_step_duration)):
            plt.plot(sessions, global_step_duration[fly, :, leg, mean], marker='.', markersize=12, linewidth=0.75, alpha=line_transparency)
            
        error_array = []
        for sesh in range (0, num_sessions):
            error_array.append(global_step_duration[:, sesh, leg, mean])

        global_step_dur_mean_var.append(np.array([np.nanmean(np.array(error_array), axis=1), np.nanstd(np.array(error_array), axis=1)])) #[mean, var]
        mean = 0
        var = 1
        plt.errorbar(sessions, global_step_dur_mean_var[leg][mean], yerr = global_step_dur_mean_var[leg][var], linewidth=1.25, color='black', marker='.', markerfacecolor='red', markersize=18)    
        plt.xticks(sessions, fontsize=12)
        plt.xlabel('Session', fontsize=18)
        plt.ylabel('Mean Step Duration (ms)', fontsize=18)
        plt.title('Mean Population Step Duration, '+leg_labels[leg], fontsize=18)
        plt.legend(fly_labels ,loc='center left', bbox_to_anchor=(1, 0.5))
        fig_name= global_plots_path+'/mean step duration '+leg_labels[leg]+fig_type
        plt1.savefig(fig_name, dpi=dpi_value)
        fig_num=fig_num+1
    
    global_step_dur_mean_var = np.array(global_step_dur_mean_var)

    #plot mean and variance of STANDARD DEVIATION
    for leg in range(0, nlegs):
        plt1=plt.figure(fig_num, figsize=[10,5])
        for fly in range (0, len(global_step_duration)):
            plt.plot(sessions, global_step_duration[fly, :, leg, std], marker='.', markersize=12, linewidth=0.75, alpha=line_transparency)
            
        error_array = []
        for sesh in range (0, num_sessions):
            error_array.append(global_step_duration[:, sesh, leg, std])

        plt.errorbar(sessions, np.nanmean(np.array(error_array)), yerr = np.nanstd(np.array(error_array)), linewidth=1.25, color='black', marker='.', markerfacecolor='red', markersize=18)      
        plt.xticks(sessions, fontsize=12)
        plt.xlabel('Session', fontsize=18)
        plt.ylabel('Variance Step Duration (ms)', fontsize=18)
        plt.title('Variance Population Step Duration, '+leg_labels[leg], fontsize=18)
        plt.legend(fly_labels ,loc='center left', bbox_to_anchor=(1, 0.5))
        fig_name= global_plots_path+'/variance step duration '+leg_labels[leg]+fig_type
        plt1.savefig(fig_name, dpi=dpi_value)
        fig_num=fig_num+1
        
    
    return global_step_freq_mean_var, global_step_dur_mean_var, fig_num



def global_step_frequency_and_duration_reps(fly_id, global_step_frequency, global_step_duration, nlegs, global_plots_path, global_data_path, fig_type, dpi_value, fig_num):
    
    #STEP FREQUENCY
    
    shape = len(np.array(global_step_frequency).shape)          
    if shape == 3: #for single file analysis... the list needs to be nested once more 
        global_step_frequency = [global_step_frequency]
    
    for f in range(0, len(global_step_frequency)):
        if not isinstance(global_step_frequency[f], list):
            global_step_frequency[f] = global_step_frequency[f].tolist()
    global_step_frequency = np.array(global_step_frequency)
    
    line_transparency = 0.3
    mean = 0
    std = 1
    
    num_reps = len(global_step_frequency[0])
    repeats = np.arange(1, num_reps+1)
    fly_labels = []
    for f in fly_id:
        fly_labels.append('fly' + str(f))
    fly_labels.append('mean + std')
    
    leg_labels = ['L1', 'L2', 'L3', 'R1', 'R2', 'R3']

    #plot mean and variance of MEAN
    for leg in range(0, nlegs):
        plt1=plt.figure(fig_num, figsize=[10,5])
        for fly in range (0, len(global_step_frequency)):
            plt.plot(repeats, global_step_frequency[fly, :, leg, mean], marker='.', markersize=12, linewidth=0.75, alpha=line_transparency)
            
        error_array = []
        for rep in range (0, num_reps):
            error_array.append(global_step_frequency[:, rep, leg, mean])

        plt.errorbar(repeats, np.nanmean(np.array(error_array), axis=1), yerr = np.nanstd(np.array(error_array), axis=1), linewidth=1.25, color='black', marker='.', markerfacecolor='red', markersize=18)      
        plt.xticks(repeats, fontsize=12)
        plt.xlabel('Repeat', fontsize=18)
        plt.ylabel('Mean Step Frequency (Hz)', fontsize=18)
        plt.title('Mean Population Step Frequency, '+leg_labels[leg], fontsize=18)
        plt.legend(fly_labels ,loc='center left', bbox_to_anchor=(1, 0.5))
        fig_name= global_plots_path+'/mean step frequency '+leg_labels[leg]+fig_type
        plt1.savefig(fig_name, dpi=dpi_value)
        fig_num=fig_num+1
    


    #plot mean and variance of STANDARD DEVIATION
    for leg in range(0, nlegs):
        plt1=plt.figure(fig_num, figsize=[10,5])
        for fly in range (0, len(global_step_frequency)):
            plt.plot(repeats, global_step_frequency[fly, :, leg, std], marker='.', markersize=12, linewidth=0.75, alpha=line_transparency)
            
        error_array = []
        for rep in range (0, num_reps):
            error_array.append(global_step_frequency[:, rep, leg, std])

        plt.errorbar(repeats, np.nanmean(np.array(error_array), axis=1), yerr = np.nanstd(np.array(error_array), axis=1), linewidth=1.25, color='black', marker='.', markerfacecolor='red', markersize=18)      
        plt.xticks(repeats, fontsize=12)
        plt.xlabel('Repeat', fontsize=18)
        plt.ylabel('Variance Step Frequency (Hz)', fontsize=18)
        plt.title('Variance Population Step Frequency, '+leg_labels[leg], fontsize=18)
        plt.legend(fly_labels ,loc='center left', bbox_to_anchor=(1, 0.5))
        fig_name= global_plots_path+'/variance step frequency '+leg_labels[leg]+fig_type
        plt1.savefig(fig_name, dpi=dpi_value)
        fig_num=fig_num+1
        
        
    
    #STEP DURATION    
        
    shape = len(np.array(global_step_duration).shape)          
    if shape == 3: #for single file analysis... the list needs to be nested once more 
        global_step_duration = [global_step_duration]
    
    for f in range(0, len(global_step_duration)):
        if not isinstance(global_step_duration[f], list):
            global_step_duration[f] = global_step_duration[f].tolist()
    global_step_duration = np.array(global_step_duration)
    
    line_transparency = 0.3
    mean = 0
    std = 1
    
    num_reps = len(global_step_duration[0])
    repeats = np.arange(1, num_reps+1)
    fly_labels = []
    for f in fly_id:
        fly_labels.append('fly' + str(f))
    fly_labels.append('mean + std')

    #plot mean and variance of MEAN
    for leg in range(0, nlegs):
        plt1=plt.figure(fig_num, figsize=[10,5])
        for fly in range (0, len(global_step_duration)):
            plt.plot(repeats, global_step_duration[fly, :, leg, mean], marker='.', markersize=12, linewidth=0.75, alpha=line_transparency)
            
        error_array = []
        for rep in range (0, num_reps):
            error_array.append(global_step_duration[:, rep, leg, mean])

        plt.errorbar(repeats, np.nanmean(np.array(error_array), axis=1), yerr = np.nanstd(np.array(error_array), axis=1), linewidth=1.25, color='black', marker='.', markerfacecolor='red', markersize=18)      
        plt.xticks(repeats, fontsize=12)
        plt.xlabel('Repeat', fontsize=18)
        plt.ylabel('Mean Step Duration (ms)', fontsize=18)
        plt.title('Mean Population Step Duration, '+leg_labels[leg], fontsize=18)
        plt.legend(fly_labels ,loc='center left', bbox_to_anchor=(1, 0.5))
        fig_name= global_plots_path+'/mean step duration '+leg_labels[leg]+fig_type
        plt1.savefig(fig_name, dpi=dpi_value)
        fig_num=fig_num+1
    


    #plot mean and variance of STANDARD DEVIATION
    for leg in range(0, nlegs):
        plt1=plt.figure(fig_num, figsize=[10,5])
        for fly in range (0, len(global_step_duration)):
            plt.plot(repeats, global_step_duration[fly, :, leg, std], marker='.', markersize=12, linewidth=0.75, alpha=line_transparency)
            
        error_array = []
        for rep in range (0, num_reps):
            error_array.append(global_step_duration[:, rep, leg, std])

        plt.errorbar(repeats, np.nanmean(np.array(error_array), axis=1), yerr = np.nanstd(np.array(error_array), axis=1), linewidth=1.25, color='black', marker='.', markerfacecolor='red', markersize=18)      
        plt.xticks(repeats, fontsize=12)
        plt.xlabel('Repeat', fontsize=18)
        plt.ylabel('Variance Step Duration (ms)', fontsize=18)
        plt.title('Variance Population Step Duration, '+leg_labels[leg], fontsize=18)
        plt.legend(fly_labels ,loc='center left', bbox_to_anchor=(1, 0.5))
        fig_name= global_plots_path+'/variance step duration '+leg_labels[leg]+fig_type
        plt1.savefig(fig_name, dpi=dpi_value)
        fig_num=fig_num+1
        
    
    return fig_num