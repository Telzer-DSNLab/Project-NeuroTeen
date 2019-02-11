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
anxious_apprehension_w1=self_report_data.anxious_app_w1.values
anxious_apprehension_w2=self_report_data.anxious_app_w2.values
anxious_apprehension_longitudinal=self_report_data.anxious_apprehension_change.values

anxious_arousal_w1=self_report_data.anxious_arousal_w1.values
anxious_arousal_w2=self_report_data.anxious_arousal_w2.values
anxious_arousal_longitudinal=self_report_data.anxious_arousal_change.values


#Get all amygdala GFC data
connectome_data=pd.read_csv('LEFT_amygdala_connectivity_wave1.csv',header=None)
connectome_data=connectome_data.drop([0],axis=1)
connectome_data=connectome_data.fillna(connectome_data.mean()) #convert NAN to Mean via imputation
Left_amygdala_w1=connectome_data.values

connectome_data=pd.read_csv('LEFT_amygdala_connectivity_wave2.csv',header=None)
connectome_data=connectome_data.drop([0],axis=1)
connectome_data=connectome_data.fillna(connectome_data.mean()) #convert NAN to Mean via imputation
Left_amygdala_w2=connectome_data.values

connectome_data=pd.read_csv('LEFT_amygdala_connectivity_longitudinal.csv',header=None)
connectome_data=connectome_data.drop([0],axis=1)
connectome_data=connectome_data.fillna(connectome_data.mean()) #convert NAN to Mean via imputation
Left_amygdala_longitudinal=connectome_data.values

connectome_data=pd.read_csv('RIGHT_amygdala_connectivity_wave1.csv',header=None)
connectome_data=connectome_data.drop([0],axis=1)
connectome_data=connectome_data.fillna(connectome_data.mean()) #convert NAN to Mean via imputation
Right_amygdala_w1=connectome_data.values

connectome_data=pd.read_csv('RIGHT_amygdala_connectivity_wave2.csv',header=None)
connectome_data=connectome_data.drop([0],axis=1)
connectome_data=connectome_data.fillna(connectome_data.mean()) #convert NAN to Mean via imputation
Right_amygdala_w2=connectome_data.values

connectome_data=pd.read_csv('RIGHT_amygdala_connectivity_longitudinal.csv',header=None)
connectome_data=connectome_data.drop([0],axis=1)
connectome_data=connectome_data.fillna(connectome_data.mean()) #convert NAN to Mean via imputation
Right_amygdala_longitudinal=connectome_data.values



n_folds=8
kf=KFold(n_splits=8)


####################################################################
## Implement Nested cross validation
####################################################################
# Import linear model and run
# Also produce summary statistics and save in arrays
# Also implement nested cross-validation for hyperparameter estimates

y_predict = np.zeros((n_folds,13)) #rows=n_iterations, col=test_size
y_truth = np.zeros((n_folds,13))
coefs = np.zeros((n_folds,258))
hparam = np.zeros((n_folds,1))
counter = 0


for k, (train, test) in enumerate(kf.split(Left_amygdala_w1,anxious_apprehension_w1)):
	Ridge_cv = linear_model.RidgeCV(alphas=np.arange(0.01,10,0.1))
	Ridge_cv.fit(Left_amygdala_w1[train],anxious_apprehension_w1[train])
	print('R^2 of Ridge= {}'.format(Ridge_cv.score(Left_amygdala_w1[train],anxious_apprehension_w1[train]))) #execute LOO nested CV just on training set (NESTED)
	hparam[counter,0] = Ridge_cv.alpha_
	y_predict[counter,:]=Ridge_cv.predict(Left_amygdala_w1[test])
	y_truth[counter,:] = anxious_apprehension_w1[test]
	coefs[counter,:] = Ridge_cv.coef_
	counter = counter +1

print(hparam)

MSE = mean_squared_error(np.reshape(y_predict,len(anxious_apprehension_w1)), np.reshape(y_truth,len(anxious_apprehension_w1)))
CorrSp = scipy.stats.spearmanr(np.reshape(y_predict,len(anxious_apprehension_w1)),np.reshape(y_truth,len(anxious_apprehension_w1)))
CorrTau = scipy.stats.kendalltau(np.reshape(y_predict,len(anxious_apprehension_w1)),np.reshape(y_truth,len(anxious_apprehension_w1)))
CorrPear = scipy.stats.pearsonr(np.reshape(y_predict,len(anxious_apprehension_w1)),np.reshape(y_truth,len(anxious_apprehension_w1)))

print('Left Amyg to Anx App Wave 1 MSE:{} Corr Spearman:{} Corr Tau: {} Corr Pearson: {}\n\n'.format(MSE,CorrSp,CorrTau,CorrPear))

current_line=['Left Amyg with Anx App',1,CorrPear,CorrSp]
master_csv.append(current_line)

y_predict = np.zeros((n_folds,13)) #rows=n_iterations, col=test_size
y_truth = np.zeros((n_folds,13))
coefs = np.zeros((n_folds,258))
hparam = np.zeros((n_folds,1))
counter = 0


for k, (train, test) in enumerate(kf.split(Left_amygdala_w2,anxious_apprehension_w2)):
	Ridge_cv = linear_model.RidgeCV(alphas=np.arange(0.01,10,0.1))
	Ridge_cv.fit(Left_amygdala_w2[train],anxious_apprehension_w2[train])
	print('WAVE 2 R^2 of Ridge= {}'.format(Ridge_cv.score(Left_amygdala_w2[train],anxious_apprehension_w2[train]))) #execute LOO nested CV just on training set (NESTED)
	hparam[counter,0] = Ridge_cv.alpha_
	y_predict[counter,:]=Ridge_cv.predict(Left_amygdala_w2[test])
	y_truth[counter,:] = anxious_apprehension_w2[test] 
	coefs[counter,:] = Ridge_cv.coef_
	counter = counter +1

print(hparam)

MSE = mean_squared_error(np.reshape(y_predict,len(anxious_apprehension_w2)), np.reshape(y_truth,len(anxious_apprehension_w2)))
CorrSp = scipy.stats.spearmanr(np.reshape(y_predict,len(anxious_apprehension_w2)),np.reshape(y_truth,len(anxious_apprehension_w2)))
CorrTau = scipy.stats.kendalltau(np.reshape(y_predict,len(anxious_apprehension_w2)),np.reshape(y_truth,len(anxious_apprehension_w2)))
CorrPear = scipy.stats.pearsonr(np.reshape(y_predict,len(anxious_apprehension_w2)),np.reshape(y_truth,len(anxious_apprehension_w2)))

print('Left Amyg to Anx App WAVE 2 MSE:{} Corr Spearman:{} Corr Tau: {} Corr Pearson: {}\n\n'.format(MSE,CorrSp,CorrTau,CorrPear))
current_line=['Left Amyg with Anx App',2,CorrPear,CorrSp]
master_csv.append(current_line)


y_predict = np.zeros((n_folds,13)) #rows=n_iterations, col=test_size
y_truth = np.zeros((n_folds,13))
coefs = np.zeros((n_folds,258))
hparam = np.zeros((n_folds,1))
counter = 0

for k, (train, test) in enumerate(kf.split(Right_amygdala_w1,anxious_apprehension_w1)):
	Ridge_cv = linear_model.RidgeCV(alphas=np.arange(0.01,10,0.1))
	Ridge_cv.fit(Right_amygdala_w1[train],anxious_apprehension_w1[train])
	print('WAVE 1 R^2 of Ridge= {}'.format(Ridge_cv.score(Right_amygdala_w1[train],anxious_apprehension_w1[train]))) #execute LOO nested CV just on training set (NESTED)
	hparam[counter,0] = Ridge_cv.alpha_
	y_predict[counter,:]=Ridge_cv.predict(Right_amygdala_w1[test])
	y_truth[counter,:] = anxious_apprehension_w1[test] 
	coefs[counter,:] = Ridge_cv.coef_
	counter = counter +1

print(hparam)

MSE = mean_squared_error(np.reshape(y_predict,len(anxious_apprehension_w1)), np.reshape(y_truth,len(anxious_apprehension_w1)))
CorrSp = scipy.stats.spearmanr(np.reshape(y_predict,len(anxious_apprehension_w1)),np.reshape(y_truth,len(anxious_apprehension_w1)))
CorrTau = scipy.stats.kendalltau(np.reshape(y_predict,len(anxious_apprehension_w1)),np.reshape(y_truth,len(anxious_apprehension_w1)))
CorrPear = scipy.stats.pearsonr(np.reshape(y_predict,len(anxious_apprehension_w1)),np.reshape(y_truth,len(anxious_apprehension_w1)))

print('RIGHT Amyg to anx app WAVE 1 MSE :{} Corr Spearman:{} Corr Tau: {} Corr Pearson: {}\n\n'.format(MSE,CorrSp,CorrTau,CorrPear))
current_line=['Right Amyg with Anx App',1,CorrPear,CorrSp]
master_csv.append(current_line)

y_predict = np.zeros((n_folds,13)) #rows=n_iterations, col=test_size
y_truth = np.zeros((n_folds,13))
coefs = np.zeros((n_folds,258))
hparam = np.zeros((n_folds,1))
counter = 0

for k, (train, test) in enumerate(kf.split(Right_amygdala_w2,anxious_apprehension_w2)):
	Ridge_cv = linear_model.RidgeCV(alphas=np.arange(0.01,10,0.1))
	Ridge_cv.fit(Right_amygdala_w2[train],anxious_apprehension_w2[train])
	print('WAVE 2 R^2 of Ridge= {}'.format(Ridge_cv.score(Right_amygdala_w2[train],anxious_apprehension_w2[train]))) #execute LOO nested CV just on training set (NESTED)
	hparam[counter,0] = Ridge_cv.alpha_
	y_predict[counter,:]=Ridge_cv.predict(Right_amygdala_w2[test])
	y_truth[counter,:] = anxious_apprehension_w2[test] 
	coefs[counter,:] = Ridge_cv.coef_
	counter = counter +1

print(hparam)

MSE = mean_squared_error(np.reshape(y_predict,len(anxious_apprehension_w2)), np.reshape(y_truth,len(anxious_apprehension_w2)))
CorrSp = scipy.stats.spearmanr(np.reshape(y_predict,len(anxious_apprehension_w2)),np.reshape(y_truth,len(anxious_apprehension_w2)))
CorrTau = scipy.stats.kendalltau(np.reshape(y_predict,len(anxious_apprehension_w2)),np.reshape(y_truth,len(anxious_apprehension_w2)))
CorrPear = scipy.stats.pearsonr(np.reshape(y_predict,len(anxious_apprehension_w2)),np.reshape(y_truth,len(anxious_apprehension_w2)))

print('Right Amyg to WAVE 2 MSE RIGHT:{} Corr Spearman:{} Corr Tau: {} Corr Pearson: {}\n\n'.format(MSE,CorrSp,CorrTau,CorrPear))
current_line=['Right Amyg with Anx App',2,CorrPear,CorrSp]
master_csv.append(current_line)


y_predict = np.zeros((n_folds,13)) #rows=n_iterations, col=test_size
y_truth = np.zeros((n_folds,13))
coefs = np.zeros((n_folds,258))
hparam = np.zeros((n_folds,1))
counter = 0


for k, (train, test) in enumerate(kf.split(Left_amygdala_longitudinal,anxious_apprehension_longitudinal)):
	Ridge_cv = linear_model.RidgeCV(alphas=np.arange(0.01,10,0.1))
	Ridge_cv.fit(Left_amygdala_longitudinal[train],anxious_apprehension_longitudinal[train])
	print('R^2 of Ridge= {}'.format(Ridge_cv.score(Left_amygdala_longitudinal[train],anxious_apprehension_longitudinal[train]))) #execute LOO nested CV just on training set (NESTED)
	hparam[counter,0] = Ridge_cv.alpha_
	y_predict[counter,:]=Ridge_cv.predict(Left_amygdala_longitudinal[test])
	y_truth[counter,:] = anxious_apprehension_longitudinal[test]
	coefs[counter,:] = Ridge_cv.coef_
	counter = counter +1

print(hparam)

MSE = mean_squared_error(np.reshape(y_predict,len(anxious_apprehension_longitudinal)), np.reshape(y_truth,len(anxious_apprehension_longitudinal)))
CorrSp = scipy.stats.spearmanr(np.reshape(y_predict,len(anxious_apprehension_longitudinal)),np.reshape(y_truth,len(anxious_apprehension_longitudinal)))
CorrTau = scipy.stats.kendalltau(np.reshape(y_predict,len(anxious_apprehension_longitudinal)),np.reshape(y_truth,len(anxious_apprehension_longitudinal)))
CorrPear = scipy.stats.pearsonr(np.reshape(y_predict,len(anxious_apprehension_longitudinal)),np.reshape(y_truth,len(anxious_apprehension_longitudinal)))

print('Left Longitdinal MSE:{} Corr Spearman:{} Corr Tau: {} Corr Pearson: {}\n\n'.format(MSE,CorrSp,CorrTau,CorrPear))
current_line=['Left Amyg-Diff with Anx App change','longitudinal',CorrPear,CorrSp]
master_csv.append(current_line)


y_predict = np.zeros((n_folds,13)) #rows=n_iterations, col=test_size
y_truth = np.zeros((n_folds,13))
coefs = np.zeros((n_folds,258))
hparam = np.zeros((n_folds,1))
counter = 0


for k, (train, test) in enumerate(kf.split(Right_amygdala_longitudinal,anxious_apprehension_longitudinal)):
	Ridge_cv = linear_model.RidgeCV(alphas=np.arange(0.01,10,0.1))
	Ridge_cv.fit(Right_amygdala_longitudinal[train],anxious_apprehension_longitudinal[train])
	print('R^2 of Ridge= {}'.format(Ridge_cv.score(Right_amygdala_longitudinal[train],anxious_apprehension_longitudinal[train]))) #execute LOO nested CV just on training set (NESTED)
	hparam[counter,0] = Ridge_cv.alpha_
	y_predict[counter,:]=Ridge_cv.predict(Right_amygdala_longitudinal[test])
	y_truth[counter,:] = anxious_apprehension_longitudinal[test]
	coefs[counter,:] = Ridge_cv.coef_
	counter = counter +1

print(hparam)

MSE = mean_squared_error(np.reshape(y_predict,len(anxious_apprehension_longitudinal)), np.reshape(y_truth,len(anxious_apprehension_longitudinal)))
CorrSp = scipy.stats.spearmanr(np.reshape(y_predict,len(anxious_apprehension_longitudinal)),np.reshape(y_truth,len(anxious_apprehension_longitudinal)))
CorrTau = scipy.stats.kendalltau(np.reshape(y_predict,len(anxious_apprehension_longitudinal)),np.reshape(y_truth,len(anxious_apprehension_longitudinal)))
CorrPear = scipy.stats.pearsonr(np.reshape(y_predict,len(anxious_apprehension_longitudinal)),np.reshape(y_truth,len(anxious_apprehension_longitudinal)))

print('RIGHT Long MSE:{} Corr Spearman:{} Corr Tau: {} Corr Pearson: {}\n\n'.format(MSE,CorrSp,CorrTau,CorrPear))
current_line=['Right Amyg-Diff with Anx App change','longitudinal',CorrPear,CorrSp]
master_csv.append(current_line)

y_predict = np.zeros((n_folds,13)) #rows=n_iterations, col=test_size
y_truth = np.zeros((n_folds,13))
coefs = np.zeros((n_folds,258))
hparam = np.zeros((n_folds,1))
counter = 0


for k, (train, test) in enumerate(kf.split(Left_amygdala_w1,anxious_arousal_w1)):
	Ridge_cv = linear_model.RidgeCV(alphas=np.arange(0.01,10,0.1))
	Ridge_cv.fit(Left_amygdala_w1[train],anxious_arousal_w1[train])
	print('R^2 of Ridge= {}'.format(Ridge_cv.score(Left_amygdala_w1[train],anxious_arousal_w1[train]))) #execute LOO nested CV just on training set (NESTED)
	hparam[counter,0] = Ridge_cv.alpha_
	y_predict[counter,:]=Ridge_cv.predict(Left_amygdala_w1[test])
	y_truth[counter,:] = anxious_arousal_w1[test]
	coefs[counter,:] = Ridge_cv.coef_
	counter = counter +1

print(hparam)

MSE = mean_squared_error(np.reshape(y_predict,len(anxious_arousal_w1)), np.reshape(y_truth,len(anxious_arousal_w1)))
CorrSp = scipy.stats.spearmanr(np.reshape(y_predict,len(anxious_arousal_w1)),np.reshape(y_truth,len(anxious_arousal_w1)))
CorrTau = scipy.stats.kendalltau(np.reshape(y_predict,len(anxious_arousal_w1)),np.reshape(y_truth,len(anxious_arousal_w1)))
CorrPear = scipy.stats.pearsonr(np.reshape(y_predict,len(anxious_arousal_w1)),np.reshape(y_truth,len(anxious_arousal_w1)))

print('Left Amyg to Anx Arousal Wave 1 MSE:{} Corr Spearman:{} Corr Tau: {} Corr Pearson: {}\n\n'.format(MSE,CorrSp,CorrTau,CorrPear))

current_line=['Left Amyg with Anx Arousal',1,CorrPear,CorrSp]
master_csv.append(current_line)

y_predict = np.zeros((n_folds,13)) #rows=n_iterations, col=test_size
y_truth = np.zeros((n_folds,13))
coefs = np.zeros((n_folds,258))
hparam = np.zeros((n_folds,1))
counter = 0


for k, (train, test) in enumerate(kf.split(Left_amygdala_w2,anxious_arousal_w2)):
	Ridge_cv = linear_model.RidgeCV(alphas=np.arange(0.01,10,0.1))
	Ridge_cv.fit(Left_amygdala_w2[train],anxious_arousal_w2[train])
	print('WAVE 2 R^2 of Ridge= {}'.format(Ridge_cv.score(Left_amygdala_w2[train],anxious_arousal_w2[train]))) #execute LOO nested CV just on training set (NESTED)
	hparam[counter,0] = Ridge_cv.alpha_
	y_predict[counter,:]=Ridge_cv.predict(Left_amygdala_w2[test])
	y_truth[counter,:] = anxious_arousal_w2[test] 
	coefs[counter,:] = Ridge_cv.coef_
	counter = counter +1

print(hparam)

MSE = mean_squared_error(np.reshape(y_predict,len(anxious_arousal_w2)), np.reshape(y_truth,len(anxious_arousal_w2)))
CorrSp = scipy.stats.spearmanr(np.reshape(y_predict,len(anxious_arousal_w2)),np.reshape(y_truth,len(anxious_arousal_w2)))
CorrTau = scipy.stats.kendalltau(np.reshape(y_predict,len(anxious_arousal_w2)),np.reshape(y_truth,len(anxious_arousal_w2)))
CorrPear = scipy.stats.pearsonr(np.reshape(y_predict,len(anxious_arousal_w2)),np.reshape(y_truth,len(anxious_arousal_w2)))

print('Left Amyg to Anx Arousal WAVE 2 MSE:{} Corr Spearman:{} Corr Tau: {} Corr Pearson: {}\n\n'.format(MSE,CorrSp,CorrTau,CorrPear))
current_line=['Left Amyg with Anx Arousal',2,CorrPear,CorrSp]
master_csv.append(current_line)


y_predict = np.zeros((n_folds,13)) #rows=n_iterations, col=test_size
y_truth = np.zeros((n_folds,13))
coefs = np.zeros((n_folds,258))
hparam = np.zeros((n_folds,1))
counter = 0

for k, (train, test) in enumerate(kf.split(Right_amygdala_w1,anxious_arousal_w1)):
	Ridge_cv = linear_model.RidgeCV(alphas=np.arange(0.01,10,0.1))
	Ridge_cv.fit(Right_amygdala_w1[train],anxious_arousal_w1[train])
	print('WAVE 1 R^2 of Ridge= {}'.format(Ridge_cv.score(Right_amygdala_w1[train],anxious_arousal_w1[train]))) #execute LOO nested CV just on training set (NESTED)
	hparam[counter,0] = Ridge_cv.alpha_
	y_predict[counter,:]=Ridge_cv.predict(Right_amygdala_w1[test])
	y_truth[counter,:] = anxious_arousal_w1[test] 
	coefs[counter,:] = Ridge_cv.coef_
	counter = counter +1

print(hparam)

MSE = mean_squared_error(np.reshape(y_predict,len(anxious_arousal_w1)), np.reshape(y_truth,len(anxious_arousal_w1)))
CorrSp = scipy.stats.spearmanr(np.reshape(y_predict,len(anxious_arousal_w1)),np.reshape(y_truth,len(anxious_arousal_w1)))
CorrTau = scipy.stats.kendalltau(np.reshape(y_predict,len(anxious_arousal_w1)),np.reshape(y_truth,len(anxious_arousal_w1)))
CorrPear = scipy.stats.pearsonr(np.reshape(y_predict,len(anxious_arousal_w1)),np.reshape(y_truth,len(anxious_arousal_w1)))

print('RIGHT Amyg to anx app WAVE 1 MSE :{} Corr Spearman:{} Corr Tau: {} Corr Pearson: {}\n\n'.format(MSE,CorrSp,CorrTau,CorrPear))
current_line=['Right Amyg with Anx Arousal',1,CorrPear,CorrSp]
master_csv.append(current_line)

y_predict = np.zeros((n_folds,13)) #rows=n_iterations, col=test_size
y_truth = np.zeros((n_folds,13))
coefs = np.zeros((n_folds,258))
hparam = np.zeros((n_folds,1))
counter = 0

for k, (train, test) in enumerate(kf.split(Right_amygdala_w2,anxious_arousal_w2)):
	Ridge_cv = linear_model.RidgeCV(alphas=np.arange(0.01,10,0.1))
	Ridge_cv.fit(Right_amygdala_w2[train],anxious_arousal_w2[train])
	print('WAVE 2 R^2 of Ridge= {}'.format(Ridge_cv.score(Right_amygdala_w2[train],anxious_arousal_w2[train]))) #execute LOO nested CV just on training set (NESTED)
	hparam[counter,0] = Ridge_cv.alpha_
	y_predict[counter,:]=Ridge_cv.predict(Right_amygdala_w2[test])
	y_truth[counter,:] = anxious_arousal_w2[test] 
	coefs[counter,:] = Ridge_cv.coef_
	counter = counter +1

print(hparam)

MSE = mean_squared_error(np.reshape(y_predict,len(anxious_arousal_w2)), np.reshape(y_truth,len(anxious_arousal_w2)))
CorrSp = scipy.stats.spearmanr(np.reshape(y_predict,len(anxious_arousal_w2)),np.reshape(y_truth,len(anxious_arousal_w2)))
CorrTau = scipy.stats.kendalltau(np.reshape(y_predict,len(anxious_arousal_w2)),np.reshape(y_truth,len(anxious_arousal_w2)))
CorrPear = scipy.stats.pearsonr(np.reshape(y_predict,len(anxious_arousal_w2)),np.reshape(y_truth,len(anxious_arousal_w2)))

print('Right Amyg to WAVE 2 MSE RIGHT:{} Corr Spearman:{} Corr Tau: {} Corr Pearson: {}\n\n'.format(MSE,CorrSp,CorrTau,CorrPear))
current_line=['Right Amyg with Anx Arousal',2,CorrPear,CorrSp]
master_csv.append(current_line)


y_predict = np.zeros((n_folds,13)) #rows=n_iterations, col=test_size
y_truth = np.zeros((n_folds,13))
coefs = np.zeros((n_folds,258))
hparam = np.zeros((n_folds,1))
counter = 0


for k, (train, test) in enumerate(kf.split(Left_amygdala_longitudinal,anxious_arousal_longitudinal)):
	Ridge_cv = linear_model.RidgeCV(alphas=np.arange(0.01,10,0.1))
	Ridge_cv.fit(Left_amygdala_longitudinal[train],anxious_arousal_longitudinal[train])
	print('R^2 of Ridge= {}'.format(Ridge_cv.score(Left_amygdala_longitudinal[train],anxious_arousal_longitudinal[train]))) #execute LOO nested CV just on training set (NESTED)
	hparam[counter,0] = Ridge_cv.alpha_
	y_predict[counter,:]=Ridge_cv.predict(Left_amygdala_longitudinal[test])
	y_truth[counter,:] = anxious_arousal_longitudinal[test]
	coefs[counter,:] = Ridge_cv.coef_
	counter = counter +1

print(hparam)

MSE = mean_squared_error(np.reshape(y_predict,len(anxious_arousal_longitudinal)), np.reshape(y_truth,len(anxious_arousal_longitudinal)))
CorrSp = scipy.stats.spearmanr(np.reshape(y_predict,len(anxious_arousal_longitudinal)),np.reshape(y_truth,len(anxious_arousal_longitudinal)))
CorrTau = scipy.stats.kendalltau(np.reshape(y_predict,len(anxious_arousal_longitudinal)),np.reshape(y_truth,len(anxious_arousal_longitudinal)))
CorrPear = scipy.stats.pearsonr(np.reshape(y_predict,len(anxious_arousal_longitudinal)),np.reshape(y_truth,len(anxious_arousal_longitudinal)))

print('Left Longitdinal MSE:{} Corr Spearman:{} Corr Tau: {} Corr Pearson: {}\n\n'.format(MSE,CorrSp,CorrTau,CorrPear))
current_line=['Left Amyg-Diff with Anx Arousal change','longitudinal',CorrPear,CorrSp]
master_csv.append(current_line)


y_predict = np.zeros((n_folds,13)) #rows=n_iterations, col=test_size
y_truth = np.zeros((n_folds,13))
coefs = np.zeros((n_folds,258))
hparam = np.zeros((n_folds,1))
counter = 0


for k, (train, test) in enumerate(kf.split(Right_amygdala_longitudinal,anxious_arousal_longitudinal)):
	Ridge_cv = linear_model.RidgeCV(alphas=np.arange(0.01,10,0.1))
	Ridge_cv.fit(Right_amygdala_longitudinal[train],anxious_arousal_longitudinal[train])
	print('R^2 of Ridge= {}'.format(Ridge_cv.score(Right_amygdala_longitudinal[train],anxious_arousal_longitudinal[train]))) #execute LOO nested CV just on training set (NESTED)
	hparam[counter,0] = Ridge_cv.alpha_
	y_predict[counter,:]=Ridge_cv.predict(Right_amygdala_longitudinal[test])
	y_truth[counter,:] = anxious_arousal_longitudinal[test]
	coefs[counter,:] = Ridge_cv.coef_
	counter = counter +1

print(hparam)

MSE = mean_squared_error(np.reshape(y_predict,len(anxious_arousal_longitudinal)), np.reshape(y_truth,len(anxious_arousal_longitudinal)))
CorrSp = scipy.stats.spearmanr(np.reshape(y_predict,len(anxious_arousal_longitudinal)),np.reshape(y_truth,len(anxious_arousal_longitudinal)))
CorrTau = scipy.stats.kendalltau(np.reshape(y_predict,len(anxious_arousal_longitudinal)),np.reshape(y_truth,len(anxious_arousal_longitudinal)))
CorrPear = scipy.stats.pearsonr(np.reshape(y_predict,len(anxious_arousal_longitudinal)),np.reshape(y_truth,len(anxious_arousal_longitudinal)))

print('RIGHT Long MSE:{} Corr Spearman:{} Corr Tau: {} Corr Pearson: {}\n\n'.format(MSE,CorrSp,CorrTau,CorrPear))
current_line=['Right Amyg-Diff with Anx Arousal change','longitudinal',CorrPear,CorrSp]
master_csv.append(current_line)


with open('RESULTS_Amygdala_DataDriven.csv','a') as f:
	writer=csv.writer(f)
	writer.writerows(master_csv)
