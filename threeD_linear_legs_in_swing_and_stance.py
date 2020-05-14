import numpy as np
import matplotlib.pyplot as plt


def num_legs_in_swing_and_stance(swing_stance_mat, time, fig_num, save_plots, fig_rep_dir, fig_type, dpi_value):
    
    num_swing_legs=[]
    num_stance_legs=[]
    
    for frame in range(0, len(swing_stance_mat[0])):
        swing_count = 0.0
        stance_count = 0.0
        for leg in range(0, len(swing_stance_mat)):
            if(swing_stance_mat[leg][frame] == 0): #in swing_stance_mat, stance=1 and swing=0
                swing_count = swing_count+1
            if(swing_stance_mat[leg][frame] == 1):
                stance_count = stance_count+1
        num_swing_legs.append(swing_count)
        num_stance_legs.append(stance_count)
    
    
    # plot data 
    
    num_swing_legs = np.array(num_swing_legs)
    
#     plt1=plt.figure(fig_num, figsize=[10,5])
#     plt.plot(time, num_swing_legs, color='black', linewidth=1.25)
#     plt.xlabel('time (seconds)', fontsize=18)
#     plt.ylabel('num legs', fontsize=18)
#     plt.title('Number of Legs in Swing', fontsize=18)
#     fig_num=fig_num+1
#     fig_name= fig_rep_dir+'/num swing legs'+fig_type
#     plt1.savefig(fig_name, dpi=dpi_value)
    
    
    num_stance_legs = np.array(num_stance_legs)
    
#     plt1=plt.figure(fig_num, figsize=[10,5])
#     plt.plot(time, num_stance_legs, color='black', linewidth=1.25)
#     plt.xlabel('time (seconds)', fontsize=18)
#     plt.ylabel('num legs', fontsize=18)
#     plt.title('Number of Legs in Stance', fontsize=18)
#     fig_num=fig_num+1
#     fig_name= fig_rep_dir+'/num stance legs'+fig_type
#     plt1.savefig(fig_name, dpi=dpi_value)
        
    return num_swing_legs, num_stance_legs, fig_num





def global_num_legs_in_swing_and_stance(fly_id, global_num_swing_legs, global_num_stance_legs, nlegs, global_plots_path, global_data_path, fig_type, dpi_value, fig_num):
    
    # NUM SWING LEGS
    
    shape = len(np.array(global_num_swing_legs).shape)          
    if shape == 2: #for single file analysis... the list needs to be nested once more 
        global_num_swing_legs = [global_num_swing_legs]

    for f in range(0, len(global_num_swing_legs)):
        if not isinstance(global_num_swing_legs[f], list):
            global_num_swing_legs[f] = global_num_swing_legs[f].tolist()
    global_num_swing_legs = np.array(global_num_swing_legs)
    
    line_transparency = 0.3
    mean = 0
    std = 1
    
    num_sessions = len(global_num_swing_legs[0])
    sessions = np.arange(1, num_sessions+1)
    fly_labels = []
    for f in fly_id:
        fly_labels.append('fly' + str(f))
    fly_labels.append('mean + std')
    
    #plot mean and variance of MEAN
    plt1=plt.figure(fig_num, figsize=[10,5])
    for fly in range (0, len(global_num_swing_legs)):
        plt.plot(sessions, global_num_swing_legs[fly, :, mean], marker='.', markersize=12, linewidth=0.75, alpha=line_transparency)

    error_array = []
    for sesh in range (0, num_sessions):
        error_array.append(global_num_swing_legs[:, sesh, mean])
                     
    global_num_swing_legs_mean_var = np.array([np.nanmean(np.array(error_array), axis=1), np.nanstd(np.array(error_array), axis=1)]) #[mean, var]
    mean = 0
    var = 1
    plt.errorbar(sessions, global_num_swing_legs_mean_var[mean], yerr = global_num_swing_legs_mean_var[var], linewidth=1.25, color='black', marker='.', markerfacecolor='red', markersize=18)    
    plt.xticks(sessions, fontsize=12)
    plt.xlabel('Session', fontsize=18)
    plt.ylabel('Mean Num Legs in Swing', fontsize=18)
    plt.title('Mean Population Num Legs in Swing', fontsize=18)
    plt.legend(fly_labels ,loc='center left', bbox_to_anchor=(1, 0.5))
    fig_name= global_plots_path+'/mean num swing legs'+fig_type
    plt1.savefig(fig_name, dpi=dpi_value)
    fig_num=fig_num+1



    #plot mean and variance of STANDARD DEVIATION

    plt1=plt.figure(fig_num, figsize=[10,5])
    for fly in range (0, len(global_num_swing_legs)):
        plt.plot(sessions, global_num_swing_legs[fly, :, std], marker='.', markersize=12, linewidth=0.75, alpha=line_transparency)
            
    error_array = []
    for sesh in range (0, num_sessions):
        error_array.append(global_num_swing_legs[:, sesh, std])
                     
    plt.errorbar(sessions, np.nanmean(np.array(error_array)), yerr = np.nanstd(np.array(error_array)), linewidth=1.25, color='black', marker='.', markerfacecolor='red', markersize=18)   
    plt.xticks(sessions, fontsize=12)
    plt.xlabel('Session', fontsize=18)
    plt.ylabel('Variance Num Legs in Swing', fontsize=18)
    plt.title('Variance Population Num Legs in Swing', fontsize=18)
    plt.legend(fly_labels ,loc='center left', bbox_to_anchor=(1, 0.5))
    fig_name= global_plots_path+'/variance num swing legs'+fig_type
    plt1.savefig(fig_name, dpi=dpi_value)
    fig_num=fig_num+1
    
    
    
    # NUM STANCE LEGS
    
    shape = len(np.array(global_num_stance_legs).shape)          
    if shape == 2: #for single file analysis... the list needs to be nested once more 
        global_num_stance_legs = [global_num_stance_legs]

    for f in range(0, len(global_num_stance_legs)):
        if not isinstance(global_num_stance_legs[f], list):
            global_num_stance_legs[f] = global_num_stance_legs[f].tolist()
    global_num_stance_legs = np.array(global_num_stance_legs)
    
    line_transparency = 0.3
    mean = 0
    std = 1
    
    num_sessions = len(global_num_stance_legs[0])
    sessions = np.arange(1, num_sessions+1)
    fly_labels = []
    for f in fly_id:
        fly_labels.append('fly' + str(f))
    fly_labels.append('mean + std')
    
    #plot mean and variance of MEAN
    plt1=plt.figure(fig_num, figsize=[10,5])
    for fly in range (0, len(global_num_stance_legs)):
        plt.plot(sessions, global_num_stance_legs[fly, :, mean], marker='.', markersize=12, linewidth=0.75, alpha=line_transparency)

    error_array = []
    for sesh in range (0, num_sessions):
        error_array.append(global_num_stance_legs[:, sesh, mean])
                     
    global_num_stance_legs_mean_var = np.array([np.nanmean(np.array(error_array), axis=1), np.nanstd(np.array(error_array), axis=1)]) #[mean, var]
    mean = 0
    var = 1
    plt.errorbar(sessions, global_num_stance_legs_mean_var[mean], yerr = global_num_stance_legs_mean_var[var], linewidth=1.25, color='black', marker='.', markerfacecolor='red', markersize=18)    
    plt.xticks(sessions, fontsize=12)
    plt.xlabel('Session', fontsize=18)
    plt.ylabel('Mean Num Legs in Stance', fontsize=18)
    plt.title('Mean Population Num Legs in Stance', fontsize=18)
    plt.legend(fly_labels ,loc='center left', bbox_to_anchor=(1, 0.5))
    fig_name= global_plots_path+'/mean num stance legs'+fig_type
    plt1.savefig(fig_name, dpi=dpi_value)
    fig_num=fig_num+1



    #plot mean and variance of STANDARD DEVIATION

    plt1=plt.figure(fig_num, figsize=[10,5])
    for fly in range (0, len(global_num_stance_legs)):
        plt.plot(sessions, global_num_stance_legs[fly, :, std], marker='.', markersize=12, linewidth=0.75, alpha=line_transparency)
            
    error_array = []
    for sesh in range (0, num_sessions):
        error_array.append(global_num_stance_legs[:, sesh, std])
                     
    plt.errorbar(sessions, np.nanmean(np.array(error_array)), yerr = np.nanstd(np.array(error_array)), linewidth=1.25, color='black', marker='.', markerfacecolor='red', markersize=18)   
    plt.xticks(sessions, fontsize=12)
    plt.xlabel('Session', fontsize=18)
    plt.ylabel('Variance Num Legs in Stance', fontsize=18)
    plt.title('Variance Population Num Legs in Stance', fontsize=18)
    plt.legend(fly_labels ,loc='center left', bbox_to_anchor=(1, 0.5))
    fig_name= global_plots_path+'/variance num stance legs'+fig_type
    plt1.savefig(fig_name, dpi=dpi_value)
    fig_num=fig_num+1
    
    
    return global_num_swing_legs_mean_var, global_num_stance_legs_mean_var, fig_num


def global_num_legs_in_swing_and_stance_reps(fly_id, global_num_swing_legs, global_num_stance_legs, nlegs, global_plots_path, global_data_path, fig_type, dpi_value, fig_num):
    
    # NUM SWING LEGS
    
    shape = len(np.array(global_num_swing_legs).shape)          
    if shape == 2: #for single file analysis... the list needs to be nested once more 
        global_num_swing_legs = [global_num_swing_legs]

    for f in range(0, len(global_num_swing_legs)):
        if not isinstance(global_num_swing_legs[f], list):
            global_num_swing_legs[f] = global_num_swing_legs[f].tolist()
    global_num_swing_legs = np.array(global_num_swing_legs)
    
    line_transparency = 0.3
    mean = 0
    std = 1
    
    num_reps = len(global_num_swing_legs[0])
    repeats = np.arange(1, num_reps+1)
    fly_labels = []
    for f in fly_id:
        fly_labels.append('fly' + str(f))
    fly_labels.append('mean + std')
    
    #plot mean and variance of MEAN
    plt1=plt.figure(fig_num, figsize=[10,5])
    for fly in range (0, len(global_num_swing_legs)):
        plt.plot(repeats, global_num_swing_legs[fly, :, mean], marker='.', markersize=12, linewidth=0.75, alpha=line_transparency)

    error_array = []
    for reps in range (0, num_reps):
        error_array.append(global_num_swing_legs[:, reps, mean])
                     
    plt.errorbar(repeats, np.nanmean(np.array(error_array), axis=1), yerr = np.nanstd(np.array(error_array), axis=1), linewidth=1.25, color='black', marker='.', markerfacecolor='red', markersize=18)    
    plt.xticks(repeats, fontsize=12)
    plt.xlabel('Repeat', fontsize=18)
    plt.ylabel('Mean Num Legs in Swing', fontsize=18)
    plt.title('Mean Population Num Legs in Swing', fontsize=18)
    plt.legend(fly_labels ,loc='center left', bbox_to_anchor=(1, 0.5))
    fig_name= global_plots_path+'/mean num swing legs'+fig_type
    plt1.savefig(fig_name, dpi=dpi_value)
    fig_num=fig_num+1



    #plot mean and variance of STANDARD DEVIATION

    plt1=plt.figure(fig_num, figsize=[10,5])
    for fly in range (0, len(global_num_swing_legs)):
        plt.plot(repeats, global_num_swing_legs[fly, :, std], marker='.', markersize=12, linewidth=0.75, alpha=line_transparency)
            
    error_array = []
    for reps in range (0, num_reps):
        error_array.append(global_num_swing_legs[:, reps, std])
                     
    plt.errorbar(repeats, np.nanmean(np.array(error_array), axis=1), yerr = np.nanstd(np.array(error_array), axis=1), linewidth=1.25, color='black', marker='.', markerfacecolor='red', markersize=18)   
    plt.xticks(repeats, fontsize=12)
    plt.xlabel('Repeat', fontsize=18)
    plt.ylabel('Variance Num Legs in Swing', fontsize=18)
    plt.title('Variance Population Num Legs in Swing', fontsize=18)
    plt.legend(fly_labels ,loc='center left', bbox_to_anchor=(1, 0.5))
    fig_name= global_plots_path+'/variance num swing legs'+fig_type
    plt1.savefig(fig_name, dpi=dpi_value)
    fig_num=fig_num+1
    
    
    
    # NUM STANCE LEGS
    
    shape = len(np.array(global_num_stance_legs).shape)          
    if shape == 2: #for single file analysis... the list needs to be nested once more 
        global_num_stance_legs = [global_num_stance_legs]

    for f in range(0, len(global_num_stance_legs)):
        if not isinstance(global_num_stance_legs[f], list):
            global_num_stance_legs[f] = global_num_stance_legs[f].tolist()
    global_num_stance_legs = np.array(global_num_stance_legs)
    
    line_transparency = 0.3
    mean = 0
    std = 1
    
    num_reps = len(global_num_stance_legs[0])
    repeats = np.arange(1, num_reps+1)
    fly_labels = []
    for f in fly_id:
        fly_labels.append('fly' + str(f))
    fly_labels.append('mean + std')
    
    #plot mean and variance of MEAN
    plt1=plt.figure(fig_num, figsize=[10,5])
    for fly in range (0, len(global_num_stance_legs)):
        plt.plot(repeats, global_num_stance_legs[fly, :, mean], marker='.', markersize=12, linewidth=0.75, alpha=line_transparency)

    error_array = []
    for reps in range (0, num_reps):
        error_array.append(global_num_stance_legs[:, reps, mean])
                     
    plt.errorbar(repeats, np.nanmean(np.array(error_array), axis=1), yerr = np.nanstd(np.array(error_array), axis=1), linewidth=1.25, color='black', marker='.', markerfacecolor='red', markersize=18)    
    plt.xticks(repeats, fontsize=12)
    plt.xlabel('Repeat', fontsize=18)
    plt.ylabel('Mean Num Legs in Stance', fontsize=18)
    plt.title('Mean Population Num Legs in Stance', fontsize=18)
    plt.legend(fly_labels ,loc='center left', bbox_to_anchor=(1, 0.5))
    fig_name= global_plots_path+'/mean num stance legs'+fig_type
    plt1.savefig(fig_name, dpi=dpi_value)
    fig_num=fig_num+1



    #plot mean and variance of STANDARD DEVIATION

    plt1=plt.figure(fig_num, figsize=[10,5])
    for fly in range (0, len(global_num_stance_legs)):
        plt.plot(repeats, global_num_stance_legs[fly, :, std], marker='.', markersize=12, linewidth=0.75, alpha=line_transparency)
            
    error_array = []
    for reps in range (0, num_reps):
        error_array.append(global_num_stance_legs[:, reps, std])
                     
    plt.errorbar(repeats, np.nanmean(np.array(error_array), axis=1), yerr = np.nanstd(np.array(error_array), axis=1), linewidth=1.25, color='black', marker='.', markerfacecolor='red', markersize=18)   
    plt.xticks(repeats, fontsize=12)
    plt.xlabel('Repeat', fontsize=18)
    plt.ylabel('Variance Num Legs in Stance', fontsize=18)
    plt.title('Variance Population Num Legs in Stance', fontsize=18)
    plt.legend(fly_labels ,loc='center left', bbox_to_anchor=(1, 0.5))
    fig_name= global_plots_path+'/variance num stance legs'+fig_type
    plt1.savefig(fig_name, dpi=dpi_value)
    fig_num=fig_num+1
    
    
    return fig_num
