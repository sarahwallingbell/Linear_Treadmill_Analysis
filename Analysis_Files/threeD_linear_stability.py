import os
import csv
import math
import matplotlib.pyplot as plt
import numpy as np
from shapely.geometry import Point
from shapely.geometry import Polygon
from shapely.ops import nearest_points

# Static Stability
# Calculates static stability and area of polygon over time
# Parameters: swing stance matrix, unadcusted classified top camera data, directories for exporting data and plots


def static_stability(swing_stance_mat, thorax, l_x_pos, l_y_pos, r_x_pos, r_y_pos, time, fig_num, save_plots, fig_rep_dir, fig_type, dpi_value):

    polygon_area = []
    positive_stability = [] #nan if unstable, dist com<->polygon if stable
    magnitude_stability = []  #dist com<->polygon if stable, negative if unstable, positive if stable
    max_magnitude_stability = [] #the com<->polygon distance at max stability 
    normed_magnitude_stability = [] #nan if unstable, mag_stability/max_stability if stable 
    stable_boolean = [] # stable=1, unstable=0


    #combine x and y coords for all legs [L1, L2, L3, R1, R2, R3]
    leg_x_coords = l_x_pos
    leg_x_coords.extend(r_x_pos)
    leg_y_coords = l_y_pos
    leg_y_coords.extend(r_y_pos)

    swing_stance_mat_array = np.array(swing_stance_mat)

    # For each frame
    for frame in range (0, len(swing_stance_mat[0])):          

        # Get legs in stance (==1)
        stance_legs = np.where(swing_stance_mat_array[:, frame] == 1)[0]

        # To have any static stability, at least three legs must be in stance           
        if len(stance_legs) != 3:
            positive_stability.append(math.nan)
            magnitude_stability.append(math.nan)
            max_magnitude_stability.append(math.nan)
            normed_magnitude_stability.append(math.nan)
            stable_boolean.append(math.nan)
            polygon_area.append(math.nan)
        else:
            #find x and y coords of all legs in stance 
            stance_legs_x = []
            stance_legs_y = []
            for leg in stance_legs:
                stance_legs_x.append(leg_x_coords[leg][frame])
                stance_legs_y.append(leg_y_coords[leg][frame])     

            # Calculate polygon in (x, y) plane 
            polygon_coords = np.column_stack((np.array(stance_legs_x), np.array(stance_legs_y)))
            polygon = Polygon(polygon_coords)
            polygon_area.append(polygon.area)

            # Calculate static stability 
            com = Point([thorax['thorax_x'][frame], thorax['thorax_y'][frame]]) # center of mass 

            if (polygon.contains(com)): # check if com is inside polygon
                #STABLE 
                com_stability_distance = polygon.exterior.distance(com)
                polygon_center = polygon.centroid.coords
                max_stability_distance = polygon.exterior.distance(Point(polygon_center))
                norm_stability_distance = com_stability_distance/max_stability_distance

                #save values
                stable_boolean.append(1.0)
                positive_stability.append(com_stability_distance)
                magnitude_stability.append(com_stability_distance)
                max_magnitude_stability.append(max_stability_distance)
                normed_magnitude_stability.append(norm_stability_distance)

            else:
                #UNSTABLE
                p0_point, p1_point = nearest_points(polygon, com)
                p0 = np.array(p0_point)
                p1 = np.array(p1_point)
                com_stability_distance = -1 * math.sqrt((p0[0] - p1[0])**2 + (p0[1] - p1[1])**2)

                #save values 
                stable_boolean.append(0.0)
                positive_stability.append(math.nan)
                magnitude_stability.append(com_stability_distance) 
               # max_magnitude_stability.append(math.nan)
                polygon_center = polygon.centroid.coords
                max_stability_distance = polygon.exterior.distance(Point(polygon_center))
                max_magnitude_stability.append(max_stability_distance)
                
                normed_magnitude_stability.append(math.nan)

    magnitude_stability_array = np.array(magnitude_stability)
    
#     plt1=plt.figure(fig_num, figsize=[10,5])
#     plt.plot(time, magnitude_stability_array, color='black', linewidth=1.25)
#     plt.xlabel('time (seconds)', fontsize=18)
#     plt.ylabel('distance between com and polygon (mm)', fontsize=18)
#     plt.title('Static Stability', fontsize=18)
#     fig_num=fig_num+1
#     fig_name= fig_rep_dir+'/static stability'+fig_type
#     plt1.savefig(fig_name, dpi=dpi_value)
    
                    
    return polygon_area, positive_stability, magnitude_stability, normed_magnitude_stability, stable_boolean, max_magnitude_stability, fig_num





def global_static_stability(fly_id, global_static_stability_positive, global_static_stability_magnitude, global_static_stability_normed, global_static_stability_boolean, global_polygon_area, nlegs, global_plots_path, global_data_path, fig_type, dpi_value, fig_num):
    
    #STATIC STABILITY POSITIVE
    
    shape = len(np.array(global_static_stability_positive).shape)          
    if shape == 2: #for single file analysis... the list needs to be nested once more 
        global_static_stability_positive = [global_static_stability_positive]

    for f in range(0, len(global_static_stability_positive)):
        if not isinstance(global_static_stability_positive[f], list):
            global_static_stability_positive[f] = global_static_stability_positive[f].tolist()
    global_static_stability_positive = np.array(global_static_stability_positive)
    
    line_transparency = 0.3
    mean = 0
    std = 1
    
    num_sessions = len(global_static_stability_positive[0])
    sessions = np.arange(1, num_sessions+1)
    fly_labels = []
    for f in fly_id:
        fly_labels.append('fly' + str(f))
    fly_labels.append('mean + std')

    #plot mean and variance of MEAN
    plt1=plt.figure(fig_num, figsize=[10,5])
    for fly in range (0, len(global_static_stability_positive)):
        plt.plot(sessions, global_static_stability_positive[fly, :, mean], marker='.', markersize=12, linewidth=0.75, alpha=line_transparency)

    error_array = []
    for sesh in range (0, num_sessions):
        error_array.append(global_static_stability_positive[:, sesh, mean])
                     
    global_static_stability_positive_mean_var = np.array([np.nanmean(np.array(error_array), axis=1), np.nanstd(np.array(error_array), axis=1)]) #[mean, var]
    mean = 0
    var = 1
    plt.errorbar(sessions, global_static_stability_positive_mean_var[mean], yerr = global_static_stability_positive_mean_var[var], linewidth=1.25, color='black', marker='.', markerfacecolor='red', markersize=18) 
    plt.xticks(sessions, fontsize=12)
    plt.xlabel('Session', fontsize=18)
    plt.ylabel('Mean Distance Between Thorax and Polygon (mm)', fontsize=18)
    plt.title('Mean Population Static Stability', fontsize=18)
    plt.legend(fly_labels ,loc='center left', bbox_to_anchor=(1, 0.5))
    fig_name= global_plots_path+'/mean static stability'+fig_type
    plt1.savefig(fig_name, dpi=dpi_value)
    fig_num=fig_num+1

    #plot mean and variance of STANDARD DEVIATION

    plt2=plt.figure(fig_num, figsize=[10,5])
    for fly in range (0, len(global_static_stability_positive)):
        plt.plot(sessions, global_static_stability_positive[fly, :, std], marker='.', markersize=12, linewidth=0.75, alpha=line_transparency)
            
    error_array = []
    for sesh in range (0, num_sessions):
        error_array.append(global_static_stability_positive[:, sesh, std])
                     
    plt.errorbar(sessions, np.nanmean(np.array(error_array)), yerr = np.nanstd(np.array(error_array)), linewidth=1.25, color='black', marker='.', markerfacecolor='red', markersize=18)   
    plt.xticks(sessions, fontsize=12)
    plt.xlabel('Session', fontsize=18)
    plt.ylabel('Variance Distance Between Thorax and Polygon (mm)', fontsize=18)
    plt.title('Variance Population Static Stability', fontsize=18)
    plt.legend(fly_labels ,loc='center left', bbox_to_anchor=(1, 0.5))
    fig_name= global_plots_path+'/variance static stability'+fig_type
    plt2.savefig(fig_name, dpi=dpi_value)
    fig_num=fig_num+1
    
    #STATIC STABILITY NORMED
    
    shape = len(np.array(global_static_stability_normed).shape)          
    if shape == 2: #for single file analysis... the list needs to be nested once more 
        global_static_stability_normed = [global_static_stability_normed]

    for f in range(0, len(global_static_stability_normed)):
        if not isinstance(global_static_stability_normed[f], list):
            global_static_stability_normed[f] = global_static_stability_normed[f].tolist()
    global_static_stability_normed = np.array(global_static_stability_normed)
    
    line_transparency = 0.3
    mean = 0
    std = 1
    
    num_sessions = len(global_static_stability_normed[0])
    sessions = np.arange(1, num_sessions+1)
    fly_labels = []
    for f in fly_id:
        fly_labels.append('fly' + str(f))
    fly_labels.append('mean + std')

    #plot mean and variance of MEAN
    plt1=plt.figure(fig_num, figsize=[10,5])
    for fly in range (0, len(global_static_stability_normed)):
        plt.plot(sessions, global_static_stability_normed[fly, :, mean], marker='.', markersize=12, linewidth=0.75, alpha=line_transparency)

    error_array = []
    for sesh in range (0, num_sessions):
        error_array.append(global_static_stability_normed[:, sesh, mean])
                     
    global_static_stability_normed_mean_var = np.array([np.nanmean(np.array(error_array), axis=1), np.nanstd(np.array(error_array), axis=1)]) #[mean, var]
    mean = 0
    var = 1
    plt.errorbar(sessions, global_static_stability_normed_mean_var[mean], yerr = global_static_stability_normed_mean_var[var], linewidth=1.25, color='black', marker='.', markerfacecolor='red', markersize=18)    
    plt.xticks(sessions, fontsize=12)
    plt.xlabel('Session', fontsize=18)
    plt.ylabel('Stability', fontsize=18)
    plt.title('Mean Population Static Stability Normed', fontsize=18)
    plt.legend(fly_labels ,loc='center left', bbox_to_anchor=(1, 0.5))
    fig_name= global_plots_path+'/mean static stability normed'+fig_type
    plt1.savefig(fig_name, dpi=dpi_value)
    fig_num=fig_num+1
    
    
    #plot mean and variance of STANDARD DEVIATION

    plt2=plt.figure(fig_num, figsize=[10,5])
    for fly in range (0, len(global_static_stability_normed)):
        plt.plot(sessions, global_static_stability_normed[fly, :, std], marker='.', markersize=12, linewidth=0.75, alpha=line_transparency)
            
    error_array = []
    for sesh in range (0, num_sessions):
        error_array.append(global_static_stability_normed[:, sesh, std])
                     
    plt.errorbar(sessions, np.nanmean(np.array(error_array)), yerr = np.nanstd(np.array(error_array)), linewidth=1.25, color='black', marker='.', markerfacecolor='red', markersize=18)   
    plt.xticks(sessions, fontsize=12)
    plt.xlabel('Session', fontsize=18)
    plt.ylabel('Stability', fontsize=18)
    plt.title('Variance Population Static Stability Normed', fontsize=18)
    plt.legend(fly_labels ,loc='center left', bbox_to_anchor=(1, 0.5))
    fig_name= global_plots_path+'/variance static stability normed'+fig_type
    plt2.savefig(fig_name, dpi=dpi_value)
    fig_num=fig_num+1
    
    
#     #STATIC STABILITY (POS & NEG)
    
#     shape = len(np.array(global_static_stability_magnitude).shape)          
#     if shape == 2: #for single file analysis... the list needs to be nested once more 
#         global_static_stability_magnitude = [global_static_stability_magnitude]

#     for f in range(0, len(global_static_stability_magnitude)):
#         if not isinstance(global_static_stability_magnitude[f], list):
#             global_static_stability_magnitude[f] = global_static_stability_magnitude[f].tolist()
#     global_static_stability_magnitude = np.array(global_static_stability_magnitude)
    
#     line_transparency = 0.3
#     mean = 0
#     std = 1
    
#     num_sessions = len(global_static_stability_magnitude[0])
#     sessions = np.arange(1, num_sessions+1)
#     fly_labels = []
#     for f in fly_id:
#         fly_labels.append('fly' + str(f))
#     fly_labels.append('mean + std')

#     #plot mean and variance of MEAN
#     plt1=plt.figure(fig_num, figsize=[10,5])
#     for fly in range (0, len(global_static_stability_magnitude)):
#         plt.plot(sessions, global_static_stability_magnitude[fly, :, mean], marker='.', markersize=12, linewidth=0.75, alpha=line_transparency)

#     error_array = []
#     for sesh in range (0, num_sessions):
#         error_array.append(global_static_stability_magnitude[:, sesh, mean])
                     
#     global_static_stability_mean_var = np.array([np.nanmean(np.array(error_array), axis=1), np.nanstd(np.array(error_array), axis=1)]) #[mean, var]
#     mean = 0
#     var = 1
#     plt.errorbar(sessions, global_static_stability_mean_var[mean], yerr = global_static_stability_mean_var[var], linewidth=1.25, color='black', marker='.', markerfacecolor='red', markersize=18)    
#     plt.xticks(sessions, fontsize=12)
#     plt.xlabel('Session', fontsize=18)
#     plt.ylabel('Mean Distance Between Thorax and Polygon (mm)', fontsize=18)
#     plt.title('Mean Population Static Stability', fontsize=18)
#     plt.legend(fly_labels ,loc='center left', bbox_to_anchor=(1, 0.5))
#     fig_name= global_plots_path+'/mean static stability'+fig_type
#     plt1.savefig(fig_name, dpi=dpi_value)
#     fig_num=fig_num+1

#     #plot mean and variance of STANDARD DEVIATION

#     plt2=plt.figure(fig_num, figsize=[10,5])
#     for fly in range (0, len(global_static_stability_magnitude)):
#         plt.plot(sessions, global_static_stability_magnitude[fly, :, std], marker='.', markersize=12, linewidth=0.75, alpha=line_transparency)
            
#     error_array = []
#     for sesh in range (0, num_sessions):
#         error_array.append(global_static_stability_magnitude[:, sesh, std])
                     
#     plt.errorbar(sessions, np.nanmean(np.array(error_array)), yerr = np.nanstd(np.array(error_array)), linewidth=1.25, color='black', marker='.', markerfacecolor='red', markersize=18)   
#     plt.xticks(sessions, fontsize=12)
#     plt.xlabel('Session', fontsize=18)
#     plt.ylabel('Variance Distance Between Thorax and Polygon (mm)', fontsize=18)
#     plt.title('Variance Population Static Stability', fontsize=18)
#     plt.legend(fly_labels ,loc='center left', bbox_to_anchor=(1, 0.5))
#     fig_name= global_plots_path+'/variance static stability'+fig_type
#     plt2.savefig(fig_name, dpi=dpi_value)
#     fig_num=fig_num+1
    
#     #PERCENT STABLE
#     shape = len(np.array(global_static_stability_boolean).shape)          
#     if shape == 2: #for single file analysis... the list needs to be nested once more 
#         global_static_stability_boolean = [global_static_stability_boolean]

#     for f in range(0, len(global_static_stability_boolean)):
#         if not isinstance(global_static_stability_boolean[f], list):
#             global_static_stability_boolean[f] = global_static_stability_boolean[f].tolist()
#     global_static_stability_boolean = np.array(global_static_stability_boolean)
    
#     line_transparency = 0.3
#     mean = 0
#     std = 1
#     num_sessions = len(global_static_stability_boolean)
#     sessions = np.arange(1, num_sessions+1)
#     print("sessions", sessions)
#     fly_labels = []
#     for f in fly_id:
#         fly_labels.append('fly' + str(f))
#     fly_labels.append('mean + std')
    
#     print("global_static_stability_boolean", global_static_stability_boolean)
#     print("global_static_stability_boolean[0, :]", global_static_stability_boolean[0, :])

#     #plot mean and variance of MEAN
#     plt1=plt.figure(fig_num, figsize=[10,5])
#     for fly in range (0, len(global_static_stability_boolean)):
#         plt.plot(sessions, global_static_stability_boolean[fly, :], marker='.', markersize=12, linewidth=0.75, alpha=line_transparency)

#     print("global_static_stability_boolean", global_static_stability_boolean)
#     global_percent_stable_mean_var = np.array([np.nanmean(global_static_stability_boolean), np.nanstd(global_static_stability_boolean)]) #[mean, var]
#     print("global_percent_stable_mean_var", global_percent_stable_mean_var)
#     print("global_percent_stable_mean_var[0]", global_percent_stable_mean_var[0])
#     print("global_percent_stable_mean_var[1]", global_percent_stable_mean_var[1])
#     mean = 0
#     var = 1
#     plt.errorbar(sessions, global_percent_stable_mean_var[mean], yerr = global_percent_stable_mean_var[var], linewidth=1.25, color='black', marker='.', markerfacecolor='red', markersize=18) 
#     plt.xticks(sessions, fontsize=12)
#     plt.xlabel('Session', fontsize=18)
#     plt.ylabel('Percent Stable', fontsize=18)
#     plt.title('Percent Stable', fontsize=18)
#     plt.legend(fly_labels ,loc='center left', bbox_to_anchor=(1, 0.5))
#     fig_name= global_plots_path+'/mean percent stable'+fig_type
#     plt1.savefig(fig_name, dpi=dpi_value)
#     fig_num=fig_num+1

    #PERCENT STABLE
    shape = len(np.array(global_polygon_area).shape)          
    if shape == 2: #for single file analysis... the list needs to be nested once more 
        global_polygon_area = [global_polygon_area]

    for f in range(0, len(global_polygon_area)):
        if not isinstance(global_polygon_area[f], list):
            global_polygon_area[f] = global_polygon_area[f].tolist()
    global_polygon_area = np.array(global_polygon_area)

    line_transparency = 0.3
    mean = 0
    std = 1
    
    num_sessions = len(global_static_stability_boolean[0])
    sessions = np.arange(1, num_sessions+1)
    fly_labels = []
    for f in fly_id:
        fly_labels.append('fly' + str(f))
    fly_labels.append('mean + std')

    #plot mean and variance of MEAN
    plt3=plt.figure(fig_num, figsize=[10,5])
    for fly in range (0, len(global_static_stability_boolean)):
        plt.plot(sessions, global_static_stability_boolean[fly], marker='.', markersize=12, linewidth=0.75, alpha=line_transparency)

    global_percent_stability_mean_var = np.array([np.nanmean(global_static_stability_boolean), np.nanstd(global_static_stability_boolean)]) #[mean]
    mean = 0
    var = 1
    plt.errorbar(sessions, global_percent_stability_mean_var[mean], yerr=global_percent_stability_mean_var[var], linewidth=1.25, color='black', marker='.', markerfacecolor='red', markersize=18)    
    plt.xticks(sessions, fontsize=12)
    plt.xlabel('Session', fontsize=18)
    plt.ylabel('Percent Stability', fontsize=18)
    plt.title('Mean Percent Stability', fontsize=18)
    plt.legend(fly_labels ,loc='center left', bbox_to_anchor=(1, 0.5))
    fig_name= global_plots_path+'/mean percent stability'+fig_type
    plt3.savefig(fig_name, dpi=dpi_value)
    fig_num=fig_num+1

    
    #POLYGON AREA
    shape = len(np.array(global_polygon_area).shape)          
    if shape == 2: #for single file analysis... the list needs to be nested once more 
        global_polygon_area = [global_polygon_area]

    for f in range(0, len(global_polygon_area)):
        if not isinstance(global_polygon_area[f], list):
            global_polygon_area[f] = global_polygon_area[f].tolist()
    global_polygon_area = np.array(global_polygon_area)
    
    line_transparency = 0.3
    mean = 0
    std = 1
    
    num_sessions = len(global_polygon_area[0])
    sessions = np.arange(1, num_sessions+1)
    fly_labels = []
    for f in fly_id:
        fly_labels.append('fly' + str(f))
    fly_labels.append('mean + std')

    #plot mean and variance of MEAN
    plt3=plt.figure(fig_num, figsize=[10,5])
    for fly in range (0, len(global_polygon_area)):
        plt.plot(sessions, global_polygon_area[fly, :, mean], marker='.', markersize=12, linewidth=0.75, alpha=line_transparency)

    error_array = []
    for sesh in range (0, num_sessions):
        error_array.append(global_polygon_area[:, sesh, mean])
                     
    global_polygon_area_mean_var = np.array([np.nanmean(np.array(error_array), axis=1), np.nanstd(np.array(error_array), axis=1)]) #[mean, var]
    mean = 0
    var = 1
    plt.errorbar(sessions, global_polygon_area_mean_var[mean], yerr = global_polygon_area_mean_var[var], linewidth=1.25, color='black', marker='.', markerfacecolor='red', markersize=18)    
    plt.xticks(sessions, fontsize=12)
    plt.xlabel('Session', fontsize=18)
    plt.ylabel('Mean Polygon Area (mm$\mathregular{^{2}}$)', fontsize=18)
    plt.title('Mean Population Polygon Area', fontsize=18)
    plt.legend(fly_labels ,loc='center left', bbox_to_anchor=(1, 0.5))
    fig_name= global_plots_path+'/mean polygon area'+fig_type
    plt3.savefig(fig_name, dpi=dpi_value)
    fig_num=fig_num+1

    #plot mean and variance of STANDARD DEVIATION

    plt4=plt.figure(fig_num, figsize=[10,5])
    for fly in range (0, len(global_polygon_area)):
        plt.plot(sessions, global_polygon_area[fly, :, std], marker='.', markersize=12, linewidth=0.75, alpha=line_transparency)
            
    error_array = []
    for sesh in range (0, num_sessions):
        error_array.append(global_polygon_area[:, sesh, std])
                     
    plt.errorbar(sessions, np.nanmean(np.array(error_array)), yerr = np.nanstd(np.array(error_array)), linewidth=1.25, color='black', marker='.', markerfacecolor='red', markersize=18)   
    plt.xticks(sessions, fontsize=12)
    plt.xlabel('Session', fontsize=18)
    plt.ylabel('Variance Polygon Area (mm$\mathregular{^{2}}$)', fontsize=18)
    plt.title('Variance Population Polygon Area', fontsize=18)
    plt.legend(fly_labels ,loc='center left', bbox_to_anchor=(1, 0.5))
    fig_name= global_plots_path+'/variance polygon area'+fig_type
    plt4.savefig(fig_name, dpi=dpi_value)
    fig_num=fig_num+1
    
    
    return global_static_stability_positive_mean_var, global_static_stability_normed_mean_var, global_percent_stability_mean_var, global_polygon_area_mean_var, fig_num
    
    
    
    
    
def global_static_stability_reps(fly_id, global_static_stability_magnitude, global_static_stability_normed, global_static_stability_boolean, global_polygon_area, nlegs, global_plots_path, global_data_path, fig_type, dpi_value, fig_num):
    
    #STATIC STABILITY 
    
    shape = len(np.array(global_static_stability_magnitude).shape)          
    if shape == 2: #for single file analysis... the list needs to be nested once more 
        global_static_stability_magnitude = [global_static_stability_magnitude]

    for f in range(0, len(global_static_stability_magnitude)):
        if not isinstance(global_static_stability_magnitude[f], list):
            global_static_stability_magnitude[f] = global_static_stability_magnitude[f].tolist()
    global_static_stability_magnitude = np.array(global_static_stability_magnitude)
    
    line_transparency = 0.3
    mean = 0
    std = 1
    
    num_reps = len(global_static_stability_magnitude[0])
    repeats = np.arange(1, num_reps+1)
    fly_labels = []
    for f in fly_id:
        fly_labels.append('fly' + str(f))
    fly_labels.append('mean + std')

    #plot mean and variance of MEAN
    plt1=plt.figure(fig_num, figsize=[10,5])
    for fly in range (0, len(global_static_stability_magnitude)):
        plt.plot(repeats, global_static_stability_magnitude[fly, :, mean], marker='.', markersize=12, linewidth=0.75, alpha=line_transparency)

    error_array = []
    for reps in range (0, num_reps):
        error_array.append(global_static_stability_magnitude[:, reps, mean])
                     
    plt.errorbar(repeats, np.nanmean(np.array(error_array), axis=1), yerr = np.nanstd(np.array(error_array), axis=1), linewidth=1.25, color='black', marker='.', markerfacecolor='red', markersize=18)    
    plt.xticks(repeats, fontsize=12)
    plt.xlabel('Repeat', fontsize=18)
    plt.ylabel('Mean Distance Between Thorax and Polygon (mm)', fontsize=18)
    plt.title('Mean Population Static Stability', fontsize=18)
    plt.legend(fly_labels ,loc='center left', bbox_to_anchor=(1, 0.5))
    fig_name= global_plots_path+'/mean static stability'+fig_type
    plt1.savefig(fig_name, dpi=dpi_value)
    fig_num=fig_num+1

    #plot mean and variance of STANDARD DEVIATION

    plt2=plt.figure(fig_num, figsize=[10,5])
    for fly in range (0, len(global_static_stability_magnitude)):
        plt.plot(repeats, global_static_stability_magnitude[fly, :, std], marker='.', markersize=12, linewidth=0.75, alpha=line_transparency)
            
    error_array = []
    for reps in range (0, num_reps):
        error_array.append(global_static_stability_magnitude[:, reps, std])
                     
    plt.errorbar(repeats, np.nanmean(np.array(error_array), axis=1), yerr = np.nanstd(np.array(error_array), axis=1), linewidth=1.25, color='black', marker='.', markerfacecolor='red', markersize=18)   
    plt.xticks(repeats, fontsize=12)
    plt.xlabel('Repeat', fontsize=18)
    plt.ylabel('Variance Distance Between Thorax and Polygon (mm)', fontsize=18)
    plt.title('Variance Population Static Stability', fontsize=18)
    plt.legend(fly_labels ,loc='center left', bbox_to_anchor=(1, 0.5))
    fig_name= global_plots_path+'/variance static stability'+fig_type
    plt2.savefig(fig_name, dpi=dpi_value)
    fig_num=fig_num+1
    
    
    #POLYGON AREA
    shape = len(np.array(global_polygon_area).shape)          
    if shape == 2: #for single file analysis... the list needs to be nested once more 
        global_polygon_area = [global_polygon_area]

    for f in range(0, len(global_polygon_area)):
        if not isinstance(global_polygon_area[f], list):
            global_polygon_area[f] = global_polygon_area[f].tolist()
    global_polygon_area = np.array(global_polygon_area)
    
    line_transparency = 0.3
    mean = 0
    std = 1
    
    num_reps = len(global_polygon_area[0])
    repeats = np.arange(1, num_reps+1)
    fly_labels = []
    for f in fly_id:
        fly_labels.append('fly' + str(f))
    fly_labels.append('mean + std')

    #plot mean and variance of MEAN
    plt3=plt.figure(fig_num, figsize=[10,5])
    for fly in range (0, len(global_polygon_area)):
        plt.plot(repeats, global_polygon_area[fly, :, mean], marker='.', markersize=12, linewidth=0.75, alpha=line_transparency)

    error_array = []
    for reps in range (0, num_reps):
        error_array.append(global_polygon_area[:, reps, mean])
                     
    plt.errorbar(repeats, np.nanmean(np.array(error_array), axis=1), yerr = np.nanstd(np.array(error_array), axis=1), linewidth=1.25, color='black', marker='.', markerfacecolor='red', markersize=18)    
    plt.xticks(repeats, fontsize=12)
    plt.xlabel('Repeat', fontsize=18)
    plt.ylabel('Mean Polygon Area (mm$\mathregular{^{2}}$)', fontsize=18)
    plt.title('Mean Population Polygon Area', fontsize=18)
    plt.legend(fly_labels ,loc='center left', bbox_to_anchor=(1, 0.5))
    fig_name= global_plots_path+'/mean polygon area'+fig_type
    plt3.savefig(fig_name, dpi=dpi_value)
    fig_num=fig_num+1

    #plot mean and variance of STANDARD DEVIATION

    plt4=plt.figure(fig_num, figsize=[10,5])
    for fly in range (0, len(global_polygon_area)):
        plt.plot(repeats, global_polygon_area[fly, :, std], marker='.', markersize=12, linewidth=0.75, alpha=line_transparency)
            
    error_array = []
    for reps in range (0, num_reps):
        error_array.append(global_polygon_area[:, reps, std])
                     
    plt.errorbar(repeats, np.nanmean(np.array(error_array), axis=1), yerr = np.nanstd(np.array(error_array), axis=1), linewidth=1.25, color='black', marker='.', markerfacecolor='red', markersize=18)   
    plt.xticks(repeats, fontsize=12)
    plt.xlabel('Repeat', fontsize=18)
    plt.ylabel('Variance Polygon Area (mm$\mathregular{^{2}}$)', fontsize=18)
    plt.title('Variance Population Polygon Area', fontsize=18)
    plt.legend(fly_labels ,loc='center left', bbox_to_anchor=(1, 0.5))
    fig_name= global_plots_path+'/variance polygon area'+fig_type
    plt4.savefig(fig_name, dpi=dpi_value)
    fig_num=fig_num+1
    
    
    return fig_num
    