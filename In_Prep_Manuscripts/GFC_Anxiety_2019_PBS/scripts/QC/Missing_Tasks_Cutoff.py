import os
import csv
import pandas as pd
import subprocess
import pyreadstat

path_to_subs='/Volumes/DSNLab/User_Files/PaulSharp/Dissertation/QC_Check'
path_to_data='/Volumes/DSNLab/User_Files/PaulSharp/Dissertation/data/wave1'
path_to_data_w2='/Volumes/DSNLab/User_Files/PaulSharp/Dissertation/data/wave2'
os.chdir(path_to_subs)
missing_data_1='Missing_Task_Data_w1.csv'
df_wave1=pd.read_csv(missing_data_1)
missing_data_2='Missing_Task_Data_w2.csv'
df_wave2=pd.read_csv(missing_data_2)

cutoff=25.0

master_csv=[['Subject', 'Missing_data','Met_cutoff']]

task_data_info={'BOLD_Cups_Parent':5.0,
'BOLD_Cups_Peer':5.0,
'BOLD_Cups_Self':5.0,
'BOLD_Ratings_1':8.0,
'BOLD_Ratings_2':8.0,
'BOLD_Resting_State':8.0,
'BOLD_Shapes_1':6.5,
'BOLD_Shapes_2':6.5}

name_csv='GFC_SelfReport.sav'

os.chdir('/Users/paulsharp/Documents/Dissertation_studies/data')
df_full,meta=pyreadstat.read_sav(name_csv,user_missing=True, apply_value_formats=False)
GFC_Subs=[]
for sub in df_full.NT_ID:
	sub=sub[-3:]
	GFC_Subs.append(sub)

current_total_time=0
for row in range(len(df_wave1)):
	gfc_sub=df_wave1.Subject[row][-3:]
	if gfc_sub in GFC_Subs:
		skip='no'
	else:
		skip='yes'

	if row==0:
		if skip=='no': 
			prev_sub=df_wave1.Subject[row]
			current_total_time+=task_data_info[df_wave1.Task_Missing[row]]
	else:
		if skip=='no':
			current_sub=df_wave1.Subject[row]
			if current_sub==prev_sub:
				current_total_time+=task_data_info[df_wave1.Task_Missing[row]]
			else:
				if current_total_time>24:
					met_cutoff='NO'
				else:
					met_cutoff='YES'
				current_line=[prev_sub,current_total_time,met_cutoff]
				master_csv.append(current_line)			
				prev_sub=df_wave1.Subject[row]
				current_total_time=task_data_info[df_wave1.Task_Missing[row]]

current_total_time=0
for row in range(len(df_wave2)):
	gfc_sub=df_wave2.Subject[row][-3:]
	if gfc_sub in GFC_Subs:
		skip='no'
	else:
		skip='yes'

	if row==0:
		if skip=='no': 
			prev_sub=df_wave2.Subject[row]
			current_total_time+=task_data_info[df_wave2.Task_Missing[row]]
	else:
		if skip=='no':
			current_sub=df_wave2.Subject[row]
			if current_sub==prev_sub:
				current_total_time+=task_data_info[df_wave2.Task_Missing[row]]
			else:
				if current_total_time>24:
					met_cutoff='NO'
				else:
					met_cutoff='YES'
				current_line=[prev_sub,current_total_time,met_cutoff]
				master_csv.append(current_line)			
				prev_sub=df_wave2.Subject[row]
				current_total_time=task_data_info[df_wave2.Task_Missing[row]]

os.chdir(path_to_subs)
with open('Missing_Task_Data_GFCsubs_Only.csv', 'a') as f:
	w=csv.writer(f)
	w.writerows(master_csv)
