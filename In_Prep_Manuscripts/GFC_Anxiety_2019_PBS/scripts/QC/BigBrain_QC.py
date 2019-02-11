import os
from csv import reader
import pandas as pd
import subprocess
import pyreadstat

path_to_subs='/Volumes/DSNLab/User_Files/PaulSharp/Dissertation/QC_Check'
path_to_data='/Volumes/DSNLab/User_Files/PaulSharp/Dissertation/data/wave1'
path_to_data_w2='/Volumes/DSNLab/User_Files/PaulSharp/Dissertation/data/wave2'
path_to_data_final='/Volumes/DSNLab/User_Files/PaulSharp/Dissertation/data/final_dataset'
roi_counts={}
QC_to_Power={1: 1, 2: 2, 3: 3, 4: 4, 5: 5, 6: 6, 7: 7, 8: 8, 9: 9, 10: 10, 11: 11, 12: 12, 13: 13, 14: 15, 15: 17, 16: 18, 17: 19, 18: 21, 19: 22, 20: 23, 21: 24, 22: 25, 23: 27, 24: 28, 25: 29, 26: 30, 27: 31, 28: 32, 29: 33, 30: 34, 31: 35, 32: 36, 33: 37, 34: 38, 35: 39, 36: 40, 37: 47, 38: 49, 39: 50, 40: 53, 41: 54, 42: 76, 43: 78, 44: 81, 45: 82, 46: 83, 47: 84, 48: 85, 49: 97, 50: 98, 51: 99, 52: 100, 53: 109, 54: 116, 55: 117, 56: 119, 57: 121, 58: 123, 59: 124, 60: 125, 61: 126, 62: 127, 63: 128, 64: 129, 65: 132, 66: 136, 67: 137, 68: 138, 69: 139, 70: 141, 71: 142, 72: 143, 73: 150, 74: 151, 75: 153, 76: 154, 77: 161, 78: 165, 79: 172, 80: 174, 81: 178, 82: 179, 83: 180, 84: 181, 85: 182, 86: 183, 87: 184, 88: 185, 89: 191, 90: 192, 91: 193, 92: 203, 93: 205, 94: 211, 95: 243, 96: 244, 97: 245, 98: 246, 99: 247, 100: 248, 101: 249, 102: 250, 103: 251, 104: 253, 105: 254, 106: 255, 107: 256, 108: 258, 109: 259, 110: 261, 111: 262, 112: 263, 113: 264}
power_bb={}

batch_number_to_subj_id_conversion={'batch273': 'NT2206', 'batch272': 'NT2205', 'batch271': 'NT2204', 'batch270': 'NT2203', 'batch277': 'NT2210', 'batch276': 'NT2209', 'batch275': 'NT2208', 'batch274': 'NT2207', 'batch6': 'NT1007', 'batch7': 'NT1008', 'batch279': 'NT2212', 'batch5': 'NT1006', 'batch2': 'NT1003', 'batch3': 'NT1004', 'batch1': 'NT1001', 'batch121': 'NT1158', 'batch278': 'NT2211', 'batch8': 'NT1009', 'batch9': 'NT1010', 'batch87': 'NT1118', 'batch108': 'NT1143', 'batch85': 'NT1116', 'batch84': 'NT1115', 'batch83': 'NT1114', 'batch82': 'NT1112', 'batch81': 'NT1111', 'batch80': 'NT1110', 'batch101': 'NT1136', 'batch100': 'NT1135', 'batch103': 'NT1138', 'batch102': 'NT1137', 'batch105': 'NT1140', 'batch4': 'NT1005', 'batch89': 'NT1122', 'batch88': 'NT1119', 'batch246': 'NT2161', 'batch247': 'NT2162', 'batch244': 'NT2158', 'batch245': 'NT2160', 'batch242': 'NT2156', 'batch243': 'NT2157', 'batch240': 'NT2154', 'batch241': 'NT2155', 'batch253': 'NT2182', 'batch248': 'NT2163', 'batch249': 'NT2172', 'batch18': 'NT1023', 'batch19': 'NT1024', 'batch42': 'NT1060', 'batch14': 'NT1017', 'batch15': 'NT1018', 'batch16': 'NT1019', 'batch17': 'NT1022', 'batch10': 'NT1011', 'batch11': 'NT1012', 'batch12': 'NT1013', 'batch13': 'NT1015', 'batch94': 'NT1128', 'batch95': 'NT1130', 'batch96': 'NT1131', 'batch97': 'NT1132', 'batch178': 'NT2058', 'batch179': 'NT2059', 'batch63': 'NT1087', 'batch93': 'NT1126', 'batch174': 'NT2047', 'batch175': 'NT2054', 'batch176': 'NT2055', 'batch177': 'NT2056', 'batch98': 'NT1133', 'batch171': 'NT2043', 'batch172': 'NT2044', 'batch173': 'NT2045', 'batch29': 'NT1040', 'batch28': 'NT1038', 'batch21': 'NT1026', 'batch20': 'NT1025', 'batch23': 'NT1028', 'batch22': 'NT1027', 'batch25': 'NT1030', 'batch24': 'NT1029', 'batch27': 'NT1037', 'batch26': 'NT1032', 'batch169': 'NT2038', 'batch168': 'NT2037', 'batch167': 'NT2032', 'batch166': 'NT2030', 'batch165': 'NT2029', 'batch164': 'NT2028', 'batch163': 'NT2027', 'batch162': 'NT2023', 'batch161': 'NT2022', 'batch160': 'NT2019', 'batch140': 'NT1186', 'batch129': 'NT1170', 'batch90': 'NT1123', 'batch36': 'NT1054', 'batch37': 'NT1055', 'batch34': 'NT1047', 'batch35': 'NT1048', 'batch32': 'NT1045', 'batch33': 'NT1046', 'batch30': 'NT1043', 'batch31': 'NT1044', 'batch92': 'NT1125', 'batch38': 'NT1056', 'batch39': 'NT1057', 'batch170': 'NT2040', 'batch78': 'NT1107', 'batch99': 'NT1134', 'batch259': 'NT2189', 'batch153': 'NT2010', 'batch150': 'NT2007', 'batch151': 'NT2008', 'batch156': 'NT2013', 'batch157': 'NT2015', 'batch154': 'NT2011', 'batch155': 'NT2012', 'batch251': 'NT2175', 'batch250': 'NT2173', 'batch158': 'NT2017', 'batch159': 'NT2018', 'batch255': 'NT2185', 'batch254': 'NT2184', 'batch257': 'NT2187', 'batch256': 'NT2186', 'batch130': 'NT1172', 'batch131': 'NT1173', 'batch132': 'NT1174', 'batch133': 'NT1175', 'batch134': 'NT1176', 'batch135': 'NT1178', 'batch136': 'NT1179', 'batch137': 'NT1182', 'batch138': 'NT1184', 'batch139': 'NT1185', 'batch43': 'NT1061', 'batch72': 'NT1098', 'batch41': 'NT1059', 'batch40': 'NT1058', 'batch47': 'NT1065', 'batch46': 'NT1064', 'batch45': 'NT1063', 'batch44': 'NT1062', 'batch49': 'NT1070', 'batch48': 'NT1068', 'batch109': 'NT1144', 'batch188': 'NT2074', 'batch86': 'NT1117', 'batch145': 'NT1191', 'batch144': 'NT1190', 'batch147': 'NT9999', 'batch146': 'NT1192', 'batch141': 'NT1187', 'batch229': 'NT2136', 'batch143': 'NT1189', 'batch79': 'NT1108', 'batch224': 'NT2128', 'batch228': 'NT2135', 'batch226': 'NT2133', 'batch227': 'NT2134', 'batch220': 'NT2122', 'batch221': 'NT2124', 'batch222': 'NT2125', 'batch223': 'NT2126', 'batch123': 'NT1161', 'batch122': 'NT1160', 'batch288': 'NT2221', 'batch120': 'NT1157', 'batch127': 'NT1167', 'batch126': 'NT1166', 'batch125': 'NT1163', 'batch124': 'NT1162', 'batch282': 'NT2215', 'batch283': 'NT2216', 'batch280': 'NT2213', 'batch128': 'NT1169', 'batch286': 'NT2219', 'batch287': 'NT2220', 'batch284': 'NT2217', 'batch285': 'NT2218', 'batch50': 'NT1071', 'batch51': 'NT1072', 'batch52': 'NT1074', 'batch53': 'NT1075', 'batch54': 'NT1077', 'batch55': 'NT1078', 'batch56': 'NT1079', 'batch57': 'NT1080', 'batch58': 'NT1081', 'batch59': 'NT1083', 'batch119': 'NT1156', 'batch118': 'NT1155', 'batch149': 'NT2006', 'batch281': 'NT2214', 'batch104': 'NT1139', 'batch148': 'NT2005', 'batch91': 'NT1124', 'batch107': 'NT1142', 'batch239': 'NT2151', 'batch238': 'NT2147', 'batch237': 'NT2145', 'batch236': 'NT2144', 'batch235': 'NT2143', 'batch234': 'NT2142', 'batch233': 'NT2141', 'batch232': 'NT2140', 'batch231': 'NT2139', 'batch230': 'NT2137', 'batch116': 'NT1153', 'batch117': 'NT1154', 'batch114': 'NT1150', 'batch115': 'NT1151', 'batch112': 'NT1148', 'batch113': 'NT1149', 'batch110': 'NT1145', 'batch111': 'NT1147', 'batch106': 'NT1141', 'batch199': 'NT2088', 'batch291': 'NT2228', 'batch290': 'NT2226', 'batch293': 'NT99999999', 'batch292': 'NT2999', 'batch196': 'NT2085', 'batch289': 'NT2222', 'batch69': 'NT1095', 'batch68': 'NT1093', 'batch198': 'NT2087', 'batch64': 'NT1088', 'batch65': 'NT1089', 'batch197': 'NT2086', 'batch194': 'NT2081', 'batch195': 'NT2084', 'batch61': 'NT1085', 'batch60': 'NT1084', 'batch190': 'NT2077', 'batch62': 'NT1086', 'batch152': 'NT2009', 'batch66': 'NT1090', 'batch258': 'NT2188', 'batch192': 'NT2079', 'batch193': 'NT2080', 'batch202': 'NT2093', 'batch203': 'NT2095', 'batch200': 'NT2090', 'batch201': 'NT2092', 'batch206': 'NT2098', 'batch207': 'NT2099', 'batch204': 'NT2096', 'batch205': 'NT2097', 'batch208': 'NT2102', 'batch209': 'NT2103', 'batch225': 'NT2131', 'batch260': 'NT2190', 'batch261': 'NT2191', 'batch262': 'NT2193', 'batch263': 'NT2194', 'batch264': 'NT2196', 'batch265': 'NT2197', 'batch266': 'NT2198', 'batch267': 'NT2199', 'batch268': 'NT2200', 'batch269': 'NT2201', 'batch181': 'NT2061', 'batch180': 'NT2060', 'batch183': 'NT2063', 'batch182': 'NT2062', 'batch185': 'NT2068', 'batch184': 'NT2064', 'batch187': 'NT2072', 'batch186': 'NT2071', 'batch189': 'NT2075', 'batch73': 'NT1099', 'batch70': 'NT1096', 'batch71': 'NT1097', 'batch76': 'NT1104', 'batch77': 'NT1106', 'batch74': 'NT1102', 'batch75': 'NT1103', 'batch252': 'NT2176', 'batch142': 'NT1188', 'batch191': 'NT2078', 'batch215': 'NT2114', 'batch214': 'NT2111', 'batch217': 'NT2116', 'batch216': 'NT2115', 'batch211': 'NT2106', 'batch210': 'NT2104', 'batch213': 'NT2110', 'batch212': 'NT2107', 'batch219': 'NT2119', 'batch218': 'NT2118', 'batch67': 'NT1092'}

across_subs_bad_ROIs=[]

remove_subs_too_little_data=[
'NT1062',
'NT2062',
'NT1084',
'NT2084',
'NT1102',
'NT2102',
'NT1077',
'NT2077',
'NT1015',
'NT2015',
'NT1110',
'NT2110',
'NT1010',
'NT2010',
'NT1058',
'NT2058',
'NT1137',
'NT2137',
'NT1097',
'NT2097',
'NT99999999',
'NT9999'
]


name_csv='GFC_SelfReport.sav'
os.chdir('/Users/paulsharp/Documents/Dissertation_studies/data')
df_full,meta=pyreadstat.read_sav(name_csv,user_missing=True, apply_value_formats=False)
GFC_Subs=[]
for sub in df_full.NT_ID:
	sub=sub[-3:]
	GFC_Subs.append(sub)




#create conversion dictionary called power_bb from Power 264 to Big Brain 300 parcellation 
os.chdir(path_to_subs)
with open('convert_Power_to_bigbrain.csv', 'r') as f:
	r=reader(f)
	lines=[l for l in r]

for row in lines:
	if row[0]=='New':
		print 'New'
	elif row[1]=="Removed":
		power_bb[int(row[0])]=-9
	else:
		power_bb[int(row[0])]=int(row[1])

with open('Counts_BAD_ROIs_GFC_SubsOnly_after_removing_subs_too_little_data_BEST.csv', 'r') as f:
	r=reader(f)
	lines=[l for l in r]

for row in lines:
	if row[0]=='ROI':
		skip='first_row' #unused variable just to mark skipping the first row
	else:
		if int(row[1])>13:
			across_subs_bad_ROIs.append(power_bb[int(row[0])])
# across_subs_bad_ROIs.append(0) #first column always unnecessary


#find bad ROIs per subject
for sub in range(1,294):
	os.chdir(path_to_subs)
	full_NT_sub_id=batch_number_to_subj_id_conversion['batch{}'.format(sub)]
	if full_NT_sub_id not in remove_subs_too_little_data: #do not include subs with too little data
		if full_NT_sub_id[-3:] in GFC_Subs: #include ONLY subs with full data at wave 1 & wave 2

			current_file='QC_{}.csv'.format(sub)
			x=pd.read_csv(current_file)
			if len(x.Subject) > 0:
				subject_id=x.Subject[0]
				bad_rois=x.ROI.unique()
				bad_rois=[power_bb[QC_to_Power[int(x)]] for x in bad_rois.tolist() if type(x)==int and power_bb[QC_to_Power[int(x)]] not in across_subs_bad_ROIs]
				print 'Subject {} has bad_rois: {}'.format(full_NT_sub_id,bad_rois)
			else:
				bad_rois=[]
				print 'Subject {} has bad_rois: {}'.format(full_NT_sub_id,bad_rois)

			bad_rois=[x for x in bad_rois if x>0]

			if full_NT_sub_id[2]=='1':
				os.chdir(path_to_data)
			else:
				os.chdir(path_to_data_w2)
			data=pd.read_csv('GFC_connectome_{}.csv'.format(full_NT_sub_id), header=None)
			data=data.drop(data.columns[0],axis=1) #drop unnecesary first column
			print data.columns
			for roi in bad_rois:
				data.loc[[roi]]=''
				data[roi]=''
				#print data[roi]

			data=data.drop(across_subs_bad_ROIs,axis=0)
			# temp_drop=across_subs_bad_ROIs
			# print temp_drop
			# temp_drop=temp_drop.remove(0)
			data=data.drop(across_subs_bad_ROIs,axis=1)
			os.chdir(path_to_data_final)
			data.to_csv('GFC_connectome_{}_QCapplied.csv'.format(full_NT_sub_id), header=False, index=False)


