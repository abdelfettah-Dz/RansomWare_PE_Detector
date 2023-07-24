import numpy as np
import pickle as pk
import pprint
import os
import json
import time
##########################################################source cuckoo_venv/bin/activate



###############################################################################
##############################  GLOBAL_VARIABLES  ##############################
###############################################################################
Path="/home/abdelfettah/Documents/PFE/Website/"
#variables names after processing
api_variables= np.load(os.path.join(Path,'vectors/api_data.npy'))
drop_variables= np.load(os.path.join(Path,'vectors/drop_data.npy'))
reg_variables= np.load(os.path.join(Path,'vectors/reg_data.npy'))
files_variables= np.load(os.path.join(Path,'vectors/files_data.npy'))
files_ext_variables= np.load(os.path.join(Path,'vectors/files_ext_data.npy'))
dir_variables= np.load(os.path.join(Path,'vectors/dir_data.npy'))

#Selected Features indexes
general_features= np.genfromtxt(os.path.join(Path,"selectedFeatures/general.csv"), delimiter= ",", dtype= "i")
api_features= np.genfromtxt(os.path.join(Path,"selectedFeatures/api.csv"), delimiter= ",", dtype= "i")
drop_features= np.genfromtxt(os.path.join(Path,"selectedFeatures/Drop.csv"), delimiter= ",", dtype= "i")
reg_features= np.genfromtxt(os.path.join(Path,"selectedFeatures/Reg.csv"), delimiter= ",", dtype= "i")
files_features= np.genfromtxt(os.path.join(Path,"selectedFeatures/files.csv"), delimiter= ",", dtype= "i")
files_ext_features= np.genfromtxt(os.path.join(Path,"selectedFeatures/file_ext.csv"), delimiter= ",", dtype= "i")
dir_features= np.genfromtxt(os.path.join(Path,"selectedFeatures/Dir.csv"), delimiter= ",", dtype= "i")

#Deep Learning Models
api_model= pk.load(open(os.path.join(Path,'models/api_model.pickle'), 'rb'))
file_ext_model= pk.load(open(os.path.join(Path,'models/files_ext_model.pickle'), 'rb'))
file_model= pk.load(open(os.path.join(Path,'models/files_model.pickle'), 'rb'))
dir_model= pk.load(open(os.path.join(Path,'models/Dir_model.pickle'), 'rb'))
drop_model= pk.load(open(os.path.join(Path,'models/DROP_model.pickle'), 'rb'))
reg_model= pk.load(open(os.path.join(Path,'models/Reg_model.pickle'), 'rb'))
general_model= pk.load(open(os.path.join(Path,'models/general_model.pickle'), 'rb'))
final_model= pk.load(open(os.path.join(Path,'models/final_model.pickle'), 'rb'))


##############################################################################
################################  PARSER #####################################
##############################################################################
#API CALLS
def getApi(report):
# Initialize an empty array to store the API invocations
  api_invocations = []

# Extract API invocations from behavior section
  try:
    behavior = report['behavior']
    for process in behavior['processes']:
        for call in process['calls']:
            api_invocations.append(call['api'])
  except KeyError:
    pass

  # construct and return the API invocations Vector
  return np.array([1 if element in api_invocations else 0 for element in api_variables])


 ####################################################################
#DROP
def getDrop(report):
  # Initialize an empty array to store the dropped files
  extensions = []
  # Extract the extensions from the dropped files
  try:
    dropped_files = report['dropped']
    for file_info in dropped_files:
        file_path = file_info['name']
        file_extension = os.path.splitext(file_path)[1][1:]  # Remove the leading dot (.)
        extensions.append(file_extension)
  except KeyError:
    pass
  # Convert the extensions to a NumPy array
  extensions_array = np.array(extensions)

  # construct and return the Drop Vector
  return np.array([1 if element in extensions_array else 0 for element in drop_variables])


###########################################################################
#REG
def getReg(report):
  # Initialize an empty array to store the Registry key operations
  registry_operations = []
  # Extract the Registry key operations from the report
  summary = report['behavior']['summary']
  try:
    registry_operations.extend([('OPENED', key) for key in summary['regkey_opened']])
  except KeyError:
    pass
  try:
    registry_operations.extend([('READ', key) for key in summary['regkey_read']])
  except KeyError:
    pass
  try:
    registry_operations.extend([('WRITTEN', key) for key in summary['regkey_written']])
  except KeyError:
    pass
  try:
    registry_operations.extend([('DELETED', key) for key in summary['regkey_deleted']])
  except KeyError:
    pass
  # Convert the registry_operations to a NumPy array
  registry_operations = np.array(registry_operations)

  # construct and return Registry key operations vector
  return np.array([1 if element in registry_operations.tolist() else 0 for element in reg_variables.tolist()])


################################################################################
#FILES
def getFile(report):
  # Initialize an empty array to store the file operations
  file_operations = []
  # Extract file operations from the report
  summary = report['behavior']['summary']
  try:
    file_operations.extend([('OPENED', key) for key in summary['file_opened']])
  except KeyError:
    pass
  try:
    file_operations.extend([('READ', key) for key in summary['file_read']])
  except KeyError:
    pass
  try:
    file_operations.extend([('WRITTEN', key) for key in summary['file_written']])
  except KeyError:
    pass
  try:
    file_operations.extend([('DELETED', key) for key in summary['file_deleted']])
  except KeyError:
    pass
  # Convert the registry_operations to a NumPy array
  file_operations = np.array(file_operations)

  # construct and return Registry key operations vector
  return np.array([1 if element in file_operations.tolist() else 0 for element in files_variables.tolist()])


##############################################################################
#FILES_EXT
def getFileExt(report):
  # Initialize an empty array to store the file operations
  file_ext_operations = []
  # Extract file operations from the report
  summary = report['behavior']['summary']
  try:
    file_ext_operations.extend([('OPENED', os.path.splitext(key)[1][1:]) for key in summary['file_opened']])
  except KeyError:
    pass
  try:
    file_ext_operations.extend([('READ', os.path.splitext(key)[1][1:]) for key in summary['file_read']])
  except KeyError:
    pass
  try:
    file_ext_operations.extend([('WRITTEN', os.path.splitext(key)[1][1:]) for key in summary['file_written']])
  except KeyError:
    pass
  try:
    file_ext_operations.extend([('DELETED', os.path.splitext(key)[1][1:]) for key in summary['file_deleted']])
  except KeyError:
    pass

  # Convert the registry_operations to a NumPy array
  file_ext_operations = np.array(file_ext_operations)

  # construct and return Registry key operations vector
  return np.array([1 if element in file_ext_operations.tolist() else 0 for element in files_ext_variables.tolist()])

###############################################################################
#DIR
def getDir(report):
  # Initialize an empty array to store the file operations
  dir_operations = []
  # Extract file operations from the report
  summary = report['behavior']['summary']
  try:
    dir_operations.extend([('CREATED', key) for key in summary['directory_created']])
  except KeyError:
    pass
  try:
    dir_operations.extend([('ENUMERATED', key) for key in summary['directory_enumerated']])
  except KeyError:
    pass
  # Convert the registry_operations to a NumPy array
  dir_operations = np.array(dir_operations)

  # construct and return Registry key operations vector
  return np.array([1 if element in dir_operations.tolist() else 0 for element in dir_variables.tolist()])


#############################################################################
################################FINAL_VECTOR#################################
#############################################################################
#CONSTRUCT DATA VECTOR
def getDataVector(reportFile):
  #collect data
  api= getApi(reportFile)
  drop= getDrop(reportFile)
  reg= getReg(reportFile)
  files= getFile(reportFile)
  fileExt= getFileExt(reportFile)
  dir= getDir(reportFile)
  # Concatenate all the arrays into a single array
  data = np.concatenate((api, drop, reg, files, fileExt, dir))
  #return the data vector
  return np.reshape(data, (1, data.shape[0]))


#############################################################################
#############################   PREDICTION   ################################
#############################################################################
#Make a Vector Using the Predictions of the base models
def models_predict(reportFile):
    #construct the input vector
    data= getDataVector(reportFile)
    #predict using the base leaarners and construct the final predictions vector
    finalVector = np.column_stack((general_model.predict(data[:,general_features]),
                       api_model.predict(data[:,api_features]),
                       drop_model.predict(data[:,drop_features]),
                       reg_model.predict(data[:,reg_features]),
                       file_model.predict(data[:,files_features]),
                       file_ext_model.predict(data[:,files_ext_features]),
                       dir_model.predict(data[:,dir_features]),
                       ))
    return finalVector

###############################################################################
###############################################################################
#RETURN FINAL LABEL
def final_predict_label(reportFile):
    data= models_predict(reportFile)
    prediction= final_model.predict(data)
    return "Ransomware" if prediction >= 0.5 else "goodWare"

#RETURN PERCENTAGE
def final_predict_percentage(reportFile):
    data= models_predict(reportFile)
    prediction= final_model.predict(data)
    return prediction

###############################################################################
