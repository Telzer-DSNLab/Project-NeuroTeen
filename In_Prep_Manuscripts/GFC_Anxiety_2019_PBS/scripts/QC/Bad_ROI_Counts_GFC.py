import os
import csv
import pandas as pd
import subprocess
import pyreadstat

path_to_subs='/Volumes/DSNLab/User_Files/PaulSharp/Dissertation/QC_Check'
path_to_data='/Volumes/DSNLab/User_Files/PaulSharp/Dissertation/data/wave1'
path_to_data_w2='/Volumes/DSNLab/User_Files/PaulSharp/Dissertation/data/wave2'
master_csv=[['ROI','count']]
QC_to_Power={1: 1, 2: 2, 3: 3, 4: 4, 5: 5, 6: 6, 7: 7, 8: 8, 9: 9, 10: 10, 11: 11, 12: 12, 13: 13, 14: 15, 15: 17, 16: 18, 17: 19, 18: 21, 19: 22, 20: 23, 21: 24, 22: 25, 23: 27, 24: 28, 25: 29, 26: 30, 27: 31, 28: 32, 29: 33, 30: 34, 31: 35, 32: 36, 33: 37, 34: 38, 35: 39, 36: 40, 37: 47, 38: 49, 39: 50, 40: 53, 41: 54, 42: 76, 43: 78, 44: 81, 45: 82, 46: 83, 47: 84, 48: 85, 49: 97, 50: 98, 51: 99, 52: 100, 53: 109, 54: 116, 55: 117, 56: 119, 57: 121, 58: 123, 59: 124, 60: 125, 61: 126, 62: 127, 63: 128, 64: 129, 65: 132, 66: 136, 67: 137, 68: 138, 69: 139, 70: 141, 71: 142, 72: 143, 73: 150, 74: 151, 75: 153, 76: 154, 77: 161, 78: 165, 79: 172, 80: 174, 81: 178, 82: 179, 83: 180, 84: 181, 85: 182, 86: 183, 87: 184, 88: 185, 89: 191, 90: 192, 91: 193, 92: 203, 93: 205, 94: 211, 95: 243, 96: 244, 97: 245, 98: 246, 99: 247, 100: 248, 101: 249, 102: 250, 103: 251, 104: 253, 105: 254, 106: 255, 107: 256, 108: 258, 109: 259, 110: 261, 111: 262, 112: 263, 113: 264}
roi_counts={}
name_csv='GFC_SelfReport.sav'
os.chdir('/Users/paulsharp/Documents/Dissertation_studies/data')
df_full,meta=pyreadstat.read_sav(name_csv,user_missing=True, apply_value_formats=False)
GFC_Subs=[]
for sub in df_full.NT_ID:
	sub=sub[-3:]
	GFC_Subs.append(sub)

remove_subs_too_little_data=['NT1084',
'NT1062',
'NT2084',
'NT2102',
'NT2077',
'NT2015',
'NT99999999',
'NT2110',
'NT2010',
'NT2058',
'NT2137',
'NT2097']


for sub in range(1,294):
	os.chdir(path_to_subs)
	current_file='QC_{}.csv'.format(sub)
	if os.path.getsize(current_file) > 36:
		x=pd.read_csv(current_file)
		subject_id=x.Subject[0][-3:]
		full_sub_id=x.Subject[0]
		if full_sub_id not in remove_subs_too_little_data:
			if subject_id in GFC_Subs:
				bad_rois=x.ROI.unique()
				print 'OLD BAD ROIS: {}\n'.format(bad_rois)
				bad_rois=[QC_to_Power[x] for x in bad_rois.tolist() if type(x)==int or type(x)==float]
				print 'CONVERTED ROIS: {}\n'.format(bad_rois)
				for roi in bad_rois:
					if roi in roi_counts.keys():
						roi_counts[roi]+=1
					else:
						roi_counts[roi]=1


		#bad_rois.append(0) #first row and column are non-usable headers to-be-deleted

		
		# if subject_id != 'Subject':
		# 	if subject_id[2]=='1':
		# 		os.chdir(path_to_data)
		# 	else:
		# 		os.chdir(path_to_data_w2)
		# 	data=pd.read_csv('GFC_connectome_{}.csv'.format(subject_id), header=None)
		# 	data=data.drop(bad_rois,axis=1)
		# 	data=data.drop(bad_rois,axis=0)
		# 	data.to_csv('GFC_connectome_{}_removedbadROIs.csv'.format(subject_id))


for roi in roi_counts.keys():
	roi_count=roi_counts[roi]
	current_line=[roi,roi_count]
	master_csv.append(current_line)

os.chdir(path_to_subs)
with open('Counts_BAD_ROIs_GFC_SubsOnly_after_removing_subs_too_little_data_BEST.csv', 'a') as f:
	w=csv.writer(f)
	w.writerows(master_csv)