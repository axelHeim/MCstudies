import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def df_call(df,col_name,filter_col,greater_than,filter_errors=False,error=-1):
    if filter_col != '' and (error != -1 and filter_errors==True):
        return df[(df[filter_col] > greater_than) & (df["num errors"]== error)][col_name]
    
    elif filter_col != '':
        return df[df[filter_col] > greater_than][col_name]
    
    elif error != -1 and filter_errors==True:
        return df[(df["num errors"]== error)][col_name]
      
    else:
        return df[col_name]


def plot_histos_pandas_df(df,col_name,bins,density,title,xlabel,ylabel,save_path,legendpos="right",filter_col='',greater_than=0):
    figsize=(16,10)
    plt.rcParams.update({'font.size': 13})

    fig, ax = plt.subplots()

    fig.set_size_inches(figsize)
    colors = ['b', 'g', 'r', 'y', 'm', 'c', 'k']

    fig.suptitle(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    
    
    df_tmp = df_call(df,col_name,filter_col,greater_than)
    mean_all = round(df_tmp.mean(),2)
    std_all = round(df_tmp.std(),2)
    num_all = df_tmp.shape[0]

    n, bins, patches = ax.hist(df[col_name],
            bins=bins,
            density=density, alpha=0.0,histtype='step')

    elem = np.argmax(n)
    peak = round((bins[elem] + bins[elem+1])/2.,2)

    
    ax.hist(df_tmp,
            bins=bins,
            density=density, alpha=0.5, label=(r'all, $\overline{x}$='+ str(mean_all) + ', std='+ str(std_all) + 
                                               ', peak='+str(peak)+', N='+str(num_all)),color=colors[0],histtype='step')


    for i in range(3):
        df_tmp = df_call(df,col_name,filter_col,greater_than,filter_errors=True,error=i)
        mean_filter = round(df_tmp.mean(),2)
        std_filter = round(df_tmp.std(),2)
        num_filter = df_tmp.shape[0]
        
        n, bins, patches = ax.hist(df_tmp,
            bins=bins,
            density=density, alpha=0.0,histtype='step')

        elem = np.argmax(n)
        peak_filter = round((bins[elem] + bins[elem+1])/2.,2)


        ax.hist(df_tmp,
                bins=bins,
                density=density, alpha=0.5, label=(str(i) + r' errors, $\overline{x}$='+ str(mean_filter) + 
                        ', std='+ str(std_filter) + ', peak='+str(peak_filter)+', N='+str(num_filter) )
                ,color=colors[i+1],histtype='step')





    ax.legend(loc=f'upper {legendpos}')

    plt.savefig(save_path)