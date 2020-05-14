# Append Analyzed
# If append_analyzed in main == True, appends "_analyzed" to the end of the file name so that it's not re-analyzed if this program is run again
# Parameters: three file names to be appended
# Returns: three file names with "_append"
import os

def append_analyzed(file):       
#Append 'analyzed' to csv files (e.g. 'original_file_name_analyzed.csv')
    
    filename, file_extension = os.path.splitext(file)
    new_file = filename + '_analyzed' + file_extension
    os.rename(file, new_file)
    
    return file


