import matplotlib.pyplot as plt
import numpy as np

def global_heading_angle(fly_id, global_heading_angle, global_plots_path, global_data_path, fig_type, dpi_value, fig_num):

    shape = len(np.array(global_heading_angle).shape)          
    if shape == 2: #for single file analysis... the list needs to be nested once more 
        global_heading_angle = [global_heading_angle]

    for f in range(0, len(global_heading_angle)):
        if not isinstance(global_heading_angle[f], list):
            global_heading_angle[f] = global_heading_angle[f].tolist()
    global_heading_angle = np.array(global_heading_angle)
    
    line_transparency = 0.3
    mean = 0
    std = 1
    
    num_sessions = len(global_heading_angle[0])
    sessions = np.arange(1, num_sessions+1)
    fly_labels = []
    for f in fly_id:
        fly_labels.append('fly' + str(f))
    fly_labels.append('mean + std')

    #plot mean and variance of MEAN
    plt1=plt.figure(fig_num, figsize=[10,5])
    for fly in range (0, len(global_heading_angle)):
        plt.plot(sessions, global_heading_angle[fly, :, mean], marker='.', markersize=12, linewidth=0.75, alpha=line_transparency)

    error_array = []
    for sesh in range (0, num_sessions):
        error_array.append(global_heading_angle[:, sesh, mean])
                     
    global_heading_angle_mean_var = np.array([np.nanmean(np.array(error_array), axis=1), np.nanstd(np.array(error_array), axis=1)]) #[mean, var]
    mean = 0
    var = 1
    plt.errorbar(sessions, global_heading_angle_mean_var[mean], yerr = global_heading_angle_mean_var[var], linewidth=1.25, color='black', marker='.', markerfacecolor='red', markersize=18)    
    plt.xticks(sessions, fontsize=12)
    plt.xlabel('Session', fontsize=18)
    plt.ylabel('Mean Heading Angle ($^\circ$)', fontsize=18)
    plt.title('Mean Population Heading Angle', fontsize=18)
    plt.legend(fly_labels ,loc='center left', bbox_to_anchor=(1, 0.5))
    fig_name= global_plots_path+'/mean heading angle'+fig_type
    plt1.savefig(fig_name, dpi=dpi_value)
    fig_num=fig_num+1



    #plot mean and variance of STANDARD DEVIATION

    plt1=plt.figure(fig_num, figsize=[10,5])
    for fly in range (0, len(global_heading_angle)):
        plt.plot(sessions, global_heading_angle[fly, :, std], marker='.', markersize=12, linewidth=0.75, alpha=line_transparency)
            
    error_array = []
    for sesh in range (0, num_sessions):
        error_array.append(global_heading_angle[:, sesh, std])
                     
    plt.errorbar(sessions, np.nanmean(np.array(error_array), axis=1), yerr = np.nanstd(np.array(error_array), axis=1), linewidth=1.25, color='black', marker='.', markerfacecolor='red', markersize=18)   
    plt.xticks(sessions, fontsize=12)
    plt.xlabel('Session', fontsize=18)
    plt.ylabel('Variance Heading Angle ($^\circ$)', fontsize=18)
    plt.title('Variance Population Heading Angle', fontsize=18)
    plt.legend(fly_labels ,loc='center left', bbox_to_anchor=(1, 0.5))
    fig_name= global_plots_path+'/variance heading angle'+fig_type
    plt1.savefig(fig_name, dpi=dpi_value)
    fig_num=fig_num+1
    
    
    return global_heading_angle_mean_var, fig_num

def global_heading_angle_reps(fly_id, global_heading_angle, global_plots_path, global_data_path, fig_type, dpi_value, fig_num):

    shape = len(np.array(global_heading_angle).shape)          
    if shape == 2: #for single file analysis... the list needs to be nested once more 
        global_heading_angle = [global_heading_angle]

    for f in range(0, len(global_heading_angle)):
        if not isinstance(global_heading_angle[f], list):
            global_heading_angle[f] = global_heading_angle[f].tolist()
    global_heading_angle = np.array(global_heading_angle)
    
    line_transparency = 0.3
    mean = 0
    std = 1
    
    num_reps = len(global_heading_angle[0])
    repeats = np.arange(1, num_reps+1)
    fly_labels = []
    for f in fly_id:
        fly_labels.append('fly' + str(f))
    fly_labels.append('mean + std')

    #plot mean and variance of MEAN
    plt1=plt.figure(fig_num, figsize=[10,5])
    for fly in range (0, len(global_heading_angle)):
        plt.plot(repeats, global_heading_angle[fly, :, mean], marker='.', markersize=12, linewidth=0.75, alpha=line_transparency)

    error_array = []
    for rep in range (0, num_reps):
        error_array.append(global_heading_angle[:, rep, mean])

    plt.errorbar(repeats, np.nanmean(np.array(error_array), axis=1), yerr = np.nanstd(np.array(error_array), axis=1), linewidth=1.25, color='black', marker='.', markerfacecolor='red', markersize=18)    
    plt.ylim(-50, 50)
    plt.yticks(np.arange(-50, 60, step=10))  # Set label locations.
    plt.xticks(repeats, fontsize=12)
    plt.xlabel('Repeat', fontsize=18)
    plt.ylabel('Mean Heading Angle ($^\circ$)', fontsize=18)
    plt.title('Mean Population Heading Angle', fontsize=18)
    plt.legend(fly_labels ,loc='center left', bbox_to_anchor=(1, 0.5))
    fig_name= global_plots_path+'/mean heading angle'+fig_type
    plt1.savefig(fig_name, dpi=dpi_value)
    fig_num=fig_num+1



    #plot mean and variance of STANDARD DEVIATION

    plt1=plt.figure(fig_num, figsize=[10,5])
    for fly in range (0, len(global_heading_angle)):
        plt.plot(repeats, global_heading_angle[fly, :, std], marker='.', markersize=12, linewidth=0.75, alpha=line_transparency)
            
    error_array = []
    for rep in range (0, num_reps):
        error_array.append(global_heading_angle[:, rep, std])
                     
    plt.errorbar(repeats, np.nanmean(np.array(error_array), axis=1), yerr = np.nanstd(np.array(error_array), axis=1), linewidth=1.25, color='black', marker='.', markerfacecolor='red', markersize=18)   
    plt.xticks(repeats, fontsize=12)
    plt.xlabel('Repeat', fontsize=18)
    plt.ylabel('Variance Heading Angle ($^\circ$)', fontsize=18)
    plt.title('Variance Population Heading Angle', fontsize=18)
    plt.legend(fly_labels ,loc='center left', bbox_to_anchor=(1, 0.5))
    fig_name= global_plots_path+'/variance heading angle'+fig_type
    plt1.savefig(fig_name, dpi=dpi_value)
    fig_num=fig_num+1
    
    
    return fig_num