import os

def make_result_folders(save_plots, save_plots_path, save_data, save_data_path, fly, session, repeat):
    
    #Check for fly folder in figures and data folders. Make folder if it doesn't exist. 
    if (save_plots == True):
        fly_num_str = 'fly' + str(fly)
        fig_fly_dir = os.path.join(save_plots_path, fly_num_str)
        if not os.path.exists(fig_fly_dir):
            os.mkdir(fig_fly_dir)
            
        #Check for session folders in fly folder
        sesh_num_str = 'session' + str(session)
        fig_sesh_dir = os.path.join(fig_fly_dir, sesh_num_str)
        if not os.path.exists(fig_sesh_dir):
            os.mkdir(fig_sesh_dir)
              
        #Check for repeat folders in session folder
        rep_num_str = 'video' + str(repeat)
        fig_rep_dir = os.path.join(fig_sesh_dir, rep_num_str) #where to save figures 
        if not os.path.exists(fig_rep_dir):
            os.mkdir(fig_rep_dir)
    else:
        fig_rep_dir = "null"
            
    if (save_data == True):
        fly_num_str = 'fly' + str(fly)
        data_fly_dir = os.path.join(save_data_path, fly_num_str)
        if not os.path.exists(data_fly_dir):
            os.mkdir(data_fly_dir) 
    
        #Check for session folders in fly folders
        sesh_num_str = 'session' + str(session)
        data_sesh_dir = os.path.join(data_fly_dir, sesh_num_str)
        if not os.path.exists(data_sesh_dir):
            os.mkdir(data_sesh_dir)
        
        #Check for repeat folders in session folders
        rep_num_str = 'video' + str(repeat)
        data_rep_dir = os.path.join(data_sesh_dir, rep_num_str) #where to save data 
        if not os.path.exists(data_rep_dir):
            os.mkdir(data_rep_dir)
    else:
        data_rep_dir = "null"
        
    return fig_rep_dir, data_rep_dir