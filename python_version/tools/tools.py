#!/usr/bin/python3


'''
Make plots of 1D and 2D probablility distributions out of the ROOT histograms from EFTfitter.

Combine plots of 2 or 3 1D and 2D probablility distributions into a single plot.
'''

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

# Compute the CL regions
def getCL1D(cl, xmin, xmax, hist):

#     #  compute range of histogram
    xrange = np.abs(xmin)+np.abs(xmax)

    vol=np.sum(hist.values);
    
    vals = []
    for i in range(len(hist.values)):
        vals.append([i,hist.values[i]])
    vals=np.array(vals)
    vals=vals[vals[:,1].argsort()[::-1]]
    
    level1=0
    valsret=[]
    for i in vals:
        if np.sum(level1)<=vol*cl:
            level1+=i[1]
            valsret.append([i[0],i[1]])
        else:
            valsret.append([i[0],0.0])
    valsret=np.array(valsret)
    valsret=valsret[valsret[:,0].argsort()]
    
    x=[]
    y=[]
    for i in valsret:
        x.append(i[0])
        y.append(i[1])
        
    return x,y



def axis_names_1d(histname, euler=False):
    coeff_name=''
    y_name=''
    if not euler:
        if 'cptbR' in histname:
            coeff_name+=r'Re ( $c_{\varphi tb})$'
            y_name+=r'p ( Re ( $c_{\varphi tb}$ ) $|$ data )'
        elif 'cptbI' in histname:    
            coeff_name+=r'Im ( $c_{\varphi tb}$'
            y_name+=r'p ( Im ( $c_{\varphi tb}$ ) $|$ data )'
        elif 'cbwR' in histname:
            coeff_name+=r'Re ( $c_{bW}$ )'
            y_name+=r'p (  Re ( $c_{bW}$ ) $|$ data )'
        elif 'cbwI' in histname:
            coeff_name+=r'Im ( $c_{bW})$'
            y_name+=r'p ( Im ( $c_{bW}$ ) $|$ data )'
        elif 'ctwR' in histname:
            coeff_name+=r'Re ( $c_{tW}$ )'
            y_name+=r'p (  Re ( $c_{tW}$ ) $|$ data )'
        elif 'ctwI' in histname:
            coeff_name+=r'Im ( $c_{tW})$'
            y_name+=r'p ( Im ( $c_{tW}$ ) $|$ data )'
        elif 'cpq' in histname:
            coeff_name+=r'$c_{\varphi Q}$'
            y_name+=r'p (  $c_{\varphi Q}$ $|$ data )'
        elif 'cqq' in histname:
            coeff_name+=r'$c_{Qq}^{3,1}$'
            y_name+=r'p (  $c_{Qq}^{3,1}$ $|$ data )'
        elif 'P' in histname:
            coeff_name+=r'Polarization'
            y_name+=r'p (  Polarization $|$ data )'
        else:
            coeff_name='tmp'
            y_name=r'p \left( tmp | data \right)'
    else:
        if 'cptbR' in histname:
            coeff_name+=r'$|c_{\varphi tb}|$'
            y_name+=r'p (  $|c_{\varphi tb}|$ $|$ data )'
        elif 'cptbI' in histname:    
            coeff_name+=r'Arg($c_{\varphi tb}$)'
            y_name+=r'p (  Arg($c_{\varphi tb}$) $|$ data )'
        elif 'cbwR' in histname:
            coeff_name+=r'$|c_{bW}|$'
            y_name+=r'p (  $|c_{bW}|$ $|$ data )'
        elif 'cbwI' in histname:
            coeff_name+=r'Arg($c_{c_{bW}}$)'
            y_name+=r'p (  Arg($c_{c_{bW}}$) $|$ data )'
        elif 'ctwR' in histname:
            coeff_name+=r'$|c_{tW}|$'
            y_name+=r'p (  $|c_{tW}|$ $|$ data )'
        elif 'ctwI' in histname:
            coeff_name+=r'Arg($c_{c_{tW}}$)'
            y_name+=r'p (  Arg($c_{c_{tW}}$) $|$ data )'
        elif 'cpq' in histname:
            coeff_name+=r'$c_{\varphi Q}$'
            y_name+=r'p (  $c_{\varphi Q}$ $|$ data )'
        elif 'cqq' in histname:
            coeff_name+=r'$c_{Qq}^{3,1}$'
            y_name+=r'p (  $c_{Qq}^{3,1}$ $|$ data )'
        elif 'P' in histname:
            coeff_name+=r'Polarization'
            y_name+=r'p (  Polarization $|$ data )'
        else:
            coeff_name='tmp'
            y_name=r'p \left( tmp | data \right)'
    
    return coeff_name, y_name

def axis_names_2d(histname, euler=False):
    coeff_name=''
    if not euler:
        if 'cptbR' in histname:
            coeff_name+=r'$c_{\varphi tb}$'
        elif 'cptbI' in histname:    
            coeff_name+=r'Im($c_{\varphi tb}$'
        elif 'cbwR' in histname:
            coeff_name+=r'Re($c_{bW}$)'
        elif 'cbwI' in histname:
            coeff_name+=r'Im($c_{bW}$)'
        elif 'ctwR' in histname:
            coeff_name+=r'Re($c_{tW}$)'
        elif 'ctwI' in histname:
            coeff_name+=r'Im($c_{tW}$)'
        elif 'cpq' in histname:
            coeff_name+=r'$c_{\varphi Q}$'
        elif 'cqq' in histname:
            coeff_name+=r'$c_{Qq}^{3,1}$'
        elif 'P' in histname:
            coeff_name+=r'Polarization'
        else:
            coeff_name='tmp'
    else:
        if 'cptbR' in histname:
            coeff_name+=r'$|c_{\varphi tb}|$'
        elif 'cptbI' in histname:    
            coeff_name+=r'Arg($c_{\varphi tb})$'
        elif 'cbwR' in histname:
            coeff_name+=r'$|c_{bW}|$'
        elif 'cbwI' in histname:
            coeff_name+=r'Arg($c_{bW}$)'
        elif 'ctwR' in histname:
            coeff_name+=r'$|c_{tW}|$'
        elif 'ctwI' in histname:
            coeff_name+=r'Arg($c_{tW}$)'
        elif 'cpq' in histname:
            coeff_name+=r'$c_{\varphi Q}$'
        elif 'cqq' in histname:
            coeff_name+=r'$c_{Qq}^{3,1}$'
        elif 'P' in histname:
            coeff_name+=r'Polarization'
        else:
            coeff_name='tmp'
        
    return coeff_name


def plot_one_dim_histogram(histname, cly68, cly95, cly100, euler=False, color1='lime', color2='yellow', legend_loc='upper right'):
    plt.rc('font',**{'family':'sans-serif','sans-serif':['Helvetica']})
    ## for Palatino and other serif fonts use:
    #rc('font',**{'family':'serif','serif':['Palatino']})
    plt.rc('text', usetex=True)
    
    histname=histname.split(';')[0]
    
    coeff_name, y_name = axis_names_1d(histname, euler=euler)
    
    fig, ax = plt.subplots(1, 1, figsize=(10, 10))
    # ax.set_aspect(0.1)
    ax.set_xlabel(coeff_name, fontsize=32)
    ax.set_ylabel(y_name, fontsize=32)
    ax.plot(cly100, c='black')
    ax.fill_between([i for i in range(0,500)],0,cly95, edgecolor=color2, facecolor=color2, alpha=1)
    ax.fill_between([i for i in range(0,500)],0,cly68, edgecolor=color1, facecolor=color1, alpha=1)
    # ax[0,0].grid(b=True, which='both')
    
    ten_range=[]
    full_ten_range=[]
    long_range=[]
    pol_range=[]
    for i in range(-10,11,2):
        full_ten_range.append('$'+str(i)+'$')
    for i in range(0,11):
        ten_range.append('$'+str(i)+'$')
    for i in np.round(np.arange(0,40,5),decimals=0):
        long_range.append('$'+str(i)+'$')
    for i in np.round(np.arange(0,1.1,0.1),decimals=2):
        pol_range.append('$'+str(i)+'$')
    angle_range=[r'-$\pi$',r'-$\frac{\pi}{2}$',r'$0$',r'$\frac{\pi}{2}$',r'$\pi$']
    if 'cpq' in histname or 'cqq' in histname:
        x_range=full_ten_range
        div=10
    elif 'cptbR' in histname:
        x_range=long_range
        div=7
    elif 'cbwI' in histname or 'ctwI' in histname or 'cptbI' in histname:
        if not euler:
            x_range=full_ten_range
            div=10
        else:
            x_range=angle_range
            div=4
    elif 'cbwR' in histname or 'ctwR' in histname:
        if not euler:
            x_range=full_ten_range
            div=10
        else:
            x_range=ten_range
            div=5
    elif 'P' in histname:
        x_range=pol_range
        div=10
            
    plt.xticks(np.arange(0, 500*(1+1/div), 500/div), x_range)
    ax.tick_params(axis='both', which='major', labelsize=16, pad=10)
    
    yellow_patch = mpatches.Patch(color=color2, label=r'95.5\% CL')
    lime_patch = mpatches.Patch(color=color1, label=r'68.5\% CL')
    leg = plt.legend(handles=[yellow_patch,lime_patch], fontsize=24, loc=legend_loc)
    leg.get_frame().set_linewidth(0.0)

#     plt.tight_layout()
    plt.savefig('plots/1D/'+histname+'.pdf')
    plt.close()
    
    
    
def combine_one_dim_histogram(histname, cly_1, cly_2, cly100_1, cly100_2, measurement1=r'M1', measurement2=r'M2', euler=False, c1='purple', c2='gold', legend_loc='upper right'):
    plt.rc('font',**{'family':'sans-serif','sans-serif':['Helvetica']})
    plt.rc('text', usetex=True)
    
    histname=histname.split(';')[0]
    
    coeff_name, y_name = axis_names_1d(histname, euler=euler)
    
    fig, ax = plt.subplots(1, 1, figsize=(10, 10))
    # ax.set_aspect(0.1)
    ax.set_xlabel(coeff_name, fontsize=32)
    ax.set_ylabel(y_name, fontsize=32)
    ax.fill_between([i for i in range(0,500)],0,cly_1, edgecolor=c1, facecolor=c1, alpha=0.5)
    ax.fill_between([i for i in range(0,500)],0,cly_2, edgecolor=c2, facecolor=c2, alpha=0.5)
    # ax[0,0].grid(b=True, which='both')
    
    ten_range=[]
    full_ten_range=[]
    long_range=[]
    pol_range=[]
    for i in range(-10,11,2):
        full_ten_range.append('$'+str(i)+'$')
    for i in range(0,11):
        ten_range.append('$'+str(i)+'$')
    for i in np.round(np.arange(0,40,5),decimals=0):
        long_range.append('$'+str(i)+'$')
    for i in np.round(np.arange(0,1.1,0.1),decimals=2):
        pol_range.append('$'+str(i)+'$')
    angle_range=[r'-$\pi$',r'-$\frac{\pi}{2}$',r'$0$',r'$\frac{\pi}{2}$',r'$\pi$']
    if 'cpq' in histname or 'cqq' in histname:
        x_range=full_ten_range
        div=10
    elif 'cptbR' in histname:
        x_range=long_range
        div=7
    elif 'cbwI' in histname or 'ctwI' in histname or 'cptbI' in histname:
        if not euler:
            x_range=full_ten_range
            div=10
        else:
            x_range=angle_range
            div=4
    elif 'cbwR' in histname or 'ctwR' in histname:
        if not euler:
            x_range=full_ten_range
            div=10
        else:
            x_range=ten_range
            div=5
    elif 'P' in histname:
        x_range=pol_range
        div=10
        
    plt.xticks(np.arange(0, 500*(1+1/div), 500/div), x_range)
    ax.tick_params(axis='both', which='major', labelsize=16, pad=10)
    
    patch1 = mpatches.Patch(color=c1, label=measurement1)
    patch2 = mpatches.Patch(color=c2, label=measurement2)
    leg = plt.legend(handles=[patch1,patch2], fontsize=20, loc=legend_loc)
    leg.get_frame().set_linewidth(0.0)

#     plt.tight_layout()
    plt.savefig('plots/1D_combined/'+histname+'.pdf')
    plt.close()
    
    
    
def plot_two_dim_histogram(histname, c_min=-10, c_max=10, cptb_min=0, cptb_max=35, euler=False, color1='lime', color2='yellow', legend_loc='upper right'):
    histname=histname.split(';')[0]
    data_in=np.array(eftfitter[histname].values)
    plt.rc('font',**{'family':'sans-serif','sans-serif':['Helvetica']})
    plt.rc('text', usetex=True)
           
    coeff1, coeff2=histname.split('_0_')[1].split(';')[0].split('_')
    
    coeff_name_1 = axis_names_2d(coeff1, euler=euler)
    coeff_name_2 = axis_names_2d(coeff2, euler=euler)
    
    fig, ax = plt.subplots(1, 1, figsize=(10, 10))
    # ax.set_aspect(0.1)
    ax.set_xlabel(coeff_name_1, fontsize=32)
    ax.set_ylabel(coeff_name_2, fontsize=32)

    ten_range=[]
    full_ten_range=[]
    long_range=[]
    pol_range=[]
    for i in np.arange(c_min,c_max+1,2):
        full_ten_range.append('$'+str(i)+'$')
    for i in np.arange(0,c_max+1):
        ten_range.append('$'+str(i)+'$')
    for i in np.round(np.arange(cptb_min,cptb_max+5,5),decimals=0):
        long_range.append('$'+str(i)+'$')
    for i in np.round(np.arange(0,1.1,0.1),decimals=2):
        pol_range.append('$'+str(i)+'$')
    angle_range=[r'-$\pi$',r'-$\frac{\pi}{2}$',r'$0$',r'$\frac{\pi}{2}$',r'$\pi$']
    if 'cpq' in coeff1 or 'cqq' in coeff1:
        x_range=full_ten_range
        divx=10
    elif 'cptbR' in coeff1:
        x_range=long_range
        divx=7
    elif 'cbwI' in coeff1 or 'ctwI' in coeff1 or 'cptbI' in coeff1:
        if not euler:
            x_range=full_ten_range
            divx=10
        else:
            x_range=angle_range
            divx=4
    elif 'cbwR' in coeff1 or 'ctwR' in coeff1:
        if not euler:
            x_range=full_ten_range
            divx=10
        else:
            x_range=ten_range
            divx=5
    elif 'P' in coeff1:
        x_range=pol_range
        divx=10
    
    if 'cpq' in coeff2 or 'cqq' in coeff2:
        y_range=full_ten_range
        divy=10
    elif 'cptbR' in coeff2:
        y_range=long_range
        divy=7
    elif 'cbwI' in coeff2 or 'ctwI' in coeff2 or 'cptbI' in coeff2:
        if not euler:
            y_range=full_ten_range
            divy=10
        else:
            y_range=angle_range
            divy=4
    elif 'cbwR' in coeff2 or 'ctwR' in coeff2:
        if not euler:
            y_range=full_ten_range
            divy=10
        else:
            y_range=ten_range
            divy=5
    elif 'P' in coeff2:
        y_range=pol_range
        divy=10
    
    xmin_bin=0
    xmax_bin=500
    ymin_bin=0
    ymax_bin=500
    
    data=data_in[ymin_bin:ymax_bin-1,xmin_bin:xmax_bin]
    
    vol2d=np.sum(data)
    flat_2d=np.array(data).flatten()
    flat_2d[::-1].sort()
    level_2d=0
    cont_val_68=0
    cont_val_95=0
    for i in flat_2d:
        level_2d+=i
        if level_2d <= vol2d*0.685:
            cont_val_68=i
        elif level_2d > vol2d*0.685 and level_2d <= vol2d*0.955:
            cont_val_95=i
        else:
            break
    ax.contourf(data, levels=[cont_val_95,cont_val_68,10], colors=[color2,color1])
    # ax[0,0].grid(b=True, which='both')
    
    plt.xticks(np.arange(xmin_bin, xmax_bin*(1+1/divx), xmax_bin/divx), x_range)
    plt.yticks(np.arange(ymin_bin, ymax_bin*(1+1/divy), ymax_bin/divy), y_range)
    ax.tick_params(axis='both', which='major', labelsize=16, pad=10)
    ax.grid(b=True, which='both')
    
    yellow_patch = mpatches.Patch(color=color2, label=r'95.5\% CL')
    lime_patch = mpatches.Patch(color=color1, label=r'68.5\% CL')
    leg = plt.legend(handles=[yellow_patch,lime_patch], fontsize=16, loc=legend_loc)
    leg.get_frame().set_linewidth(0.0)

#     plt.tight_layout()
    plt.savefig('plots/2D/'+histname+'.pdf')
    plt.close()
    
    
    
    
def combine_two_dim_histogram(eftfitter1, eftfitter2, histname, measurement1="M1", measurement2="M2", euler=False, 
    color1='purple', color2='gold', legend_loc='upper right'):
    c_min=-10
    c_max=10
    cptb_min=0
    cptb_max=35   
    plt.rc('font',**{'family':'sans-serif','sans-serif':['Helvetica']})
    plt.rc('text', usetex=True)
    
    
    histname=histname.split(';')[0]
    data_in_1=np.array(eftfitter1[histname].values)
    data_in_2=np.array(eftfitter2[histname].values)
           
    coeff1, coeff2=histname.split('_0_')[1].split(';')[0].split('_')
    
    coeff_name_1 = axis_names_2d(coeff1, euler=euler)
    coeff_name_2 = axis_names_2d(coeff2, euler=euler)
    
    fig, ax = plt.subplots(1, 1, figsize=(10, 10))
    # ax.set_aspect(0.1)
    ax.set_xlabel(coeff_name_1, fontsize=32)
    ax.set_ylabel(coeff_name_2, fontsize=32)
    
    ten_range=[]
    full_ten_range=[]
    long_range=[]
    pol_range=[]
    for i in np.arange(c_min,c_max+1,2):
        full_ten_range.append('$'+str(i)+'$')
    for i in np.arange(0,c_max+1):
        ten_range.append('$'+str(i)+'$')
    for i in np.round(np.arange(cptb_min,cptb_max+5,5),decimals=0):
        long_range.append('$'+str(i)+'$')
    for i in np.round(np.arange(0,1.1,0.1),decimals=2):
        pol_range.append('$'+str(i)+'$')
    angle_range=[r'-$\pi$',r'-$\frac{\pi}{2}$',r'$0$',r'$\frac{\pi}{2}$',r'$\pi$']
    if 'cpq' in coeff1 or 'cqq' in coeff1:
        x_range=full_ten_range
        divx=10
    elif 'cptbR' in coeff1:
        x_range=long_range
        divx=7
    elif 'cbwI' in coeff1 or 'ctwI' in coeff1 or 'cptbI' in coeff1:
        if not euler:
            x_range=full_ten_range
            divx=10
        else:
            x_range=angle_range
            divx=4
    elif 'cbwR' in coeff1 or 'ctwR' in coeff1:
        if not euler:
            x_range=full_ten_range
            divx=10
        else:
            x_range=ten_range
            divx=5
    elif 'P' in coeff1:
        x_range=pol_range
        divx=10
        
    if 'cpq' in coeff2 or 'cqq' in coeff2:
        y_range=full_ten_range
        divy=10
    elif 'cptbR' in coeff2:
        y_range=long_range
        divy=7
    elif 'cbwI' in coeff2 or 'ctwI' in coeff2 or 'cptbI' in coeff2:
        if not euler:
            y_range=full_ten_range
            divy=10
        else:
            y_range=angle_range
            divy=4
    elif 'cbwR' in coeff2 or 'ctwR' in coeff2:
        if not euler:
            y_range=full_ten_range
            divy=10
        else:
            y_range=ten_range
            divy=5
    elif 'P' in coeff2:
        y_range=pol_range
        divy=10
    
    xmin_bin=0
    xmax_bin=500
    ymin_bin=0
    ymax_bin=500
        
    data1=data_in_1[ymin_bin:ymax_bin-1,xmin_bin:xmax_bin]
    data2=data_in_2[ymin_bin:ymax_bin-1,xmin_bin:xmax_bin]
    
    vol2d_1=np.sum(data1)
    vol2d_2=np.sum(data2)
    flat_2d_1=np.array(data1).flatten()
    flat_2d_1[::-1].sort()
    flat_2d_2=np.array(data2).flatten()
    flat_2d_2[::-1].sort()
    level_2d_1=0
    level_2d_2=0
    
    cont_val_95_1=0
    for i in flat_2d_1:
        level_2d_1+=i
        if level_2d_1 <= vol2d_1*0.955:
            cont_val_95_1=i
        else:
            break
    cont_val_95_2=0
    for i in flat_2d_2:
        level_2d_2+=i
        if level_2d_2 <= vol2d_2*0.955:
            cont_val_95_2=i
        else:
            break
            
#     color1='dodgerblue'
#     color2='red'
#     color2='limegreen'
    
    ax.contourf(data1, levels=[cont_val_95_1,10], colors=color1, alpha=0.7)
    ax.contourf(data2, levels=[cont_val_95_2,10], colors=color2, alpha=0.7)
    # ax[0,0].grid(b=True, which='both')
    
    plt.xticks(np.arange(xmin_bin, xmax_bin*(1+1/divx), xmax_bin/divx), x_range)
    plt.yticks(np.arange(ymin_bin, ymax_bin*(1+1/divy), ymax_bin/divy), y_range)
    ax.tick_params(axis='both', which='major', labelsize=16, pad=10)
    ax.grid(b=True, which='both')
    
    patch1 = mpatches.Patch(color=color1, label=measurement1)
    patch2 = mpatches.Patch(color=color2, label=measurement2)
    patch3 = mpatches.Patch(color='w', label=r'95\% CL')
    leg = plt.legend(handles=[patch1,patch2,patch3], fontsize=16, loc=legend_loc)
    leg.get_frame().set_linewidth(0.0)

#     plt.tight_layout()
    plt.savefig('plots/2D_combined/'+histname+'.pdf')
    plt.close()
    
    
    
    
def combine_three_histograms(eftfitter1, eftfitter2, eftfitter3, histname, measurement1="M1", measurement2="M2", measurement3="M3",color1='firebrick', color2='deepskyblue', color3='gold', legend_loc='lower right'):
    c_min=-10
    c_max=10
    cptb_min=0
    cptb_max=35   
    euler=False
    plt.rc('font',**{'family':'sans-serif','sans-serif':['Helvetica']})
    plt.rc('text', usetex=True)
    
    
    histname=histname.split(';')[0]
    data_in_1=np.array(eftfitter1[histname].values)
    data_in_2=np.array(eftfitter2[histname].values)
    data_in_3=np.array(eftfitter3[histname].values)
           
    coeff1, coeff2=histname.split('_0_')[1].split(';')[0].split('_')
    
    coeff_name_1 = axis_names_2d(coeff1, euler=euler)
    coeff_name_2 = axis_names_2d(coeff2, euler=euler)
    
    fig, ax = plt.subplots(1, 1, figsize=(10, 10))
    # ax.set_aspect(0.1)
    ax.set_xlabel(coeff_name_1, fontsize=32)
    ax.set_ylabel(coeff_name_2, fontsize=32)
    
    ten_range=[]
    full_ten_range=[]
    long_range=[]
    pol_range=[]
    for i in np.arange(c_min,c_max+1,2):
        full_ten_range.append('$'+str(i)+'$')
    for i in np.arange(0,c_max+1):
        ten_range.append('$'+str(i)+'$')
    for i in np.round(np.arange(cptb_min,cptb_max+5,5),decimals=0):
        long_range.append('$'+str(i)+'$')
    for i in np.round(np.arange(0,1.1,0.1),decimals=2):
        pol_range.append('$'+str(i)+'$')
    angle_range=[r'-$\pi$',r'-$\frac{\pi}{2}$',r'$0$',r'$\frac{\pi}{2}$',r'$\pi$']
    if 'cpq' in coeff1 or 'cqq' in coeff1:
        x_range=full_ten_range
        divx=10
    elif 'cptbR' in coeff1:
        x_range=long_range
        divx=7
    elif 'cbwI' in coeff1 or 'ctwI' in coeff1 or 'cptbI' in coeff1:
        if not euler:
            x_range=full_ten_range
            divx=10
        else:
            x_range=angle_range
            divx=4
    elif 'cbwR' in coeff1 or 'ctwR' in coeff1:
        if not euler:
            x_range=full_ten_range
            divx=10
        else:
            x_range=ten_range
            divx=5
    elif 'P' in coeff1:
        x_range=pol_range
        divx=10
        
    if 'cpq' in coeff2 or 'cqq' in coeff2:
        y_range=full_ten_range
        divy=10
    elif 'cptbR' in coeff2:
        y_range=long_range
        divy=7
    elif 'cbwI' in coeff2 or 'ctwI' in coeff2 or 'cptbI' in coeff2:
        if not euler:
            y_range=full_ten_range
            divy=10
        else:
            y_range=angle_range
            divy=4
    elif 'cbwR' in coeff2 or 'ctwR' in coeff2:
        if not euler:
            y_range=full_ten_range
            divy=10
        else:
            y_range=ten_range
            divy=5
    elif 'P' in coeff2:
        y_range=pol_range
        divy=10
    
    xmin_bin=0
    xmax_bin=500
    ymin_bin=0
    ymax_bin=500
        
    data1=data_in_1[ymin_bin:ymax_bin-1,xmin_bin:xmax_bin]
    data2=data_in_2[ymin_bin:ymax_bin-1,xmin_bin:xmax_bin]
    data3=data_in_3[ymin_bin:ymax_bin-1,xmin_bin:xmax_bin]
    
    vol2d_1=np.sum(data1)
    vol2d_2=np.sum(data2)
    vol2d_3=np.sum(data3)
    flat_2d_1=np.array(data1).flatten()
    flat_2d_1[::-1].sort()
    flat_2d_2=np.array(data2).flatten()
    flat_2d_2[::-1].sort()
    flat_2d_3=np.array(data3).flatten()
    flat_2d_3[::-1].sort()
    level_2d_1=0
    level_2d_2=0
    level_2d_3=0
    
    cont_val_95_1=0
    for i in flat_2d_1:
        level_2d_1+=i
        if level_2d_1 <= vol2d_1*0.685:
            cont_val_95_1=i
        else:
            break
    cont_val_95_2=0
    for i in flat_2d_2:
        level_2d_2+=i
        if level_2d_2 <= vol2d_2*0.685:
            cont_val_95_2=i
        else:
            break
    cont_val_95_3=0
    for i in flat_2d_3:
        level_2d_3+=i
        if level_2d_3 <= vol2d_3*0.685:
            cont_val_95_3=i
        else:
            break
            
#     color1='dodgerblue'
#     color2='red'
    
    ax.contourf(data1, levels=[cont_val_95_1,10], colors=color1, alpha=0.7)
    ax.contourf(data2, levels=[cont_val_95_2,10], colors=color2, alpha=0.7)
    ax.contourf(data3, levels=[cont_val_95_3,10], colors=color3, alpha=0.9)
    # ax[0,0].grid(b=True, which='both')
    
    plt.xticks(np.arange(xmin_bin, xmax_bin*(1+1/divx), xmax_bin/divx), x_range)
    plt.yticks(np.arange(ymin_bin, ymax_bin*(1+1/divy), ymax_bin/divy), y_range)
    ax.tick_params(axis='both', which='major', labelsize=16, pad=10)
    ax.grid(b=True, which='both')
    
    patch1 = mpatches.Patch(color=color1, label=measurement1)
    patch2 = mpatches.Patch(color=color2, label=measurement2)
    patch3 = mpatches.Patch(color=color3, label=measurement3)
    patch4 = mpatches.Patch(color='w', label=r'95\% CL')
    leg = plt.legend(handles=[patch1,patch2,patch3,patch4], fontsize=16, loc=legend_loc)
    leg.get_frame().set_linewidth(0.0)

#     plt.tight_layout()
    plt.savefig('plots/3_combined/'+histname+'.pdf')
    plt.close()