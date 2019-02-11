import pandas as pd 
import numpy as np 
import os
import csv

data_path='/Users/paulsharp/Documents/Dissertation_studies/data/QC_Applied'
output_path='/Users/paulsharp/Documents/Dissertation_studies/data'
self_report_path='/Users/paulsharp/Documents/Dissertation_studies/data'
os.chdir(self_report_path)
self_report_data=pd.read_csv('Self_report_full_data_all_timepoints.csv')

os.chdir(data_path)
subs_wave_2=[x for x in os.listdir(os.curdir) if x[17]=='2']
subs_wave_1=[x for x in os.listdir(os.curdir) if x[17]=='1']
sub_order_out=[['Subject_Order']]

os.chdir(output_path)

sub_order_df=pd.read_csv('Subject_Order_GFC_Feature_Matrix_amygdala_only.csv')
subjects=sub_order_df.Subject_Order
sub_order=sub_order_df.Subject_Order.tolist()
print(sub_order)



region_names=['dmpfc_left',
'dmpfc_right',
'vmpfc_left',
'vmpfc_right',
'vlpfc_left',
'vlpfc_right']

mast_csv_w1_Leftamyg=[['Subject','dmpfc_left1','dmpfc_left2','dmpfc_left3',
'dmpfc_right1','dmpfc_right2','vmpfc_left1','vmpfc_left2',
'vmpfc_right1','vmpfc_right2','vmpfc_right3','vmpfc_right4',
'vlpfc_left1','vlpfc_left2','vlpfc_left3','vlpfc_left4','vlpfc_left5',
'vlpfc_right1','vlpfc_right2','vlpfc_right3','vlpfc_right4',
'vlpfc_right5','vlpfc_right6','vlpfc_right7','vlpfc_right8']]

mast_csv_w1_Rightamyg=[['Subject','dmpfc_left1','dmpfc_left2','dmpfc_left3',
'dmpfc_right1','dmpfc_right2','vmpfc_left1','vmpfc_left2',
'vmpfc_right1','vmpfc_right2','vmpfc_right3','vmpfc_right4',
'vlpfc_left1','vlpfc_left2','vlpfc_left3','vlpfc_left4','vlpfc_left5',
'vlpfc_right1','vlpfc_right2','vlpfc_right3','vlpfc_right4',
'vlpfc_right5','vlpfc_right6','vlpfc_right7','vlpfc_right8']]

mast_csv_w2_Leftamyg=[['Subject','dmpfc_left1','dmpfc_left2','dmpfc_left3',
'dmpfc_right1','dmpfc_right2','vmpfc_left1','vmpfc_left2',
'vmpfc_right1','vmpfc_right2','vmpfc_right3','vmpfc_right4',
'vlpfc_left1','vlpfc_left2','vlpfc_left3','vlpfc_left4','vlpfc_left5',
'vlpfc_right1','vlpfc_right2','vlpfc_right3','vlpfc_right4',
'vlpfc_right5','vlpfc_right6','vlpfc_right7','vlpfc_right8']]

mast_csv_w2_Rightamyg=[['Subject','dmpfc_left1','dmpfc_left2','dmpfc_left3',
'dmpfc_right1','dmpfc_right2','vmpfc_left1','vmpfc_left2',
'vmpfc_right1','vmpfc_right2','vmpfc_right3','vmpfc_right4',
'vlpfc_left1','vlpfc_left2','vlpfc_left3','vlpfc_left4','vlpfc_left5',
'vlpfc_right1','vlpfc_right2','vlpfc_right3','vlpfc_right4',
'vlpfc_right5','vlpfc_right6','vlpfc_right7','vlpfc_right8']]

mast_csv_diff_left=[['Subject','dmpfc_left1','dmpfc_left2','dmpfc_left3',
'dmpfc_right1','dmpfc_right2','vmpfc_left1','vmpfc_left2',
'vmpfc_right1','vmpfc_right2','vmpfc_right3','vmpfc_right4',
'vlpfc_left1','vlpfc_left2','vlpfc_left3','vlpfc_left4','vlpfc_left5',
'vlpfc_right1','vlpfc_right2','vlpfc_right3','vlpfc_right4',
'vlpfc_right5','vlpfc_right6','vlpfc_right7','vlpfc_right8']]

mast_csv_diff_right=[['Subject','dmpfc_left1','dmpfc_left2','dmpfc_left3',
'dmpfc_right1','dmpfc_right2','vmpfc_left1','vmpfc_left2',
'vmpfc_right1','vmpfc_right2','vmpfc_right3','vmpfc_right4',
'vlpfc_left1','vlpfc_left2','vlpfc_left3','vlpfc_left4','vlpfc_left5',
'vlpfc_right1','vlpfc_right2','vlpfc_right3','vlpfc_right4',
'vlpfc_right5','vlpfc_right6','vlpfc_right7','vlpfc_right8']]



region_nums=[[96, 97, 104],[107, 116],[99, 102],[2, 110, 111, 112],
[82, 176, 177, 215, 240],[10, 123, 181, 184, 189, 209, 217, 241]]

os.chdir(data_path)

sub_count=0
for sub in sub_order:
	sub_wave1=sub
	print(sub_wave1)
	current_sub=[sub]
	sub_order_out.append(current_sub)
	sub_wave2='NT2'+sub[-3:]
	current_line1_left=[]
	current_line1_left.append(sub_wave1)
	current_line2_left=[]
	current_line2_left.append(sub_wave2)
	current_line1_right=[]
	current_line1_right.append(sub_wave1)
	current_line2_right=[]
	current_line2_right.append(sub_wave2)
	diff_left=[]
	diff_left.append(sub_wave1)
	diff_right=[]
	diff_right.append(sub_wave1)
	for region in region_nums:
		for reg in region:
			#Define amygdala connectomes
			#wave2
			wave1_gfc=pd.read_csv('GFC_connectome_{}_QCapplied.csv'.format(sub_wave1))

			#determine which ROW each ROI in list region_num is in current dataframe
			counter=0
			for i in wave1_gfc.columns:
				if i == '{}.0'.format(reg):
					index_reg=counter
				counter+=1

			wave2_gfc=pd.read_csv('GFC_connectome_{}_QCapplied.csv'.format(sub_wave2))

			amygdala_left_w2=wave2_gfc['243.0'][index_reg]
			current_line2_left.append(amygdala_left_w2)
			amygdala_right_w2=wave2_gfc['244.0'][index_reg]
			current_line2_right.append(amygdala_right_w2)

			
			#wave1
			amygdala_left_w1=wave1_gfc['243.0'][index_reg]
			current_line1_left.append(amygdala_left_w1)
			amygdala_right_w1=wave1_gfc['244.0'][index_reg]
			current_line1_right.append(amygdala_right_w2)

			#Wave2 - Wave 1 (longitudinal)
			diff_amygdalae_left=amygdala_left_w2-amygdala_left_w1
			diff_left.append(diff_amygdalae_left)
			diff_amygdalae_right=amygdala_right_w2-amygdala_left_w1
			diff_right.append(diff_amygdalae_right)

	mast_csv_w1_Leftamyg.append(current_line1_left)
	mast_csv_w1_Rightamyg.append(current_line1_right)
	mast_csv_w2_Leftamyg.append(current_line2_left)
	mast_csv_w2_Rightamyg.append(current_line2_right)
	mast_csv_diff_left.append(diff_left)
	mast_csv_diff_right.append(diff_right)


os.chdir(output_path)
#run correlations between self-report data and ROIs

mast_csv_w1_Leftamyg=pd.DataFrame(mast_csv_w1_Leftamyg[1:],columns=mast_csv_w1_Leftamyg[0])
print(mast_csv_w1_Leftamyg)
mast_csv_w1_Rightamyg=pd.DataFrame(mast_csv_w1_Rightamyg[1:],columns=mast_csv_w1_Rightamyg[0])
mast_csv_w2_Leftamyg=pd.DataFrame(mast_csv_w2_Leftamyg[1:],columns=mast_csv_w2_Leftamyg[0])
mast_csv_w2_Rightamyg=pd.DataFrame(mast_csv_w2_Rightamyg[1:],columns=mast_csv_w2_Rightamyg[0])
mast_csv_diff_left=pd.DataFrame(mast_csv_diff_left[1:],columns=mast_csv_diff_left[0])
mast_csv_diff_right=pd.DataFrame(mast_csv_diff_right[1:],columns=mast_csv_diff_right[0])


pd_1=pd.concat([self_report_data,mast_csv_w1_Leftamyg],axis=1).corr()
pd_2=pd.concat([self_report_data,mast_csv_w1_Rightamyg],axis=1).corr()
pd_3=pd.concat([self_report_data,mast_csv_w2_Leftamyg],axis=1).corr()
pd_4=pd.concat([self_report_data,mast_csv_w2_Rightamyg],axis=1).corr()
pd_5=pd.concat([self_report_data,mast_csv_diff_left],axis=1).corr()
pd_6=pd.concat([self_report_data,mast_csv_diff_right],axis=1).corr()


pd_1.to_csv('w1_Leftamyg.csv')
pd_2.to_csv('w1_Rightamyg.csv')
pd_3.to_csv('w2_Leftamyg.csv')
pd_4.to_csv('w2_Rightamyg.csv')
pd_5.to_csv('diff_left.csv')
pd_6.to_csv('diff_right.csv')




os.chdir(output_path)
with open('Subject_Order_aPrioriHypotheses_reIndexed.csv', 'a') as f:
	w=csv.writer(f)
	w.writerows(sub_order_out)


