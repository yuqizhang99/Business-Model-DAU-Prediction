import pandas as pd
import numpy as np
from Model import DAUPredictor
from Model import get_paras
from datetime import datetime,timedelta

def oneDayDAU(startDate,t,maxn,database,avg_dnu,r1NUGoal,r7NUGoal,r30NUGoal,r1AUGoal,r7AUGoal,r30AUGoal,flag):
    #as for flag, "t" stands for training, "p" stands for prediction
    if flag == "t":
        dau0, r1NU, r7NU, r30NU, r1AU, r7AU, r30AU, dau_real = get_paras(startDate, t, database, flag)
    elif flag == "p":
        dau0, r1NU, r7NU, r30NU, r1AU, r7AU, r30AU = get_paras (startDate, t, database, flag)
    current_r1NU = r1NU + (r1NUGoal-r1NU)*t/maxn
    current_r7NU = r7NU + (r7NUGoal-r7NU)*t/maxn
    current_r30NU = r30NU + (r30NUGoal-r30NU)*t/maxn
    current_r1AU = r1AU + (r1AUGoal-r1AU)*t/maxn
    current_r7AU = r7AU + (r7AUGoal-r7AU)*t/maxn
    current_r30AU = r30AU + (r30AUGoal-r30AU)*t/maxn

    model = DAUPredictor(t, dau0, avg_dnu, r1NU, r7NU, r30NU, r1AU, r7AU, r30AU, current_r1NU,current_r7NU, current_r30NU, current_r1AU, current_r7AU,current_r30AU)
    dau_predicted, dau_pre, dau_t, r1NU_model, r7NU_model, r30NU_model, r1AU_model, r7AU_model, r30AU_model = model.output()
    if flag == "t":
        return startDate, t, dau_real, dau_predicted, dau_pre, dau_t,r1NU_model,r7NU_model, r30NU_model,r1AU_model,r7AU_model, r30AU_model
    elif flag == "p":
        return startDate, t, dau_predicted, dau_pre, dau_t, r1NU_model, r7NU_model, r30NU_model, r1AU_model, r7AU_model, r30AU_model

# This function provide a choice of whether to input period or enddate
def periodDAU (records, startDate, t, database, avg_dnu, r1NUGoal, r7NUGoal, r30NUGoal, r1AUGoal, r7AUGoal, r30AUGoal, flag, type, *args):
    #type includes maxn, maxenddate, corresponding args are maxn,maxendDate
    if type == "maxn":
        temp = str(startDate)
        end = datetime(year=int(temp[0:4]),month=int(temp[4:6]),day=int(temp[6:8])) + timedelta(days=args[0])
        maxEndDate = int(end.strftime('%Y%m%d'))
        maxn = args[0]
    elif type == "maxenddate":
        maxEndDate = args[0]
        maxn = (datetime(year=int(str(maxEndDate)[0:4]), month=int(str(maxEndDate)[4:6]),day=int(str(maxEndDate)[6:8])) - datetime(year=int(str(startDate)[0:4]),month=int(str(startDate)[4:6]),day=int(str(startDate)[6:8]))).days
    temp = str (startDate)
    end = datetime(year=int(temp[0:4]),month=int(temp[4:6]), day=int(temp[6:8])) + timedelta(days=t)
    end = int(end.strftime('%Y%m%d'))
    if end > maxEndDate:
        return records
    else:
        if flag == "t":
            startDate,t,dau_real,dau_predicted,dau_pre,dau_t,r1NU_model,r7NU_model, r30NU_model, r1AU_model, r7AU_model, r30AU_model = oneDayDAU(startDate, t, maxn, database, avg_dnu, r1NUGoal, r7NUGoal, r30NUGoal, r1AUGoal, r7AUGoal, r30AUGoal, flag)
            records.append([startDate,t,maxn,float(dau_real),float(dau_predicted), dau_pre,dau_t,r1NU_model,r7NU_model,r30NU_model,r1AU_model,r7AU_model,r30AU_model,float(t*dau_predicted),float(t*dau_pre)])
            return periodDAU(records,startDate,t+1,database,avg_dnu,r1NUGoal,r7NUGoal,r30NUGoal,r1AUGoal,r7AUGoal,r30AUGoal,flag,type,*args)
        elif flag == "p":
            startDate,t,dau_predicted,dau_pre,dau_t,r1NU_model,r7NU_model,r30NU_model,r1AU_model,r7AU_model,r30AU_model = oneDayDAU(startDate,t,maxn,database,avg_dnu,r1NUGoal, r7NUGoal, r30NUGoal, r1AUGoal, r7AUGoal, r30AUGoal, flag)
            records.append([startDate,t, maxn, float(dau_predicted), dau_pre,dau_t,r1NU_model,r7NU_model,r30NU_model,r1AU_model,r7AU_model,r30AU_model,float(t*dau_predicted),float(t*dau_pre)])
            return periodDAU(records,startDate,t+1,database,avg_dnu,r1NUGoal,r7NUGoal,r30NUGoal,r1AUGoal,r7AUGoal,r30AUGoal,flag,type,*args)
