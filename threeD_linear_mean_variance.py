import numpy as np
import math

def compute_stats(f_lin_vel, f_heading_angle, f_rot_vel, f_step_amp, f_step_h, f_step_frequency, f_step_duration, f_stance_duration, f_swing_duration, f_num_swing_legs, f_num_stance_legs, f_phase, f_polygon_area, f_positive_stability, f_magnitude_stability, f_normed_magnitude_stability, f_stable_boolean):
    # linear velocity
    mean_lin_vel=np.nanmean(f_lin_vel)
    std_lin_vel=np.nanstd(f_lin_vel)
    lin_vel_stat=[mean_lin_vel, std_lin_vel]
    
    # heading angle
    mean_heading_angle=np.nanmean(f_heading_angle)
    std_heading_angle=np.nanstd(f_heading_angle)
    heading_angle_stat=[mean_heading_angle, std_heading_angle]
    
    # rotational velocity
    mean_rot_vel=np.nanmean(f_rot_vel)
    std_rot_vel=np.nanstd(f_rot_vel)
    rot_vel_stat=[mean_rot_vel, std_rot_vel]
    
    # num legs in swing
    mean_num_swing_legs=np.nanmean(f_num_swing_legs)
    std_num_swing_legs=np.nanstd(f_num_swing_legs)
    num_swing_legs_stat=[mean_num_swing_legs, std_num_swing_legs]
    
    # num legs in stance
    mean_num_stance_legs=np.nanmean(f_num_stance_legs)
    std_num_stance_legs=np.nanstd(f_num_stance_legs)
    num_stance_legs_stat=[mean_num_stance_legs, std_num_stance_legs]
    
    # static stability 
    mean_positive_stability=np.nanmean(f_positive_stability)
    std_positive_stability=np.nanstd(f_positive_stability)
    positive_stability_stat=[mean_positive_stability, std_positive_stability]
    
    mean_magnitude_stability=np.nanmean(f_magnitude_stability)
    std_magnitude_stability=np.nanstd(f_magnitude_stability)
    magnitude_stability_stat=[mean_magnitude_stability, std_magnitude_stability]
    
    mean_normed_magnitude_stability=np.nanmean(f_normed_magnitude_stability)
    std_normed_magnitude_stability=np.nanstd(f_normed_magnitude_stability)
    normed_magnitude_stability_stat=[mean_normed_magnitude_stability, std_normed_magnitude_stability]
    
    num_stable = np.nansum(f_stable_boolean)
    len_boolean = np.count_nonzero(~np.isnan(f_stable_boolean)) #number of non-nan indices
    percent_stable = num_stable/len_boolean

    f_stable_boolean = f_stable_boolean[np.logical_not(np.isnan(f_stable_boolean))] #eliminate non-walking indices 
    num_stable = np.count_nonzero(f_stable_boolean)
    len_boolean = len(f_stable_boolean)
    percent_stable_boolean=(num_stable/len_boolean) 
    stable_boolean_stat= percent_stable_boolean
    
    # polygon area 
    mean_polygon_area=np.nanmean(f_polygon_area)
    std_polygon_area=np.nanstd(f_polygon_area)
    polygon_area_stat=[mean_polygon_area, std_polygon_area]
    
    # step amplitude
    step_amp_stat=[]
    step_h_stat=[]
    phase_stat=[]
    step_freq_stat=[]
    step_dur_stat=[]
    stance_dur_stat=[]
    swing_dur_stat=[]
    for leg in range(0,len(f_step_amp)):
        mean_step_amp=np.nanmean(f_step_amp[leg])
        std_step_amp=np.nanstd(f_step_amp[leg])
        step_amp_stat.append([mean_step_amp, std_step_amp])
        
        # step height
        mean_step_h=np.nanmean(f_step_h[leg])
        std_step_h=np.nanstd(f_step_h[leg])
        step_h_stat.append([mean_step_h, std_step_h])
    
        # step frequency
        mean_step_freq=np.nanmean(f_step_frequency[leg])
        std_step_freq=np.nanstd(f_step_frequency[leg])
        step_freq_stat.append([mean_step_freq, std_step_freq])
        
        # step duration
        mean_step_dur=np.nanmean(f_step_duration[leg])
        std_step_dur=np.nanstd(f_step_duration[leg])
        step_dur_stat.append([mean_step_dur, std_step_dur])
        
        # stance duration
        mean_stance_dur=np.nanmean(f_stance_duration[leg])
        std_stance_dur=np.nanstd(f_stance_duration[leg])
        stance_dur_stat.append([mean_stance_dur, std_stance_dur])
        
        # swing duration
        mean_swing_dur=np.nanmean(f_swing_duration[leg])
        std_swing_dur=np.nanstd(f_swing_duration[leg])
        swing_dur_stat.append([mean_swing_dur, std_swing_dur])
    
        # phase
        mean_phase=np.nanmean(f_phase[leg])
        std_phase=np.nanstd(f_phase[leg])
        phase_stat.append([mean_phase, std_phase])
    
    return lin_vel_stat, heading_angle_stat, rot_vel_stat, step_amp_stat, step_h_stat, step_freq_stat, step_dur_stat, stance_dur_stat, swing_dur_stat, num_swing_legs_stat, num_stance_legs_stat, phase_stat, polygon_area_stat, positive_stability_stat, magnitude_stability_stat, normed_magnitude_stability_stat, stable_boolean_stat
    
    