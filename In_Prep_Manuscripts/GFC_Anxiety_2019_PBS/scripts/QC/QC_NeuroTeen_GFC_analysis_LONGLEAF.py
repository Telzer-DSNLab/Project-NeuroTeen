#assemble functional connectomes for GFC analysis 
#Written by Paul Sharp 12/19/2018

#run for each wave by changing wave variable 

import os
import csv
import nipype.interfaces.fsl as fsl
import datetime
import sys

'''Set up variables and paths'''

prefix='NT' #prefix defining subjects
prefix_atlas='Power' #prefix defining atlas ROIs
path_to_subs='/pine/scr/p/s/psharp89/GFC_analysis/all_GFC_files/batch{}'.format(sys.argv[1])
subjects=[x for x in os.listdir(path_to_subs) if x.startswith(prefix)]
output_path='/pine/scr/p/s/psharp89/GFC_analysis/QC/batch{}'.format(sys.argv[1])
path_to_rois='/pine/scr/p/s/psharp89/GFC_analysis/power_atlas_ROIs'
rois=['Power_ROI_sphere_binarized_0.nii.gz', 'Power_ROI_sphere_binarized_1.nii.gz', 
'Power_ROI_sphere_binarized_2.nii.gz', 'Power_ROI_sphere_binarized_3.nii.gz', 'Power_ROI_sphere_binarized_4.nii.gz', 
'Power_ROI_sphere_binarized_5.nii.gz', 'Power_ROI_sphere_binarized_6.nii.gz', 'Power_ROI_sphere_binarized_7.nii.gz', 
'Power_ROI_sphere_binarized_8.nii.gz', 'Power_ROI_sphere_binarized_9.nii.gz', 'Power_ROI_sphere_binarized_10.nii.gz', 
'Power_ROI_sphere_binarized_11.nii.gz', 'Power_ROI_sphere_binarized_12.nii.gz', 'Power_ROI_sphere_binarized_14.nii.gz', 
'Power_ROI_sphere_binarized_16.nii.gz', 'Power_ROI_sphere_binarized_17.nii.gz', 'Power_ROI_sphere_binarized_18.nii.gz', 'Power_ROI_sphere_binarized_20.nii.gz', 
'Power_ROI_sphere_binarized_21.nii.gz', 'Power_ROI_sphere_binarized_22.nii.gz', 'Power_ROI_sphere_binarized_23.nii.gz', 'Power_ROI_sphere_binarized_24.nii.gz', 
'Power_ROI_sphere_binarized_26.nii.gz', 'Power_ROI_sphere_binarized_27.nii.gz', 'Power_ROI_sphere_binarized_28.nii.gz', 'Power_ROI_sphere_binarized_29.nii.gz', 'Power_ROI_sphere_binarized_30.nii.gz', 'Power_ROI_sphere_binarized_31.nii.gz', 'Power_ROI_sphere_binarized_32.nii.gz', 'Power_ROI_sphere_binarized_33.nii.gz', 'Power_ROI_sphere_binarized_34.nii.gz', 'Power_ROI_sphere_binarized_35.nii.gz', 'Power_ROI_sphere_binarized_36.nii.gz', 'Power_ROI_sphere_binarized_37.nii.gz', 'Power_ROI_sphere_binarized_38.nii.gz', 'Power_ROI_sphere_binarized_39.nii.gz', 'Power_ROI_sphere_binarized_46.nii.gz', 'Power_ROI_sphere_binarized_48.nii.gz', 'Power_ROI_sphere_binarized_49.nii.gz', 'Power_ROI_sphere_binarized_52.nii.gz', 'Power_ROI_sphere_binarized_53.nii.gz', 'Power_ROI_sphere_binarized_75.nii.gz', 'Power_ROI_sphere_binarized_77.nii.gz', 'Power_ROI_sphere_binarized_80.nii.gz', 'Power_ROI_sphere_binarized_81.nii.gz', 'Power_ROI_sphere_binarized_82.nii.gz', 'Power_ROI_sphere_binarized_83.nii.gz', 'Power_ROI_sphere_binarized_84.nii.gz', 'Power_ROI_sphere_binarized_96.nii.gz', 'Power_ROI_sphere_binarized_97.nii.gz', 'Power_ROI_sphere_binarized_98.nii.gz', 'Power_ROI_sphere_binarized_99.nii.gz', 'Power_ROI_sphere_binarized_108.nii.gz', 'Power_ROI_sphere_binarized_115.nii.gz', 'Power_ROI_sphere_binarized_116.nii.gz', 'Power_ROI_sphere_binarized_118.nii.gz', 'Power_ROI_sphere_binarized_120.nii.gz', 'Power_ROI_sphere_binarized_122.nii.gz', 'Power_ROI_sphere_binarized_123.nii.gz', 'Power_ROI_sphere_binarized_124.nii.gz', 'Power_ROI_sphere_binarized_125.nii.gz', 'Power_ROI_sphere_binarized_126.nii.gz', 'Power_ROI_sphere_binarized_127.nii.gz', 'Power_ROI_sphere_binarized_128.nii.gz', 'Power_ROI_sphere_binarized_131.nii.gz', 'Power_ROI_sphere_binarized_135.nii.gz', 'Power_ROI_sphere_binarized_136.nii.gz', 'Power_ROI_sphere_binarized_137.nii.gz', 'Power_ROI_sphere_binarized_138.nii.gz', 'Power_ROI_sphere_binarized_140.nii.gz', 'Power_ROI_sphere_binarized_141.nii.gz', 'Power_ROI_sphere_binarized_142.nii.gz', 'Power_ROI_sphere_binarized_149.nii.gz', 'Power_ROI_sphere_binarized_150.nii.gz', 'Power_ROI_sphere_binarized_152.nii.gz', 'Power_ROI_sphere_binarized_153.nii.gz', 'Power_ROI_sphere_binarized_160.nii.gz', 'Power_ROI_sphere_binarized_164.nii.gz', 'Power_ROI_sphere_binarized_171.nii.gz', 'Power_ROI_sphere_binarized_173.nii.gz', 'Power_ROI_sphere_binarized_177.nii.gz', 'Power_ROI_sphere_binarized_178.nii.gz', 'Power_ROI_sphere_binarized_179.nii.gz', 'Power_ROI_sphere_binarized_180.nii.gz', 'Power_ROI_sphere_binarized_181.nii.gz', 'Power_ROI_sphere_binarized_182.nii.gz', 'Power_ROI_sphere_binarized_183.nii.gz', 'Power_ROI_sphere_binarized_184.nii.gz', 'Power_ROI_sphere_binarized_190.nii.gz', 'Power_ROI_sphere_binarized_191.nii.gz', 'Power_ROI_sphere_binarized_192.nii.gz', 'Power_ROI_sphere_binarized_202.nii.gz', 'Power_ROI_sphere_binarized_204.nii.gz', 'Power_ROI_sphere_binarized_210.nii.gz', 'Power_ROI_sphere_binarized_242.nii.gz', 'Power_ROI_sphere_binarized_243.nii.gz', 'Power_ROI_sphere_binarized_244.nii.gz', 'Power_ROI_sphere_binarized_245.nii.gz', 'Power_ROI_sphere_binarized_246.nii.gz', 'Power_ROI_sphere_binarized_247.nii.gz', 'Power_ROI_sphere_binarized_248.nii.gz', 'Power_ROI_sphere_binarized_249.nii.gz', 'Power_ROI_sphere_binarized_250.nii.gz', 'Power_ROI_sphere_binarized_252.nii.gz', 'Power_ROI_sphere_binarized_253.nii.gz', 'Power_ROI_sphere_binarized_254.nii.gz', 'Power_ROI_sphere_binarized_255.nii.gz', 'Power_ROI_sphere_binarized_257.nii.gz', 'Power_ROI_sphere_binarized_258.nii.gz', 'Power_ROI_sphere_binarized_260.nii.gz', 'Power_ROI_sphere_binarized_261.nii.gz', 'Power_ROI_sphere_binarized_262.nii.gz', 'Power_ROI_sphere_binarized_263.nii.gz']


tasks=['BOLD_Cups_Parent',
'BOLD_Cups_Peer',
'BOLD_Cups_Self',
'BOLD_Ratings_1',
'BOLD_Ratings_2',
'BOLD_Resting_State',
'BOLD_Shapes_1',
'BOLD_Shapes_2']



Bad_ROIs=[['Subject','Task','ROI','Percent_of_Sphere']]

for subject in subjects:
	os.chdir(path_to_subs)
	os.chdir(subject)
	for task in tasks:
		current_smoothed_functional='prep.default.{}_MCcorrected_smooth6mm_MNI2mm_denoised.nii.gz'.format(task)
		if os.path.exists(current_smoothed_functional):
			get_first_vol=fsl.ImageMaths(in_file=current_smoothed_functional, op_string=' -roi 0 -1 0 -1 0 -1 0 1', out_file='{}/first_vol.nii.gz'.format(output_path))
			get_first_vol.run()
			print 'Get first vol worked'
		roi_num=1
		if os.path.exists(current_smoothed_functional):
			for roi in rois:
				get_reduced_sphere=fsl.ImageMaths(in_file='{}/first_vol.nii.gz'.format(output_path), op_string='-mul {}/{}'.format(path_to_rois,roi), out_file='{}/reduced_sphere.nii.gz'.format(output_path))
				get_reduced_sphere.run()
				#get volume of each ROI in native diffusion space
				get_volume_ROI = fsl.ImageStats(in_file='{}/reduced_sphere.nii.gz'.format(output_path), op_string='-V > {}/ROI_volumes.txt'.format(output_path))
				get_volume_ROI.run()
				with open('{}/ROI_volumes.txt'.format(output_path), 'r') as f:
					lines=f.readlines()
					line=lines[0].split()
				roi_vol=float(line[0])
				percent_sphere=roi_vol/81.0 #81.0 is the size of each sphere with 10mm diameter
				current_info_for_csv=[subject,task,roi_num,percent_sphere]
				now = datetime.datetime.now()
				g=open('{}/record.txt'.format(output_path),'a')
				g.write('Another iteration at {}:{}:{}\n'.format(now.hour,now.minute,now.second))
				if percent_sphere <0.80:
					print current_info_for_csv
					Bad_ROIs.append(current_info_for_csv)		
				roi_num+=1

		

os.chdir(output_path)
with open('QC_output_ROIs_less_than_80_percent_coverage.csv', 'a') as f:
	writer=csv.writer(f)
	writer.writerows(Bad_ROIs)	
