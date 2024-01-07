#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 26 23:18:53 2023

@author: okapi
"""

import numpy as np
import pandas as pd


SUBJECTS = ['S0' + str(ii) for ii in np.arange(1,10)] + ['S' + str(ii) for ii in np.arange(10,17)] 

times = np.arange(-1.7,1.2001,1/600)

# select this time interval
tmin = np.argmin(np.abs(times+0.8))
tmax = np.argmin(np.abs(times-0.3))+1

imposed_rot = pd.read_csv('/run/media/okapi/TOSHIBA EXT/elbow_rot_imposed.csv') 


for s, subj in enumerate(SUBJECTS):
    
    
    #load rotation values in each trial
    #and normalize by imposed condition
    imp = imposed_rot[imposed_rot['Subjects']==subj]['Mean elbow rot'].iloc[0]
    rot = np.load('/run/media/okapi/TOSHIBA EXT/' + subj + '_elbow_rot_unnorm_cleaned.npy')/imp 

    
    # here we log10-transform power data 
    # but not beta volume as it has zeros (so you need to add non-zero small value + result doesn't improve)

    # this is the selection of vertices from M1 we use based on cluster analysis of source data (TFCE-corrected)
    #10Hz: [ 2,  4, 22, 23, 27, 36, 37]
    #12Hz: [ 0,  1,  2,  3,  4,  5,  6,  9, 10, 13, 15, 18, 20, 22, 23, 24, 25, 27, 28, 30, 36, 37, 38, 39, 40, 43, 44, 51, 52, 53, 54]
    #15Hz: [ 1,  2,  3,  4,  5,  6,  9, 10, 11, 12, 15, 20, 21, 22, 23, 24, 25, 26, 27, 28, 30, 31, 36, 37, 38, 42, 43, 44, 45, 48, 49, 50, 51, 52, 53, 54]
    # for beta volume we use vertices for 15Hz, at least by now
    
    #z-scoring is important to take into account individual variability in alpha/beta
   
    # 10Hz power: load, log10 transform, average over vertices, z-transform
    alpha = np.load('/run/media/okapi/TOSHIBA EXT/'+subj+'_power_10Hz_unnorm_superlet_3_20_17-12_indepo_in_M1_clusterbased_vertexselection.npy')
    alpha = np.log10(alpha).mean(1)
    alpha = (alpha - np.mean(alpha))/ np.std(alpha)

    # 12Hz power: load, log10 transform, average over vertices, z-transform
    alpha2 = np.load('/run/media/okapi/TOSHIBA EXT/'+subj+'_power_12Hz_unnorm_superlet_3_20_17-12_indepo_in_M1_clusterbased_vertexselection.npy')
    alpha2 = np.log10(alpha2).mean(1)
    alpha2 = (alpha2 - np.mean(alpha2))/ np.std(alpha2)
    
    # 15Hz power: load, log10 transform, average over vertices, z-transform
    beta = np.load('/run/media/okapi/TOSHIBA EXT/'+subj+'_power_15Hz_unnorm_superlet_3_20_17-12_indepo_in_M1_clusterbased_vertexselection.npy')
    beta = np.log10(beta).mean(1)
    beta = (beta - np.mean(beta))/ np.std(beta)

    # beta volume: load, average over vertices, z-transform
    beta2 = np.load('/run/media/okapi/TOSHIBA EXT/'+subj+'_betavolume_13-30Hz_unnorm_superlet_4_40_17-12_indepo_in_M1_clusterbased_vertexselection.npy')
    beta2 = beta2.mean(0)
    beta2 = (beta2 - np.mean(beta2))/ np.std(beta2)
    
    # create dataframes for each trial and merge them for each subject, then save
    df = pd.DataFrame()
    for tr in range(alpha.shape[0]):
            
        df_time = pd.DataFrame({'Subject': subj,
                                    'Label': 'M1',
                                    'Trial': tr,
                                    'Time': times[tmin:tmax],
                                    'AlphaPower10': alpha[tr,tmin:tmax],
                                    'AlphaPower12': alpha2[tr,tmin:tmax],
                                    'BetaPower15': beta[tr,tmin:tmax], 
                                    'BetaVolume': beta2[tr,tmin:tmax], 
                                    'Rotation': rot[tr]})
        df = pd.concat([df, df_time])
        
    df.to_csv('/run/media/okapi/TOSHIBA EXT/for_r/' + subj + '_M1_superlet_20_alpha10_and_12_beta15_and_betavolume_rot_inh_-08to03_allepo_centered_ind_vert.csv')
            