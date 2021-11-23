import pandas as pd
from datetime import datetime,timedelta
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score
from ConsecutiveDAUPrediction import periodDAU
from Model import get_paras

class DAUAdjustor():
    def __init__(self,Day0, period, expected_average_dnu, r1NUGoal, r7NUGoal, r30NUGoal, r1AUGoal, r7AUGoal, r30AUGoal) :
        self.Day0 = Day0
        self.period = period
        self.expected_average_dnu = expected_average_dnu
        self.r1NUGoal = r1NUGoal
        self.r7NUGoal = r7NUGoal
        self.r30NUGoal = r30NUGoal
        self.r1AUGoal = r1AUGoal
        self.r7AUGoal = r7AUGoal
        self.r30AUGoal = r30AUGoal
        self.database = None
        self.sample = None
        
    
    def insertDatabase(self,database):
        self.database = database
        
    def buildTrainingSet(self,learning_period):
        #prepare data
        endDate = datetime(year=int(str(self.Day0)[0:4]), month=int (str(self.Day0)[4:6]), day=int (str(self.Day0)[6:8])) + timedelta(days=self.period)
        endDate = int(endDate.strftime('%Y%m%d'))
        
        temp = str(self.Day0)
        
        duration = max(learning_period,40)
        midDate = datetime(year=int(temp[0:4]) , month=int(temp[4:6]), day=int(temp[6:8])) + timedelta(days=-duration)
        midDate = int(midDate.strftime('%Y%m%d'))
                      
                      
        mDate = "-".join([str(midDate)[0:4] ,str(midDate)[4:6],str(midDate)[6:8]])
        training_set = pd.date_range(start=mDate,periods=duration+1).date.tolist()
        training_set = [int(item.strftime('%Y%m%d')) for item in training_set]
        
                         
        sample = []
        for start in training_set:
            t = 1
            temp = str(start)
            end = datetime(year=int(temp[0:4]), month=int(temp[4:6]),day=int(temp[6:8]))+timedelta(days=t)
            end = int(end.strftime('%Y%m%d'))
            sample += periodDAU([],start,t,self.database,self.expected_average_dnu,self.r1NUGoal,self.r7NUGoal,self.r30NUGoal,self.r1AUGoal,self.r7AUGoal,self.r30AUGoal, "t", "maxenddate", self.Day0)
        sample = pd.DataFrame(np.array(sample),columns=['startDate','t','n','dau_real','dau_predicted','dau_pre','dau_t','r1NU_model','r7NU_model','r30NU_model','r1AU_model','r7AU_model','r30AU_model','t*dau_predicted','t*dau_pre'])
        sample_trained = sample.copy()
        sample_trained = sample_trained.astype({'dau_real':'float','dau_t':'float'})
        sample_trained.loc[:,'dau_real-dau_t'] = sample_trained.loc[:,'dau_real'] - sample_trained.loc[:,'dau_t']
        self.sample = sample_trained
        

    #model training & model prediction
    def adjustDAU(self):
        sub_sample = self.sample.copy()#split
        X1 = sub_sample[['dau_pre']]
        X2 = sub_sample[['dau_pre','t*dau_pre']]
        Y = sub_sample['dau_real-dau_t']
        Xs = [X1,X2]
        variables = ['dau_pre',['dau_pre','t*dau_pre']]
        
        models = []
        scores = []
        for X in Xs:
            X_train,X_test,Y_train,Y_test = train_test_split(X,Y,random_state=42)
            lr = LinearRegression(fit_intercept = False)
            model = lr.fit(X_train,Y_train)
            yhat = model.predict(X_test)
            score = r2_score(Y_test,yhat)
            score = 1 - (1-score)*(len(Y_test)-1)/(len(Y_test)-len(X.columns)-1) #adjusted r2
            scores.append(score) #discover the best model
            models.append(model)
        
        model = 'b' if scores.index(max(scores)) == 0 else 'at+b'

        print(self.Day0,1,self.database,self.expected_average_dnu,self.r1NUGoal,self.r7NUGoal,self.r30NUGoal,self.r1AUGoal,self.r7AUGoal,self.r30AUGoal,"p","maxn",self.period)
        predict = periodDAU([],self.Day0,1,self.database,self.expected_average_dnu,self.r1NUGoal,self.r7NUGoal,self.r30NUGoal,self.r1AUGoal,self.r7AUGoal,self.r30AUGoal,"p","maxn",self.period)
        predict = pd.DataFrame(np.array(predict),columns=['startDate','t','n','dau_predicted','dau_pre','dau_t','r1NU_model','r7NU_model','r30NU_model','r1AU_model','r7AU_model','r30AU_model','t*dau_predicted','t*dau_pre'])
        predict.insert(len(predict.columns),'model',model)
        predict = predict.astype({'dau_t':'float'})
        
        X = predict[variables[scores.index(max(scores))]]
        best_model = models[scores.index(max(scores))]
        Y_predict = best_model.predict(X)
        Y_predict = Y_predict + predict['dau_t']
        predict.insert(len(predict.columns),'dau_adjusted',Y_predict)

        predict.to_csv("adjusted result.csv",index=False)

if  __name__ == "__main__":
    database = pd.read_csv("database.csv")
    dau0,r1NU,r7NU,r30NU,r1AU,r7AU,r30AU = get_paras(20210830,0,database,"p")
    adjustment = DAUAdjustor(20210701,60,342683,r1NU,r7NU,r30NU,r1AU,r7AU,r30AU)
    adjustment.insertDatabase(database)
    adjustment.buildTrainingSet(50)
    adjustment.adjustDAU()
    
    

                
