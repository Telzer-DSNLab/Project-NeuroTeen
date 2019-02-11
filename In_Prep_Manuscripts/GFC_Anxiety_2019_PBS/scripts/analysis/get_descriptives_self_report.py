 #import libraries
import nibabel as nib
import numpy as np
import pylab as pl
from scipy import stats
import scipy
import os
import pandas as pd
import csv

from sklearn import linear_model #for regression analysis
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import KFold


path_data='/Users/paulsharp/Documents/Dissertation_studies/data'
os.chdir(path_data)

master_csv=[['Substance_of_Correlation','Wave','Pearson_Corr','Spearman_Corr']]

#Get self-report data in vectors
self_report_data=pd.read_csv('Self_report_full_data_all_timepoints_and_gender.csv')
anxious_apprehension_w1=self_report_data.anxious_app_w1
print('\n anxious_apprehension_w1 count:{}'.format(self_report_data['anxious_app_w1'].value_counts()))
print('anxious_apprehension_w1 descriptives:{}\n'.format(anxious_apprehension_w1.describe()))

anxious_apprehension_w2=self_report_data.anxious_app_w2
print('\n anxious_apprehension_w2 count:{}'.format(self_report_data['anxious_app_w2'].value_counts()))
print('anxious_apprehension_w2 descriptives:{}\n'.format(anxious_apprehension_w2.describe()))

anxious_apprehension_longitudinal=self_report_data.anxious_apprehension_change
print('\n anxious_apprehension_longitudinal count:{}'.format(self_report_data['anxious_apprehension_change'].value_counts()))
print('anxious_apprehension_longitudinal descriptives:{}\n'.format(anxious_apprehension_longitudinal.describe()))

anxious_arousal_w1=self_report_data.anxious_arousal_w1
print('\n anxious_arousal_w1 count:{}'.format(self_report_data['anxious_arousal_w1'].value_counts()))
print('anxious_arousal_w1 descriptives:{}\n'.format(anxious_arousal_w1.describe()))
anxious_arousal_w2=self_report_data.anxious_arousal_w2
print('\n anxious_arousal_w2 count:{}'.format(self_report_data['anxious_arousal_w2'].value_counts()))
print('anxious_arousal_w2 descriptives:{}\n'.format(anxious_arousal_w2.describe()))
anxious_arousal_longitudinal=self_report_data.anxious_arousal_change
print('\n anxious_arousal_longitudinal count:{}'.format(self_report_data['anxious_arousal_change'].value_counts()))
print('anxious_arousal_longitudinal descriptives:{}\n'.format(anxious_arousal_longitudinal.describe()))


