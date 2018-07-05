# -*- coding: utf-8 -*-
"""
    cardiowheel.hrv
    ---------------

    This module provides various methods to perform
    Heart Rate Variability (HRV) analysis.

    :copyright: (c) 2016 by CardioID Technologies Lda.
    :license: All rights reserved.
"""

# Imports
# built-in

# 3rd party
import matplotlib.patches as patches
import matplotlib.path as path
import matplotlib.pyplot as plt
import numpy as np
import scipy.signal as ss
from scipy import interpolate
from sklearn import metrics
from sklearn.metrics import mean_squared_error
import math
from math import acos, hypot

# local

# Globals


def rr_resample(ts, RR, sampling_rate=4.0):
    """Resample a sequence of RR intervals into an evenly sampled signal.
    
    Uses cubic spline interpolation.
    
    Parameters
    ----------
    ts : array
        Input time reference.
    RR : array
        Input RR signal.
    sampling_rate : int, float, optional
        Sampling frequency of resampled signal.
    
    Returns
    -------
    ts_r : array
        Resampled time reference.
    RR_r : array
        Resampled RR signal.
    
    """
    
#    # interpolate
#    cs = interpolate.interp1d(ts, RR, kind='linear')
#    # resample
    dt = 1. / float(sampling_rate)
    ts_r = np.arange(ts[0], ts[-1], dt)
#    RR_r = cs(ts_r)
    
    RR_r=np.array([]);
    for i in range(0,len(ts_r)-1):
        
        if any(ts==ts_r[i]):
            pos=np.where(ts==ts_r[i]);
            RR_r=np.append(RR_r,RR[pos]);
        else:
            x0=ts[ts<ts_r[i]];
            if len(ts)>1: 
                x0=x0[-1];
            x1=ts[ts>ts_r[i]];
            if len(x1)>1: 
                x1=x1[0];

            pos=np.where(ts==x0);
            y0=RR[pos];
            pos=np.where(ts==x1);
            y1=RR[pos];
            RR_r=np.append(RR_r,y0+(y1-y0)*(ts_r[i]-x0)/(x1-x0));
    
    
    return ts_r, RR_r 


def time_features(RR, nbins=512, pNN_max=1.0):
    """Compute time-domain HRV features.
    
    Parameters
    ----------
    RR : array
        Input RR signal.
    nbins : int, optional
        Number of bins to use in pNNx histogram.
    pNN_max : float, optional
        Maximum range for the pNNx histogram.
    
    Returns
    -------
    HR : array
        Instantaneous heart rate.
    RMSSD : float
        Root mean square of successive RR differences.
    mNN : float
        Average RR.
    sdNN : float
        RR standard deviation.
    mHR : float
        Average HR.
    sdHR : float
        HR standard deviation.
    bins : array
        pNNx histogram bins.
    pNNx : array
        Histogram of successive RR diferences.
    pNN50 : float
        Fraction of consecutive RR intervals that differ by more than 50 ms.
    
    """
    
    HR = 60. / RR
    
    dRR = np.diff(RR)
    RMSSD = np.sqrt(np.mean(dRR**2))
    
    sdNN = np.std(RR, ddof=1)
    mNN = np.mean(RR)
    
    sdHR = np.std(HR, ddof=1)
    mHR = np.mean(HR)
    
    adRR = np.abs(dRR)
    A = float(len(dRR))
    pNNx, bins = np.histogram(adRR, bins=nbins, range=(0, pNN_max),
                              density=False)
    pNNx = pNNx / A
    pNN50 = np.sum(adRR > 0.05) / A
    
    return HR, RMSSD, mNN, sdNN, mHR, sdHR, bins, pNNx, pNN50


def plot_pNNx(bins, pNNx):
    """Plot the pNNx histogram.
    
    Parameters
    ----------
    bins : array
        pNNx histogram bins.
    pNNx : array
        Histogram of successive RR diferences.
    
    """
    
    fig = plt.figure()
    ax = fig.add_subplot(111)
    
    # get the corners of the rectangles for the histogram
    left = np.array(bins[:-1])
    right = np.array(bins[1:])
    bottom = np.zeros(len(left))
    top = bottom + pNNx
    
    # we need a (numrects x numsides x 2) numpy array for the path helper
    # function to build a compound path
    XY = np.array([[left, left, right, right], [bottom, top, top, bottom]]).T
    
    # get the Path object
    barpath = path.Path.make_compound_path_from_polys(XY)
    
    # make a patch out of it
    patch = patches.PathPatch(barpath, facecolor='blue', edgecolor='gray',
                              alpha=0.8)
    ax.add_patch(patch)
    
    # update the view limits
    ax.set_xlim(left[0], right[-1])
    ax.set_ylim(bottom.min(), top.max())
    
    ax.grid()
    plt.show()


def frequency_features(ts, RR, sampling_rate=4.0):
    """Compute frequency-domain HRV features.
    
    Parameters
    ----------
    ts : array
        Input time reference.
    RR : array
        Input RR signal.
    sampling_rate : int, float, optional
        Sampling frequency for resampled signal.
    
    Returns
    -------
    its : array
        Interpolated RR time reference.
    iRR : array
        Interpolated instantaneous RR intervals.
    iHR : array
        Interpolated instantaneous heart rate.
    VLF : float
        Very low frequency band power [0.003, 0.04) Hz.
    LF : float
        Low frquency band power [0.04, 0.15) Hz.
    HF : float
        High frequency band power [0.15, 0.4) Hz.
    TF : float
        Total power in the VLF, LF, and HF bands.
    L2HF : float
        Ratio of LF to HF power.
    nuLF : float
        LF power in normalized units.
    nuHF : float
        HF power in normalized units.
    
    """
    
    # resample
    its, iRR = rr_resample(ts, RR, sampling_rate=sampling_rate)
    iHR = 60. / iRR
    
    size = int(5 * sampling_rate)
    f, pwr = ss.welch(iRR, sampling_rate, window='hann', nperseg=size,
                      noverlap=size/2, nfft=1024, scaling='density')
    
    # VLF
    idx = np.logical_and(0.003 <= f, f < 0.04)
    x = f[idx]
    y = pwr[idx]
    VLF = metrics.auc(x, y)
    
    # LF
    idx = np.logical_and(0.04 <= f, f < 0.15)
    x = f[idx]
    y = pwr[idx]
    LF = metrics.auc(x, y)
    
    # HF
    idx = np.logical_and(0.15 <= f, f < 0.4)
    x = f[idx]
    y = pwr[idx]
    HF = metrics.auc(x, y)
    
    TF = VLF + LF + HF
    L2HF = LF / HF
    nuLF = LF / (TF - VLF)
    nuHF = HF / (TF - VLF)
    
    return its, iRR, iHR, VLF, LF, HF, TF, L2HF, nuLF, nuHF, f, pwr

def nonlinear_features(R, Fs):
    """Compute Heart Rate Variability (HRV) metrics
    from a sequence of R peak locations.
    
    Parameters
    ----------
    R : array
        R peak positions (samples).
    Fs :      int
        Sampling Frequency
    Returns
    -------
    SD1 : float
        Dispersion of the points (Standard Deviation) around the 45 degrees axis
    SD2 : float
        Dispersion of the points (Standard Deviation) around the 135 degrees axis  
    SD2SD1: float
        SD2/SD1 ratio
    eig1 : float
        First Eigen value of the Principal Component Analysis.
    eig2 : float
        Second Eigen value of the Principal Component Analysis.
    SD1pca : float
        Dispersion of the points (Standard Deviation) around the axis of the first principal component.
    SD2pca : float
        Dispersion of the points (Standard Deviation) around the axis of the second principal component.
    SD2SD1pca : float
        SD2pca/SD1pca ratio.
    mse_V : float
        Mean squared error between the 45 degrees rotation matrix and the principal directions matrix.
    error_SD1 : float
        Relative error between SD1 and SD1pca.
    error_SD2 : float
        Relative error between SD2 and SD2pca.
    error_SD2SD1 : float
        Relative error between SD2SD1 and SD2SD1pca.
    """
#    R = R * Fs
    
    Rn = np.diff(R)
    Rnn = Rn[1:]
    Rn = Rn[0:-1]
    
    Table = np.array([Rn, Rnn])
    V45 = np.array([[1/np.sqrt(2),-1/np.sqrt(2)],[1/np.sqrt(2),1/np.sqrt(2)]]);
    Table_ = np.matmul(V45, Table, out=None)
    SD1 = np.sqrt(np.var(Table_[0,:]))
    SD2 = np.sqrt(np.var(Table_[1,:]))
    SD2SD1 = SD2/SD1
    
    Rn0 = np.mean(Rn)
    Rnn0 = np.mean(Rnn)
    
    Table_cent = np.array([Rn-Rn0, Rnn-Rnn0])
    cov_matrix = np.matmul(Table_cent, Table_cent.T, out=None)/len(Rn)
    W,Vpca = np.linalg.eig(cov_matrix)
    
    if Vpca[0,0] < 0: 
        vpca0=math.asin(-Vpca[0,0])
        v450=math.asin(-V45[0,1])
    else:
        vpca0=math.acos(Vpca[0,0])
        v450=math.acos(V45[0,0])
               

    if W[0]<W[1]:
        eig1 = W[0]
        eig2 = W[1]
    else:
        eig1 = W[1]
        eig2 = W[0]

    Table_pca =  np.matmul(Vpca, Table, out=None)
    SD1pca = np.sqrt(np.var(Table_pca[0,:]))
    SD2pca = np.sqrt(np.var(Table_pca[1,:]))
    if SD1>SD2 and SD1pca>SD2pca: 
        pass
    else:
        if SD1<SD2 and SD1pca<SD2pca:
            pass
        else:
            aux=SD1pca
            SD1pca=SD2pca
            SD2pca=aux
            
    SD2SD1pca = SD2pca/SD1pca
    
    
#    mse_V = mean_squared_error(V45,Vpca)
    mse_V=vpca0-v450
    error_SD1 = np.abs(SD1-SD1pca)/SD1
    error_SD2 = np.abs(SD2-SD2pca)/SD2
    error_SD2SD1 = np.abs(SD2SD1-SD2SD1pca)/SD2SD1

    alpha = np.array([])
    area = np.array([])
    for i in range(0,len(Rn)-3):
        aux = (Rn[i]*Rn[i+1]+Rn[i+1]*Rn[i+2])/(hypot(Rn[i],Rn[i+1])+hypot(Rn[i+1],Rn[i+2]))
        aux2 = 0.5*abs(Rn[i]*(Rn[i+2]-Rn[i+3])-Rn[i+1]*(Rn[i+1]-Rn[i+3])+Rn[i+2]*(Rn[i+1]-Rn[i+2]))
        alpha = np.append(alpha,acos(aux))
        area = np.append(area,aux2)
    alpha = np.mean(alpha)
    area = np.mean(area)
    
    return SD1, SD2, SD2SD1, eig1, eig2, SD1pca, SD2pca, SD2SD1pca, Vpca, mse_V, error_SD1, error_SD2, error_SD2SD1, alpha, area #incluir en outputs

def hrv(R, sampling_rate):
    """Compute Heart Rate Variability (HRV) metrics
    from a sequence of R peak locations.
    
    Parameters
    ----------
    R : array
        R peak positions (samples).
    sampling_rate : int, float
        Sampling rate (Hz).
    
    Returns
    -------
    ts : array
        RR time reference.
    RR : array
        Instantaneous RR intervals.
    HR : array
        Instantaneous heart rate.
    its : array
        Interpolated RR time reference.
    iRR : array
        Interpolated instantaneous RR intervals.
    iHR : array
        Interpolated instantaneous heart rate.
    f   : array
        Frequencies to represent spectrogram.
    pwr: array
        Power of the Welch spectrum.
    features : dict
        A dictionary containing the computed metrics:
        RMSSD : float
        Root mean square of successive RR differences.
        mNN : float
            Average RR.
        sdNN : float
            RR standard deviation.
        mHR : float
            Average HR.
        sdHR : float
            HR standard deviation.
        bins : array
            pNNx histogram bins.
        pNNx : array
            Histogram of successive RR diferences.
        pNN50 : float
            Fraction of consecutive RR intervals that differ by more than 50 ms.
        VLF : float
            Very low frequency band power [0.003, 0.04) Hz.
        LF : float
            Low frquency band power [0.04, 0.15) Hz.
        HF : float
            High frequency band power [0.15, 0.4) Hz.
        TF : float
            Total power in the VLF, LF, and HF bands.
        L2HF : float
            Ratio of LF to HF power.
        nuLF : float
            LF power in normalized units.
        nuHF : float
            HF power in normalized units.
    
    Raises
    ------
    ValueError
        If there are not ebough R peaks to perform computations.
    
    """
    
    # ensure array of floats
    R = np.array(R, dtype='float')
    
    if len(R) < 4:
        raise ValueError("Not enough R peaks to perform computations.")
    
    # ensure float
    Fs = float(sampling_rate)
    
    # convert samples to time units
    R /= Fs
    
    # compute RR and exclude values outside physiological limits (HR > 200 and HR < 40)
    RR = np.diff(R)
    ts = R[:-1] + RR / 2
    
    #remove hr out of physiological accepted values
    indy = np.nonzero(np.logical_and(RR >= 60./220, RR <= 60./40))
    ts = ts[indy]
    RR = RR[indy]
    
    hr = 60./RR
    
#    print hr
    # remove outliers
    index = 0
    removeIndex = []
    
    for i in range(0,len(RR)-1,1):
        if abs(hr[i+1]-hr[index]) > 40: # and abs(ts[i+1]-ts[index])<1500:
            if index == 0 and abs(hr[index]-np.mean(hr))>20:
                index = i+1
                
            removeIndex.append(i+1)
        else:
            index = i+1
      
    ts = np.delete(ts, np.array(removeIndex))
    RR = np.delete(RR, np.array(removeIndex))

    if len(RR)<5:
        HR, RMSSD, mNN, sdNN, mHR, sdHR, bins, pNNx, pNN50 = [-1], [-1], [-1], [-1], [-1], [-1], [-1], [-1], [-1]
        its, iRR, iHR, VLF, LF, HF, TF, L2HF, nuLF, nuHF, f, pwr = [-1], [-1], [-1], [-1], [-1], [-1], [-1], [-1], [-1], [-1], [-1], [-1]
        SD1, SD2, SD2SD1, eig1, eig2, SD1pca, SD2pca, SD2SD1pca, Vpca, mse_V, error_SD1, error_SD2, error_SD2SD1, alpha, area = [-1], [-1], [-1], [-1], [-1], [-1], [-1], [-1], [-1], [-1], [-1], [-1],[-1], [-1], [-1]
    else:
        # time domain
        aux = time_features(RR, nbins=512, pNN_max=1.0)
        HR, RMSSD, mNN, sdNN, mHR, sdHR, bins, pNNx, pNN50 = aux
        # frquency domain
        bux = frequency_features(ts, RR, sampling_rate=4.0)
        its, iRR, iHR, VLF, LF, HF, TF, L2HF, nuLF, nuHF, f, pwr = bux
        
        #nonlinear features (geometric features)
        cux = nonlinear_features(R, Fs)
        SD1, SD2, SD2SD1, eig1, eig2, SD1pca, SD2pca, SD2SD1pca, Vpca, mse_V, error_SD1, error_SD2, error_SD2SD1, alpha, area = cux
        
    
    features = {
        'VLF': VLF,
        'LF': LF,
        'HF': HF,
        'TF': TF,
        'L2HF': L2HF,
        'nuLF': nuLF,
        'nuHF': nuHF,
        'RMSSD': RMSSD,
        'sdNN': sdNN,
        'mNN': mNN,
        'sdHR': sdHR,
        'mHR': mHR,
        'bins': bins,
        'pNNx': pNNx,
        'pNN50': pNN50,
        'SD1': SD1,
        'SD2': SD2,
        'SD2SD1': SD2SD1,
        'eig1': eig1,
        'eig2': eig2,
        'SD1pca': SD1pca, 
        'SD2pca': SD2pca, 
        'SD2SD1pca': SD2SD1pca, 
        'mse_V': mse_V, 
        'error_SD1': error_SD1, 
        'error_SD2': error_SD2, 
        'error_SD2SD1': error_SD2SD1,
        'alpha':    alpha,
        'area': area
    }
    
    return ts, RR, HR, its, iRR, iHR, f, pwr, Vpca, features

