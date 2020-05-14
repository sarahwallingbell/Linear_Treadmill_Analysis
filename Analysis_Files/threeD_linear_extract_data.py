import pandas as pd
import numpy as np

def extract_data(csv_file, fps):
    
    data = pd.read_csv(csv_file)
    
    #print(data)
    headers = list(data)
    
    head = data[headers[18:21]]
    thorax = data[headers[24:27]]
    abdomen = data[headers[30:33]]
    
    l1 = data[headers[36:39]]
    l2 = data[headers[42:45]]
    l3 = data[headers[48:51]]
    
    r1 = data[headers[54:57]]
    r2 = data[headers[60:63]]
    r3 = data[headers[66:69]]
    
    
    # normalize these to the thorax (~center of mass)
    l1_norm = l1 - thorax.values.astype(float)
    l2_norm = l2 - thorax.values.astype(float)
    l3_norm = l3 - thorax.values.astype(float)
    l_x_norm = [l1_norm, l2_norm, l3_norm]
    
    r1_norm = r1 - thorax.values.astype(float)
    r2_norm = r2 - thorax.values.astype(float)
    r3_norm = r3 - thorax.values.astype(float)
    r_x_norm = [r1_norm, r2_norm, r3_norm]


    # isolate the x position only of the legs
    l1_x=l1[l1.columns[0]]
    l2_x=l2[l2.columns[0]]
    l3_x=l3[l3.columns[0]]
    l_x_pos=[l1_x, l2_x, l3_x]
    
    r1_x=r1[r1.columns[0]]
    r2_x=r2[r2.columns[0]]
    r3_x=r3[r3.columns[0]]
    r_x_pos=[r1_x, r2_x, r3_x]
    
    # isolate the y position only of the legs
    l1_y=l1[l1.columns[1]]
    l2_y=l2[l2.columns[1]]
    l3_y=l3[l3.columns[1]]
    l_y_pos=[l1_y, l2_y, l3_y]
    
    r1_y=r1[r1.columns[0]]
    r2_y=r2[r2.columns[0]]
    r3_y=r3[r3.columns[0]]
    r_y_pos=[r1_y, r2_y, r3_y]
    
    # isolate the x position only of the legs
    l1_z=l1[l1.columns[2]]
    l2_z=l2[l2.columns[2]]
    l3_z=l3[l3.columns[2]]
    l_z_pos=[l1_z, l2_z, l3_z]
    
    r1_z=r1[r1.columns[0]]
    r2_z=r2[r2.columns[0]]
    r3_z=r3[r3.columns[0]]
    r_z_pos=[r1_z, r2_z, r3_z]
    
    
    dt = 1/fps
    time = np.arange(0, len(l1)*dt, dt)
    nlegs = 6
    
    return head, thorax, abdomen, l1_norm, l2_norm, l3_norm, l1, l2, l3, l_x_pos, l_y_pos, l_z_pos, r1_norm, r2_norm, r3_norm, r1, r2, r3, r_x_pos, r_y_pos, r_z_pos, time, nlegs