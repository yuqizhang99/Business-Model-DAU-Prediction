
from statsmodels.tsa.seasonal import seasonal_decompose
import pandas as pd
import numpy as np
from datetime import datetime
from sklearn.linear_model import LinearRegression
from scipy.optimize import curve_fit
from math import pi
from random import gauss

'''input pandas.DataFrame/pandas.Series with date_index
    # pandas.DataFrame.dropna(inplace=True) applied before is suggested
'''
def decomposition(seasonal_data):
    seasonal_data.dropna(inplace=True)
    result = seasonal_decompose(seasonal_data,model='additive')
    return result.trend,result.seasonal,result.resid

def regenerate(trend,seasonal,resid,length):
    trend = pd.DataFrame(trend.dropna(inplace=False)) # in shape (n,1)
    trend.reset_index(inplace=True)
    X = [[index,index**2] for index in trend.index]
    lr = LinearRegression()
    lr.fit(X,trend['trend'])

    def periodfunc(x,s1,s2,s3,s4,s5):
        return s1*np.sin(2*pi*x)+s2*np.cos(2*pi*x)+s3*np.sin(4*pi*x)+s4*np.cos(4*pi*x)+s5 
    
    seasonal = pd.DataFrame(seasonal.dropna(inplace=False))
    seasonal.reset_index(inplace=True)
    Ys = seasonal['seasonal']
    #initial value
    maxi = 1
    maxR_squared = 0
    maxpopt = [0,0,0,0,0]
    for i in range(1,366):
        # apply lambda x : x/period method to identify period
        periodXs = pd.DataFrame(seasonal.index).apply(lambda x:x/i).to_numpy().reshape((seasonal.index.shape[0],))
        popt,pcov = curve_fit(periodfunc,periodXs,Ys)
        for_SSresid = lambda x:periodfunc(x,popt[0],popt[1],popt[2],popt[3],popt[4])
        R_squared = 1 - sum((Ys - for_SSresid(periodXs))**2)/sum((Ys - np.average(Ys))**2)
        maxi = i if R_squared > maxR_squared else maxi
        maxpopt = popt if R_squared > maxR_squared else maxpopt
        maxR_squared = R_squared if R_squared > maxR_squared else maxR_squared
    resid = resid.dropna(inplace=False)

    X1 = [[i,i**2] for i in range(length)]
    sim_data = 0
    sim_data = np.array(lr.predict(X1)) # trend
    sim_data += np.array(list(map(periodfunc,np.array(range(length))/maxi,[maxpopt[0]]*length,[maxpopt[1]]*length,[maxpopt[2]]*length,[maxpopt[3]]*length,[maxpopt[4]]*length))) #seasonality
    sim_data += [gauss(0,np.std(resid)) for _ in range(length)] #noise
    return sim_data # return numpy.array

if __name__ == "__main__":
    df = pd.read_csv("test.csv")
    df = df[df.date >= 20210401].copy()
    dates = pd.DataFrame(df['date'],columns=['date'])
    dates.reset_index(drop=True,inplace=True)
    df['date'] = df['date'].apply(lambda date: datetime(year=int(str(date)[0:4]),month =int(str(date)[4:6]),day=int(str(date)[6:8])))
    sim_df = dates
    cols = list(df.columns)
    cols.remove('date')
    for col in cols:
        sample_data = df[["date",col]].copy()
        sample_data.sort_values("date")
        sample_data.set_index("date",inplace=True)
        trend,seasonal,resid = decomposition(sample_data)
        sim_data = regenerate(trend,seasonal,resid,sample_data.shape[0])
        if col in ('dau','dnu'):
            new_df = pd.DataFrame(pd.DataFrame(sim_data).apply(int,axis=1),columns=[col]) #obtain integer
        else:
            new_df = pd.DataFrame(sim_data,columns=[col])
        sim_df = pd.concat([sim_df,new_df],axis=1)
    sim_df.to_csv('database.csv',index=False)

    
    


