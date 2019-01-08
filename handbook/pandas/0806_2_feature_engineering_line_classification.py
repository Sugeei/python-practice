
# coding: utf-8

# ### 0 载入数据 training : travel_time_range_8_9.csv
# # 构造测试集，导入另外两张属性表，合并 ， 构造特征

# In[122]:


import os
rootdir = '../../hanxiaoyang/AliTraffic/data' #AliTraffic data
# os.path.join(rootdir,'gy_contest_link_info.csv')


# In[123]:



get_ipython().magic(u'matplotlib inline')

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

import warnings
warnings.filterwarnings("ignore")
# pd.options.display.mpl_style = 'default'


# # 载入训练数据 ， 筛选后的每天6，7，8点的数据

# In[124]:


time_travel = pd.read_csv('./travel_time_range_8_9.csv')
time_travel['link_ID'] = time_travel['link_ID'].astype(str)


# In[125]:


time_travel.columns


# In[126]:


# len(time_travel.time_interval.unique())


# In[127]:


link_info_data = pd.read_csv(os.path.join(rootdir,'gy_contest_link_info.txt'),sep=';')
link_info_data['link_ID'] = link_info_data['link_ID'].astype(str)


# In[129]:


link_top_data = pd.read_csv(os.path.join(rootdir,'gy_contest_link_top_20170715.txt'),sep=';')
link_top_data['link_ID'] = link_top_data['link_ID'].astype(str)
link_top_data = link_top_data.fillna('000')


# In[133]:


time_travel['month'] = pd.DatetimeIndex(time_travel.date).month
time_travel.head()
# time_travel.date.unique()
# time_travel.travel_time.sort_values


# In[73]:


def extrac_interval(interval):
    return ''.join(interval[11:20].split(':'))
    # 返回 time_interval 中的时间字符。 不带日期信息


# In[74]:


time_travel['interval'] = time_travel['time_interval'].apply(extrac_interval) 


# ### ---------------------------------------------------------------------------------------------------------
# # 

# ### 0. data clean
# 

# In[75]:


# link_info_data.info()
# link_info_data.time_interval


# In[76]:


# pd.DataFrame({'a':[1,2,3]})


# ### outliers and missing
# 

# ### 

# ### ---------------------------------------------------------------------------------------------------------
# # 生成测试数据集

# In[77]:


# 提取2016年6月6点~8点的数据
base_df = time_travel[time_travel['month']==6]

base_df = base_df.sort_values('time_interval')
base_df = base_df.reset_index()
base_df = base_df.drop('index',1)
# base_df
# print base_df['month'].unique()


# In[78]:


# time_interval = 


# In[79]:


# 生成测试集
df_test = base_df[(base_df['month']==6)&(base_df['hour']==7)]

def generate_test_data(x):
    to_hour = x[-9:-7]
    if to_hour == '08':
        new_x = x[:12]+'08'+x[14:-9]+'09'+x[-7:]
    else:
        new_x = x[:12]+'08'+x[14:-9]+'08'+x[-7:]
    return new_x
    
df_test['time_interval'] = df_test['time_interval'].apply(generate_test_data)


# In[80]:


# df_test.head()


# In[81]:


time_interval = pd.DataFrame({'time_interval':df_test.time_interval.unique()})
# date = pd.DataFrame({'date':df_test.date.unique()})
link_ID = pd.DataFrame({'link_ID':df_test.link_ID.unique()})

time_interval['key']=1
# date['key']=1
link_ID['key']=1


# In[82]:


def extract_date_from_interval(interval):
    return interval[1:11]


# time_interval = pd.merge(time_interval, df_test[['date','time_interval']], on='time_interval', how='left')
time_interval['date'] = time_interval['time_interval'].apply(extract_date_from_interval)

pre_test = pd.merge(time_interval,link_ID)
pre_test.info()


# In[83]:


# time_interval
pre_test = pre_test.drop('key',1)
pre_test['link_ID'] = pre_test['link_ID'].astype(str)
pre_test['interval'] = pre_test['time_interval'].apply(extrac_interval) 
# base_df.info()

pre_test['date_format'] = pd.to_datetime(pre_test['date'])

pre_test['hour'] = pre_test['time_interval'].apply(lambda x: int(x[12:14]))
# partial_data = training_data[training_data.hour.isin([6,7,8])]

pre_test['year'] = pd.DatetimeIndex(pre_test.date_format).year
pre_test['month'] = pd.DatetimeIndex(pre_test.date_format).month#dataset.Name.str.extract(' ([A-Za-z]+)\.', expand=False)
pre_test['day'] = pd.DatetimeIndex(pre_test.date_format).day
# combine['dow'] = pd.DatetimeIndex(combine.date_format).dayofweek
# base_df['doy'] = pd.DatetimeIndex(base_df.record_date).dayofyear


pre_test.head()
# test.dtypes


# In[84]:


pre_test.dtypes


# ### ---------------------------------------------------------------------------------------------------------
# # 加载 道路属性数据表

# In[85]:


# 

link_top_data = pd.read_csv(os.path.join(rootdir,'gy_contest_link_top_20170715.txt'),sep=';')
link_top_data['link_ID'] = link_top_data['link_ID'].astype(str)
link_top_data = link_top_data.fillna('000')


# In[86]:


link_info_data = pd.read_csv(os.path.join(rootdir,'gy_contest_link_info.txt'),sep=';')
link_info_data['link_ID'] = link_info_data['link_ID'].astype(str)


# In[87]:


# 合并数据
property_data = pd.merge(link_info_data, link_top_data, how='left', on=['link_ID'])


# In[88]:


#### 1.1.1 汇入/出口 道路条数 
# 汇入/出口 道路条数
def link_nums(x):
    link_list = x.split('#')
    if link_list[0] == '000':   
        nums = 0
    else:
        nums = len(link_list)
    return nums

property_data['in_links_nums'] = property_data['in_links'].apply(link_nums)
property_data['out_links_nums'] = property_data['out_links'].apply(link_nums)



# In[89]:


#### 1.1.2 汇入/出口 道路宽度和
# 汇入/出口 道路宽度和
def link_width_sum(x):
    link_list = x.split('#')
    if link_list[0] == '000':   
        width = 0
    else:
        width = 0
        for link in link_list:
            width += property_data[property_data['link_ID']==link]['width'].values[0]
    return width

property_data['in_link_width_sum'] = property_data['in_links'].apply(link_width_sum)
property_data['out_link_width_sum'] = property_data['out_links'].apply(link_width_sum)


# In[90]:


#### 1.1.3 汇入/出口 道路平均长度
# 汇入/出口 道路平均长度
def link_length_mean(x):
    length_list = []
    link_list = x.split('#')
    if link_list[0] == '000': 
        length = 0
        length_list.append(length)
    else:
        for link in link_list:
            length = property_data[property_data['link_ID']==link]['length'].values[0]
            length_list.append(length)
    length_mean = np.mean(length_list)
    length_mean = round(length_mean,1)
    return length_mean

property_data['in_link_length_mean'] = property_data['in_links'].apply(link_length_mean)
property_data['out_link_length_mean'] = property_data['out_links'].apply(link_length_mean)


# In[91]:


property_data.head()
# 3377906284395510514
property_data[property_data.link_ID == 3377906284395510514]
property_data.dtypes


# ### ---------------------------------------------------------------------------------------------------------
# # 模型训练 准备训练集，测试集 与 标签

# In[92]:


train = time_travel[['link_ID','date','time_interval','travel_time','interval']]
# y = time_travel.travel_time

# combine = [train, test]
train['flag'] = 1
pre_test['flag'] = 0 # 加上标签列， 便于后面拆分 
pre_test['travel_time'] = 0
combine = pd.concat([train, pre_test])


# In[93]:


combine.head()
# combine.dtypes


# In[94]:


combine.columns


# In[95]:


# 合并 道路属性数据 与通行时间数据
# for ds in combine:
combine = pd.merge(combine, property_data, how='left', on=['link_ID'])


# #### 计算通行速度

# In[143]:


plt.boxplot(combine['travel_time'])
plt.axis([0,2,0,50])


# ### ---------------------------------------------------------------------------------------------------------
# # 构建 基本特征

# In[134]:


combine['speed'] = combine['length']/combine['travel_time']
combine['travel_time'].values
combine.dtypes


# ### ---------------------------------------------------------------------------------------------------------
# # 构建 基本特征

# In[97]:


# train = raw_data[['date','time_interval','link_ID']]
# raw_data.head()


# In[98]:


# test = pd.merge(test,raw_data[['date','time_interval','link_ID']])


# In[99]:


# # 拼接测试集
# base_df = pd.concat([base_df, df_test]).sort_values(['time_interval'])
# base_df = base_df.reset_index()
# base_df = base_df.drop('index',1)


# In[100]:


# base_df['hour'] = base_df['time_interval'].apply(lambda x: int(x[12:14])) # 重新计算hour


# In[101]:


# 132*30*30
# 900*132
combine.head()


# In[102]:


# base_df.info()

combine['date_format'] = pd.to_datetime(combine['date'])

combine['hour'] = combine['time_interval'].apply(lambda x: int(x[12:14]))
# partial_data = training_data[training_data.hour.isin([6,7,8])]

combine['year'] = pd.DatetimeIndex(combine.date_format).year
combine['month'] = pd.DatetimeIndex(combine.date_format).month#dataset.Name.str.extract(' ([A-Za-z]+)\.', expand=False)
combine['day'] = pd.DatetimeIndex(combine.date_format).day
combine['dow'] = pd.DatetimeIndex(combine.date_format).dayofweek
# base_df['doy'] = pd.DatetimeIndex(base_df.record_date).dayofyear


# In[103]:


# combine['date'] = pd.to_datetime(combine['date'])

 # 单独提取时间片， 不带日期信息


# In[104]:


combine.head()


# #### 1.6 前一时段的特征
#     ——引入pieces周期特征增加时间序列描述

# #### 这里与powerAI不同。这里需要预测每条link上每两分钟时间片的平均旅行时间，相当于要预测每个企业的用电量
# #### 不能聚合，只能分别处理。for 循环？还是把link_ID当作一个特征？
# 
# #### 这里只做 前一时段所有道路的统计值，即 按时段分组

# In[105]:


# # 计算每段路通行速度
# # 
# train_with_line_property = pd.merge(time_travel, property_data, how='left', on=['link_ID'])
# train_with_line_property['velocity'] = train_with_line_property['length']/train_with_line_property['travel_time']
# train_with_line_property


# In[106]:


# # 按时段分组，计算所有路段的速度均值

# time_interval_group_data = train_with_line_property[['time_interval','velocity']].groupby(['time_interval']).agg(['mean'])
# time_interval_group_data.columns = time_interval_group_data.columns.droplevel(0)
# time_interval_group_data = time_interval_group_data.reset_index()
# time_interval_group_data.columns = ['time_interval','velocity_mean']
# time_interval_group_data


# #### 按照 interval 算均值

# In[107]:



time_interval_group_data = combine[['interval','travel_time']].groupby(['interval']).agg(['mean'])
time_interval_group_data.columns = time_interval_group_data.columns.droplevel(0)
time_interval_group_data = time_interval_group_data.reset_index()
# time_interval_group_data.columns = ['time_interval','velocity_mean']
time_interval_group_data = time_interval_group_data.rename(columns = {'mean':'mean_of_interval'})
# time_interval_group_data['date'] = pd.to_datetime(time_interval_group_data['date'])
time_interval_group_data.head()


# In[108]:


# time_interval_group_data.head()
# 合并数据, 数据格式不同也是没法合并 
combine = pd.merge(combine, time_interval_group_data, on='interval', how='left')
combine.head()


# #### 按照link_id 算均值

# In[109]:



time_interval_group_data = train[['link_ID','travel_time']].groupby(['link_ID']).agg(['mean'])
time_interval_group_data.columns = time_interval_group_data.columns.droplevel(0)
time_interval_group_data = time_interval_group_data.reset_index()
# time_interval_group_data.columns = ['time_interval','velocity_mean']
time_interval_group_data = time_interval_group_data.rename(columns = {'mean':'mean_of_line'})
# time_interval_group_data['date'] = pd.to_datetime(time_interval_group_data['date'])
time_interval_group_data.head()


# In[110]:


# time_interval_group_data.head()
# 合并数据, 数据格式不同也是没法合并 
combine = pd.merge(combine, time_interval_group_data, on='link_ID', how='left')
combine.head()


# #### 计算日均通行时长
# 

# In[111]:



time_interval_group_data = combine[['date','travel_time']].groupby(['date']).agg(['mean'])
time_interval_group_data.columns = time_interval_group_data.columns.droplevel(0)
time_interval_group_data = time_interval_group_data.reset_index()
# time_interval_group_data.columns = ['time_interval','velocity_mean']
time_interval_group_data = time_interval_group_data.rename(columns = {'mean':'mean_of_date'})
# time_interval_group_data['date'] = pd.to_datetime(time_interval_group_data['date'])
time_interval_group_data.head()


# In[112]:


# time_interval_group_data.head()
# 合并数据, 数据格式不同也是没法合并 
combine = pd.merge(combine, time_interval_group_data, on='date', how='left')
combine.head()


# #### 节假日特征

# In[113]:


def is_holiday(original_data):
    original_data['holiday'] = 0
    original_data.loc[(original_data['date']=='2016-03-08'),['holiday']] = 1
    original_data.loc[(original_data['date']>='2016-04-02') & (original_data['date']<='2016-04-04'),['holiday']] = 1
    original_data.loc[(original_data['date']>='2016-04-30') & (original_data['date']<='2016-05-02'),['holiday']] = 1
    original_data.loc[(original_data['date']>='2016-06-09') & (original_data['date']<='2016-06-11'),['holiday']] = 1
    return original_data
    
combine = is_holiday(combine)


# In[114]:


def pre_holiday(original_data):
    original_data['day_before_holiday'] = 0
    original_data.loc[(original_data['date']=='2016-04-01'),['day_before_holiday']] = 1
    original_data.loc[(original_data['date']=='2016-04-29'),['day_before_holiday']] = 1
    original_data.loc[(original_data['date']=='2016-06-08'),['day_before_holiday']] = 1
    return original_data

combine = pre_holiday(combine)


# In[115]:


def post_holiday(original_data):
    original_data['day_after_holiday'] = 0
    original_data.loc[(original_data['date']=='2016-04-05'),['day_after_holiday']] = 1
    original_data.loc[(original_data['date']=='2016-05-03'),['day_after_holiday']] = 1
    original_data.loc[(original_data['date']=='2016-06-12'),['day_after_holiday']] = 1
    return original_data

combine = post_holiday(combine)


# In[116]:


def is_workday(original_data):
    original_data['is_workday'] = 1
    original_data.loc[(original_data['dow']>=5),['is_workday']] = 0
    original_data.loc[(original_data['date']=='2016-06-12'),['is_workday']] = 1
    original_data.loc[(original_data['date']=='2016-04-04'),['is_workday']] = 0
    return original_data

combine = is_workday(combine)


# In[120]:


combine.speed.values


# #### 道路通行速度均值, 区分工作日 与休息日

# In[119]:


# 历史 各道路 速度均值
historical_velocity_mean = combine[['link_ID','speed','is_workday']].groupby(by=['link_ID','is_workday']).agg(['mean'])

historical_velocity_mean = historical_velocity_mean.reset_index()
historical_velocity_mean.columns = ['link_ID','is_workday','velocity_mean']
# historical_velocity_mean
combine = pd.merge(combine, historical_velocity_mean, on=['link_ID','is_workday'], how='left')
# combine.head()
historical_velocity_mean


# #### 道路通行时长均值, 区分工作日 与休息日

# In[59]:


# 历史 各道路 时长均值
historical_travel_time_mean = combine[['link_ID','travel_time', 'is_workday']].groupby(by=['link_ID','is_workday']).agg(['mean'])

historical_travel_time_mean = historical_travel_time_mean.reset_index()
historical_travel_time_mean.columns = ['link_ID','is_workday','travel_time_mean']
# historical_travel_time_mean

# time_interval_group_data.head()
# 合并数据, 数据格式不同也是没法合并 
combine = pd.merge(combine, historical_travel_time_mean, on=['link_ID','is_workday'], how='left')
combine.head()


# # 提取列

# In[54]:


combine.columns


# In[127]:


df = combine[[ u'link_ID', u'interval', u'flag',
       u'travel_time', u'length', u'width', u'link_class', u'in_links_nums', u'out_links_nums', u'in_link_width_sum',
       u'out_link_width_sum', u'hour', u'month', u'day', u'dow',  u'year',u'mean_of_interval',
       u'mean_of_line', u'mean_of_date']]
df.head()


# In[4]:


df.columns


# ### 读取构造好特征的数据集

# In[2]:



get_ipython().magic(u'matplotlib inline')

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

import warnings
warnings.filterwarnings("ignore")
# pd.options.display.mpl_style = 'default'

df = pd.read_csv('train_test_dataset.csv')


# # 生成训练集 测试集

# In[5]:



train = df[df.train_flag==1]
y = train['travel_time']
train = train.drop(['train_flag','travel_time'],1)

test = df[df.train_flag==0]
test = test.drop(['train_flag','travel_time'],1)


# In[6]:


test.head()


# ### ---------------------------------------------------------------------------------------------------------

# ### ======================================================

# # 建模

# # ### LightGBM建模

# In[130]:


import lightgbm as lgb
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import GridSearchCV

train[[ u'link_ID', u'interval', u'hour', u'month', u'day', u'dow']] = train[[ u'link_ID', u'interval', u'hour', u'month', u'day', u'dow']].astype(str)

X_lgb = train.values
y_lgb = y.values.reshape(train.values.shape[0],)


estimator = lgb.LGBMRegressor(colsample_bytree=0.8, subsample=0.9, subsample_freq=5)

param_grid = {
    'learning_rate': [0.1, 0.2],
    'n_estimators': [400, 800],
#     'num_leaves':[128, 1024, 4096]
}

#fit_params = {'sample_weight':, 'early_stopping_rounds':5, 'categorical_feature':[0,1,2,3,4,5]}
#fit_params = {'early_stopping_rounds':5, 'categorical_feature':[0,1,2,3,4,5]}
#fit_params = {'categorical_feature':[0,1,2,3,4,5]}
#gbm = GridSearchCV(estimator, param_grid, fit_params=fit_params)
gbm = GridSearchCV(estimator, param_grid)

gbm.fit(X_lgb, y_lgb)

print "----------------------cv results--------------------------"
print gbm.cv_results_

print "----------------------------cv------------------------------"
print gbm.cv

print('Best parameters found by grid search are:', gbm.best_params_)


# In[131]:


# 预测

# label变换  # 如果用速度来做预测，这里要注意在后面要变换成旅行时间


y_predict = gbm.predict(test.values)


# ### ExtraTreesRegressor / RandomForestRegressor

# In[132]:


# from sklearn.model_selection import GridSearchCV
# from sklearn.ensemble import ExtraTreesRegressor
# from sklearn.ensemble import RandomForestRegressor

# reg = ExtraTreesRegressor()


# In[133]:


# reg.fit(train_X, train_y)


# In[134]:


# 预测


# label变换  # 如果用速度来做预测，这里要注意变换成旅行时间



# In[135]:


# y_predict = reg.predict(test_X.values)


# In[136]:


# y_predict[:10] #


# # 生成提交结果

# In[145]:


test['travel_time'] = y_predict
#pre_test
test.head()


# In[156]:


# test['date'] = str(test['year']) + str(test['month']) + str(test['day'])
# test = test.drop('date',1)
sample_data.columns


# In[148]:


# sample_data = test[['link_ID','time_interval','length']]
pre_test.head()


# In[160]:


# sample_data['date'] = sample_data['time_interval'].apply(lambda x: x[1:11])
# sample_data['velocity'] = y_predict
# sample_data['travel_time'] = sample_data['length']/sample_data['velocity']
sample_data = pd.merge(pre_test, test, on=['year','month','day','link_ID','interval'])
sample_data.head()

sample_data = sample_data[[u'time_interval', u'date', u'link_ID',u'travel_time']]
sample_data['travel_time'] = sample_data['travel_time'].astype(str)
sample_data.dtypes


# # 生成结果文件

# In[161]:


# 拼接结果

sample_data = sample_data.apply(lambda df: df.link_ID+'#'+df.date+'#'+df.time_interval+'#'+df.travel_time+'\n', axis=1)

sample_data = sample_data.reset_index()
sample_data = sample_data.drop('index',1)


# In[162]:


# 保存结果文件
lines = sample_data.shape[0]

f = open("./submit_data.txt", "w+")

for line in range(lines):
    line_res = sample_data[0].values[line]
#     print line_res
    f.write(line_res)
    
f.close()


# In[ ]:


get_ipython().magic(u'save -f feature_engineer []')


# In[ ]:




