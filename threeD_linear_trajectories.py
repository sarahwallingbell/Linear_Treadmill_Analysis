import csv
import os 
import matplotlib.pyplot as plt
import numpy as np

# Leg Trajectories 
# Plot leg trajectories of the fly relative to head before and after classification 
# Parameters: adjusted data (raw and classified), is walking array, directories for exporting data and plots,  L1 data for time calculation 


def plot_xtraj(l1, l2, l3, r1, r2, r3, fps, save_plots, fig_rep_dir, fig_type, dpi_value, fig_num):

    dt = 1/fps
    time = np.arange(0, len(l1)*dt, dt)
    
#     plt1=plt.figure(fig_num,figsize=[20,20])
    
#      # l1
#     plt.subplot(3,1,1)
#     plt.plot(time, l1[l1.columns[0]], color='black', linewidth=1.25)
#     plt.xlim(15, 20)
#     plt.xlabel('Time (seconds)', fontsize=18)
#     plt.ylabel('X position (mm)', fontsize=18)
#     plt.title('l1 x trajectory', fontsize=18)
    
#     # l2
#     plt.subplot(3,1,2)
#     plt.plot(time, l2[l2.columns[0]], color='red', linewidth=1.25)
#     plt.xlim(15, 20)
#     plt.xlabel('Time (seconds)', fontsize=18)
#     plt.ylabel('X position (mm)', fontsize=18)
#     plt.title('l2 x trajectory', fontsize=18)
    
#     # l3
#     plt.subplot(3,1,3)
#     plt.plot(time, l3[l3.columns[0]], color='blue', linewidth=1.25)
#     plt.xlim(15, 20)
#     plt.xlabel('Time (seconds)', fontsize=18)
#     plt.ylabel('X position (mm)', fontsize=18)
#     plt.title('l3 x trajectory', fontsize=18)
    
#     fig_name= fig_rep_dir+'/x_trajectories_left'+fig_type
#     plt1.savefig(fig_name, dpi=dpi_value)
    
#     fig_num = fig_num + 1
    
#     plt2=plt.figure(fig_num,figsize=[20,20])
    
#     # r1
#     plt.subplot(3,1,1)
#     plt.plot(time, r1[r1.columns[0]], color='black', linewidth=1.25)
#     plt.xlabel('Time (seconds)', fontsize=18)
#     plt.ylabel('X position (mm)', fontsize=18)
#     plt.title('r1 x trajectory', fontsize=18)
    
#     # r2
#     plt.subplot(3,1,2)
#     plt.plot(time, r2[r2.columns[0]], color='red', linewidth=1.25)
#     plt.xlabel('Time (seconds)', fontsize=18)
#     plt.ylabel('X position (mm)', fontsize=18)
#     plt.title('r2 x trajectory', fontsize=18)
    
#     # r3
#     plt.subplot(3,1,3)
#     plt.plot(time, r3[r3.columns[0]], color='blue', linewidth=1.25)
#     plt.xlabel('Time (seconds)', fontsize=18)
#     plt.ylabel('X position (mm)', fontsize=18)
#     plt.title('r3 x trajectory', fontsize=18)
    
#     fig_name= fig_rep_dir+'/x_trajectories_right'+fig_type
#     plt2.savefig(fig_name, dpi=dpi_value)

#     fig_num = fig_num + 1
           
    return fig_num
        
        
        
        
        
        
        
        
        
        
        
        
        
        

# def plot_trajectories_OLD(L1_mm, L2_mm, L3_mm, R1_mm, R2_mm, R3_mm, LH_mm, RH_mm, BL_mm, BR_mm, L1_mm_classified, L2_mm_classified, L3_mm_classified, R1_mm_classified, R2_mm_classified, R3_mm_classified, LH_mm_classified, RH_mm_classified, BL_mm_classified, BR_mm_classified, is_walking, save_plots, fig_rep_dir, save_data, data_rep_dir, L1): 


#     #(1a) Unclassified limb trajectories 
#     plt.close('all')
#     plt1a = plt.figure(1)
#     plt.rc('xtick', labelsize=10)
#     plt.rc('ytick', labelsize=10)
#     plt.plot(L1_mm[:, 0], L1_mm[:, 1]) 
#     plt.plot(L2_mm[:, 0], L2_mm[:, 1])
#     plt.plot(L3_mm[:, 0], L3_mm[:, 1]) 
#     plt.plot(R1_mm[:, 0], R1_mm[:, 1]) 
#     plt.plot(R2_mm[:, 0], R2_mm[:, 1]) 
#     plt.plot(R3_mm[:, 0], R3_mm[:, 1]) 
#     plt.plot(LH_mm[:, 0], LH_mm[:, 1]) 
#     plt.plot(RH_mm[:, 0], RH_mm[:, 1]) 
#     plt.gca().invert_yaxis() #invert y axis to match camera lens -- pixel (0,0) point in upper left corner
#     title = 'Raw Limb and Body Trajectories'
#     plt.title(title, fontsize = 15)
#     plt.legend(['Left Front', 'Left Mid', 'Left Hind', 'Right Front', 'Right Mid', 'Right Hind', 'Left Head (l)', 'Right Head (r)'])
#     plt.xlabel('x position (mm)', fontsize = 10) #label x axis 
#     plt.ylabel('y position (mm)', fontsize = 10) #label y axis
#     title_underscore = title.replace(" ", "_") + '_px'
#     title_svg = title_underscore + '.svg'
#     plt.show()
#     if (save_plots == True):
#         plt1a.savefig(os.path.join(fig_rep_dir, title_svg), bbox_inches='tight', dpi=1000)
    
#     if (save_data == True):
#         # Put raw trajectory data into matrix to save 
#         export_data = [L1_mm, L2_mm, L3_mm, R1_mm, R2_mm, R3_mm, LH_mm, RH_mm]
#         csv_file_path = os.path.join(data_rep_dir, title_underscore)
#         #save the list of lists
#         with open(csv_file_path, "w") as output:
#             writer = csv.writer(output, lineterminator='\n')
#             writer.writerows(export_data)
    
#     #(1b) Classified limb trajectories 
#     plt1b = plt.figure(2)
#     plt.rc('xtick', labelsize=10)
#     plt.rc('ytick', labelsize=10)
#     plt.plot(L1_mm_classified[:, 0], L1_mm_classified[:, 1]) 
#     plt.plot(L2_mm_classified[:, 0], L2_mm_classified[:, 1])
#     plt.plot(L3_mm_classified[:, 0], L3_mm_classified[:, 1])
#     plt.plot(R1_mm_classified[:, 0], R1_mm_classified[:, 1]) 
#     plt.plot(R2_mm_classified[:, 0], R2_mm_classified[:, 1]) 
#     plt.plot(R3_mm_classified[:, 0], R3_mm_classified[:, 1]) 
#     plt.plot(LH_mm_classified[:, 0], LH_mm_classified[:, 1]) 
#     plt.plot(RH_mm_classified[:, 0], RH_mm_classified[:, 1]) 
#     plt.gca().invert_yaxis() #invert y axis to match camera lens -- pixel (0,0) point in upper left corner
#     title = 'Classified Limb and Body Trajectories'
#     plt.title(title, fontsize = 15)
#     plt.legend(['Left Front', 'Left Mid', 'Left Hind', 'Right Front', 'Right Mid', 'Right Hind', 'Left Head (l)', 'Right Head (r)'])
#     plt.xlabel('x position (mm)', fontsize = 10) #label x axis 
#     plt.ylabel('y position (mm)', fontsize = 10) #label y axis
#     title_underscore = title.replace(" ", "_") + '_px'
#     title_svg = title_underscore + '.svg'
#     plt.show()
#     if (save_plots == True):
#         plt1b.savefig(os.path.join(fig_rep_dir, title_svg), bbox_inches='tight', dpi=1000)
    
#     if (save_data == True):
#         # Put classified trajectory data into matrix to save 
#         export_data = [L1_mm_classified, L2_mm_classified, L3_mm_classified, R1_mm_classified, R2_mm_classified, R3_mm_classified, LH_mm_classified, RH_mm_classified]
#         csv_file_path = os.path.join(data_rep_dir, title_underscore)
#         #save the list of lists
#         with open(csv_file_path, "w") as output:
#             writer = csv.writer(output, lineterminator='\n')
#             writer.writerows(export_data)
    
#     #(1c) Unclassified limb trajectories repositioned
#     plt1c = plt.figure(200)
#     plt.rc('xtick', labelsize=10)
#     plt.rc('ytick', labelsize=10)
#     #Head locations: LH(0, .2) RH(0, -.2)
#     plt.plot(L1_mm[:, 0]*(-1), (L1_mm[:, 1]+.2)*(-1))
#     plt.plot(L2_mm[:, 0]*(-1), (L2_mm[:, 1]+.2)*(-1))
#     plt.plot(L3_mm[:, 0]*(-1), (L3_mm[:, 1]+.2)*(-1))
#     plt.plot(R1_mm[:, 0], R1_mm[:, 1]-.2) 
#     plt.plot(R2_mm[:, 0], R2_mm[:, 1]-.2) 
#     plt.plot(R3_mm[:, 0], R3_mm[:, 1]-.2) 
#     plt.plot(LH_mm[:, 0]*(-1), (LH_mm[:, 1]+.2)*(-1))
#     plt.plot(RH_mm[:, 0], RH_mm[:, 1]-.2) 
#     plt.plot(BL_mm[:, 0]*(-1), (BL_mm[:, 1]+.2)*(-1))
#     plt.plot(BR_mm[:, 0], BR_mm[:, 1]-.2) 
#     plt.gca().invert_yaxis() #invert y axis to match camera lens -- pixel (0,0) point in upper left corner
#     title = 'Raw repositioned Limb and Body Trajectories'
#     plt.title(title, fontsize = 15)
#     plt.legend(['Left Front', 'Left Mid', 'Left Hind', 'Right Front', 'Right Mid', 'Right Hind', 'Left Head', 'Right Head', 'Body (l)', 'Body (r)'])
#     plt.xlabel('x position (mm)', fontsize = 10) #label x axis 
#     plt.ylabel('y position (mm)', fontsize = 10) #label y axis
#     title_underscore = title.replace(" ", "_") + '_px'
#     title_svg = title_underscore + '.svg'
#     plt.show()
#     if (save_plots == True):
#         plt1c.savefig(os.path.join(fig_rep_dir, title_svg), bbox_inches='tight', dpi=1000)
    
#     #(1d) Classified limb trajectories repositioned 
#     plt1d = plt.figure(200)
#     plt.rc('xtick', labelsize=10)
#     plt.rc('ytick', labelsize=10)
#     #Head locations: LH(0, .2) RH(0, -.2)
#     plt.plot(L1_mm_classified[:, 0]*(-1), (L1_mm_classified[:, 1]+.2)*(-1))
#     plt.plot(L2_mm_classified[:, 0]*(-1), (L2_mm_classified[:, 1]+.2)*(-1))
#     plt.plot(L3_mm_classified[:, 0]*(-1), (L3_mm_classified[:, 1]+.2)*(-1))
#     plt.plot(R1_mm_classified[:, 0], R1_mm_classified[:, 1]-.2) 
#     plt.plot(R2_mm_classified[:, 0], R2_mm_classified[:, 1]-.2) 
#     plt.plot(R3_mm_classified[:, 0], R3_mm_classified[:, 1]-.2) 
#     plt.plot(LH_mm_classified[:, 0]*(-1), (LH_mm_classified[:, 1]+.2)*(-1))
#     plt.plot(RH_mm_classified[:, 0], RH_mm_classified[:, 1]-.2) 
#     plt.plot(BL_mm_classified[:, 0]*(-1), (BL_mm_classified[:, 1]+.2)*(-1))
#     plt.plot(BR_mm_classified[:, 0], BR_mm_classified[:, 1]-.2) 
#     plt.gca().invert_yaxis() #invert y axis to match camera lens -- pixel (0,0) point in upper left corner
#     title = 'Classified Repositioned Limb and Body Trajectories'
#     plt.title(title, fontsize = 15)
#     #plt.legend(['Left Front', 'Left Mid', 'Left Hind', 'Right Front', 'Right Mid', 'Right Hind', 'Left Head', 'Right Head', 'Body (l)', 'Body (r)'])
#     plt.xlabel('x position (mm)', fontsize = 10) #label x axis 
#     plt.ylabel('y position (mm)', fontsize = 10) #label y axis
#     title_underscore = title.replace(" ", "_") + '_px'
#     title_svg = title_underscore + '.svg'
#     plt.show()
#     if (save_plots == True):
#         plt1d.savefig(os.path.join(fig_rep_dir, title_svg), bbox_inches='tight', dpi=1000)

#     #(2a) Unclassified left limb trajectories 
#     plt2a = plt.figure(3)  
#     plt.plot(L1_mm[:, 0], L1_mm[:, 1])
#     plt.plot(L2_mm[:, 0], L2_mm[:, 1])
#     plt.plot(L3_mm[:, 0], L3_mm[:, 1])
#     plt2a.gca().invert_xaxis()
#     title = 'Raw Left Foot Trajectories'
#     plt.title(title, fontsize = 15)
#     plt.legend(['Left Front', 'Left Mid', 'Left Hind']) 
#     plt.xlabel('x position (mm)') #label x axis 
#     plt.ylabel('y position (mm)') #label y axis 
#     title_underscore = title.replace(" ", "_")
#     title_svg = title_underscore + '_px' + '.svg'
#     plt.show()
#     if (save_plots == True):
#         plt2a.savefig(os.path.join(fig_rep_dir, title_svg), bbox_inches='tight', dpi=1000)
    
#     #(2b) Classified left limb trajectories 
#     plt2b = plt.figure(4)  
#     plt.plot(L1_mm_classified[:, 0], L1_mm_classified[:, 1])
#     plt.plot(L2_mm_classified[:, 0], L2_mm_classified[:, 1])
#     plt.plot(L3_mm_classified[:, 0], L3_mm_classified[:, 1])
#     plt2b.gca().invert_xaxis()
#     #label legend
#     title = 'Classified Left Foot Trajectories'
#     plt.title(title, fontsize = 15)
#     plt.legend(['Left Front', 'Left Mid', 'Left Hind']) 
#     plt.xlabel('x position (mm)') #label x axis 
#     plt.ylabel('y position (mm)') #label y axis 
#     title_underscore = title.replace(" ", "_")
#     title_svg = title_underscore + '_px' + '.svg'
#     plt.show()
#     if (save_plots == True):
#         plt2b.savefig(os.path.join(fig_rep_dir, title_svg), bbox_inches='tight', dpi=1000)
    
#     #(3a) Unclassified right limb trajectories 
#     plt3a = plt.figure(5)  
#     plt.plot(R1_mm[:, 0], R1_mm[:, 1])
#     plt.plot(R2_mm[:, 0], R2_mm[:, 1])
#     plt.plot(R3_mm[:, 0], R3_mm[:, 1])
#     plt3a.gca().invert_yaxis()
#     title = 'Raw Right Foot Trajectories'
#     plt.title(title, fontsize = 15)
#     plt.legend(['Right Front', 'Right Mid', 'Right Hind']) 
#     plt.xlabel('x position (mm)') #label x axis 
#     plt.ylabel('y position (mm)') #label y axis 
#     title_underscore = title.replace(" ", "_")
#     title_svg = title_underscore + '_px' + '.svg'
#     if (save_plots == True):
#         plt3a.savefig(os.path.join(fig_rep_dir, title_svg), bbox_inches='tight', dpi=1000)

#     #(3b) Classified right limb trajectories 
#     plt3b = plt.figure(6)  
#     plt.plot(R1_mm_classified[:, 0], R1_mm_classified[:, 1])
#     plt.plot(R2_mm_classified[:, 0], R2_mm_classified[:, 1])
#     plt.plot(R3_mm_classified[:, 0], R3_mm_classified[:, 1])
#     plt3b.gca().invert_yaxis()
#     title = 'Classified Right Foot Trajectories'
#     plt.title(title, fontsize = 15)
#     plt.legend(['Right Front', 'Right Mid', 'Right Hind']) 
#     plt.xlabel('x position (mm)') #label x axis 
#     plt.ylabel('y position (mm)') #label y axis 
#     title_underscore = title.replace(" ", "_")
#     title_svg = title_underscore + '_px' + '.svg'
#     if (save_plots == True):
#         plt3b.savefig(os.path.join(fig_rep_dir, title_svg), bbox_inches='tight', dpi=1000)


    
#     #(4a) Unclassified leg x positions
#     fps = 200 # frames per second 
#     dt = 1/fps # time between frames
#     time = np.arange(0, len(L1)*dt, dt) #numpy short hand for making a spaced array

#     plt4a1 = plt.figure(7, figsize = (100, 10))
#     plt.rc('xtick', labelsize=50)
#     plt.rc('ytick', labelsize=50)
#     plt.plot(time, L1_mm[:, 0], color = 'blue')
#     title = 'Raw L1 X Trajectory'
#     plt.title(title, fontsize = 100)
#     plt.xlabel('time (s)', fontsize = 75)
#     plt.ylabel('x position (mm)', fontsize = 75)
#     plt.autoscale(enable=True, axis = 'x', tight = True)
#     title_underscore = title.replace(" ", "_")
#     title_svg = title_underscore + '.svg'   
#     plt.show()
#     if (save_plots == True):
#         plt4a1.savefig(os.path.join(fig_rep_dir, title_svg), bbox_inches='tight', dpi=1000)

#     plt4a2 = plt.figure(8, figsize = (100, 10))
#     plt.rc('xtick', labelsize=50)
#     plt.rc('ytick', labelsize=50)
#     plt.plot(time, L2_mm[:, 0], color = 'orange')
#     title = 'Raw L2 X Trajectory'
#     plt.title(title, fontsize = 100)
#     plt.xlabel('time (s)', fontsize = 75)
#     plt.ylabel('x position (mm)', fontsize = 75)
#     plt.autoscale(enable=True, axis = 'x', tight = True)
#     title_underscore = title.replace(" ", "_")
#     title_svg = title_underscore + '.svg'
#     plt.show()
#     if (save_plots == True):
#         plt4a2.savefig(os.path.join(fig_rep_dir, title_svg), bbox_inches='tight', dpi=1000)

#     plt4a3 = plt.figure(9, figsize = (100, 10))
#     plt.rc('xtick', labelsize=50)
#     plt.rc('ytick', labelsize=50)
#     plt.plot(time, L3_mm[:, 0], color = 'green')
#     title = 'Raw L3 X Trajectory'
#     plt.title(title, fontsize = 100)
#     plt.xlabel('time (s)', fontsize = 75)
#     plt.ylabel('x position (mm)', fontsize = 75)
#     plt.autoscale(enable=True, axis = 'x', tight = True)
#     title_underscore = title.replace(" ", "_")
#     title_svg = title_underscore + '.svg'
#     plt.show()
#     if (save_plots == True):
#         plt4a3.savefig(os.path.join(fig_rep_dir, title_svg), bbox_inches='tight', dpi=1000)

#     plt4a4 = plt.figure(10, figsize = (100, 10))
#     plt.rc('xtick', labelsize=50)
#     plt.rc('ytick', labelsize=50)
#     plt.plot(time, R1_mm[:, 0], color = 'blue')
#     title = 'Raw R1 X Trajectory'
#     plt.title(title, fontsize = 100)
#     plt.xlabel('time (s)', fontsize = 75)
#     plt.ylabel('x position (mm)', fontsize = 75)
#     plt.autoscale(enable=True, axis = 'x', tight = True)
#     title_underscore = title.replace(" ", "_")
#     title_svg = title_underscore + '.svg'
#     plt.show()
#     if (save_plots == True):
#         plt4a4.savefig(os.path.join(fig_rep_dir, title_svg), bbox_inches='tight', dpi=1000)

#     plt4a5 = plt.figure(11, figsize = (100, 10))
#     plt.rc('xtick', labelsize=50)
#     plt.rc('ytick', labelsize=50)
#     plt.plot(time, R2_mm[:, 0], color = 'orange')
#     title = 'Raw R2 X Trajectory'
#     plt.title(title, fontsize = 100)
#     plt.xlabel('time (s)', fontsize = 75)
#     plt.ylabel('x position (mm)', fontsize = 75)
#     plt.autoscale(enable=True, axis = 'x', tight = True)
#     title_underscore = title.replace(" ", "_")
#     title_svg = title_underscore + '.svg'
#     plt.show()
#     if (save_plots == True):
#         plt4a5.savefig(os.path.join(fig_rep_dir, title_svg), bbox_inches='tight', dpi=1000)

#     plt4a6 = plt.figure(12, figsize = (100, 10))
#     plt.rc('xtick', labelsize=50)
#     plt.rc('ytick', labelsize=50)
#     plt.plot(time, R3_mm[:, 0], color = 'green')
#     title = 'Raw R3 X Trajectory'
#     plt.title(title, fontsize = 100)
#     plt.xlabel('time (s)', fontsize = 75)
#     plt.ylabel('x position (mm)', fontsize = 75)
#     plt.autoscale(enable=True, axis = 'x', tight = True)
#     title_underscore = title.replace(" ", "_")
#     title_svg = title_underscore + '.svg'
#     plt.show()
#     if (save_plots == True):
#         plt4a6.savefig(os.path.join(fig_rep_dir, title_svg), bbox_inches='tight', dpi=1000)

    
#     #(4b) Classified leg x positions   
#     plt4b1 = plt.figure(13, figsize = (100, 10))
#     plt.rc('xtick', labelsize=50)
#     plt.rc('ytick', labelsize=50)
#     plt.plot(time, L1_mm_classified[:, 0], color = 'blue')
#     title = 'Classified L1 X Trajectory'
#     plt.title(title, fontsize = 100)
#     plt.xlabel('time (s)', fontsize = 75)
#     plt.ylabel('x position (mm)', fontsize = 75)
#     plt.autoscale(enable=True, axis = 'x', tight = True)
#     title_underscore = title.replace(" ", "_")
#     title_svg = title_underscore + '.svg'   
#     plt.show()
#     if (save_plots == True):
#         plt4b1.savefig(os.path.join(fig_rep_dir, title_svg), bbox_inches='tight', dpi=1000)

#     plt4b2 = plt.figure(14, figsize = (100, 10))
#     plt.rc('xtick', labelsize=50)
#     plt.rc('ytick', labelsize=50)
#     plt.plot(time, L2_mm_classified[:, 0], color = 'orange')
#     title = 'Classified L2 X Trajectory'
#     plt.title(title, fontsize = 100)
#     plt.xlabel('time (s)', fontsize = 75)
#     plt.ylabel('x position (mm)', fontsize = 75)
#     plt.autoscale(enable=True, axis = 'x', tight = True)
#     title_underscore = title.replace(" ", "_")
#     title_svg = title_underscore + '.svg'
#     plt.show()
#     if (save_plots == True):
#         plt4b2.savefig(os.path.join(fig_rep_dir, title_svg), bbox_inches='tight', dpi=1000)

#     plt4b3 = plt.figure(15, figsize = (100, 10))
#     plt.rc('xtick', labelsize=50)
#     plt.rc('ytick', labelsize=50)
#     plt.plot(time, L3_mm_classified[:, 0], color = 'green')
#     title = 'Classified L3 X Trajectory'
#     plt.title(title, fontsize = 100)
#     plt.xlabel('time (s)', fontsize = 75)
#     plt.ylabel('x position (mm)', fontsize = 75)
#     plt.autoscale(enable=True, axis = 'x', tight = True)
#     title_underscore = title.replace(" ", "_")
#     title_svg = title_underscore + '.svg'
#     plt.show()
#     if (save_plots == True):
#         plt4b3.savefig(os.path.join(fig_rep_dir, title_svg), bbox_inches='tight', dpi=1000)

#     plt4b4 = plt.figure(16, figsize = (100, 10))
#     plt.rc('xtick', labelsize=50)
#     plt.rc('ytick', labelsize=50)
#     plt.plot(time, R1_mm_classified[:, 0], color = 'blue')
#     title = 'Classified R1 X Trajectory'
#     plt.title(title, fontsize = 100)
#     plt.xlabel('time (s)', fontsize = 75)
#     plt.ylabel('x position (mm)', fontsize = 75)
#     plt.autoscale(enable=True, axis = 'x', tight = True)
#     title_underscore = title.replace(" ", "_")
#     title_svg = title_underscore + '.svg'
#     plt.show()
#     if (save_plots == True):
#         plt4b4.savefig(os.path.join(fig_rep_dir, title_svg), bbox_inches='tight', dpi=1000)

#     plt4b5 = plt.figure(17, figsize = (100, 10))
#     plt.rc('xtick', labelsize=50)
#     plt.rc('ytick', labelsize=50)
#     plt.plot(time, R2_mm_classified[:, 0], color = 'orange')
#     title = 'Classified R2 X Trajectory'
#     plt.title(title, fontsize = 100)
#     plt.xlabel('time (s)', fontsize = 75)
#     plt.ylabel('x position (mm)', fontsize = 75)
#     plt.autoscale(enable=True, axis = 'x', tight = True)
#     title_underscore = title.replace(" ", "_")
#     title_svg = title_underscore + '.svg'
#     plt.show()
#     if (save_plots == True):
#         plt4b5.savefig(os.path.join(fig_rep_dir, title_svg), bbox_inches='tight', dpi=1000)

#     plt4b6 = plt.figure(18, figsize = (100, 10))
#     plt.rc('xtick', labelsize=50)
#     plt.rc('ytick', labelsize=50)
#     plt.plot(time, R3_mm_classified[:, 0], color = 'green')
#     title = 'Classified R3 X Trajectory'
#     plt.title(title, fontsize = 100)
#     plt.xlabel('time (s)', fontsize = 75)
#     plt.ylabel('x position (mm)', fontsize = 75)
#     plt.autoscale(enable=True, axis = 'x', tight = True)
#     title_underscore = title.replace(" ", "_")
#     title_svg = title_underscore + '.svg'
#     plt.show()
#     if (save_plots == True):
#         plt4b6.savefig(os.path.join(fig_rep_dir, title_svg), bbox_inches='tight', dpi=1000)

    
#     #(4c) Classified lef x positions zoomed 
#     xmin = 20
#     xmax = 21
    
#     plt4b1 = plt.figure(19, figsize = (100, 10))
#     plt.rc('xtick', labelsize=50)
#     plt.rc('ytick', labelsize=50)
#     plt.plot(time, L1_mm_classified[:, 0], color = 'blue')
#     title = 'Classified L1 X Trajectory'
#     plt.title(title, fontsize = 100)
#     plt.xlabel('time (s)', fontsize = 75)
#     plt.ylabel('x position (mm)', fontsize = 75)
#     axes = plt.gca()
#     axes.set_xlim([xmin,xmax])
#     title_underscore = title.replace(" ", "_") + 'Zoomed'
#     title_svg = title_underscore + '.svg'  
#     plt.show()
#     if (save_plots == True):
#         plt4b1.savefig(os.path.join(fig_rep_dir, title_svg), bbox_inches='tight', dpi=1000)

#     plt4b2 = plt.figure(20, figsize = (100, 10))
#     plt.rc('xtick', labelsize=50)
#     plt.rc('ytick', labelsize=50)
#     plt.plot(time, L2_mm_classified[:, 0], color = 'orange')
#     title = 'Classified L2 X Trajectory'
#     plt.title(title, fontsize = 100)
#     plt.xlabel('time (s)', fontsize = 75)
#     plt.ylabel('x position (mm)', fontsize = 75)
#     axes = plt.gca()
#     axes.set_xlim([xmin,xmax])
#     title_underscore = title.replace(" ", "_") + 'Zoomed'
#     title_svg = title_underscore + '.svg'
#     plt.show()
#     if (save_plots == True):
#         plt4b2.savefig(os.path.join(fig_rep_dir, title_svg), bbox_inches='tight', dpi=1000)

#     plt4b3 = plt.figure(21, figsize = (100, 10))
#     plt.rc('xtick', labelsize=50)
#     plt.rc('ytick', labelsize=50)
#     plt.plot(time, L3_mm_classified[:, 0], color = 'green')
#     title = 'Classified L3 X Trajectory'
#     plt.title(title, fontsize = 100)
#     plt.xlabel('time (s)', fontsize = 75)
#     plt.ylabel('x position (mm)', fontsize = 75)
#     axes = plt.gca()
#     axes.set_xlim([xmin,xmax])
#     title_underscore = title.replace(" ", "_") + 'Zoomed'
#     title_svg = title_underscore + '.svg'
#     plt.show()
#     if (save_plots == True):
#         plt4b3.savefig(os.path.join(fig_rep_dir, title_svg), bbox_inches='tight', dpi=1000)

#     plt4b4 = plt.figure(22, figsize = (100, 10))
#     plt.rc('xtick', labelsize=50)
#     plt.rc('ytick', labelsize=50)
#     plt.plot(time, R1_mm_classified[:, 0], color = 'blue')
#     title = 'Classified R1 X Trajectory'
#     plt.title(title, fontsize = 100)
#     plt.xlabel('time (s)', fontsize = 75)
#     plt.ylabel('x position (mm)', fontsize = 75)
#     axes = plt.gca()
#     axes.set_xlim([xmin,xmax])
#     title_underscore = title.replace(" ", "_") + 'Zoomed'
#     title_svg = title_underscore + '.svg'
#     plt.show()
#     if (save_plots == True):
#         plt4b4.savefig(os.path.join(fig_rep_dir, title_svg), bbox_inches='tight', dpi=1000)

#     plt4b5 = plt.figure(23, figsize = (100, 10))
#     plt.rc('xtick', labelsize=50)
#     plt.rc('ytick', labelsize=50)
#     plt.plot(time, R2_mm_classified[:, 0], color = 'orange')
#     title = 'Classified R2 X Trajectory'
#     plt.title(title, fontsize = 100)
#     plt.xlabel('time (s)', fontsize = 75)
#     plt.ylabel('x position (mm)', fontsize = 75)
#     axes = plt.gca()
#     axes.set_xlim([xmin,xmax])
#     title_underscore = title.replace(" ", "_") + 'Zoomed'
#     title_svg = title_underscore + '.svg'
#     plt.show()
#     if (save_plots == True):
#         plt4b5.savefig(os.path.join(fig_rep_dir, title_svg), bbox_inches='tight', dpi=1000)

#     plt4b6 = plt.figure(24, figsize = (100, 10))
#     plt.rc('xtick', labelsize=50)
#     plt.rc('ytick', labelsize=50)
#     plt.plot(time, R3_mm_classified[:, 0], color = 'green')
#     title = 'Classified R3 X Trajectory'
#     plt.title(title, fontsize = 100)
#     plt.xlabel('time (s)', fontsize = 75)
#     plt.ylabel('x position (mm)', fontsize = 75)
#     axes = plt.gca()
#     axes.set_xlim([xmin,xmax])
#     title_underscore = title.replace(" ", "_") + 'Zoomed'
#     title_svg = title_underscore + '.svg'
#     plt.show()
#     if (save_plots == True):
#         plt4b6.savefig(os.path.join(fig_rep_dir, title_svg), bbox_inches='tight', dpi=1000)

    
#     #(5a) Unclassified repositioned x trajectories
    
#     # Reposition (shift) legs x trajectories for graphing purposes 
#     spacing = 3
#     L1_repo_x = (L1_mm[:,0] - np.nanmean(L1_mm[:,0]))-spacing
#     L2_repo_x = (L2_mm[:,0] - np.nanmean(L2_mm[:,0]))-(2*spacing)
#     L3_repo_x = (L3_mm[:,0] - np.nanmean(L3_mm[:,0]))-(3*spacing)
#     R1_repo_x = (R1_mm[:,0] - np.nanmean(R1_mm[:,0]))+spacing
#     R2_repo_x = (R2_mm[:,0] - np.nanmean(R2_mm[:,0]))+(2*spacing)
#     R3_repo_x = (R3_mm[:,0] - np.nanmean(R3_mm[:,0]))+(3*spacing)

#     plt5a = plt.figure(25, figsize = (10, 10))
#     plt.rc('xtick', labelsize=10)
#     plt.rc('ytick', labelsize=10)
#     plt.plot(L1_repo_x, time, linewidth = 0.5)
#     plt.plot(L2_repo_x, time, linewidth = 0.5)
#     plt.plot(L3_repo_x, time, linewidth = 0.5)
#     plt.plot(R1_repo_x, time, linewidth = 0.5)
#     plt.plot(R2_repo_x, time, linewidth = 0.5)
#     plt.plot(R3_repo_x, time, linewidth = 0.5)
#     plt.gca().invert_yaxis()
#     title = 'Raw Repositioned X Trajectories'
#     plt.title(title, fontsize = 20)
#     plt.ylabel('time (s)', fontsize = 10)
#     plt.xlabel('x position (mm)', fontsize = 10)
#     plt.legend(['Left Front', 'Left Mid', 'Left Hind', 'Right Front', 'Right Mid', 'Right Hind']) 
#     plt.autoscale(enable=True, axis = 'y', tight = True)
#     title_underscore = title.replace(" ", "_")
#     title_svg = title_underscore + '.svg'
#     plt.show()
#     if (save_plots == True):
#         plt5a.savefig(os.path.join(fig_rep_dir, title_svg), bbox_inches='tight', dpi=1000)

    

#     #(5b) Classified repositioned x trajectories
#     L1_repo_x_classified = (L1_mm_classified[:,0] - np.nanmean(L1_mm_classified[:,0]))-spacing
#     L2_repo_x_classified = (L2_mm_classified[:,0] - np.nanmean(L2_mm_classified[:,0]))-(2*spacing)
#     L3_repo_x_classified = (L3_mm_classified[:,0] - np.nanmean(L3_mm_classified[:,0]))-(3*spacing)
#     R1_repo_x_classified = (R1_mm_classified[:,0] - np.nanmean(R1_mm_classified[:,0]))+spacing
#     R2_repo_x_classified = (R2_mm_classified[:,0] - np.nanmean(R2_mm_classified[:,0]))+(2*spacing)
#     R3_repo_x_classified = (R3_mm_classified[:,0] - np.nanmean(R3_mm_classified[:,0]))+(3*spacing)

#     # Plot repositioned leg X trajectories together 
#     plt5b = plt.figure(26, figsize = (10, 10))
#     plt.rc('xtick', labelsize=10)
#     plt.rc('ytick', labelsize=10)
#     plt.plot(L1_repo_x_classified, time, linewidth = 0.5)
#     plt.plot(L2_repo_x_classified, time, linewidth = 0.5)
#     plt.plot(L3_repo_x_classified, time, linewidth = 0.5)
#     plt.plot(R1_repo_x_classified, time, linewidth = 0.5)
#     plt.plot(R2_repo_x_classified, time, linewidth = 0.5)
#     plt.plot(R3_repo_x_classified, time, linewidth = 0.5)
#     plt.gca().invert_yaxis()
#     title = 'Classified Repositioned X Trajectories'
#     plt.title(title, fontsize = 20)
#     plt.ylabel('time (s)', fontsize = 10)
#     plt.xlabel('x position (mm)', fontsize = 10)
#     plt.legend(['Left Front', 'Left Mid', 'Left Hind', 'Right Front', 'Right Mid', 'Right Hind']) 
#     plt.autoscale(enable=True, axis = 'y', tight = True)
#     title_underscore = title.replace(" ", "_")
#     title_svg = title_underscore + '.svg'
#     plt.show()
#     if (save_plots == True):
#         plt5b.savefig(os.path.join(fig_rep_dir, title_svg), bbox_inches='tight', dpi=1000)

    
#     #(5c) Classified repositioned x trajectories zoomed 
#     plt5c = plt.figure(27, figsize = (10, 10))
#     plt.rc('xtick', labelsize=10)
#     plt.rc('ytick', labelsize=10)
#     plt.plot(L1_repo_x_classified, time, linewidth = 0.5)
#     plt.plot(L2_repo_x_classified, time, linewidth = 0.5)
#     plt.plot(L3_repo_x_classified, time, linewidth = 0.5)
#     plt.plot(R1_repo_x_classified, time, linewidth = 0.5)
#     plt.plot(R2_repo_x_classified, time, linewidth = 0.5)
#     plt.plot(R3_repo_x_classified, time, linewidth = 0.5)
#     plt.gca().invert_yaxis()
#     title = 'Classified Repositioned X Trajectories'
#     plt.title(title, fontsize = 20)
#     plt.ylabel('time (s)', fontsize = 10)
#     plt.xlabel('x position (mm)', fontsize = 10)
#     plt.legend(['Left Front', 'Left Mid', 'Left Hind', 'Right Front', 'Right Mid', 'Right Hind']) 
#     plt.autoscale(enable=True, axis = 'y', tight = True)
#     axes = plt.gca()
#     axes.set_ylim([12,10])
#     title_underscore = title.replace(" ", "_") +  '_Zoomed'
#     title_svg = title_underscore + '.svg'
#     plt.show()
#     if (save_plots == True):
#         plt5c.savefig(os.path.join(fig_rep_dir, title_svg), bbox_inches='tight', dpi=1000)


    
#     #(6a) Unclassified repositioned y trajectories
    
#     spacing = 3
#     L1_repo_y = (L1_mm[:,1] - np.nanmean(L1_mm[:,1]))-spacing
#     L2_repo_y = (L2_mm[:,1] - np.nanmean(L2_mm[:,1]))-(2*spacing)
#     L3_repo_y = (L3_mm[:,1] - np.nanmean(L3_mm[:,1]))-(3*spacing)
#     R1_repo_y = (R1_mm[:,1] - np.nanmean(R1_mm[:,1]))+spacing
#     R2_repo_y = (R2_mm[:,1] - np.nanmean(R2_mm[:,1]))+(2*spacing)
#     R3_repo_y = (R3_mm[:,1] - np.nanmean(R3_mm[:,1]))+(3*spacing)

#     # Plot repositioned leg y trajectories together 
#     plt6a = plt.figure(28, figsize = (10, 10))
#     plt.rc('xtick', labelsize=10)
#     plt.rc('ytick', labelsize=10)
#     plt.plot(L1_repo_y, time, linewidth = 0.5)
#     plt.plot(L2_repo_y, time, linewidth = 0.5)
#     plt.plot(L3_repo_y, time, linewidth = 0.5)
#     plt.plot(R1_repo_y, time, linewidth = 0.5)
#     plt.plot(R2_repo_y, time, linewidth = 0.5)
#     plt.plot(R3_repo_y, time, linewidth = 0.5)
#     plt.gca().invert_yaxis()
#     title = 'Raw Repositioned Y Trajectories'
#     plt.title(title, fontsize = 20)
#     plt.ylabel('time (s)', fontsize = 10)
#     plt.xlabel('y position (mm)', fontsize = 10)
#     plt.legend(['Left Front', 'Left Mid', 'Left Hind', 'Right Front', 'Right Mid', 'Right Hind']) 
#     plt.autoscale(enable=True, axis = 'y', tight = True)
#     title_underscore = title.replace(" ", "_") 
#     title_svg = title_underscore + '.svg'
#     plt.show()
#     if (save_plots == True):
#         plt6a.savefig(os.path.join(fig_rep_dir, title_svg), bbox_inches='tight', dpi=1000)

#     #(6b) Classified repositioned y trajectories 
    
#     L1_repo_y_classified = (L1_mm_classified[:,1] - np.nanmean(L1_mm_classified[:,1]))-spacing
#     L2_repo_y_classified = (L2_mm_classified[:,1] - np.nanmean(L2_mm_classified[:,1]))-(2*spacing)
#     L3_repo_y_classified = (L3_mm_classified[:,1] - np.nanmean(L3_mm_classified[:,1]))-(3*spacing)
#     R1_repo_y_classified = (R1_mm_classified[:,1] - np.nanmean(R1_mm_classified[:,1]))+spacing
#     R2_repo_y_classified = (R2_mm_classified[:,1] - np.nanmean(R2_mm_classified[:,1]))+(2*spacing)
#     R3_repo_y_classified = (R3_mm_classified[:,1] - np.nanmean(R3_mm_classified[:,1]))+(3*spacing)

#     # Plot repositioned leg y trajectories together 
#     plt6b = plt.figure(29, figsize = (10, 10))
#     plt.rc('xtick', labelsize=10)
#     plt.rc('ytick', labelsize=10)
#     plt.plot(L1_repo_y_classified, time, linewidth = 0.5)
#     plt.plot(L2_repo_y_classified, time, linewidth = 0.5)
#     plt.plot(L3_repo_y_classified, time, linewidth = 0.5)
#     plt.plot(R1_repo_y_classified, time, linewidth = 0.5)
#     plt.plot(R2_repo_y_classified, time, linewidth = 0.5)
#     plt.plot(R3_repo_y_classified, time, linewidth = 0.5)
#     plt.gca().invert_yaxis()
#     title = 'Classified Repositioned Y Trajectories'
#     plt.title(title, fontsize = 20)
#     plt.ylabel('time (s)', fontsize = 10)
#     plt.xlabel('y position (mm)', fontsize = 10)
#     plt.legend(['Left Front', 'Left Mid', 'Left Hind', 'Right Front', 'Right Mid', 'Right Hind']) 
#     plt.autoscale(enable=True, axis = 'y', tight = True)
#     title_underscore = title.replace(" ", "_") 
#     title_svg = title_underscore + '.svg'
#     plt.show()
#     if (save_plots == True):
#         plt6b.savefig(os.path.join(fig_rep_dir, title_svg), bbox_inches='tight', dpi=1000)

#     #(6c) Classified repositioned y trajectories zoomed 
#     plt6c = plt.figure(30, figsize = (10, 10))
#     plt.rc('xtick', labelsize=10)
#     plt.rc('ytick', labelsize=10)
#     plt.plot(L1_repo_y_classified, time, linewidth = 0.5)
#     plt.plot(L2_repo_y_classified, time, linewidth = 0.5)
#     plt.plot(L3_repo_y_classified, time, linewidth = 0.5)
#     plt.plot(R1_repo_y_classified, time, linewidth = 0.5)
#     plt.plot(R2_repo_y_classified, time, linewidth = 0.5)
#     plt.plot(R3_repo_y_classified, time, linewidth = 0.5)
#     plt.gca().invert_yaxis()
#     title = 'Classified Repositioned Y Trajectories'
#     plt.title(title, fontsize = 20)
#     plt.ylabel('time (s)', fontsize = 10)
#     plt.xlabel('y position (mm)', fontsize = 10)
#     plt.legend(['Left Front', 'Left Mid', 'Left Hind', 'Right Front', 'Right Mid', 'Right Hind']) 
#     plt.autoscale(enable=True, axis = 'y', tight = True)
#     axes = plt.gca()
#     axes.set_ylim([12,10])
#     title_underscore = title.replace(" ", "_") +  '_Zoomed'
#     title_svg = title_underscore + '.svg'
#     plt.show()
#     if (save_plots == True):
#         plt6c.savefig(os.path.join(fig_rep_dir, title_svg), bbox_inches='tight', dpi=1000)
