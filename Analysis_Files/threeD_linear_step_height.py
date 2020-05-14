import matplotlib.pyplot as plt
import numpy as np

def step_height(stance_start, stance_end, l_z_pos, r_z_pos, fig_num, save_plots, fig_rep_dir, fig_type, dpi_value):
    step_height_store=[]
    swing_time_store=[] # frame number of when stance is entered
    
    stance_start_left = stance_start[0:3]
    stance_end_left = stance_end[0:3]
    
    stance_start_right = stance_start[3:6]
    stance_end_right = stance_end[3:6]
    
    #LEFT

    for leg in range(0,len(stance_start_left)):
        # use each stance start as a point of reference and find the next stance end point
        step_h=[]
        step_frame=[]
        for stance in range(0,len(stance_start_left[leg])):
            itr=0
            # go until the next stance is found
            end_idx=0
            while stance_end_left[leg][itr] < stance_start_left[leg][stance]:
                itr=itr+1 # iterate through to find next end
                if itr > len(stance_end_left[leg])-1: # deals with boundary condition
                    break
            if itr > len(stance_end_left[leg])-1: # end boundary condition
                # if step (i.e. stance) is not completed then ignore the last stance initiation
                pass
            elif itr-1 < 0: # starting boundry condition
                pass
            else:
                max_h=max(l_z_pos[leg][stance_end_left[leg][itr-1]:stance_start_left [leg][stance]])
                z0=l_z_pos[leg][stance_end_left[leg][itr-1]]
                h=abs(max_h-z0)      
                step_h.append(h)
                step_frame.append(stance_start_left [leg][stance])
    
        step_height_store.append(np.array(step_h))
        swing_time_store.append(np.array(step_frame))
        
    #RIGHT 
        
    for leg in range(0,len(stance_start_right)):
        # use each stance start as a point of reference and find the next stance end point
        step_h=[]
        step_frame=[]
        for stance in range(0,len(stance_start_right[leg])):
            itr=0
            # go until the next stance is found
            end_idx=0
            while stance_end_right[leg][itr] < stance_start_right[leg][stance]:
                itr=itr+1 # iterate through to find next end
                if itr > len(stance_end_right[leg])-1: # deals with boundary condition
                    break
            if itr > len(stance_end_right[leg])-1: # end boundary condition
                # if step (i.e. stance) is not completed then ignore the last stance initiation
                pass
            elif itr-1 < 0: # starting boundry condition
                pass
            else:
                max_h=max(l_z_pos[leg][stance_end_right[leg][itr-1]:stance_start_right [leg][stance]])
                z0=l_z_pos[leg][stance_end_right[leg][itr-1]]
                h=abs(max_h-z0)      
                step_h.append(h)
                step_frame.append(stance_start_right [leg][stance])
    
        step_height_store.append(np.array(step_h))
        swing_time_store.append(np.array(step_frame))
        
        
#     #plot step height
#     plt8=plt.figure(fig_num, figsize=[10,5])
#     plt.plot(swing_time_store[0], step_height_store[0], color='black', linewidth=1.25)
#     plt.xlabel('frame (#)', fontsize= 18)
#     plt.ylabel('step height (mm)', fontsize= 18)
#     plt.title('l1 step height', fontsize= 18)
#     fig_num=fig_num+1
#     fig_name= fig_rep_dir+'/l1 step height'+fig_type
#     plt8.savefig(fig_name, dpi=dpi_value)
    
#     plt9=plt.figure(fig_num, figsize=[10,5])
#     plt.plot(swing_time_store[1], step_height_store[1], color='black', linewidth=1.25)
#     plt.xlabel('frame (#)', fontsize= 18)
#     plt.ylabel('step height (mm)', fontsize= 18)
#     plt.title('l2 step height', fontsize= 18)
#     fig_num=fig_num+1
#     fig_name= fig_rep_dir+'/l2 step height'+fig_type
#     plt9.savefig(fig_name, dpi=dpi_value)
    
#     plt10=plt.figure(fig_num, figsize=[10,5])
#     plt.plot(swing_time_store[2], step_height_store[2], color='black', linewidth=1.25)
#     plt.xlabel('frame (#)', fontsize= 18)
#     plt.ylabel('step height (mm)', fontsize= 18)
#     plt.title('l3 step height', fontsize= 18)
#     fig_num=fig_num+1
#     fig_name= fig_rep_dir+'/l3 step height'+fig_type
#     plt10.savefig(fig_name, dpi=dpi_value)
        
        
    return(step_height_store, swing_time_store, fig_num)
   

    
    
    
    
def global_step_height(fly_id, global_step_height, nlegs, global_plots_path, global_data_path, fig_type, dpi_value, fig_num):
    
    shape = len(np.array(global_step_height).shape)          
    if shape == 3: #for single file analysis... the list needs to be nested once more 
        global_step_height = [global_step_height]

    for f in range(0, len(global_step_height)):
        if not isinstance(global_step_height[f], list):
            global_step_height[f] = global_step_height[f].tolist()
    global_step_height = np.array(global_step_height)
    
    line_transparency = 0.3
    mean = 0
    std = 1
    
    num_sessions = len(global_step_height[0])
    sessions = np.arange(1, num_sessions+1)
    fly_labels = []
    for f in fly_id:
        fly_labels.append('fly' + str(f))
    fly_labels.append('mean + std')

    leg_labels = ['L1', 'L2', 'L3', 'R1', 'R2', 'R3']
    
    global_step_height_mean_var = []
    
    #plot mean and variance of MEAN
    for leg in range(0, nlegs):
        plt1=plt.figure(fig_num, figsize=[10,5])
        for fly in range (0, len(global_step_height)):
            plt.plot(sessions, global_step_height[fly, :, leg, mean], marker='.', markersize=12, linewidth=0.75, alpha=line_transparency)
            
        error_array = []
        for sesh in range (0, num_sessions):
            error_array.append(global_step_height[:, sesh, leg, mean])

        global_step_height_mean_var.append(np.array([np.nanmean(np.array(error_array), axis=1), np.nanstd(np.array(error_array), axis=1)])) #[mean, var]
        mean = 0
        var = 1
        plt.errorbar(sessions, global_step_height_mean_var[leg][mean], yerr = global_step_height_mean_var[leg][var], linewidth=1.25, color='black', marker='.', markerfacecolor='red', markersize=18)          
        plt.xticks(sessions, fontsize=12)
        plt.xlabel('Session', fontsize=18)
        plt.ylabel('Mean Step Height (mm)', fontsize=18)
        plt.title('Mean Population Step Height, '+leg_labels[leg], fontsize=18)
        plt.legend(fly_labels ,loc='center left', bbox_to_anchor=(1, 0.5))
        fig_name= global_plots_path+'/mean step height '+leg_labels[leg]+fig_type
        plt1.savefig(fig_name, dpi=dpi_value)
        fig_num=fig_num+1
    
    global_step_height_mean_var = np.array(global_step_height_mean_var)

    #plot mean and variance of STANDARD DEVIATION
    for leg in range(0, nlegs):
        plt1=plt.figure(fig_num, figsize=[10,5])
        for fly in range (0, len(global_step_height)):
            plt.plot(sessions, global_step_height[fly, :, leg, std], marker='.', markersize=12, linewidth=0.75, alpha=line_transparency)
            
        error_array = []
        for sesh in range (0, num_sessions):
            error_array.append(global_step_height[:, sesh, leg, std])

        plt.errorbar(sessions, np.nanmean(np.array(error_array)), yerr = np.nanstd(np.array(error_array)), linewidth=1.25, color='black', marker='.', markerfacecolor='red', markersize=18)      
        plt.xticks(sessions, fontsize=12)
        plt.xlabel('Session', fontsize=18)
        plt.ylabel('Variance Step Height (mm)', fontsize=18)
        plt.title('Variance Population Step Height, '+leg_labels[leg], fontsize=18)
        plt.legend(fly_labels ,loc='center left', bbox_to_anchor=(1, 0.5))
        fig_name= global_plots_path+'/variance step height '+leg_labels[leg]+fig_type
        plt1.savefig(fig_name, dpi=dpi_value)
        fig_num=fig_num+1
    
    
    return global_step_height_mean_var, fig_num



def global_step_height_reps(fly_id, global_step_height, nlegs, global_plots_path, global_data_path, fig_type, dpi_value, fig_num):
    
    shape = len(np.array(global_step_height).shape)          
    if shape == 3: #for single file analysis... the list needs to be nested once more 
        global_step_height = [global_step_height]

    for f in range(0, len(global_step_height)):
        if not isinstance(global_step_height[f], list):
            global_step_height[f] = global_step_height[f].tolist()
    global_step_height = np.array(global_step_height)
    
    line_transparency = 0.3
    mean = 0
    std = 1
    
    num_reps = len(global_step_height[0])
    repeats = np.arange(1, num_reps+1)
    fly_labels = []
    for f in fly_id:
        fly_labels.append('fly' + str(f))
    fly_labels.append('mean + std')

    leg_labels = ['L1', 'L2', 'L3', 'R1', 'R2', 'R3']
    
    global_step_height_mean_var = []
    
    #plot mean and variance of MEAN
    for leg in range(0, nlegs):
        plt1=plt.figure(fig_num, figsize=[10,5])
        for fly in range (0, len(global_step_height)):
            plt.plot(repeats, global_step_height[fly, :, leg, mean], marker='.', markersize=12, linewidth=0.75, alpha=line_transparency)
            
        error_array = []
        for rep in range (0, num_reps):
            error_array.append(global_step_height[:, rep, leg, mean])

        global_step_height_mean_var.append(np.array([np.nanmean(np.array(error_array), axis=1), np.nanstd(np.array(error_array), axis=1)])) #[mean, var]
        mean = 0
        var = 1
        plt.errorbar(sessions, global_step_height_mean_var[leg][mean], yerr = global_step_height_mean_var[leg][var], linewidth=1.25, color='black', marker='.', markerfacecolor='red', markersize=18)         
        plt.xticks(repeats, fontsize=12)
        plt.xlabel('Repeat', fontsize=18)
        plt.ylabel('Mean Step Height (mm)', fontsize=18)
        plt.title('Mean Population Step Height, '+leg_labels[leg], fontsize=18)
        plt.legend(fly_labels ,loc='center left', bbox_to_anchor=(1, 0.5))
        fig_name= global_plots_path+'/mean step height '+leg_labels[leg]+fig_type
        plt1.savefig(fig_name, dpi=dpi_value)
        fig_num=fig_num+1
    
    global_step_height_mean_var = np.array(global_step_height_mean_var)

    #plot mean and variance of STANDARD DEVIATION
    for leg in range(0, nlegs):
        plt1=plt.figure(fig_num, figsize=[10,5])
        for fly in range (0, len(global_step_height)):
            plt.plot(repeats, global_step_height[fly, :, leg, std], marker='.', markersize=12, linewidth=0.75, alpha=line_transparency)
            
        error_array = []
        for rep in range (0, num_reps):
            error_array.append(global_step_height[:, rep, leg, std])

        plt.errorbar(repeats, np.nanmean(np.array(error_array), axis=1), yerr = np.nanstd(np.array(error_array), axis=1), linewidth=1.25, color='black', marker='.', markerfacecolor='red', markersize=18)      
        plt.xticks(repeats, fontsize=12)
        plt.xlabel('Repeat', fontsize=18)
        plt.ylabel('Variance Step Height (mm)', fontsize=18)
        plt.title('Variance Population Step Height, '+leg_labels[leg], fontsize=18)
        plt.legend(fly_labels ,loc='center left', bbox_to_anchor=(1, 0.5))
        fig_name= global_plots_path+'/variance step height '+leg_labels[leg]+fig_type
        plt1.savefig(fig_name, dpi=dpi_value)
        fig_num=fig_num+1
    
    
    return fig_num