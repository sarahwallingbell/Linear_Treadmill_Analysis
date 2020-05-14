from scipy import signal
import matplotlib.pyplot as plt
import numpy as np
import scipy.signal
import math

def velocity_and_heading_angle(fly_num, head, thorax, fps, time, belt_speed, save_plots, fig_rep_dir, fig_type, dpi_value, fig_num):
    
    x = head['head_x']
    y = head['head_y']
    
#     # butterworth filter
#     fc = 15# Cut-off frequency of the filter
#     w = fc / (fps / 2) # Normalize the frequency
#     b, a = signal.butter(4, w, 'low')
#     filt_x = signal.filtfilt(b, a, x)
    
    # linear velocity
    dx=np.diff(x )
    dy=np.diff(y)
    D=np.sqrt(np.power(dy,2) + np.power(dx,2)) # distance
    dt=1/fps
    t=np.linspace(0,len(dx)/fps,len(dx))
    t_head=np.linspace(0,len(x)/fps,len(x))
    belt_vel=belt_speed
    lin_vel=((dx/dt) + belt_vel)
    
#     # plot linear velocity
#     plt1=plt.figure(fig_num, figsize=[20,5])
#     plt.plot(t,lin_vel, color='black', linewidth=1.25)
#     plt.plot(np.array([0,t[-1]]), np.array([belt_vel/correction_value, belt_vel/correction_value]), color='red', linewidth=1.5) 
#     plt.xlabel('Time (seconds)', fontsize=18)
#     plt.ylabel('Linear Velocity (mm/s)', fontsize=18)
#     plt.title('fly ' + str(fly_num) + ' linear velocity', fontsize=18)
#     fig_num=fig_num+1
    
#     fig_name= fig_rep_dir+'/linear velocity'+fig_type
#     plt1.savefig(fig_name, dpi=dpi_value)
    
    
#     # plot median filtered velocity
#     plt2=plt.figure(fig_num, figsize=[20,5])
#     plt.plot(t,linear_vel_filter, color='black', linewidth=1.25)
#     plt.plot(np.array([0,t[-1]]), np.array([belt_vel/correction_value, belt_vel/correction_value]), color='red', linewidth=1.5) 
#     plt.xlabel('Time (seconds)', fontsize=18)
#     plt.ylabel('Filtered Linear Velocity (mm/s)', fontsize=18)
#     plt.title('fly ' + str(fly_num) + ' median velocity linear velocity', fontsize=18)
#     fig_num=fig_num+1
    
#     fig_name= fig_rep_dir+'/filtered linear velocity'+fig_type
#     plt2.savefig(fig_name, dpi=dpi_value)
    
    # rotational velocity
    heading_angle=[]
    tx=thorax['thorax_x']
    ty=thorax['thorax_y']
    
    # set angle relative to thorax 
    dx_angle=x-tx
    dy_angle=y-ty
    
    # compute heading angle
    for j in range(0, len(tx)):
        heading_angle.append(math.degrees(math.atan2(dy_angle[j],dx_angle[j])))
    
    heading_angle=np.array(heading_angle) # convert to numpy array
    
#     # plot heading angle
#     plt3=plt.figure(fig_num, figsize=[20,5])
#     plt.plot(time, heading_angle, color='black', linewidth=1.25)
#     plt.xlabel('Time (seconds)', fontsize=18)
#     plt.ylabel('Heading Angle ($^\circ$)', fontsize=18)
#     plt.title('fly ' + str(fly_num) + ' Heading Angle', fontsize=18)
#     fig_num=fig_num+1
    
#     fig_name= fig_rep_dir+'/heading angle'+fig_type
#     plt3.savefig(fig_name, dpi=dpi_value)
    
    # rotational velocity
    rot_vel=np.diff(heading_angle)/dt
    t=time[1::]
#     plt4=plt.figure(fig_num, figsize=[20,5])
#     plt.plot(t,rot_vel, color='black', linewidth=1.25)
#     plt.xlabel('Time (seconds)', fontsize=18)
#     plt.ylabel('Rotational Velocity ($^\circ$/s)', fontsize=18)
#     plt.title('fly ' + str(fly_num) + ' Rotational Velocity', fontsize=18)
#     fig_num=fig_num+1
    
#     fig_name= fig_rep_dir+'/rotational velocity'+fig_type
#     plt4.savefig(fig_name, dpi=dpi_value)
    
    
    return(lin_vel, heading_angle, rot_vel, fig_num)



def global_velocity(fly_id, global_linear_velocity, global_rotational_velocity, global_plots_path, global_data_path, fig_type, dpi_value, fig_num):
    
    #LINEAR VELOCITY
    
    shape = len(np.array(global_linear_velocity).shape)          
    if shape == 2: #for single file analysis... the list needs to be nested once more 
        global_linear_velocity = [global_linear_velocity]

    for f in range(0, len(global_linear_velocity)):
        if not isinstance(global_linear_velocity[f], list):
            global_linear_velocity[f] = global_linear_velocity[f].tolist()
    global_linear_velocity = np.array(global_linear_velocity)
    
    line_transparency = 0.3
    mean = 0
    std = 1
    
    num_sessions = len(global_linear_velocity[0])
    sessions = np.arange(1, num_sessions+1)
    fly_labels = []
    for f in fly_id:
        fly_labels.append('fly' + str(f))
    fly_labels.append('mean + std')

    #plot mean and variance of MEAN
    plt1=plt.figure(fig_num, figsize=[10,5])
    for fly in range (0, len(global_linear_velocity)):
        plt.plot(sessions, global_linear_velocity[fly, :, mean], marker='.', markersize=12, linewidth=0.75, alpha=line_transparency)
            
    error_array = []
    for sesh in range (0, num_sessions):
        error_array.append(global_linear_velocity[:, sesh, mean])
                     
    global_linear_velocity_mean_var = np.array([np.nanmean(np.array(error_array), axis=1), np.nanstd(np.array(error_array), axis=1)]) #[mean, var]
    mean = 0
    var = 1
    plt.errorbar(sessions, global_linear_velocity_mean_var[mean], yerr = global_linear_velocity_mean_var[var], linewidth=1.25, color='black', marker='.', markerfacecolor='red', markersize=18)    
    plt.xticks(sessions, fontsize=12)
    plt.xlabel('Session', fontsize=18)
    plt.ylabel('Mean Linear Velocity (mm/s)', fontsize=18)
    plt.title('Mean Population Linear Velocity', fontsize=18)
    plt.legend(fly_labels ,loc='center left', bbox_to_anchor=(1, 0.5))
    fig_name= global_plots_path+'/mean linear velocity'+fig_type
    plt1.savefig(fig_name, dpi=dpi_value)
    fig_num=fig_num+1



    #plot mean and variance of STANDARD DEVIATION

    plt1=plt.figure(fig_num, figsize=[10,5])
    for fly in range (0, len(global_linear_velocity)):
        plt.plot(sessions, global_linear_velocity[fly, :, std], marker='.', markersize=12, linewidth=0.75, alpha=line_transparency)
            
    error_array = []
    for sesh in range (0, num_sessions):
        error_array.append(global_linear_velocity[:, sesh, std])
                     
    plt.errorbar(sessions, np.nanmean(np.array(error_array)), yerr = np.nanstd(np.array(error_array)), linewidth=1.25, color='black', marker='.', markerfacecolor='red', markersize=18)       
    plt.xticks(sessions, fontsize=12)
    plt.xlabel('Session', fontsize=18)
    plt.ylabel('Variance Linear Velocity (mm/s)', fontsize=18)
    plt.title('Variance Population Linear Velocity', fontsize=18)
    plt.legend(fly_labels ,loc='center left', bbox_to_anchor=(1, 0.5))
    fig_name= global_plots_path+'/variance linear velocity'+fig_type
    plt1.savefig(fig_name, dpi=dpi_value)
    fig_num=fig_num+1
    
    
    
    
    #ROTATIONAL VELOCITY
    
    shape = len(np.array(global_rotational_velocity).shape)          
    if shape == 2: #for single file analysis... the list needs to be nested once more 
        global_rotational_velocity = [global_rotational_velocity]

    for f in range(0, len(global_rotational_velocity)):
        if not isinstance(global_rotational_velocity[f], list):
            global_rotational_velocity[f] = global_rotational_velocity[f].tolist()
    global_rotational_velocity = np.array(global_rotational_velocity)
    
    line_transparency = 0.3
    mean = 0
    std = 1
    
    num_sessions = len(global_rotational_velocity[0])
    sessions = np.arange(1, num_sessions+1)
    fly_labels = []
    for f in fly_id:
        fly_labels.append('fly' + str(f))
    fly_labels.append('mean + std')

    #plot mean and variance of MEAN
    plt1=plt.figure(fig_num, figsize=[10,5])
    for fly in range (0, len(global_rotational_velocity)):
        plt.plot(sessions, global_rotational_velocity[fly, :, mean], marker='.', markersize=12, linewidth=0.75, alpha=line_transparency)
            
    error_array = []
    for sesh in range (0, num_sessions):
        error_array.append(global_rotational_velocity[:, sesh, mean])
                     
    plt.errorbar(sessions, np.nanmean(np.array(error_array)), yerr = np.nanstd(np.array(error_array)), linewidth=1.25, color='black', marker='.', markerfacecolor='red', markersize=18)      
    plt.xticks(sessions, fontsize=12)
    plt.xlabel('Session', fontsize=18)
    plt.ylabel('Mean Rotational Velocity ($^\circ$/s)', fontsize=18)
    plt.title('Mean Population Rotational Velocity', fontsize=18)
    plt.legend(fly_labels ,loc='center left', bbox_to_anchor=(1, 0.5))
    fig_name= global_plots_path+'/mean rotational velocity'+fig_type
    plt1.savefig(fig_name, dpi=dpi_value)
    fig_num=fig_num+1



    #plot mean and variance of STANDARD DEVIATION

    plt1=plt.figure(fig_num, figsize=[10,5])
    for fly in range (0, len(global_rotational_velocity)):
        plt.plot(sessions, global_rotational_velocity[fly, :, std], marker='.', markersize=12, linewidth=0.75, alpha=line_transparency)
            
    error_array = []
    for sesh in range (0, num_sessions):
        error_array.append(global_rotational_velocity[:, sesh, std])
                     
    plt.errorbar(sessions, np.nanmean(np.array(error_array)), yerr = np.nanstd(np.array(error_array)), linewidth=1.25, color='black', marker='.', markerfacecolor='red', markersize=18)      
    plt.xticks(sessions, fontsize=12)
    plt.xlabel('Session', fontsize=18)
    plt.ylabel('Variance Rotational Velocity ($^\circ$/s)', fontsize=18)
    plt.title('Variance Population Rotational Velocity', fontsize=18)
    plt.legend(fly_labels ,loc='center left', bbox_to_anchor=(1, 0.5))
    fig_name= global_plots_path+'/variance rotational velocity'+fig_type
    plt1.savefig(fig_name, dpi=dpi_value)
    fig_num=fig_num+1
    
    
    return global_linear_velocity_mean_var, fig_num
    
    
    

def global_velocity_reps(fly_id, global_linear_velocity, global_rotational_velocity, global_plots_path, global_data_path, fig_type, dpi_value, fig_num):
    
    #LINEAR VELOCITY
    
    shape = len(np.array(global_linear_velocity).shape)          
    if shape == 2: #for single file analysis... the list needs to be nested once more 
        global_linear_velocity = [global_linear_velocity]

    for f in range(0, len(global_linear_velocity)):
        if not isinstance(global_linear_velocity[f], list):
            global_linear_velocity[f] = global_linear_velocity[f].tolist()
    global_linear_velocity = np.array(global_linear_velocity)
    
    line_transparency = 0.3
    mean = 0
    std = 1
    
    num_reps = len(global_linear_velocity[0])
    repeats = np.arange(1, num_reps+1)
    fly_labels = []
    for f in fly_id:
        fly_labels.append('fly' + str(f))
    fly_labels.append('mean + std')

    #plot mean and variance of MEAN
    plt1=plt.figure(fig_num, figsize=[10,5])
    for fly in range (0, len(global_linear_velocity)):
        plt.plot(repeats, global_linear_velocity[fly, :, mean], marker='.', markersize=12, linewidth=0.75, alpha=line_transparency)
            
    error_array = []
    for rep in range (0, num_reps):
        error_array.append(global_linear_velocity[:, rep, mean])
                     
    plt.errorbar(repeats, np.nanmean(np.array(error_array), axis=1), yerr = np.nanstd(np.array(error_array), axis=1), linewidth=1.25, color='black', marker='.', markerfacecolor='red', markersize=18)    
    plt.xticks(repeats, fontsize=12)
    plt.xlabel('Repeat', fontsize=18)
    plt.ylabel('Mean Linear Velocity (mm/s)', fontsize=18)
    plt.title('Mean Population Linear Velocity', fontsize=18)
    plt.legend(fly_labels ,loc='center left', bbox_to_anchor=(1, 0.5))
    fig_name= global_plots_path+'/mean linear velocity'+fig_type
    plt1.savefig(fig_name, dpi=dpi_value)
    fig_num=fig_num+1



    #plot mean and variance of STANDARD DEVIATION

    plt1=plt.figure(fig_num, figsize=[10,5])
    for fly in range (0, len(global_linear_velocity)):
        plt.plot(repeats, global_linear_velocity[fly, :, std], marker='.', markersize=12, linewidth=0.75, alpha=line_transparency)
            
    error_array = []
    for rep in range (0, num_reps):
        error_array.append(global_linear_velocity[:, rep, std])
                     
    plt.errorbar(repeats, np.nanmean(np.array(error_array), axis=1), yerr = np.nanstd(np.array(error_array), axis=1), linewidth=1.25, color='black', marker='.', markerfacecolor='red', markersize=18)       
    plt.xticks(repeats, fontsize=12)
    plt.xlabel('Repeat', fontsize=18)
    plt.ylabel('Variance Linear Velocity (mm/s)', fontsize=18)
    plt.title('Variance Population Linear Velocity', fontsize=18)
    plt.legend(fly_labels ,loc='center left', bbox_to_anchor=(1, 0.5))
    fig_name= global_plots_path+'/variance linear velocity'+fig_type
    plt1.savefig(fig_name, dpi=dpi_value)
    fig_num=fig_num+1
    
    
    
    
    #ROTATIONAL VELOCITY
    
    shape = len(np.array(global_rotational_velocity).shape)          
    if shape == 2: #for single file analysis... the list needs to be nested once more 
        global_rotational_velocity = [global_rotational_velocity]

    for f in range(0, len(global_rotational_velocity)):
        if not isinstance(global_rotational_velocity[f], list):
            global_rotational_velocity[f] = global_rotational_velocity[f].tolist()
    global_rotational_velocity = np.array(global_rotational_velocity)
    
    line_transparency = 0.3
    mean = 0
    std = 1
    
    num_reps = len(global_rotational_velocity[0])
    repeats = np.arange(1, num_reps+1)
    fly_labels = []
    for f in fly_id:
        fly_labels.append('fly' + str(f))
    fly_labels.append('mean + std')

    #plot mean and variance of MEAN
    plt1=plt.figure(fig_num, figsize=[10,5])
    for fly in range (0, len(global_rotational_velocity)):
        plt.plot(repeats, global_rotational_velocity[fly, :, mean], marker='.', markersize=12, linewidth=0.75, alpha=line_transparency)
            
    error_array = []
    for rep in range (0, num_reps):
        error_array.append(global_rotational_velocity[:, rep, mean])
                     
    plt.errorbar(repeats, np.nanmean(np.array(error_array), axis=1), yerr = np.nanstd(np.array(error_array), axis=1), linewidth=1.25, color='black', marker='.', markerfacecolor='red', markersize=18)      
    plt.xticks(repeats, fontsize=12)
    plt.xlabel('Repeat', fontsize=18)
    plt.ylabel('Mean Rotational Velocity ($^\circ$/s)', fontsize=18)
    plt.title('Mean Population Rotational Velocity', fontsize=18)
    plt.legend(fly_labels ,loc='center left', bbox_to_anchor=(1, 0.5))
    fig_name= global_plots_path+'/mean rotational velocity'+fig_type
    plt1.savefig(fig_name, dpi=dpi_value)
    fig_num=fig_num+1



    #plot mean and variance of STANDARD DEVIATION

    plt1=plt.figure(fig_num, figsize=[10,5])
    for fly in range (0, len(global_rotational_velocity)):
        plt.plot(repeats, global_rotational_velocity[fly, :, std], marker='.', markersize=12, linewidth=0.75, alpha=line_transparency)
            
    error_array = []
    for rep in range (0, num_reps):
        error_array.append(global_rotational_velocity[:, rep, std])
                     
    plt.errorbar(repeats, np.nanmean(np.array(error_array), axis=1), yerr = np.nanstd(np.array(error_array), axis=1), linewidth=1.25, color='black', marker='.', markerfacecolor='red', markersize=18)      
    plt.xticks(repeats, fontsize=12)
    plt.xlabel('Repeat', fontsize=18)
    plt.ylabel('Variance Rotational Velocity ($^\circ$/s)', fontsize=18)
    plt.title('Variance Population Rotational Velocity', fontsize=18)
    plt.legend(fly_labels ,loc='center left', bbox_to_anchor=(1, 0.5))
    fig_name= global_plots_path+'/variance rotational velocity'+fig_type
    plt1.savefig(fig_name, dpi=dpi_value)
    fig_num=fig_num+1
    
    
    return fig_num