#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import datetime
import time
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
from IPython.display import HTML


# In[2]:


url = 'https://raw.githubusercontent.com/839Studio/Novel-Coronavirus-Updates/master/Updates_NC.csv'
df = pd.read_csv(url, error_bad_lines=False)


# In[3]:


df.head()


# In[4]:


df2=df[['报道时间','省份','城市','新增确诊','新增出院','新增死亡']]


# In[5]:


df2.columns=['Date','Prov','City','Newcase','Cured','Death']
df2=df2.fillna(0) 


# In[6]:


def convertdate(date):
    array=time.strptime(date, u"%m月%d日")
    return time.strftime("%m-%d", array)


# In[7]:


df2['Date'] = df2['Date'].apply(convertdate)


# In[8]:


df2.sort_values('Date',inplace= True)
df2.reset_index(drop=True,inplace=True)


# In[9]:


def Date_interval_list(date_start = None,date_end = None):
 
    if date_start is None:
        date_start = '01-01'
    if date_end is None:
        date_end = datetime.datetime.now().strftime('%m-%d')
 
    date_start=datetime.datetime.strptime(date_start,'%m-%d')
    date_end=datetime.datetime.strptime(date_end,'%m-%d')
    date_list = []
    date_list.append(date_start.strftime('%m-%d'))
    while date_start < date_end:
        date_start+=datetime.timedelta(days=+1)# 日期加一天
        date_list.append(date_start.strftime('%m-%d'))# 日期存入列表
    return pd.DataFrame(date_list)


# In[10]:


start_date=df2['Date'].min()
end_date=df2['Date'].max()
dat=Date_interval_list(start_date, end_date)


# In[11]:


dat.columns=['Date']
dat.loc['new']=['02-29']
dat.sort_values('Date',inplace= True)
dat.reset_index(drop=True,inplace=True)


# In[12]:


df2=pd.merge(dat,df2, how='left', on=('Date'),suffixes=('',''))
df2=df2.fillna(0) 


# In[13]:


df2['Newcase']=df2['Newcase'].astype('int')
df2['Cured']=df2['Cured'].astype('int')
df2['Death']=df2['Death'].astype('int')


# In[14]:


df2[['CumNewcase']]=df2[['Newcase']].cumsum()
df2[['CumCured']]=df2[['Cured']].cumsum()
df2[['CumDeath']]=df2[['Death']].cumsum()


# In[15]:


df2['Prov']=df2['Prov'].fillna('-') 
df2['City']=df2['City'].fillna('-') 
df2['City']=df2['City'].replace(0,'-')


# In[16]:


df3=df2[['Date','Newcase','Cured','Death','Prov']]


# In[17]:


sumbydate=df3.groupby('Date',as_index=False)[['Newcase']].sum()
sumbydate.columns=['Date','Sum_Newcase']
sumbydate[['Cum_Newcase_T']]=sumbydate[['Sum_Newcase']].cumsum()


# In[18]:


sumbydate


# In[19]:


Provlist=['河北','山西','辽宁','吉林','黑龙江','江苏','浙江','安徽','福建','江西','山东','河南',
          '湖北','湖南','广东','海南','四川','贵州','云南','陕西','甘肃','青海','台湾','内蒙古','广西','西藏','宁夏','新疆',
          '北京','上海','天津','重庆','香港','澳门']


# In[20]:


sumCN=df3.loc[df3['Prov'].isin(Provlist)]
sumCN=sumCN.groupby('Date',as_index=False)[['Newcase']].sum()
sumCN.reset_index(drop=True,inplace=True)
sumCN=pd.merge(dat,sumCN, how='left', on=('Date'),suffixes=('',''))
sumCN=sumCN.fillna(0)
sumCN['Newcase']=sumCN['Newcase'].astype('int')
sumCN[['Cum_Newcase_CN']]=sumCN[['Newcase']].cumsum()


# In[21]:


sumCN


# In[22]:


style.use('fivethirtyeight')


# In[23]:


get_ipython().run_line_magic('matplotlib', 'notebook')


# In[29]:



fig2 = plt.figure(3)
ax1 = fig2.add_subplot(1,1,1)

xt=[]       
yt=[]        
yc=[]  
def animate2(i):   
    if len(xt)==len(sumbydate['Date']):
        xt.clear()      
        yt.clear()       
        yc.clear()
    xt.append(sumbydate['Date'][i]) 
    yt.append(sumbydate['Cum_Newcase_T'][i])
    yc.append(sumCN['Cum_Newcase_CN'][i])
    return  plot_durations(xt,yt,yc)

def init():
    p1=plt.plot(sumbydate['Date'][0],sumbydate['Cum_Newcase_T'][0],'b-',linewidth=2.5,label='Global cumulative cases')
    p2=plt.plot(sumbydate['Date'][0],sumCN['Cum_Newcase_CN'][0],'r-',linewidth=1.5,label='Chinese cumulative cases')
    return p1+p2

def plot_durations(x,y1,y2):
    plt.clf()
    plt.plot(x,y1,'b-',linewidth=2.5,label='Global cumulative cases')
    plt.plot(x,y2,'r-',linewidth=1.5,label='Chinese cumulative cases')
    
    plt.text(x[-1], y1[-1], y1[-1], ha='left', va='bottom', fontsize=12)
    plt.text(x[-1], y2[-1], y2[-1], ha='left', va='top', fontsize=10)
    
    plt.xlabel('Date')
    plt.ylabel('Total cases')
    plt.title('COVID-19 Epidemic Trend')
    plt.xticks(rotation=45,fontsize='xx-small',fontweight='light',fontstretch='condensed')
    plt.legend()


ani = animation.FuncAnimation(fig2, animate2,len(sumbydate['Date']),interval=500,init_func=init)
plt.show()


# %matplotlib qt5
# is_ipython = 'qt5' in matplotlib.get_backend()
# if is_ipython:
#     from IPython import display

# # Option 1-Matplotlib animation
# plt.ion()
# 
# def plot_durations(x,y1,y2):
#     plt.figure(2)
#     plt.clf()
#     plt.plot(x,y1,'b-',linewidth=2.5,label='Global cumulative cases')
#     plt.plot(x,y2,'r-',linewidth=1.5,label='Chinese cumulative cases')
#     plt.xticks(rotation=45,fontsize='xx-small',fontweight='light',fontstretch='condensed')
#     plt.xlabel('Date')
#     plt.ylabel('Total cases')
#     plt.title('COVID-19 Epidemic Trend')
#     
#     plt.text(x[-1], y1[-1], y1[-1], ha='left', va='bottom', fontsize=12)
#     plt.text(x[-1], y2[-1], y2[-1], ha='left', va='top', fontsize=10)
#     
#     plt.legend() 
#     
#     plt.pause(0.5)  # pause a bit so that plots are updated
#     if is_ipython:
#         display.clear_output(wait=True)
#         display.display(plt.gcf())
# 
# xt=[]       
# yt=[]        
# yc=[]        
# for i in range(len(sumbydate['Date'])):
#     xt.append(sumbydate['Date'][i]) 
#     yt.append(sumbydate['Cum_Newcase_T'][i])
#     yc.append(sumCN['Cum_Newcase_CN'][i])
#     plot_durations(xt,yt,yc)

# # Option 2 for Matplotlib Animation
# plt.ion()
# 
# def plot_durations(x,y1,y2):
#     plt.figure(1)
#     #plt.clf()
#     plt.plot(x,y1,'b-',label='Global cumulative cases')
#     plt.plot(x,y2,'r-',label='Chinese cumulative cases')
#     plt.legend() 
#     plt.pause(0.3)  # pause a bit so that plots are updated
#     if is_ipython:
#         display.clear_output(wait=True)
#         display.display(plt.gcf())
# 
# xt=[0,0]
# yt=[0,0]
# yc=[0,0]
# 
# for i in range(len(sumbydate['Date'])):
#     xt[0]=xt[1]
#     yt[0]=yt[1]
#     yc[0]=yc[1]
#     xt[1]= sumbydate['Date'][i]
#     yt[1]= sumbydate['Cum_Newcase_T'][i]
#     yc[1]= sumCN['Cum_Newcase_CN'][i]
#     plot_durations(xt,yt,yc)
