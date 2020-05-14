import numpy as np
import math

def analyze_data(file, fly, session, repeat, amp_leg, fps, belt_speed, append_analyzed, save_plots, save_plots_path, fig_type, swing_stance_fig_type, dpi_value, save_data, save_data_path, fig_num):

    import os
    import pandas as pd
    import csv
    
    #Make necessary folders for local results (plots and data)
    if (save_plots == True or save_data == True):
        import threeD_linear_make_result_folders as mrf
        fig_rep_dir, data_rep_dir = mrf.make_result_folders(save_plots, save_plots_path, save_data, save_data_path, fly, session, repeat)
            
    #Extract relevant .csv file data 
    import threeD_linear_extract_data as ed
    head, thorax, abdomen, l1_norm, l2_norm, l3_norm, l1, l2, l3, l_x_pos, l_y_pos, l_z_pos, r1_norm, r2_norm, r3_norm, r1, r2, r3, r_x_pos, r_y_pos, r_z_pos, time, nlegs = ed.extract_data(file, fps)
    
    ########################################## Run Functions ##########################################
    
    #PLOT X TRAJECTORIES
    import threeD_linear_trajectories as trajectories
    fig_num = trajectories.plot_xtraj(l1, l2, l3, r1, r2, r3, fps, save_plots, fig_rep_dir, fig_type, dpi_value, fig_num)
    
    #FLY VELOCITY & HEADING ANGLE
    import threeD_linear_velocity as velocity
    linear_velocity, heading_angle, rotational_velocity, fig_num = velocity.velocity_and_heading_angle(fly, head, thorax, fps, time, belt_speed, save_plots, fig_rep_dir, fig_type, dpi_value, fig_num)
    
    #SWING STANCE 
    import threeD_linear_swing_stance as swingstance
    swing_stance_mat, stance_start, stance_end, fig_num = swingstance.swing_stance(l_x_pos, r_x_pos, nlegs, amp_leg, fig_num, save_plots, fig_rep_dir, fig_type, swing_stance_fig_type, dpi_value)
    
    ########################################## Check if continue with analysis ##########################################
    
    #If there aren't any stances for leg, end analysis of this rep. 
    save_this_rep = True
    if len(swing_stance_mat) == 1: #math.isnan(swing_stance_mat):
        save_this_rep = False
        print('Not enough steps -- rep not saved')
    else:
        for leg_stances in stance_end:
            if (len(leg_stances) < 10):
                save_this_rep = False
                print('Not enough stances -- rep not saved')
        for leg_stances in stance_start:
            if (len(leg_stances) < 10):
                save_this_rep = False
                print('Not enough stances -- rep not saved')

    ########################################## Continue with functions ##########################################
            
    if (save_this_rep):
        #Procede with analysis!
    
        #STEP HEIGHT
        import threeD_linear_step_height as stepheight
        step_height, swing_time_store, fig_num = stepheight.step_height(stance_start, stance_end, l_z_pos, r_z_pos, fig_num, save_plots, fig_rep_dir, fig_type, dpi_value)

        #STEP AMPLITUDE
        import threeD_linear_step_amplitude as stepamp
        step_amplitude, step_time_store, fig_num = stepamp.step_amplitude(stance_start, stance_end, l_x_pos, l_y_pos, fig_num, save_plots, fig_rep_dir, fig_type, dpi_value)

        #STEP FREQUENCY & DURATION
        import threeD_linear_step_frequency_and_duration as stepfreqdur
        step_frequency, step_duration, fig_num = stepfreqdur.step_freq_and_dur(stance_start, time, fig_num, save_plots, fig_rep_dir, fig_type, dpi_value)

        #DUTY FACTOR 
        import threeD_linear_duty_factor as dutyfactor
        stance_duration, swing_duration, fig_num = dutyfactor.duty_factor(stance_start, stance_end, time, fig_num, save_plots, fig_rep_dir, fig_type, dpi_value)

        #NUM LEGS IN SWING & STANCE
        import threeD_linear_legs_in_swing_and_stance as legsinswingstance
        num_swing_legs, num_stance_legs, fig_num = legsinswingstance.num_legs_in_swing_and_stance(swing_stance_mat, time, fig_num, save_plots, fig_rep_dir, fig_type, dpi_value)

        #PHASE
        import threeD_linear_phase as phase
        phase, phase_time, fig_num = phase.leg_phases(stance_start, nlegs, fig_num, save_plots, fig_rep_dir, fig_type, dpi_value)
        
        #STATIC STABILITY
        import threeD_linear_stability as stab
        polygon_area, positive_stability, magnitude_stability, normed_magnitude_stability, stable_boolean, max_magnitude_stability, fig_num = stab.static_stability(swing_stance_mat, thorax, l_x_pos, l_y_pos, r_x_pos, r_y_pos, time, fig_num, save_plots, fig_rep_dir, fig_type, dpi_value)

        #CLASSIFY WALKING
        import threeD_linear_classify_walking as classifywalking
        non_walking_indices = classifywalking.filter_walking(linear_velocity, heading_angle, head, abdomen, amp_leg, num_swing_legs, num_stance_legs, step_duration, stance_start, nlegs)
        
        #CHECK PERCENT WALKING
        num_frames = len(head)
        num_frames_not_walking = len(non_walking_indices)
        percent_not_walking = num_frames_not_walking / num_frames
        if (percent_not_walking < .9):
            #at least 1% of video is walking, so analyze the data
            print("Percent not walking: ", percent_not_walking, " -- rep saved")
            
            #FILTER DATA
            f_linear_velocity, f_heading_angle, f_rotational_velocity, f_swing_stance_mat, f_step_amplitude, f_step_height, f_step_frequency, f_step_duration, f_stance_duration, f_swing_duration, f_num_swing_legs, f_num_stance_legs, f_phase, f_polygon_area, f_positive_stability, f_magnitude_stability, f_normed_magnitude_stability, f_stable_boolean, f_max_magnitude_stability, fig_num = classifywalking.filter_data(fly, fps, non_walking_indices, linear_velocity, heading_angle, rotational_velocity, swing_stance_mat, step_amplitude, stance_start, step_height, step_frequency, step_duration, stance_duration, swing_duration, num_swing_legs, num_stance_legs, phase, phase_time, swing_time_store, polygon_area, positive_stability, magnitude_stability, normed_magnitude_stability, stable_boolean, max_magnitude_stability, fig_num, save_plots, fig_rep_dir, fig_type, swing_stance_fig_type, dpi_value)

            #FILTERED MEAN & VARIANCE
            import threeD_linear_mean_variance as stats
            linear_velocity_stat, heading_angle_stat, rotational_velocity_stat, step_amplitude_stat, step_height_stat, step_frequency_stat, step_duration_stat, stance_duration_stat, swing_duration_stat, num_swing_legs_stat, num_stance_legs_stat, phase_stat, polygon_area_stat, positive_stability_stat, magnitude_stability_stat, normed_magnitude_stability_stat, stable_boolean_stat = stats.compute_stats(f_linear_velocity, f_heading_angle, f_rotational_velocity, f_step_amplitude, f_step_height, f_step_frequency, f_step_duration, f_stance_duration, f_swing_duration, f_num_swing_legs, f_num_stance_legs, f_phase, f_polygon_area, f_positive_stability, f_magnitude_stability, f_normed_magnitude_stability, f_stable_boolean)

            #HISTOGRAM DATA
            heading_angle_list = f_heading_angle[np.logical_not(np.isnan(f_heading_angle))]
            velocity_list = f_linear_velocity[np.logical_not(np.isnan(f_linear_velocity))]
            num_stance_legs_list = f_num_stance_legs[np.logical_not(np.isnan(f_num_stance_legs))]
            stability_list = f_positive_stability[np.logical_not(np.isnan(f_positive_stability))]
            normed_stability_list = f_normed_magnitude_stability[np.logical_not(np.isnan(f_normed_magnitude_stability))]
            percent_stable_list = [] #[np.logical_not(np.isnan())]
            polygon_area_list = f_polygon_area[np.logical_not(np.isnan(f_polygon_area))]
            step_amp_list = f_step_amplitude

            #SAVE MEAN & VARIANCE RESULTS 
            np.save(data_rep_dir+'/linear_vel',np.array(linear_velocity_stat))
            np.save(data_rep_dir+'/rotational_vel',np.array(rotational_velocity_stat))
            np.save(data_rep_dir+'/heading_angle',np.array(heading_angle_stat))
            np.save(data_rep_dir+'/step_amp',np.array(step_amplitude_stat))
            np.save(data_rep_dir+'/step_h',np.array(step_height_stat))
            np.save(data_rep_dir+'/step_freq',np.array(step_frequency_stat))
            np.save(data_rep_dir+'/step_dur',np.array(step_duration_stat))
            np.save(data_rep_dir+'/stance_dur',np.array(stance_duration_stat))
            np.save(data_rep_dir+'/swing_dur',np.array(swing_duration_stat))
            np.save(data_rep_dir+'/num_swing_legs',np.array(num_swing_legs_stat))
            np.save(data_rep_dir+'/phase',np.array(phase_stat))
            np.save(data_rep_dir+'/static_stability_positive',np.array(positive_stability_stat))
            np.save(data_rep_dir+'/static_stability_magnitude',np.array(magnitude_stability_stat))
            np.save(data_rep_dir+'/static_stability_normed',np.array(normed_magnitude_stability_stat))
            np.save(data_rep_dir+'/static_stability_boolean',np.array(stable_boolean_stat))
            np.save(data_rep_dir+'/polygon_area',np.array(polygon_area_stat))

            return linear_velocity_stat, velocity_list, heading_angle_stat, heading_angle_list, rotational_velocity_stat, step_amplitude_stat, step_amp_list, step_height_stat, step_frequency_stat, step_duration_stat, stance_duration_stat, swing_duration_stat, num_swing_legs_stat, num_stance_legs_stat, num_stance_legs_list, phase_stat, polygon_area_stat, positive_stability_stat, magnitude_stability_stat, normed_magnitude_stability_stat, stable_boolean_stat, stability_list, normed_stability_list, percent_stable_list, polygon_area_list, nlegs, fig_num, save_this_rep


        else:
            #less than 1% of video is walking, don't save the data
            print("Percent not walking: ", percent_not_walking, " -- rep not saved")
            nan_array = np.array([np.nan])
            nan_array_legs = np.array([np.nan, np.nan, np.nan, np.nan, np.nan, np.nan])
            return np.nan, nan_array, np.nan, nan_array, np.nan, np.nan, nan_array_legs, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, nan_array, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, nan_array, nan_array, nan_array, nan_array, nlegs, fig_num, save_this_rep
    else:
        #Don't save this repetition
        nan_array = np.array([np.nan])
        nan_array_legs = np.array([np.nan, np.nan, np.nan, np.nan, np.nan, np.nan])
        return np.nan, nan_array, np.nan, nan_array, np.nan, np.nan, nan_array_legs, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, nan_array, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, nan_array, nan_array, nan_array, nan_array, nlegs, fig_num, save_this_rep
        
