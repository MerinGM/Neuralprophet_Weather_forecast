from datetime import datetime,timedelta
import joblib
import pandas as pd
from neuralprophet import NeuralProphet
import streamlit as st

filename = 'np_model2.sav'
old_model = joblib.load(filename)
filename1 = 'np_modeltrial.sav'
def retrain(td_precip,td_max,td_min):
    filename1 = 'np_modeltrial.sav'
    
    trial_weather = pd.read_csv("/root/weather_app/data.csv")
    trial_weather['ds'] = pd.to_datetime(trial_weather['ds'])
    
    date = datetime.today().strftime('%Y-%m-%d')
    latest = {"ds":date,"y":td_max,"precip":td_precip,"temp_min":td_min}
    df = pd.DataFrame(latest,index=[0])
    df["ds"] = pd.to_datetime(df["ds"])
    date = datetime.today()
    
    last_date = trial_weather.iloc[-1,0]
    curr_date = date - timedelta(days=1)
    print(curr_date)
    if(last_date == curr_date):
       trial_weather = pd.concat([trial_weather,df])
    else:
        for single_date in (last_date + timedelta(n) for n in range(int((date - last_date).days))):    
            new_row = {"ds":single_date,"precip":None,"temp_min":None,"y":None}
            df1=pd.DataFrame(new_row,index=[0])
            df1['ds']=pd.to_datetime(df1['ds'])
            trial_weather.append(df1)      
        trial_weather = pd.concat([trial_weather,df])
           
    new_model=NeuralProphet()
    new_model.add_lagged_regressor('precip')
    new_model.add_lagged_regressor('temp_min')
    new_model.fit(trial_weather,freq='D',epochs=10)   
    joblib.dump(new_model,filename1)
    str = "Retrained model"
    trial_weather.to_csv("/root/weather_app/data1.csv")
    return str
    
def make_prediction(periods):
    filename = 'np_model2.sav'
    old_model = joblib.load(filename)
   # filename1 = 'np_modeltrial.sav'
    
    trial_weather = pd.read_csv("/root/weather_app/data.csv")
    trial_weather['ds'] = pd.to_datetime(trial_weather['ds'])
    
    old_model.restore_trainer()
    data_future = old_model.make_future_dataframe(trial_weather, n_historic_predictions=True, periods = periods)  
    forecast = old_model.predict(data_future)
    forecast = forecast[-(periods):]
    return forecast



# def prepare(td_precip,td_max,td_min):
#     td_precip = int(td_precip)
#     td_max = int(td_max)
#     td_min = int(td_min)
#     date = datetime.today().date()
#     temp_range = td_max/td_min
#     month_max = (trial_weather.iloc[:-29,trial_weather.columns.get_loc("temp_max")]+td_max).mean()
#     month_day_max = month_max / td_max
#     monthly_avg = trial_weather.loc[(trial_weather.index.month==date.month),'temp_max'].mean()
#     day_of_year_avg = trial_weather.loc[(trial_weather.index.day_of_year==date.day),'temp_max'].mean()

#     latest = {"precip":td_precip,"temp_max":td_max,"temp_min":td_min,"temp_range":temp_range,"month_max":month_max,"month_day_max":month_day_max,"monthly_avg":monthly_avg,"day_of_year_avg":day_of_year_avg}

#     df=pd.DataFrame(latest,index=[date])
#     return df

# def predictor(df):
#     prediction = model.predict(df)
#     return prediction["yhat1"]

# """
#     trial_weather = pd.concat([trial_weather,df])
#     last_date = core_weather.iloc[len(core_weather)-1].name
#     last_date = last_date.date()
#     curr_date = date - timedelta(days=1)
# """  

# """   
#     if (last_date == curr_date):
#         core_weather = pd.concat([core_weather,df])
#     else
#        for single_date in (last_date + timedelta(n) for n in range(int((date_date - last_date).days))):

# """       

# def make_prediction(predictors,core_weather,reg):
#     train = core_weather.loc[:"2020-12-31"]
#     test = core_weather.loc["2021-01-01":]
#     reg.fit(train[predictors],train["target_tmax"])
#     predictions = reg.predict(test[predictors])
#     error = mean_absolute_error(test["target_tmax"],predictions)
#     compare = pd.concat([test["target_tmax"],pd.Series(predictions, index=test.index)],axis=1)
#     compare.columns = ["actual","predictions"]
#     return error,compare    
