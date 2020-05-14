import numpy as np
import matplotlib.pyplot as plt


# Find frames where the fly is walking:
# 1) fly is walking forward (using heading direction)
# 2) fly is walking above a specified speed threshold (5 mm/s)
# 3) fly is upright (abdomen above the head z position)

def filter_walking(lin_vel, heading_angle, head, abdomen, amp_leg, num_swing_legs, num_stance_legs, step_duration, stance_start, nlegs):
    # filter walking based on linear velocity
    vel_threshold=5 # mm/s
    non_walking_vel = np.where(lin_vel<vel_threshold)[0]
    
    # filter walking based on orientation
    orient_threshold = 90 # degrees
    non_walking_orient=np.where(np.logical_or(heading_angle > orient_threshold, heading_angle < -orient_threshold))[0]
    
    # filter walking based on upright orientation
    hz=head['head_z']
    az=abdomen['abdomen_z']
    non_walking_upright=np.where(hz<az)[0]
    
    # filter out when fly is near back of chamber (the abdomen's closer than .75mm to the back of the chamber)
    non_walking_position = np.where(abdomen['abdomen_x'] < .75)[0]
    
    # filter walking based on number of legs in stance: If 0 or 6 legs are in stance it's not walking
    non_walking_swing = np.where(num_swing_legs == 6)[0]
    if amp_leg == -1: # no amputation, filter out when 6 legs in stance
        non_walking_stance = np.where(num_stance_legs == 6)[0]
    else: # amputation, filter out when five legs in stance
        non_walking_stance = np.where(num_stance_legs == 5)[0]
        
    # filter out frames where step duration is > 200ms
    non_walking_step_dur = []
    last_frame = len(head)-1
    for leg in range(0, nlegs):
        for idx in range(0, len(step_duration[leg])):
            step_start = stance_start[leg][idx]
            step_end = stance_start[leg][idx+1]
            step_length = step_duration[leg][idx]
            if (step_length >= 200):
                non_walking_step_dur.append(np.arange(step_start, step_end))
        non_walking_step_dur.append(np.arange(stance_start[leg][-1], last_frame))        
    non_walking_step_dur= np.concatenate(non_walking_step_dur).ravel()

    # concatenate non-walking indices
    non_walking_indices = np.concatenate((non_walking_vel, non_walking_orient, non_walking_upright, non_walking_position, non_walking_swing, non_walking_stance, non_walking_step_dur), axis=0)
    non_walking_indices= np.unique(non_walking_indices)
    
#     # if walking bout is < 25 frames, change to not walking
#     a = np.diff(non_walking_indices) #[1, 2, 5, 6, 3, 4]
#     b = np.where(a > 25.0) #[2]
#     c = a[b-1] #start of non-walking indices
#     d = a[b] #end of non-walking indices
#     for j in range(len(c)):
#         non_walking_indices.append(np.arrange(c[j], d[j]))
        
#     non_walking_indices = np.concatenate(non_walking_indices)
#     non_walking_indices= np.unique(non_walking_indices)
    
    np.where(non_walking_indices==899)
    
    if np.where(non_walking_indices==899)[0].size > 0:
        non_walking_indices=non_walking_indices[0:-1]
    
    return non_walking_indices



# Filter the data based on when fly is walking. Discard frames where not walking. 
def filter_data(fly_num, fps, non_walking_indices, lin_vel, heading_angle, rot_vel, swing_stance_mat, step_amp, stance_start, step_h, step_frequency, step_duration, stance_duration, swing_duration, num_swing_legs, num_stance_legs, phase, phase_time, swing_time_store, polygon_area, positive_stability, magnitude_stability, normed_magnitude_stability, stable_boolean, max_magnitude_stability, fig_num, save_plots, fig_rep_dir, fig_type, swing_stance_fig_type, dpi_value):
    
    #velocity arrays are one frame shorter, so if last frame isn't walking, truncate it. 
    if (non_walking_indices[-1] == len(lin_vel)):
        vel_non_walking_indices = non_walking_indices[0: -1]
    else:
        vel_non_walking_indices = non_walking_indices
        
    # linear velocity
    lin_vel[vel_non_walking_indices] = np.nan
    
    # heading angle
    heading_angle[non_walking_indices] = np.nan
   
    # rotational velocity 
    rot_vel[vel_non_walking_indices] = np.nan
    
    # num legs in swing
    num_swing_legs[non_walking_indices] = np.nan
    
    # num legs in stance
    num_stance_legs[non_walking_indices] = np.nan
    
    # static stability 
    positive_stability = np.array(positive_stability)
    positive_stability[non_walking_indices] = np.nan
    magnitude_stability = np.array(magnitude_stability)
    magnitude_stability[non_walking_indices] = np.nan
    normed_magnitude_stability = np.array(normed_magnitude_stability)
    normed_magnitude_stability[non_walking_indices] = np.nan
    stable_boolean = np.array(stable_boolean)
    stable_boolean[non_walking_indices] = np.nan #unstable
    max_magnitude_stability = np.array(max_magnitude_stability)
    max_magnitude_stability[non_walking_indices] = np.nan
    
    
    # polygon area
    polygon_area = np.array(polygon_area)
    polygon_area[non_walking_indices] = np.nan
    
    # swing stance matrix
    swing_stance_mat[:, non_walking_indices] = 0.5
    
    plt1=plt.figure(fig_num, figsize=[15,2])
#     plt.rc('xtick', labelsize = 60)
#     plt.rc('ytick', labelsize = 60)
    title = 'Filtered Swing Stance Plot (stance = white; swing = black)'
    plt.title(title, fontsize = 18)
    plt.xlabel('frame number (#)', fontsize = 18)
    plt.ylabel('leg', fontsize = 18)
    labels = ['R1', 'R2', 'R3']
    axes = plt.gca()
    axes.set_yticks(np.arange(0, 3, 1))
    axes.set_yticklabels(labels)
    plt.imshow(swing_stance_mat, interpolation = 'none', cmap = 'gray',aspect='auto')
    fig_num=fig_num+1
    fig_name= fig_rep_dir+'/filtered swing stance'+swing_stance_fig_type
    plt1.savefig(fig_name, dpi=dpi_value)
    
    # step amplitude
    for leg in range(0,len(step_amp)):
        for j in range(0,len(step_amp[leg])-1):
            step=np.where(np.logical_and(non_walking_indices>=stance_start[leg][j], non_walking_indices<=stance_start[leg][j+1]))[0]
            if step.size > 0: # there is a non-step
                step_amp[leg][j]=np.nan
    
    
    # step amplitude
    for leg in range(0,len(step_amp)):
        for j in range(0,len(step_amp[leg])-1):
            step=np.where(np.logical_and(non_walking_indices>=stance_start[leg][j], non_walking_indices<=stance_start[leg][j+1]))[0]
            if step.size > 0: # there is a non-step
                step_amp[leg][j]=np.nan
    
    
    # step height
    for leg in range(0,len(step_h)):
        for j in range(0,len(step_h[leg])-1):
            step=np.where(np.logical_and(non_walking_indices>=swing_time_store[leg][j], non_walking_indices<=swing_time_store[leg][j+1]))[0]
            if step.size > 0: # there is a non-step
                step_h[leg][j]=np.nan
                
    # step frequency
    for leg in range(0,len(step_frequency)):
        for j in range(0,len(step_h[leg])-1):
            step=np.where(np.logical_and(non_walking_indices>=stance_start[leg][j], non_walking_indices<=stance_start[leg][j+1]))[0]
            if step.size > 0: # there is a non-step
                step_frequency[leg][j]=np.nan
                
    
    # step duration
    for leg in range(0,len(step_duration)):
        for j in range(0,len(step_h[leg])-1):
            step=np.where(np.logical_and(non_walking_indices>=stance_start[leg][j], non_walking_indices<=stance_start[leg][j+1]))[0]
            if step.size > 0: # there is a non-step
                step_duration[leg][j]=np.nan
    
    # stance duration 
    for leg in range(0, len(stance_duration)):
        for j in range(0, len(stance_duration[leg])-1):
            step=np.where(np.logical_and(non_walking_indices>=stance_start[leg][j], non_walking_indices<=stance_start[leg][j+1]))[0]
            if step.size > 0: # there is a non-step
                stance_duration[leg][j]=np.nan
        
        
    # swing duration 
    for leg in range(0, len(swing_duration)):
        for j in range(0, len(swing_duration[leg])-1):
            step=np.where(np.logical_and(non_walking_indices>=stance_start[leg][j], non_walking_indices<=stance_start[leg][j+1]))[0]
            if step.size > 0: # there is a non-step
                swing_duration[leg][j]=np.nan
                

    # phase
    for leg in range(0,len(phase)):
        for j in range(0,len(phase[leg])-1):
            curr_phase=np.where(np.logical_and(non_walking_indices>=phase_time[j], non_walking_indices<=phase_time[j+1]))[0]
            if curr_phase.size > 0: # there is a non-step
                phase[leg][j]=np.nan
               
         
    return lin_vel, heading_angle, rot_vel, swing_stance_mat, step_amp, step_h, step_frequency, step_duration, stance_duration, swing_duration, num_swing_legs, num_stance_legs, phase, polygon_area, positive_stability, magnitude_stability, normed_magnitude_stability, stable_boolean, max_magnitude_stability, fig_num
    
    