# -*- coding: utf-8 -*-
"""
Created on Sat Apr  8 18:26:48 2023

@author: carol
"""

## Create config file for different values
import os
output_configfiles = [] 

# in t'his second round, focus on lower melt factor, 
# thirdsround, focus on soil thicjness/depth
'''
#%% changing base values
simname = 'sphy_config_base15'
simpath = 'C:/SPHY3/sphy_20230218/'
outpath = simpath[9:]
# Path to the input text file - a generic congif file that will be changed
input_file_path = r"C:/SPHY3/sphy_config_base15.cfg"

# Path to the output files
output_configfile_base= "C:/SPHY3/" + simname 

# Values of the parameter to test
values = [1] 
# Loop through the values and create a new output file for each value
for value in values:
    # Open input file for reading
    with open(input_file_path, "r") as file:
        lines = file.readlines()
        
    # create output folder for each simulation run
    output_folder = os.path.splitext(simpath + "output_" + simname)[0]
    os.makedirs(output_folder, exist_ok=True)
    
    # create output configuration file
    output_configfile = "{}.cfg".format(output_configfile_base)
    output_configfiles.append('python sphy.py '+output_configfile[9:])

    # set new folder to be the output file folder and replace line
    outputfolder_line = output_folder[9:] + '/'
    lines[74]= "outputdir          = {}\n".format(outputfolder_line) 
    # sphy_20230218/output_GlacRunoffFrac1/'
    
    # replace parameter
    lines[370] = "GlacF             = 0.65\n" # higher is more to glacier runoff
    lines[364] = "DDFG              = 5\n"
    lines[367] = "DDFDG             = 4\n"
    lines[399] = "DDFS              = 4\n"
    lines[245] = "alphaGw           = 0.9\n" 
    lines[240] = "deltaGw           = 500\n"
    lines[486] = "kx                = 0.8\n" # higher is smoother
    lines[191] = "RootDepthFlat     = 20\n"
    lines[193] = "SubDepthFlat      = 50\n" 

    # Write the updated lines to the output file
    with open(output_configfile, "w") as file:
        file.writelines(lines)

    print("New SPHY configuration file: {}".format(output_configfile))
#
'''
#%% Glacier runoff fraction #################################################

# lets go with 0.6 for now
simname = 'GlacRunoffFrac'
simpath = 'C:/SPHY3/sphy_20230218/'
outpath = simpath[9:]
# Path to the input text file - a generic congif file that will be changed
input_file_path = r"C:/SPHY3/config_file/sphy_config_20230524.cfg"

# Path to the output files
output_configfile_base= "C:/SPHY3/" + simname +"_"

# Values of the parameter to test
values = [0.4, 0.5, 0.6] # 90% goes to glacier runoff if 0.9
counter = 10 # for this secon batch
# Loop through the values and create a new output file for each value
for value in values:
    # Open input file for reading
    with open(input_file_path, "r") as file:
        lines = file.readlines()
        
    # create output folder for each simulation run
    output_folder = os.path.splitext(simpath + "output_" + simname +"_" + str(value).replace(".", "_"))[0]
    os.makedirs(output_folder, exist_ok=True)
    
    # create output configuration file
    output_configfile = "{}{}.cfg".format(output_configfile_base, str(value).replace(".", "_"))
    output_configfiles.append('python sphy.py '+output_configfile[9:])

    # set new folder to be the output file folder and replace line
    outputfolder_line = output_folder[9:] + '/'
    lines[74]= "outputdir          = {}\n".format(outputfolder_line) 
    # sphy_20230218/output_GlacRunoffFrac1/'
    
    # replace parameter
    lines[370] = "GlacF           = {}\n".format(value) 

    # Write the updated lines to the output file
    with open(output_configfile, "w") as file:
        file.writelines(lines)

    print("New SPHY configuratio file: {}".format(output_configfile))

#%% Glacier debris covern #################################################
simname = 'GlacierMeltFactor'
simpath = 'C:/SPHY3/sphy_20230218/'
outpath = simpath[9:]
# Path to the input text file - a generic congif file that will be changed
input_file_path = r"C:/SPHY3/sphy_config_base15.cfg"

# Path to the output files
output_configfile_base= "C:/SPHY3/" + simname +"_"

# Values of the parameter to test
values1 = [4.5,5.5,6.5]
values2 = [4,5,6]
values3 =[6,8,10]
# Loop through the values and create a new output file for each value
for value1, value2, value3 in zip(values1, values2, values3):
    # Open input file for reading
    with open(input_file_path, "r") as file:
        lines = file.readlines()

    # create output folder for each simulation run
    output_folder = os.path.splitext(simpath + "output_" + simname +"_" + str(value1).replace(".", "_"))[0]
    os.makedirs(output_folder, exist_ok=True)
    
    # create output configuration file
    output_configfile = "{}{}.cfg".format(output_configfile_base, str(value1).replace(".", "_"))
    output_configfiles.append('python sphy.py '+output_configfile[9:])

    # set new folder to be the output file folder and replace line
    outputfolder_line = output_folder[9:] + '/'
    lines[74]= "outputdir          = {}\n".format(outputfolder_line) 
    
    # replace parameter
    lines[364] = "DDFG           = {}\n".format(value1) 
    lines[367] = "DDFDG          = {}\n".format(value2)
    lines[399] = "DDFS              = {}\n".format(value3)
    # Write the updated lines to the output file
    with open(output_configfile, "w") as file:
        file.writelines(lines)

    print("New SPHY configuration file: {}".format(output_configfile))

#%% Snow stuff
#%% snow coefficient#################################################
# lets go with 0.6 for now
simname = 'SnowMF'
simpath = 'C:/SPHY3/sphy_20230218/'
outpath = simpath[9:]
# Path to the input text file - a generic congif file that will be changed
input_file_path = r"C:/SPHY3/sphy_config_20230524.cfg"

# Path to the output files
output_configfile_base= "C:/SPHY3/" + simname +"_"

# Values of the parameter to test
values = [2,4,8,12,16] # 

# Loop through the values and create a new output file for each value
for value in values:
    # Open input file for reading
    with open(input_file_path, "r") as file:
        lines = file.readlines()
        
    # create output folder for each simulation run
    output_folder = os.path.splitext(simpath + "output_" + simname +"_" + str(value).replace(".", "_"))[0]
    os.makedirs(output_folder, exist_ok=True)
    
    # create output configuration file
    output_configfile = "{}{}.cfg".format(output_configfile_base, str(value).replace(".", "_"))
    output_configfiles.append('python sphy.py '+output_configfile[9:])

    # set new folder to be the output file folder and replace line
    outputfolder_line = output_folder[9:] + '/'
    lines[74]= "outputdir          = {}\n".format(outputfolder_line) 
    # sphy_20230218/output_GlacRunoffFrac1/'
    
    # replace parameter
    lines[399] = "DDFS              = {}\n".format(value)
    # Write the updated lines to the output file
    
    with open(output_configfile, "w") as file:
        file.writelines(lines)

    print("New SPHY configuratio file: {}".format(output_configfile))
##################################################    
#%% s critical temp #################################################
simname = 'SnowMF'
simpath = 'C:/SPHY3/sphy_20230218/'
outpath = simpath[9:]
# Path to the input text file - a generic congif file that will be changed
input_file_path = r"C:/SPHY3/sphy_config_20230524.cfg"

# Path to the output files
output_configfile_base= "C:/SPHY3/" + simname +"_"

# Values of the parameter to test
values = [-4, -2, 0] # 

# Loop through the values and create a new output file for each value
for value in values:
    # Open input file for reading
    with open(input_file_path, "r") as file:
        lines = file.readlines()
        
    # create output folder for each simulation run
    output_folder = os.path.splitext(simpath + "output_" + simname +"_" + str(value).replace(".", "_"))[0]
    os.makedirs(output_folder, exist_ok=True)
    
    # create output configuration file
    output_configfile = "{}{}.cfg".format(output_configfile_base, str(value).replace(".", "_"))
    output_configfiles.append('python sphy.py '+output_configfile[9:])

    # set new folder to be the output file folder and replace line
    outputfolder_line = output_folder[9:] + '/'
    lines[74]= "outputdir          = {}\n".format(outputfolder_line) 
    # sphy_20230218/output_GlacRunoffFrac1/'
    
    # replace parameter
    lines[394] = "TCrit 	           = {}\n".format(value)
    # Write the updated lines to the output file
    
    with open(output_configfile, "w") as file:
        file.writelines(lines)

    print("New SPHY configuratio file: {}".format(output_configfile))
##################################################    


#%% Routing coefficient
# 0.6 is best
# 
simname = 'RecRoutingCoef'
simpath = 'C:/SPHY3/sphy_20230218/'
outpath = simpath[9:]
# Path to the input text file - a generic congif file that will be changed
input_file_path = r"C:/SPHY3/sphy_config_base15.cfg"

# Path to the output files
output_configfile_base= "C:/SPHY3/" + simname +"_"

# Values of the parameter to test
values1 = [0.7, 0.8, 0.9]

counter = 1
# Loop through the values and create a new output file for each value
for value in values1:
    # Open input file for reading
    with open(input_file_path, "r") as file:
        lines = file.readlines()
        
     # create output folder for each simulation run
    output_folder = os.path.splitext(simpath + "output_" + simname +"_" + str(value).replace(".", "_"))[0]
    os.makedirs(output_folder, exist_ok=True)
     
     # create output configuration file
    output_configfile = "{}{}.cfg".format(output_configfile_base, str(value).replace(".", "_"))
    output_configfiles.append('python sphy.py '+output_configfile[9:])

    # set new folder to be the output file folder and replace line
    outputfolder_line = output_folder[9:] + '/'
    lines[74]= "outputdir          = {}\n".format(outputfolder_line) 
    
    # replace parameter
    lines[486] = "kx          = {}\n".format(value)  

    # Write the updated lines to the output file
    with open(output_configfile, "w") as file:
        file.writelines(lines)

    print("New SPHY configuration file: {}".format(output_configfile))
    
    #%% export the config file lis
    # Output the list of output_configfile paths to a text file
    with open('C:/SPHY3/output_configfiles5.txt', 'w') as file:
        file.write('\n'.join(output_configfiles))
        
    ######################################################################################
#%% Soil depth #################################################
# this is now a map!
# lets go with 0.6 for now
simname = 'RootDepthFlat'
simpath = 'C:/SPHY3/sphy_20230218/'
outpath = simpath[9:]
# Path to the input text file - a generic congif file that will be changed
input_file_path = r"C:/SPHY3/config_file/sphy_config_20230524.cfg"

# Path to the output files
output_configfile_base= "C:/SPHY3/" + simname +"_"

# Values of the parameter to test
values = [5, 10, 25, 50] 
counter = 1 # for this secon batch
# Loop through the values and create a new output file for each value
for value in values:
    # Open input file for reading
    with open(input_file_path, "r") as file:
        lines = file.readlines()
        
    # create output folder for each simulation run
    output_folder = os.path.splitext(simpath + "output_" + simname +"_" + str(value).replace(".", "_"))[0]
    os.makedirs(output_folder, exist_ok=True)
    
    # create output configuration file
    output_configfile = "{}{}.cfg".format(output_configfile_base, str(value).replace(".", "_"))
    output_configfiles.append('python sphy.py '+output_configfile[9:])

    # set new folder to be the output file folder and replace line
    outputfolder_line = output_folder[9:] + '/'
    lines[74]= "outputdir          = {}\n".format(outputfolder_line) 
    # sphy_20230218/output_GlacRunoffFrac1/'
    
    # replace parameter
    lines[191] = "RootDepthFlat           = {}\n".format(value) 
    # Write the updated lines to the output file
    with open(output_configfile, "w") as file:
        file.writelines(lines)

    print("New SPHY configuratio file: {}".format(output_configfile))
    
    
    #%% soil depth subzone
    # this is now a map
# lets go with 0.6 for now
simname = 'SubDepthFlat'
simpath = 'C:/SPHY3/sphy_20230218/'
outpath = simpath[9:]
# Path to the input text file - a generic congif file that will be changed
input_file_path = r"C:/SPHY3/config_file/sphy_config_20230524.cfg"

# Path to the output files
output_configfile_base= "C:/SPHY3/" + simname +"_"

# Values of the parameter to test
values = [30, 70, 100, 150,  300] # 90% goes to glacier runoff if 0.9
counter = 1 # for this secon batch
# Loop through the values and create a new output file for each value
for value in values:
    # Open input file for reading
    with open(input_file_path, "r") as file:
        lines = file.readlines()
        
    # create output folder for each simulation run
    output_folder = os.path.splitext(simpath + "output_" + simname +"_" + str(value).replace(".", "_"))[0]
    os.makedirs(output_folder, exist_ok=True)
    
    # create output configuration file
    output_configfile = "{}{}.cfg".format(output_configfile_base, str(value).replace(".", "_"))
    output_configfiles.append('python sphy.py '+output_configfile[9:])

    # set new folder to be the output file folder and replace line
    outputfolder_line = output_folder[9:] + '/'
    lines[74]= "outputdir          = {}\n".format(outputfolder_line) 
    # sphy_20230218/output_GlacRunoffFrac1/'
    
    # replace parameter
    lines[193] = "SubDepthFlat           = {}\n".format(value) 
    # Write the updated lines to the output file
    with open(output_configfile, "w") as file:
        file.writelines(lines)

    print("New SPHY configuratio file: {}".format(output_configfile))
    
#%% Infil parameter - Infiltration excess
simname = 'InfillExcess'
simpath = 'C:/SPHY3/sphy_20230218/'
outpath = simpath[9:]
# Path to the input text file - a generic congif file that will be changed
input_file_path = r"C:/SPHY3/config_file/sphy_config_20230524.cfg"

# Path to the output files
output_configfile_base= "C:/SPHY3/" + simname +"_"

# Values of the parameter to test
values = [0.1, 0.25, 0.5, 0.75] # 
counter = 1 # for this secon batch
# Loop through the values and create a new output file for each value
for value in values:
    # Open input file for reading
    with open(input_file_path, "r") as file:
        lines = file.readlines()
        
    # create output folder for each simulation run
    output_folder = os.path.splitext(simpath + "output_" + simname +"_" + str(value).replace(".", "_"))[0]
    os.makedirs(output_folder, exist_ok=True)
    
    # create output configuration file
    output_configfile = "{}{}.cfg".format(output_configfile_base, str(value).replace(".", "_"))
    output_configfiles.append('python sphy.py '+output_configfile[9:])

    # set new folder to be the output file folder and replace line
    outputfolder_line = output_folder[9:] + '/'
    lines[74]= "outputdir          = {}\n".format(outputfolder_line) 
    # sphy_20230218/output_GlacRunoffFrac1/'
    
    # replace parameter
    lines[214] = "Alpha           = {}\n".format(value) 
    # Write the updated lines to the output file
    with open(output_configfile, "w") as file:
        file.writelines(lines)

    print("New SPHY configuratio file: {}".format(output_configfile))
        
#%% Infil parameter - Labda infiltration capacity
simname = 'LabdaInfil'
simpath = 'C:/SPHY3/sphy_20230218/'
outpath = simpath[9:]
# Path to the input text file - a generic congif file that will be changed
input_file_path = r"C:/SPHY3/config_file/sphy_config_20230524.cfg"

# Path to the output files
output_configfile_base= "C:/SPHY3/" + simname +"_"

# Values of the parameter to test
values = [0.1, 0.25, 0.5, 0.75] # 
counter = 1 # for this secon batch
# Loop through the values and create a new output file for each value
for value in values:
    # Open input file for reading
    with open(input_file_path, "r") as file:
        lines = file.readlines()
        
    # create output folder for each simulation run
    output_folder = os.path.splitext(simpath + "output_" + simname +"_" + str(value).replace(".", "_"))[0]
    os.makedirs(output_folder, exist_ok=True)
    
    # create output configuration file
    output_configfile = "{}{}.cfg".format(output_configfile_base, str(value).replace(".", "_"))
    output_configfiles.append('python sphy.py '+output_configfile[9:])

    # set new folder to be the output file folder and replace line
    outputfolder_line = output_folder[9:] + '/'
    lines[74]= "outputdir          = {}\n".format(outputfolder_line) 
    # sphy_20230218/output_GlacRunoffFrac1/'
    
    # replace parameter
    lines[218] = "Labda_infil           = {}\n".format(value) 
    # Write the updated lines to the output file
    with open(output_configfile, "w") as file:
        file.writelines(lines)

    print("New SPHY configuratio file: {}".format(output_configfile))
        
#%% Infil parameter - Leffectuve saturated hydraulic condiuctivity
simname = 'Keff'
simpath = 'C:/SPHY3/sphy_20230218/'
outpath = simpath[9:]
# Path to the input text file - a generic congif file that will be changed
input_file_path = r"C:/SPHY3/config_file/sphy_config_20230524.cfg"

# Path to the output files
output_configfile_base= "C:/SPHY3/" + simname +"_"

# Values of the parameter to test
values = [0.1, 0.25, 0.5, 0.75] # 
counter = 1 # for this secon batch
# Loop through the values and create a new output file for each value
for value in values:
    # Open input file for reading
    with open(input_file_path, "r") as file:
        lines = file.readlines()
        
    # create output folder for each simulation run
    output_folder = os.path.splitext(simpath + "output_" + simname +"_" + str(value).replace(".", "_"))[0]
    os.makedirs(output_folder, exist_ok=True)
    
    # create output configuration file
    output_configfile = "{}{}.cfg".format(output_configfile_base, str(value).replace(".", "_"))
    output_configfiles.append('python sphy.py '+output_configfile[9:])

    # set new folder to be the output file folder and replace line
    outputfolder_line = output_folder[9:] + '/'
    lines[74]= "outputdir          = {}\n".format(outputfolder_line) 
    # sphy_20230218/output_GlacRunoffFrac1/'
    
    # replace parameter
    lines[220] = "K_eff          = {}\n".format(value) 
    # Write the updated lines to the output file
    with open(output_configfile, "w") as file:
        file.writelines(lines)

    print("New SPHY configuratio file: {}".format(output_configfile))
            
#%% GW parameter - GW depth
simname = 'GWdepth'
simpath = 'C:/SPHY3/sphy_20230218/'
outpath = simpath[9:]
# Path to the input text file - a generic congif file that will be changed
input_file_path = r"C:/SPHY3/config_file/sphy_config_20230524.cfg"

# Path to the output files
output_configfile_base= "C:/SPHY3/" + simname +"_"

# Values of the parameter to test
values = [1000, 2000, 3000, 4000, 5000] # 
counter = 1 # for this secon batch
# Loop through the values and create a new output file for each value
for value in values:
    # Open input file for reading
    with open(input_file_path, "r") as file:
        lines = file.readlines()
        
    # create output folder for each simulation run
    output_folder = os.path.splitext(simpath + "output_" + simname +"_" + str(value).replace(".", "_"))[0]
    os.makedirs(output_folder, exist_ok=True)
    
    # create output configuration file
    output_configfile = "{}{}.cfg".format(output_configfile_base, str(value).replace(".", "_"))
    output_configfiles.append('python sphy.py '+output_configfile[9:])

    # set new folder to be the output file folder and replace line
    outputfolder_line = output_folder[9:] + '/'
    lines[74]= "outputdir          = {}\n".format(outputfolder_line) 
    # sphy_20230218/output_GlacRunoffFrac1/'
    
    # replace parameter
    lines[235] = "GwDepth         = {}\n".format(value) 
    # Write the updated lines to the output file
    with open(output_configfile, "w") as file:
        file.writelines(lines)

    print("New SPHY configuratio file: {}".format(output_configfile))
 
#%% GW parameter - GW saturated content
simname = 'GWsat'
simpath = 'C:/SPHY3/sphy_20230218/'
outpath = simpath[9:]
# Path to the input text file - a generic congif file that will be changed
input_file_path = r"C:/SPHY3/config_file/sphy_config_20230524.cfg"

# Path to the output files
output_configfile_base= "C:/SPHY3/" + simname +"_"

# Values of the parameter to test
values = [100, 250, 500] # 
counter = 1 # for this secon batch
# Loop through the values and create a new output file for each value
for value in values:
    # Open input file for reading
    with open(input_file_path, "r") as file:
        lines = file.readlines()
        
    # create output folder for each simulation run
    output_folder = os.path.splitext(simpath + "output_" + simname +"_" + str(value).replace(".", "_"))[0]
    os.makedirs(output_folder, exist_ok=True)
    
    # create output configuration file
    output_configfile = "{}{}.cfg".format(output_configfile_base, str(value).replace(".", "_"))
    output_configfiles.append('python sphy.py '+output_configfile[9:])

    # set new folder to be the output file folder and replace line
    outputfolder_line = output_folder[9:] + '/'
    lines[74]= "outputdir          = {}\n".format(outputfolder_line) 
    # sphy_20230218/output_GlacRunoffFrac1/'
    
    # replace parameter
    lines[238] = "GwSat         = {}\n".format(value) 
    # Write the updated lines to the output file
    with open(output_configfile, "w") as file:
        file.writelines(lines)

    print("New SPHY configuratio file: {}".format(output_configfile))
                    
        
#%% Groundwater Delay % this was 149 in walters run
simname = 'Gwdelta'
simpath = 'C:/SPHY3/sphy_20230218/'
outpath = simpath[9:]
# Path to the input text file - a generic congif file that will be changed
input_file_path = r"C:/SPHY3/sphy_config_base2.cfg"

# Path to the output files
output_configfile_base= "C:/SPHY3/" + simname +"_"

# Values of the parameter to test
values1 = [1, 50, 100, 150, 200]

counter = 10
# Loop through the values and create a new output file for each value
for value in values1:
    # Open input file for reading
    with open(input_file_path, "r") as file:
        lines = file.readlines()
        
    # create output folder for each simulation run
    output_folder = os.path.splitext(simpath + "output_" + simname +"_" + str(counter))[0]
    os.makedirs(output_folder, exist_ok=True)
    
    # create output configuration file
    output_configfile = "{}{}.cfg".format(output_configfile_base, counter)
    output_configfiles.append('python sphy.py '+output_configfile[9:])

    # set new folder to be the output file folder and replace line
    outputfolder_line = output_folder[9:] + '/'
    lines[74]= "outputdir          = {}\n".format(outputfolder_line) 
    
    # replace parameter
    lines[240] = "deltaGw          = {}\n".format(value)  
    # change end date
    lines[85]= 'endyear          = 2010\n'
    counter = counter + 1
    # Write the updated lines to the output file
    with open(output_configfile, "w") as file:
        file.writelines(lines)

    print("New SPHY configuration file: {}".format(output_configfile))

#%% Bseflowdays
simname = 'BaseflowDay'
simpath = 'C:/SPHY3/sphy_20230218/'
outpath = simpath[9:]
# Path to the input text file - a generic congif file that will be changed
input_file_path = r"C:/SPHY3/sphy_config_base2.cfg"

# Path to the output files
output_configfile_base= "C:/SPHY3/" + simname +"_"

# Values of the parameter to test
values1 = [0.1,0.5,0.9]

counter = 10
# Loop through the values and create a new output file for each value
for value in values1:
    # Open input file for reading
    with open(input_file_path, "r") as file:
        lines = file.readlines()
        
    # create output folder for each simulation run
    output_folder = os.path.splitext(simpath + "output_" + simname +"_" + str(value))[0]
    os.makedirs(output_folder, exist_ok=True)
    
    # create output configuration file
    output_configfile = "{}{}.cfg".format(output_configfile_base, counter)
    output_configfiles.append('python sphy.py '+ output_configfile[9:])
    
    # set new folder to be the output file folder and replace line
    outputfolder_line = output_folder[9:] + '/'
    lines[74]= "outputdir          = {}\n".format(outputfolder_line) 
    
    # replace parameter
    lines[245] = "alphaGw           = {}\n".format(value)  
    # change end date
    lines[85]= 'endyear          = 2010\n'
    counter = counter + 1
    # Write the updated lines to the output file
    with open(output_configfile, "w") as file:
        file.writelines(lines)

    print("New SPHY configuration file: {}".format(output_configfile))

#%% export the config file lis
# Output the list of output_configfile paths to a text file
with open('C:/SPHY3/output_configfiles5.txt', 'w') as file:
    file.write('\n'.join(output_configfiles))
    
#%% redo for other paremetrs I would want to change