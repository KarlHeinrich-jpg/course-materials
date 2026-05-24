# -*- coding: utf-8 -*-
"""
Created on Mon Oct 21 16:41:34 2024

@author: hp
"""

import pandas as pd
#读取万科的数据
stock=pd.read_csv('TRD_Dalyr.csv',index_col='Trddt')
Vanke=stock[stock.Stkcd==2]
close=Vanke.Clsprc
close.head()
close.index=pd.to_datetime(close.index)
close.index.name='Date'
close.head()

#计算单期简单收益率
lagclose=close.shift(1)
lagclose.head()
Calclose=pd.DataFrame({'close':close,'lagclose':lagclose})
Calclose.head()
simpleret=(close-lagclose)/lagclose
simpleret.name='simpleret'
simpleret.head()

calret=pd.merge(Calclose,pd.DataFrame(simpleret),left_index=True,right_index=True)
calret.head()

#计算2期简单收益率，并合并数据
simpleret2=(close-close.shift(2))/close.shift(2)
simpleret2.name='simpleret2'
calret['simpleret2']=simpleret2
calret.head()

#查看12月的数据
calret.loc['2023-12',:]
