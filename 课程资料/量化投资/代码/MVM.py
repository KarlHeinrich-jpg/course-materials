
import os
os.chdir('D:\量化投资\data')


import numpy as np
import math
import matplotlib.pyplot as plt
def cal_mean(frac):
    return(0.08*frac+0.15*(1-frac))

mean=list(map(cal_mean,[x/50 for x in range(51)]))
sd_mat=np.array([list(map(lambda x: math.sqrt((x**2)*0.12**2+
((1-x)**2)*0.25**2+2*x*(1-x)*(-1.5+i*0.5)*0.12*0.25),[x/50 for x in range(51)])
) for i in range(1,6)])
#[expression for variable in sequence] list comprehension
plt.plot(sd_mat[0,:],mean,label='-1')
plt.plot(sd_mat[1,:],mean,label='-0.5')
plt.plot(sd_mat[2,:],mean,label='0')
plt.plot(sd_mat[3,:],mean,label='0.5')
plt.plot(sd_mat[4,:],mean,label='1')
plt.legend(loc='upper left')



#Markowitz模型之Python实现
import pandas as pd
stock=pd.read_table('stock.txt',sep='\t',index_col='Trddt')
stock.index=pd.to_datetime(stock.index)
fjgs=stock.loc[stock.Stkcd==600033,'Dretwd']
fjgs.name='fjgs'
zndl=stock.loc[stock.Stkcd==600023,'Dretwd']
zndl.name='zndl'
sykj=stock.loc[stock.Stkcd==600183,'Dretwd']
sykj.name='sykj'
hxyh=stock.loc[stock.Stkcd==600015,'Dretwd']
hxyh.name='hxyh'
byjc=stock.loc[stock.Stkcd==600004,'Dretwd']
byjc.name='byjc'


sh_return=pd.concat([byjc,fjgs,hxyh,sykj,zndl],axis=1)
sh_return.head()

sh_return=sh_return.dropna()
sh_return.corr()

cumreturn=(1+sh_return).cumprod()
sh_return.plot()
plt.title('Daily Return of 5 Stocks(2014-2015)')
plt.legend(loc='lower center',bbox_to_anchor=(0.5,-0.3),
          ncol=5, fancybox=True, shadow=True)

cumreturn.plot()
plt.title('Cumulative Return of 5 Stocks(2014-2015)')
sh_return.corr()


#构建MeanVariance类
#import ffn
from scipy import linalg
class MeanVariance:
    def __init__(self,returns):
        self.returns=returns
    def minVar(self,goalRet):
        covs=np.array(self.returns.cov())
        means=np.array(self.returns.mean())
        L1=np.append(np.append(covs.swapaxes(0,1),[means],0),
                     [np.ones(len(means))],0).swapaxes(0,1)
        L2=list(np.ones(len(means)))
        L2.extend([0,0])
        L3=list(means)
        L3.extend([0,0])
        L4=np.array([L2,L3])
        L=np.append(L1,L4,0)
        results=linalg.solve(L,np.append(np.zeros(len(means)),[1,goalRet],0))
        return(np.array([list(self.returns.columns),results[:-2]]))
    def frontierCurve(self):
        goals=[x/500000 for x in range(-100,4000)]  # -0.0002至0.008
        stds=list(map(lambda x: self.calVar(self.minVar(x)[1,:].astype(np.float64))**0.5,goals))
        plt.plot(stds,goals)
    def meanRet(self,fracs):
        meanreturns=self.returns.mean()
        assert len(meanreturns)==len(fracs), 'Length of fractions must be equal to number of assets'
        return(np.sum(np.multiply(meanreturns,np.array(fracs))))
    def calVar(self,fracs):
        return(np.dot(np.dot(fracs,self.returns.cov()),fracs))

#构建投资组合的有效前沿        
minVar=MeanVariance(sh_return)
minVar.frontierCurve() 

#假设目标期望收益率为 0.003， 2014年数据为训练集，计算weight
train_set=sh_return.loc['2014']
test_set=sh_return.loc['2015']
varMinimizer=MeanVariance(train_set)
goal_return=0.003
portfolio_weight=varMinimizer.minVar(goal_return)
portfolio_weight
#采用2015年数据为测试集，计算投资组合收益率、净值
test_return=np.dot(test_set,
                   np.array([portfolio_weight[1,:].astype(np.float64)]).swapaxes(0,1))
test_return=pd.DataFrame(test_return,index=test_set.index)
test_cum_return=(1+test_return).cumprod()

#与随机生成的100个组合进行比较
sim_weight=np.random.uniform(0,1,(100,5))
sim_weight=np.apply_along_axis(lambda x: x/sum(x),1,sim_weight)
sim_return=np.dot(test_set,sim_weight.swapaxes(0,1))
sim_return=pd.DataFrame(sim_return,index=test_cum_return.index)
sim_cum_return=(1+sim_return).cumprod()

plt.plot(sim_cum_return.index,sim_cum_return,color='green')
plt.plot(test_cum_return.index,test_cum_return,color='black')
plt.xticks(rotation=45)





#构建MeanVariance类，考虑存在无风险资产
class MeanVariance_rf:
    def __init__(self,returns,rf):
        self.returns=returns
        self.rf=rf
    def minVar(self,goalRet):
        covs=np.array(self.returns.cov())
        means=np.array(self.returns.mean())
        L1=np.append(covs.swapaxes(0,1),[means-self.rf],0).swapaxes(0,1)
        L2=means-self.rf
        L3=np.append(L2,np.array([0]))
        L4=L3[np.newaxis,:]
        L=np.append(L1,L4,0)
        results=linalg.solve(L,np.append(np.zeros(len(means)),[goalRet-self.rf],0))
        return(np.array([list(self.returns.columns),results[:-1]]))
    def frontierCurve(self):
        goals=[x/500000 for x in range(round(self.rf*500000),4000)]  # -0.0002至0.008
        stds=list(map(lambda x: self.calVar(self.minVar(x)[1,:].astype(np.float64))**0.5,goals))
        plt.plot(stds,goals)
    def meanRet(self,fracs):
        meanreturns=self.returns.mean()
        assert len(meanreturns)==len(fracs), 'Length of fractions must be equal to number of assets'
        return(np.sum(np.multiply(meanreturns,np.array(fracs)))+(1-np.sum(fracs))*self.rf)
    def calVar(self,fracs):
        return(np.dot(np.dot(fracs,self.returns.cov()),fracs))



minVar_rf=MeanVariance_rf(sh_return,0.001)
minVar_rf.frontierCurve() 



#假设目标期望收益率为  ， 2014年数据为训练集，计算weight
train_set=sh_return.loc['2014']
test_set=sh_return.loc['2015']
MVP=MeanVariance_rf(train_set,0.001)
goal_return=0.005
portfolio_weight_MVP=MVP.minVar(goal_return)
portfolio_weight_MVP
rf_weight_MVP=1-sum(portfolio_weight_MVP[1,:].astype(np.float64))
#采用2015年数据为测试集，计算投资组合收益率、净值
test_return_MVP=np.dot(test_set,
                   np.array([portfolio_weight_MVP[1,:].astype(np.float64)]).swapaxes(0,1))+MVP.rf*rf_weight_MVP
test_return_MVP=pd.DataFrame(test_return_MVP,index=test_set.index)
test_cum_return_MVP=(1+test_return_MVP).cumprod()

#与无风险均值方差组合进行比较
plt.plot(test_cum_return_MVP.index,test_cum_return_MVP,color='red')
plt.plot(test_cum_return.index,test_cum_return,color='black')
plt.xticks(rotation=45)



