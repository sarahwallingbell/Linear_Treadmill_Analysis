import csv
import os
import numpy as np
import matplotlib.pyplot as plt
import math

#LOCAL ANALYSIS

def leg_phases(stance_start, nlegs, fig_num, save_plots, fig_rep_dir, fig_type, dpi_value):

    # use r1 as the reference leg
    r1_ref=stance_start[3]
    phase=[]
    ref_step_time=[] # reference step time
    for j in range(0,nlegs):
        phase_leg=[]
        for step in range(0,len(r1_ref)-1):
            # specify phase range
            step_start=r1_ref[step]
            step_end=r1_ref[step+1]
            
            # find if the leg in focus has any indices in that region and if so, take the first one (theoretically, there shouldne't be more)
            curr_step=np.where(np.logical_and(stance_start[j]>=step_start, stance_start[j] <= step_end))[0]
            
            # compute phase
            if curr_step.size ==0:
                # if leg is not during the step cycles of the other leg
                phase_leg.append(np.nan)
            else:
                # calculate the phase
                curr_phase=abs(step_start-stance_start[j][curr_step[0]])/abs(step_start-step_end)
                # normalize, so that the range of phase offset is 0-.5 (0=aligned phases, .5=disaligned phases)
                if curr_phase > .5:
                    curr_phase = 1.0 - curr_phase
                phase_leg.append(curr_phase)
                
        phase.append(np.array(phase_leg))
        
    
    #plot phases 
    phase_time = r1_ref[0:-1]
    
#     plt1=plt.figure(fig_num,figsize=[20,20])
    
#     for j in range(0,len(phase)):
#         plt.subplot(len(phase),1,j+1)
#         plt.plot(phase_time, phase[j], color='black', linewidth=1.25)
#         plt.xlabel('frame (#)', fontsize=18)
#         plt.ylabel('relative phase to r1', fontsize=18)
#         plt.title('l'+str(j+1)+' phase', fontsize=18)
#     fig_num=fig_num+1
#     fig_name= fig_rep_dir+'/phase'+fig_type
#     plt1.savefig(fig_name, dpi=dpi_value)
        
    return phase, phase_time, fig_num
      
    
#GLOBAL ANALYSIS    


def global_leg_phases(fly_id, global_phase, nlegs, global_plots_path, global_data_path, fig_type, dpi_value, fig_num):
        
    shape = len(np.array(global_phase).shape) 
    if shape == 3: #for single file analysis... the list needs to be nested once more 
        global_phase = [global_phase]

    for f in range(0, len(global_phase)):
        if not isinstance(global_phase[f], list):
            global_phase[f] = global_phase[f].tolist()
    global_phase = np.array(global_phase)
        
    leg_labels = ['L1', 'L2', 'L3', 'R1', 'R2', 'R3']        
    
    line_transparency = 0.3
    mean = 0
    std = 1
    
    num_sessions = len(global_phase[0])
    sessions = np.arange(1, num_sessions+1)
    fly_labels = []
    for f in fly_id:
        fly_labels.append('fly' + str(f))
    fly_labels.append('mean + std')
    
    global_phase_mean_var = []

    #plot mean and variance of MEAN
    for leg in range(0, nlegs):
        plt1=plt.figure(fig_num, figsize=[10,5])
        for fly in range (0, len(global_phase)):
            plt.plot(sessions, global_phase[fly, :, leg, mean], marker='.', markersize=12, linewidth=0.75, alpha=line_transparency)
            
        error_array = []
        for sesh in range (0, num_sessions):
            error_array.append(global_phase[:, sesh, leg, mean])

        global_phase_mean_var.append(np.array([np.nanmean(np.array(error_array), axis=1), np.nanstd(np.array(error_array), axis=1)])) #[mean, var]
        mean = 0
        var = 1
        plt.errorbar(sessions, global_phase_mean_var[leg][mean], yerr = global_phase_mean_var[leg][var], linewidth=1.25, color='black', marker='.', markerfacecolor='red', markersize=18)       
        plt.xticks(sessions, fontsize=12)
        plt.xlabel('Session', fontsize=18)
        plt.ylabel('Mean Phase', fontsize=18)
        plt.title('Mean Population Phase, '+leg_labels[leg], fontsize=18)
        plt.legend(fly_labels ,loc='center left', bbox_to_anchor=(1, 0.5))
        fig_name= global_plots_path+'/mean population phase l'+leg_labels[leg]+fig_type
        plt1.savefig(fig_name, dpi=dpi_value)
        fig_num=fig_num+1
    
    global_phase_mean_var = np.array(global_phase_mean_var)


    #plot mean and variance of STANDARD DEVIATION
    for leg in range(0, nlegs):
        plt1=plt.figure(fig_num, figsize=[10,5])
        for fly in range (0, len(global_phase)):
            plt.plot(sessions, global_phase[fly, :, leg, std], marker='.', markersize=12, linewidth=0.75, alpha=line_transparency)
            
        error_array = []
        for sesh in range (0, num_sessions):
            error_array.append(global_phase[:, sesh, leg, std])

        plt.errorbar(sessions, np.nanmean(np.array(error_array)), yerr = np.nanstd(np.array(error_array)), linewidth=1.25, color='black', marker='.', markerfacecolor='red', markersize=18)        
        plt.xticks(sessions, fontsize=12)
        plt.xlabel('Session', fontsize=18)
        plt.ylabel('Variance Phase', fontsize=18)
        plt.title('Variance Population Phase, '+leg_labels[leg], fontsize=18)
        plt.legend(fly_labels ,loc='center left', bbox_to_anchor=(1, 0.5))
        fig_name= global_plots_path+'/variance population phase l'+leg_labels[leg]+fig_type
        plt1.savefig(fig_name, dpi=dpi_value)
        fig_num=fig_num+1
    
    
    return global_phase_mean_var, fig_num


def global_leg_phases_reps(fly_id, global_phase, nlegs, global_plots_path, global_data_path, fig_type, dpi_value, fig_num):
        
    shape = len(np.array(global_phase).shape) 
    if shape == 3: #for single file analysis... the list needs to be nested once more 
        global_phase = [global_phase]

    for f in range(0, len(global_phase)):
        if not isinstance(global_phase[f], list):
            global_phase[f] = global_phase[f].tolist()
    global_phase = np.array(global_phase)
        
    leg_labels = ['L1', 'L2', 'L3', 'R1', 'R2', 'R3']    
        
    line_transparency = 0.3
    mean = 0
    std = 1
    
    num_reps = len(global_phase[0])
    repeats = np.arange(1, num_reps+1)
    fly_labels = []
    for f in fly_id:
        fly_labels.append('fly' + str(f))
    fly_labels.append('mean + std')

    #plot mean and variance of MEAN
    for leg in range(0, nlegs):
        plt1=plt.figure(fig_num, figsize=[10,5])
        for fly in range (0, len(global_phase)):
            plt.plot(repeats, global_phase[fly, :, leg, mean], marker='.', markersize=12, linewidth=0.75, alpha=line_transparency)
            
        error_array = []
        for rep in range (0, num_reps):
            error_array.append(global_phase[:, rep, leg, mean])

        plt.errorbar(repeats, np.nanmean(np.array(error_array), axis=1), yerr = np.nanstd(np.array(error_array), axis=1), linewidth=1.25, color='black', marker='.', markerfacecolor='red', markersize=18)     
        plt.xticks(repeats, fontsize=12)
        plt.yticks(np.arange(0, 0.6, step=0.1))  # Set label locations.
        plt.ylim(0, 0.5)
        plt.xlabel('Repeat', fontsize=18)
        plt.ylabel('Mean Phase', fontsize=18)
        plt.title('Mean Population Phase, '+leg_labels[leg], fontsize=18)
        plt.legend(fly_labels ,loc='center left', bbox_to_anchor=(1, 0.5))
        fig_name= global_plots_path+'/mean population phase '+leg_labels[leg]+fig_type
        plt1.savefig(fig_name, dpi=dpi_value)
        fig_num=fig_num+1
    


    #plot mean and variance of STANDARD DEVIATION
    for leg in range(0, nlegs):
        plt1=plt.figure(fig_num, figsize=[10,5])
        for fly in range (0, len(global_phase)):
            plt.plot(repeats, global_phase[fly, :, leg, std], marker='.', markersize=12, linewidth=0.75, alpha=line_transparency)
            
        error_array = []
        for rep in range (0, num_reps):
            error_array.append(global_phase[:, rep, leg, std])

        plt.errorbar(repeats, np.nanmean(np.array(error_array), axis=1), yerr = np.nanstd(np.array(error_array), axis=1), linewidth=1.25, color='black', marker='.', markerfacecolor='red', markersize=18)        
        plt.xticks(repeats, fontsize=12)
        plt.xlabel('Repeat', fontsize=18)
        plt.ylabel('Variance Phase', fontsize=18)
        plt.title('Variance Population Phase, '+leg_labels[leg], fontsize=18)
        plt.legend(fly_labels ,loc='center left', bbox_to_anchor=(1, 0.5))
        fig_name= global_plots_path+'/variance population phase '+leg_labels[leg]+fig_type
        plt1.savefig(fig_name, dpi=dpi_value)
        fig_num=fig_num+1
    
    
    return fig_num




def get_indices(fly, sesh, fly_val, sesh_val):
    indices = []
    for index in range(0, len(fly)):
        if (fly[index] == fly_val and sesh[index] == sesh_val):
            indices.append(index)
            
    return indices


# Phase Offset and Variance
# Calculates the phase offset between legs and phase offset variance over time, and local and global phase offset probabilities. 
# Parameters: is walking array, swing stance matrix, leg stance maxima arrays, directories for exporting data and plots
# Return: phases, variances, bin_centers, normalized_bin_heights, bin_width, global_bin_heights

# def offset_and_variance(is_walking, swing_stance_matrix, stance_peak_matrix, L1_stance_maxima, L2_stance_maxima, L3_stance_maxima, R1_stance_maxima, R2_stance_maxima, R3_stance_maxima, save_plots, fig_rep_dir, save_data, data_rep_dir):
# #Phase Offset and Variance 


#     # Create matrix to hold all leg pair combinations (directional) of step phase info

#     # leg_pair_phase_matrix holds [leg1_step_period, frame_offset, phase_offset] for each step for each pair of legs where
#     #     leg1_step_period = length (number of frames) of leg1 step cycle
#     #     frame_offset = number of frames between start of leg1 step and start of next leg2 step 
#     #     phase_offset = frame_offset / leg1_step_period
#     # if frame_offset and phase_offset are negative, there was no start to leg2 step cycle during leg1 step cycle
#     num_legs = 6
#     max_num_steps = max(len(L1_stance_maxima), len(L2_stance_maxima), len(L3_stance_maxima), len(R1_stance_maxima), len(R2_stance_maxima), len(R3_stance_maxima))
#     leg_pair_phase_matrix = np.full((num_legs, num_legs, max_num_steps, 3), -1.0)


#     # Fill leg_pair_phase_matrix
#     max_phase_offset = .5

#     for leg1 in range (0, num_legs):
#         for leg2 in range (0, num_legs):
#             step_num = 0
#             for step in range (0, len(stance_peak_matrix[leg1][0])-1):
#                 if step_num < len(leg_pair_phase_matrix[leg1][leg2]):
#                     #find frame of start of leg1 step (start stance)
#                     leg1_step_start_frame = stance_peak_matrix[leg1][0][step]

#                     #find frame of end of leg1 step (end swing)
#                     leg1_step_end_frame = stance_peak_matrix[leg1][0][step+1]

#                     #if leg1 step is not_walking, set the matrix values as nans 
#                     if 0 in is_walking[leg1_step_start_frame:leg1_step_end_frame]:
#                         leg_pair_phase_matrix[leg1][leg2][step_num] = [math.nan, math.nan, math.nan]
#                         step_num = step_num + 1
#                     else:
#                         #calculate the step period
#                         leg1_step_period = leg1_step_end_frame - leg1_step_start_frame

#                         #find frame of start of leg2 step within leg1 step cycle 
#                         leg2_step_start_frames = np.where(np.logical_and(stance_peak_matrix[leg2][0] >= leg1_step_start_frame, stance_peak_matrix[leg2][0] < leg1_step_end_frame))[0]

#                         #check if leg2 starts step within leg1 step cycle. if not move onto next leg1 step. 
#                         if len(leg2_step_start_frames) > 0:
#                             leg2_step_start_frame = stance_peak_matrix[leg2][0][leg2_step_start_frames[0]]

#                             #calculate frame_offset (the number of frames between leg1 step start and leg2 step start)
#                             frame_offset = leg2_step_start_frame - leg1_step_start_frame

#                             #calculate phase_offset (frame_offset / leg1_step_period)
#                             phase_offset = frame_offset / leg1_step_period

#                             #folds data, max offset will be .5
#                             if phase_offset >= max_phase_offset:
#                                 phase_offset = .9999999999999 - phase_offset

#                             #add step period, frame_offset, and phase_offset to leg_pair_phase_matrix
#                             leg_pair_phase_matrix[leg1][leg2][step_num] = [leg1_step_period, frame_offset, phase_offset]

#                             step_num = step_num + 1



#     # Isolate phase values for each leg pair and save list in 3d matrix
#     phases = [] # list of all leg pair phase values: [[L1L1 phases], [L1L2 phases], [L1L3 phases], ..., [L2L1 phases], [L2L2 phases], ... , [R3R3 phases]]
#     phases_walking = [] # same as phases but only steps that are walking
#     i = 0
#     for leg1 in range (0, num_legs):
#         for leg2 in range (0, num_legs):
#             phase_indices = np.where(leg_pair_phase_matrix[leg1][leg2][:,2] >= 0)[0] #all non-negative phase values
            
#             #phase_indices_walking = np.where(np.isfinite(leg_pair_phase_matrix[leg1][leg2][:,2]) and leg_pair_phase_matrix[leg1][leg2][:,2] >= 0)[0]
            
#             phase_values = []
#             for phase_idx in range (0, len(phase_indices)):
#                 phase_values.append(leg_pair_phase_matrix[leg1][leg2][phase_idx,2])
#             phases.append(phase_values)
            
# #             phase_values_walking = []
# #             for phase_idx in range (0, len(phase_indices_walking)):
# #                 phase_values_walking.append(leg_pair_phase_matrix[leg1][leg2][phase_idx, 2])
# #             phases_walking.append(phase_values_walking)
                
    
# #     if math.nan in phases[0]: phasesHasNans = "True"
# #     else: phasesHasNans = "False"
# #     print("phases[L1L1] contains nans?" + phasesHasNans)

#     #phase indicis
#     L1L1 = 0; L1L2 = 1; L1L3 = 2; L1R1 = 3; L1R2 = 4; L1R3 = 5
#     L2L1 = 6; L2L2 = 7; L2L3 = 8; L2R1 = 9; L2R2 = 10; L2R3 = 11;
#     L3L1 = 12; L3L2 = 13; L3L3 = 14; L3R1 = 15; L3R2 = 16; L3R3 = 17
#     R1L1 = 18; R1L2 = 19; R1L3 = 20; R1R1 = 21; R1R2 = 22; R1R3 = 23
#     R2L1 = 24; R2L2 = 25; R2L3 = 26; R2R1 = 27; R2R2 = 28; R2R3 = 29
#     R3L1 = 30; R3L2 = 31; R3L3 = 32; R3R1 = 33; R3R2 = 34; R3R3 = 35

#     num_leg_pairs = 36
    

#     if (save_data == True):
#         #export phases matrix 
#         csv_file_path = os.path.join(data_rep_dir, 'Phases')
#         #save the list of lists
#         with open(csv_file_path, "w") as output:
#             writer = csv.writer(output, lineterminator='\n')
#             writer.writerows(phases)

    
#     L1 = 0
#     L2 = 1
#     L3 = 2
#     R1 = 3
#     R2 = 4
#     R3 = 5
    
#     num_legs = 6

#     def legPairName (legPair):
#         if legPair == L1L1: return 'L1L1'
#         elif legPair == L1L2: return 'L1L2'
#         elif legPair == L1L3: return 'L1L3'
#         elif legPair == L1R1: return 'L1R1'
#         elif legPair == L1R2: return 'L1R2'
#         elif legPair == L1R3: return 'L1R3'
#         elif legPair == L2L1: return 'L2L1'
#         elif legPair == L2L2: return 'L2L2'
#         elif legPair == L2L3: return 'L2L3'
#         elif legPair == L2R1: return 'L2R1'
#         elif legPair == L2R2: return 'L2R2'
#         elif legPair == L2R3: return 'L2R3'
#         elif legPair == L3L1: return 'L3L1'
#         elif legPair == L3L2: return 'L3L2'
#         elif legPair == L3L3: return 'L3L3'
#         elif legPair == L3R1: return 'L3R1'
#         elif legPair == L3R2: return 'L3R2'
#         elif legPair == L3R3: return 'L3R3'
#         elif legPair == R1L1: return 'R1L1'
#         elif legPair == R1L2: return 'R1L2'
#         elif legPair == R1L3: return 'R1L3'
#         elif legPair == R1R1: return 'R1R1'
#         elif legPair == R1R2: return 'R1R2'
#         elif legPair == R1R3: return 'R1R3'
#         elif legPair == R2L1: return 'R2L1'
#         elif legPair == R2L2: return 'R2L2'
#         elif legPair == R2L3: return 'R2L3'
#         elif legPair == R2R1: return 'R2R1'
#         elif legPair == R2R2: return 'R2R2'
#         elif legPair == R2R3: return 'R2R3'
#         elif legPair == R3L1: return 'R3L1'
#         elif legPair == R3L2: return 'R3L2'
#         elif legPair == R3L3: return 'R3L3'
#         elif legPair == R3R1: return 'R3R1'
#         elif legPair == R3R2: return 'R3R2 '
#         elif legPair == R3R3: return 'R3R3'

#     # Plot leg pair phases 

#     ymin = 0
#     ymax = max_phase_offset

#     #print L1L1 - L1R3
#     for legPair in range (0, num_legs): #num_leg_pairs): 
#         figNum = 36 + legPair
#         plt.rc('xtick', labelsize=10)
#         plt.rc('ytick', labelsize=10)
#         plt8 = plt.figure(figNum)
#         plt.plot(phases[legPair])
#         leg = legPairName(legPair)
#         title = '' + leg + ' Phase Offset'
#         plt.title(title, fontsize = 20)
#         plt.xlabel('step number', fontsize = 20)
#         plt.ylabel('phase offset', fontsize = 20)
#         plt.autoscale(enable=True, axis = 'x', tight = True)
#         axes = plt.gca()
#         axes.set_ylim([ymin,ymax])
#         plt.show()
#         title_underscore = title.replace(" ", "_") 
#         title_svg = title_underscore + '.svg'
#         if (save_plots == True):
#             plt8.savefig(os.path.join(fig_rep_dir, title_svg), bbox_inches='tight', dpi=1000)
     
#     if (save_data == True):
#         #export phases matrix 
#         csv_file_path = os.path.join(data_rep_dir, 'Phases')
#         with open(csv_file_path, "w") as output:
#             writer = csv.writer(output, lineterminator='\n')
#             writer.writerows(phases)
    


#     # Calculate phase variance
#     step_window = 2 #(steps)
#     step_slide = 1 #(steps)

#     variances = []

#     for leg_pair in range (0, num_leg_pairs):
#         num_steps = len(phases[leg_pair])
#         num_windows = (int ((num_steps - step_window) / step_slide)) +1
#         window_start = 0
#         window_end = step_window
#         var_window = []
#         for window in range (0, num_windows):
#             var_window.append(np.nanvar(phases[leg_pair][window_start : window_end]))
#             window_start = window_start + step_slide
#             window_end = window_end + step_slide
#         variances.append(var_window)

#     if (save_data == True):
#         #export variances matrix 
#         csv_file_path = os.path.join(data_rep_dir, 'Variances')
#         with open(csv_file_path, "w") as output:
#             writer = csv.writer(output, lineterminator='\n')
#             writer.writerows(variances)
    
#     # Plot variances 
#     #print L1L1-L1R3
#     for legPair in range (0, num_legs): #num_leg_pairs):
#         figNum = 41 + legPair
#         plt9 = plt.figure(figNum)
#         plt.rc('xtick', labelsize=10)
#         plt.rc('ytick', labelsize=10)
#         plt.plot(variances[legPair])
#         leg = legPairName(legPair)
#         title = '' + leg + ' Phase Variance'
#         plt.title(title, fontsize = 20)
#         plt.xlabel('step number', fontsize = 20)
#         plt.ylabel('variance', fontsize = 20)
#         plt.autoscale(enable=True, axis = 'x', tight = True)
#         plt.autoscale(enable=True, axis = 'y', tight = True)
#         title_underscore = title.replace(" ", "_") 
#         title_svg = title_underscore + '.svg'
#         plt.show()
#         if (save_plots == True):
#             plt9.savefig(os.path.join(fig_rep_dir, title_svg), bbox_inches='tight', dpi=1000)


# #     # Calcualte phase probabilities 
# #     bin_width = .01
# #     num_bins = int(max_phase_offset/bin_width)
# #     bin_start = bin_width/2
# #     bin_centers = np.arange(bin_start, max_phase_offset, bin_width)
# #     bin_heights = np.full((num_leg_pairs, num_bins), 0.0) # [[L1L1], [L1L2], ... [L1R3], ... [L2L1], ... [R3R3]]
# #     normalized_bin_heights = np.full((num_leg_pairs, num_bins), 0.0)
# #     for leg_pair in range (0, num_leg_pairs): # for each leg pair
# #         for phase in range (0, len(phases[leg_pair])): #for every step's phase offset
# #             #place phase offset in the appropriate bin 
# #             val = phases[leg_pair][phase]
# #             if not math.isnan(val):
# #                 val_idx = int(val * (1/bin_width))
# #                 bin_heights[leg_pair][val_idx] = bin_heights[leg_pair][val_idx] + 1
# #         #normalize bin vals by number of total values 
# #         for phase in range(0, len(bin_heights[leg_pair])):
# #             normalized_bin_heights[leg_pair][phase] = bin_heights[leg_pair][phase]/len(phases[leg_pair])
            
#     # Calcualte phase probabilities for NEW BIN SIZE
#     bin_width = .05
#     num_bins = int(max_phase_offset/bin_width)
#     bin_start = bin_width/2
#     bin_centers = np.arange(bin_start, max_phase_offset, bin_width)
#     bin_heights = np.full((num_leg_pairs, num_bins), 0.0) # [[L1L1], [L1L2], ... [L1R3], ... [L2L1], ... [R3R3]]
#     normalized_bin_heights = np.full((num_leg_pairs, num_bins), 0.0)
#     for leg_pair in range (0, num_leg_pairs): # for each leg pair
#         for phase in range (0, len(phases[leg_pair])): #for every step's phase offset
#             #place phase offset in the appropriate bin 
#             val = phases[leg_pair][phase]
#             if not math.isnan(val):
#                 val_idx = int(val * (1/bin_width))
#                 bin_heights[leg_pair][val_idx] = bin_heights[leg_pair][val_idx] + 1
#         #normalize bin vals by number of total values 
#         for phase in range(0, len(bin_heights[leg_pair])):
#             #find number of steps that ARE WALKING for this leg pair
# #             num_steps_walking = 0
# #             for step in range (0, phases[leg_pair]):
# #                 if phases[leg_pair][step] == math.nan:
# #                     num_steps_walking = num_steps_walking + 1
            
#             #normalized_bin_heights[leg_pair][phase] = bin_heights[leg_pair][phase]/len(phases[leg_pair])
#             #normalized_bin_heights[leg_pair][phase] = bin_heights[leg_pair][phase]/len(phases_walking[leg_pair])
#             num_walking_steps = 0
#             for step in range (0, len(phases[leg_pair])):
#                 if phases[leg_pair][step] >= 0:
#                     num_walking_steps = num_walking_steps + 1
#             #normalized_bin_heights[leg_pair][phase] = bin_heights[leg_pair][phase]/len(phases[leg_pair])
#             normalized_bin_heights[leg_pair][phase] = bin_heights[leg_pair][phase]/num_walking_steps
#             #print("len(phases[leg_pair]", len(phases[leg_pair]))
#             #print("num_walking_steps", num_walking_steps)
            
            
#     if (save_data == True):        
#         #export bin_centers, normalized_bin_heights, and bin_width 
#         csv_file_path = os.path.join(data_rep_dir, 'phase_offset_bin_centers')
#         with open(csv_file_path, "w") as output:
#             writer = csv.writer(output, lineterminator='\n')
#             for val in bin_centers:
#                 writer.writerow([val])

#         csv_file_path = os.path.join(data_rep_dir, 'phase_offset_normalized_bin_heights')
#         with open(csv_file_path, "w") as output:
#             writer = csv.writer(output, lineterminator='\n')
#             writer.writerows(normalized_bin_heights)    

#         bin_width_array = [bin_width]
#         csv_file_path = os.path.join(data_rep_dir, 'phase_offset_bin_width')
#         with open(csv_file_path, "w") as output:
#             writer = csv.writer(output, lineterminator='\n')
#             for val in bin_width_array:
#                 writer.writerow([val])

#     #new_bin_centers = np.arange(bin_start, max_phase_offset, new_bin_width)
#     #print histograms 
#     #note: can overlay graphs by giving them same figure number 
#     num_leg_pairs = 36
#     #print L1L1-L1R3
#     for legPair in range (0, num_legs): #num_leg_pairs):
#         figNum = 47 + legPair
#         plt10 = plt.figure(figNum)
#         plt.rc('xtick', labelsize=10)
#         plt.rc('ytick', labelsize=10)
#         axes = plt.gca()
#         axes.set_ylim([0,1])
#         plt.bar(bin_centers, normalized_bin_heights[legPair], width=bin_width) 
#         plt.autoscale(enable=True, axis = 'x', tight = True)
#         leg = legPairName(legPair)
#         title = '' + leg + ' Phase Offset Probability'
#         plt.title(title, fontsize = 20)
#         plt.xlabel('phase offset', fontsize = 20)
#         plt.ylabel('probability', fontsize = 20)
#         plt.show()
#         title_underscore = title.replace(" ", "_") 
#         title_svg = title_underscore + '.svg'
#         if (save_plots == True):
#             plt10.savefig(os.path.join(fig_rep_dir, title_svg), bbox_inches='tight', dpi=1000)

    
#     # Global phase offset probability relative to each leg 

#     # Calcualte phase probabilities 
#     global_bin_heights = np.full((num_legs, num_bins), 0.0) # [[L1], [L2], [L3], ... [R3]]
#     global_bin_count = np.full((num_legs), 0.0) #for normalization of global bins 

#     #combine the (not normalized) counts for leg pairs into counts for each leg (e.g. L1L1-L1R3 --> L1, R3L1-R3R3 --> R3)
#     leg_idx = 0
#     for leg in range (0, num_legs):
#         leg_pair_idx = leg_idx
#         #add counts from all relevant leg pairs to current leg 
#         for leg_pair in range (0, num_legs):
#             #skip leg if it's in reference to itself (e.g. L1L1)
#             if leg_pair_idx != L1L1 and leg_pair_idx != L2L2 and leg_pair_idx != L3L3 and leg_pair_idx != R1R1 and leg_pair_idx != R2R2 and leg_pair_idx != R3R3:
#                 #incriment the total number of values in the global bin by the number of vals for this leg pair 
#                 global_bin_count[leg] = global_bin_count[leg] + len(phases[leg_pair])
#                 for leg_pair_bin in range (0, num_bins):
#                     #add count in bin for leg_pair (e.g. L1L1) to count in bin for global leg (e.g. L1)
#                     global_bin_heights[leg][leg_pair_bin] = global_bin_heights[leg][leg_pair_bin] + bin_heights[leg_pair_idx][leg_pair_bin]


#             #incriment indices 
#             leg_pair_idx = leg_pair_idx + 1

#         #normalize the global bins for this leg
#         for global_bin in range (0, num_bins):
#             global_bin_heights[leg][global_bin] = global_bin_heights[leg][global_bin] / global_bin_count[leg]

#         #incriment indices 
#         leg_idx = leg_idx + num_legs

#     if (save_data == True):
#         #export global_bin_heights
#         csv_file_path = os.path.join(data_rep_dir, 'phase_offset_probability_global_bin_heights')
#         with open(csv_file_path, "w") as output:
#             writer = csv.writer(output, lineterminator='\n')
#             writer.writerows(global_bin_heights)    

#     #print histograms 
#     plt11 = plt.figure(53)
#     plt.rc('xtick', labelsize=10)
#     plt.rc('ytick', labelsize=10)
#     plt.bar(bin_centers, global_bin_heights[L1] ,width=bin_width) 
#     plt.autoscale(enable=True, axis = 'x', tight = True)
#     plt.autoscale(enable=True, axis = 'y', tight = True)
#     title = 'L1 Phase Offset Probability'
#     plt.title(title, fontsize = 20)
#     plt.xlabel('phase offset', fontsize = 20)
#     plt.ylabel('probability', fontsize = 20)
#     title_underscore = title.replace(" ", "_") 
#     title_svg = title_underscore + '.svg'
#     plt.show()
#     if (save_plots == True):
#         plt11.savefig(os.path.join(fig_rep_dir, title_svg), bbox_inches='tight', dpi=1000)

#     plt12 = plt.figure(54)
#     plt.rc('xtick', labelsize=10)
#     plt.rc('ytick', labelsize=10)
#     plt.bar(bin_centers, global_bin_heights[L2] ,width=bin_width) 
#     plt.autoscale(enable=True, axis = 'x', tight = True)
#     plt.autoscale(enable=True, axis = 'y', tight = True)
#     title = 'L2 Phase Offset Probability'
#     plt.title(title, fontsize = 20)
#     plt.xlabel('phase offset', fontsize = 20)
#     plt.ylabel('probability', fontsize = 20)
#     title_underscore = title.replace(" ", "_") 
#     title_svg = title_underscore + '.svg'
#     plt.show()
#     if (save_plots == True):
#         plt12.savefig(os.path.join(fig_rep_dir, title_svg), bbox_inches='tight', dpi=1000)

#     plt13 = plt.figure(55)
#     plt.rc('xtick', labelsize=10)
#     plt.rc('ytick', labelsize=10)
#     plt.bar(bin_centers, global_bin_heights[L3] ,width=bin_width) 
#     plt.autoscale(enable=True, axis = 'x', tight = True)
#     plt.autoscale(enable=True, axis = 'y', tight = True)
#     title = 'L3 Phase Offset Probability'
#     plt.title(title, fontsize = 20)
#     plt.xlabel('phase offset', fontsize = 20)
#     plt.ylabel('probability', fontsize = 20)
#     title_underscore = title.replace(" ", "_") 
#     title_svg = title_underscore + '.svg'
#     plt.show()
#     if (save_plots == True):
#         plt13.savefig(os.path.join(fig_rep_dir, title_svg), bbox_inches='tight', dpi=1000)

#     plt14 = plt.figure(56)
#     plt.bar(bin_centers, global_bin_heights[R1] ,width=bin_width) 
#     plt.autoscale(enable=True, axis = 'x', tight = True)
#     plt.autoscale(enable=True, axis = 'y', tight = True)
#     title = 'R1 Phase Offset Probability'
#     plt.title(title, fontsize = 20)
#     plt.xlabel('phase offset', fontsize = 20)
#     plt.ylabel('probability', fontsize = 20)
#     title_underscore = title.replace(" ", "_") 
#     title_svg = title_underscore + '.svg'
#     plt.show()
#     if (save_plots == True):
#         plt14.savefig(os.path.join(fig_rep_dir, title_svg), bbox_inches='tight', dpi=1000)

#     plt15 = plt.figure(57)
#     plt.rc('xtick', labelsize=10)
#     plt.rc('ytick', labelsize=10)
#     plt.bar(bin_centers, global_bin_heights[R2] ,width=bin_width) 
#     plt.autoscale(enable=True, axis = 'x', tight = True)
#     plt.autoscale(enable=True, axis = 'y', tight = True)
#     title = 'R2 Phase Offset Probability'
#     plt.title(title, fontsize = 20)
#     plt.xlabel('phase offset', fontsize = 20)
#     plt.ylabel('probability', fontsize = 20)
#     title_underscore = title.replace(" ", "_") 
#     title_svg = title_underscore + '.svg'
#     plt.show()
#     if (save_plots == True):
#         plt15.savefig(os.path.join(fig_rep_dir, title_svg), bbox_inches='tight', dpi=1000)

#     plt16 = plt.figure(58)
#     plt.rc('xtick', labelsize=10)
#     plt.rc('ytick', labelsize=10)
#     plt.bar(bin_centers, global_bin_heights[R3] ,width=bin_width) 
#     plt.autoscale(enable=True, axis = 'x', tight = True)
#     plt.autoscale(enable=True, axis = 'y', tight = True)
#     title = 'R3 Phase Offset Probability'
#     plt.title(title, fontsize = 20)
#     plt.xlabel('phase offset', fontsize = 20)
#     plt.ylabel('probability', fontsize = 20)
#     title_underscore = title.replace(" ", "_") 
#     title_svg = title_underscore + '.svg'
#     plt.show()
#     if (save_plots == True):
#         plt16.savefig(os.path.join(fig_rep_dir, title_svg), bbox_inches='tight', dpi=1000)
    

#     return phases, variances, bin_centers, normalized_bin_heights, bin_width, global_bin_heights


