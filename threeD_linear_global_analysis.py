import numpy as np

def analyze_global_data(fly_id, global_heading_angle, global_linear_velocity, global_rotational_velocity, global_step_amplitude, global_step_height, global_step_frequency, global_step_duration, global_stance_duration, global_swing_duration, global_num_swing_legs, global_num_stance_legs, global_phase, global_static_stability_positive, global_static_stability_magnitude, global_static_stability_normed, global_static_stability_boolean, global_polygon_area, nlegs, global_plots_path, global_data_path, fig_type, dpi_value, fig_num):
    

    # plot population data
    
    #HEADING ANGLE
    import threeD_linear_heading_angle as headingangle
    global_heading_angle_mean_var, fig_num = headingangle.global_heading_angle(fly_id, global_heading_angle, global_plots_path, global_data_path, fig_type, dpi_value, fig_num)

    #LINEAR & ROTATIONAL VELOCITY 
    import threeD_linear_velocity as velocity
    global_linear_velocity_mean_var, fig_num = velocity.global_velocity(fly_id, global_linear_velocity, global_rotational_velocity, global_plots_path, global_data_path, fig_type, dpi_value, fig_num)
    
    #PHASE
    import threeD_linear_phase as phase
    global_phase_mean_var, fig_num = phase.global_leg_phases(fly_id, global_phase, nlegs, global_plots_path, global_data_path, fig_type, dpi_value, fig_num) 
    
    #STEP FREQUENCY & DURATION
    import threeD_linear_step_frequency_and_duration as stepfreqdur
    global_step_freq_mean_var, global_step_dur_mean_var, fig_num = stepfreqdur.global_step_frequency_and_duration(fly_id, global_step_frequency, global_step_duration, nlegs, global_plots_path, global_data_path, fig_type, dpi_value, fig_num)
    
    #STEP HEIGHT
    import threeD_linear_step_height as stepheight
    global_step_height_mean_var, fig_num = stepheight.global_step_height(fly_id, global_step_height, nlegs, global_plots_path, global_data_path, fig_type, dpi_value, fig_num)
    
    #STEP AMPLITUDE
    import threeD_linear_step_amplitude as stepamp
    global_step_amp_mean_var, fig_num = stepamp.global_step_amplitude(fly_id, global_step_amplitude, nlegs, global_plots_path, global_data_path, fig_type, dpi_value, fig_num)
    
    #DUTY FACTOR
    import threeD_linear_duty_factor as dutyfactor
    global_swing_dur_mean_var, global_stance_dur_mean_var, fig_num = dutyfactor.global_duty_factor(fly_id, global_stance_duration, global_swing_duration, nlegs, global_plots_path, global_data_path, fig_type, dpi_value, fig_num)
    
    #NUM SWING & STANCE LEGS
    import threeD_linear_legs_in_swing_and_stance as swingstancelegs
    global_num_swing_legs_mean_var, global_num_stance_legs_mean_var, fig_num = swingstancelegs.global_num_legs_in_swing_and_stance(fly_id, global_num_swing_legs, global_num_stance_legs, nlegs, global_plots_path, global_data_path, fig_type, dpi_value, fig_num)
    
    #STABILITY
    import threeD_linear_stability as stability 
    global_static_stability_positive_mean_var, global_static_stability_normed_mean_var, global_percent_stability_mean_var, global_polygon_area_mean_var, fig_num = stability.global_static_stability(fly_id, global_static_stability_positive, global_static_stability_magnitude, global_static_stability_normed, global_static_stability_boolean, global_polygon_area, nlegs, global_plots_path, global_data_path, fig_type, dpi_value, fig_num)
    
    #SAVE MEAN & VAR DATA
    #body
    np.save(global_data_path+'/heading_angle_mean_var',np.array(global_heading_angle_mean_var))
    np.save(global_data_path+'/linear_velocity_mean_var',np.array(global_linear_velocity_mean_var))
    #interlimb
    np.save(global_data_path+'/phase_mean_var',np.array(global_phase_mean_var))
    np.save(global_data_path+'/num_swing_legs_mean_var',np.array(global_num_swing_legs_mean_var))
    np.save(global_data_path+'/num_stance_legs_mean_var',np.array(global_num_stance_legs_mean_var))
    #intralimb
    np.save(global_data_path+'/step_freq_mean_var',np.array(global_step_freq_mean_var))
    np.save(global_data_path+'/step_dur_mean_var',np.array(global_step_dur_mean_var))    
    np.save(global_data_path+'/step_height_mean_var',np.array(global_step_height_mean_var))
    np.save(global_data_path+'/step_amp_mean_var',np.array(global_step_amp_mean_var))
    np.save(global_data_path+'/swing_dur_mean_var',np.array(global_swing_dur_mean_var))
    np.save(global_data_path+'/stance_dur_mean_var',np.array(global_stance_dur_mean_var))
    #stability
    np.save(global_data_path+'/static_stability_positive_mean_var',np.array(global_static_stability_positive_mean_var))
    np.save(global_data_path+'/static_stability_normed_mean_var',np.array(global_static_stability_normed_mean_var))
    np.save(global_data_path+'/percent_stable_mean_var',np.array(global_percent_stability_mean_var))
    np.save(global_data_path+'/polygon_area_mean_var',np.array(global_polygon_area_mean_var))