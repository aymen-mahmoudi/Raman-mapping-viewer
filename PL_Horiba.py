import pandas as pd
import numpy as np
import seaborn as sns
from matplotlib import pyplot as plt
import cv2

def op_apply(w1,w2,a,b,op):
    if op=='+':
        res = w1*a + w2*b
    elif op == '-':
        res = w1*a - w2*b
    elif op == '*':
        res = w1*a * w2*b
    elif op == '/':
        res = w1*a / w2*b
    else:
        raise TypeError("w1 and w2 must be float and op must be '+', '-', '*' or '/'") 
    return res


def horiba_data_transformer(path):
    data = pd.read_csv(path, header = None,sep='\t')
    data=data.fillna(0)
    da=data.to_numpy()
    data1=pd.DataFrame(da,index=da[:,0], columns=da[0,:])
    data_new=data1.drop(index=0.00000, columns=0.0000)
    df=data_new[::-1].iloc[:, ::-1]
    col1=df.index.to_numpy()
    x1=[]
    c=np.linspace(0,col1.max()-col1.min(),len(col1))
    for i in c:
        x1.append(round(i,2))
        
    row1=df.columns.to_numpy()
    r=np.linspace(0,row1.max()-row1.min(),len(row1))
    f1=[]
    for i in r:
        f1.append(round(i,2))
    s=df.to_numpy()
    data2=pd.DataFrame(s,index=x1, columns=f1)
    return data2

def Horiba_plot(path,colormap,a,title):
    
    fig= plt.figure(figsize=(6,5),dpi = a)
    fig.suptitle(title, fontsize=16)
    
    sns.heatmap(data=horiba_data_transformer(path),cmap=colormap,xticklabels=20, yticklabels=20)
    plt.xlabel("X (μm)", fontsize=12)
    plt.ylabel("Y (μm)", fontsize=12)
    #plt.savefig("Map Horiba.png")



def Horiba_plot_binary(path,colormap,a,title,threshold):
 
    #print('ttt ',type(data2))
    arr = horiba_data_transformer(path).to_numpy()
    #print('ttrrrt ',type(arr))
    #print('maximm ',arr.max())
    #print(np.shape(arr))
    #print(arr.shape[0])
    
    #print(arr[2,4])
    
    

    for i in range(arr.shape[0]):
        for j in range(arr.shape[1]):
            x = arr[i,j]
            if x < threshold :
                arr[i,j] = 0
            else :
                arr[i,j] = 1
    #print(arr)


    fig= plt.figure(figsize=(6,5),dpi = a)
    fig.suptitle(title, fontsize=16)
    
    sns.heatmap(data=arr,cmap=colormap,xticklabels=20, yticklabels=20)
    plt.xlabel("X (μm)", fontsize=12)
    plt.ylabel("Y (μm)", fontsize=12)
    #plt.savefig("Map Horiba.png")



def Horiba_Raman_PL_plot(path,colormap,dpi,title,binary,threshold):
    if binary:
        Horiba_plot_binary(path,colormap,dpi,title,threshold)
    else:
        Horiba_plot(path,colormap,dpi,title)
        
        
        
def Horiba_plot_combinaison(path1,path2,w1,w2,op,colormap,dpi,triple_fig):
    data1=horiba_data_transformer(path1)
    data2=horiba_data_transformer(path2)
    data3=op_apply(w1,w2,data1,data2,op)
    
    if triple_fig:
        fig, axes = plt.subplots(1, 3, figsize=(15, 5))
        sns.heatmap(data1, annot=False, fmt=".1f", cmap=colormap, ax=axes[0])
        axes[0].set_title("data 1")
        sns.heatmap(data2, annot=False, fmt=".1f", cmap=colormap, ax=axes[1])
        axes[1].set_title("data 2")
        sns.heatmap(data3, annot=False, fmt=".1f", cmap=colormap, ax=axes[2])
        axes[2].set_title("str(w1)+'*map1 '+op+' '+str(w1)+'*map2'")
        plt.tight_layout()
        plt.show()
        
    else:
        fig= plt.figure(figsize=(6,5),dpi = dpi)
        fig.suptitle(str(w1)+'*map1 '+op+' '+str(w1)+'*map2', fontsize=16)

        sns.heatmap(data3,cmap=colormap,xticklabels=20, yticklabels=20)
        plt.xlabel("X (μm)", fontsize=12)
        plt.ylabel("Y (μm)", fontsize=12)


