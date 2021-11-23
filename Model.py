import numpy as np
from datetime import datetime,timedelta
from sklearn.linear_model import LinearRegression
class DAUPredictor():
    def __init__(self,t_end, dau0, avg_dnu, r1NU, r7NU, r30NU, r1AU, r7AU, r30AU, r1NUGoal, r7NUGoal, r30NUGoal, r1AUGoal, r7AUGoal, r30AUGoal):
        self.t_end = t_end
        self.avg_dnu = avg_dnu
        self.dau0 = dau0
        
        self.r1NU = (r1NUGoal - r1NU)*t_end/(t_end+4) + r1NU
        self.r7NU = (r7NUGoal - r7NU)*t_end/(t_end+10) + r7NU
        self.r30NU = (r30NUGoal - r30NU)*t_end/(t_end+33) + r30NU

        self.r1AU = (r1AUGoal - r1AU)*t_end/(t_end+4) + r1AU
        self.r7AU = (r7AUGoal - r7AU)*t_end/(t_end+10) + r7AU
        self.r30AU = (r30AUGoal - r30AU)*t_end/(t_end+33) + r30AU

    def output(self):
        lr = LinearRegression(fit_intercept=False)
        reg = lr.fit(np.array([[1], [7], [30]]) .reshape(-1,1), np.array ([np.log(self.r1AU) ,np.log(self.r7AU), np.log(self.r30AU) ]))
        B = reg.predict(np.array([[self.t_end]]))
        B = np.exp(B.tolist().pop())
        dau_pre = self.dau0*B

        lr = LinearRegression(fit_intercept=False)
        reg = lr.fit(np.array([[1], [7], [30]]),np.array([np.log(self.r1NU),np.log(self.r7NU), np.log(self.r30NU)]))
        a = np.exp(reg.intercept_)
        pn = np.exp(reg.coef_.tolist().pop())
        avg_dnu = self.avg_dnu
        D = a*(1-pn**self.t_end)/(1-pn)
        dau_t = avg_dnu*D

        result = dau_pre + dau_t
        return result, dau_pre, dau_t, self.r1NU, self.r7NU,self.r30NU,self.r1AU,self.r7AU, self.r30AU

#data cleaning function
def get_paras(startDate,t,database,flag): #startdate is Day0, as for flag,"t" stands for training, "p" stands for prediction
    temp = str(startDate)
    
    startDate_m1 = datetime(year=int(temp[0:4]), month=int(temp[4:6]), day=int(temp[6:8])) + timedelta (days=-1)
    startDate_m1 = int(startDate_m1.strftime('%Y%m%d'))
    
    startDate_m6 = datetime(year=int(temp[0:4]), month=int(temp[4:6]), day=int(temp[6:8])) + timedelta (days=-6)
    startDate_m6 = int(startDate_m6.strftime('%Y%m%d'))
    
    startDate_m7 = datetime(year=int(temp[0:4]), month=int(temp[4:6]), day=int(temp[6:8])) + timedelta (days=-7)
    startDate_m7 = int(startDate_m7.strftime('%Y%m%d'))
    
    startDate_m13 = datetime(year=int(temp[0:4]), month=int(temp[4:6]), day=int(temp[6:8])) + timedelta (days=-13)
    startDate_m13 = int(startDate_m13.strftime('%Y%m%d'))
    
    startDate_m30 = datetime(year=int(temp[0:4]), month=int(temp[4:6]), day=int(temp[6:8])) + timedelta (days=-30)
    startDate_m30 = int(startDate_m30.strftime('%Y%m%d'))
    
    startDate_m36 = datetime(year=int (temp[0:4]),month=int(temp[4:6]), day=int(temp[6:8])) + timedelta(days=-36)
    startDate_m36 = int(startDate_m36.strftime('%Y%m%d'))

    endDate = datetime(year=int(temp[0:4]), month=int(temp[4:6]), day=int(temp[6:8])) + timedelta(days=t)
    endDate = int(endDate.strftime('%Y%m%d'))
    
    sub_data = database
    dau0 = float(sub_data[(sub_data.date <= startDate)&(sub_data.date >= startDate_m6)]['dau'].mean())

    subsub_data = sub_data[(sub_data.date <= startDate_m1)&(sub_data.date >= startDate_m7)].copy()
    r1NU = float(subsub_data['new_retention_1d'].mean())
    r1AU = float(subsub_data['retention_1d'].mean())
    
    subsub_data = sub_data[(sub_data.date <= startDate_m7)&(sub_data.date >= startDate_m13)].copy()
    r7NU = float(subsub_data['new_retention_7d'].mean())
    r7AU = float(subsub_data['retention_7d'].mean())
    
    subsub_data = sub_data[(sub_data.date <= startDate_m30)&(sub_data.date >= startDate_m36)].copy()
    r30NU = float(subsub_data['new_retention_30d'].mean())
    r30AU = float(subsub_data['retention_30d'].mean())
    
    

    if flag == "t":
        ss_data = sub_data[sub_data.date == endDate].copy()
        dau_real = int(ss_data['dau'])
        return dau0, r1NU, r7NU, r30NU, r1AU, r7AU, r30AU, dau_real
    elif flag == "p":
        return dau0, r1NU, r7NU, r30NU, r1AU, r7AU, r30AU

    


