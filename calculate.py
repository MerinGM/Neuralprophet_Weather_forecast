from datetime import datetime,timedelta
import joblib
import pandas as pd
trial_weather = pd.read_csv("trial_weather.csv",parse_dates=['Unnamed: 0'],index_col=['Unnamed: 0'])
trial_weather.index = pd.to_datetime(trial_weather.index)


filename = 'joblib_model1.sav'
model = joblib.load(filename)

def prepare(td_precip,td_max,td_min):
    td_precip = int(td_precip)
    td_max = int(td_max)
    td_min = int(td_min)
    date = datetime.today().date()
    temp_range = td_max/td_min
    month_max = (trial_weather.iloc[:-29,trial_weather.columns.get_loc("temp_max")]+td_max).mean()
    month_day_max = month_max / td_max
    monthly_avg = trial_weather.loc[(trial_weather.index.month==date.month),'temp_max'].mean()
    day_of_year_avg = trial_weather.loc[(trial_weather.index.day_of_year==date.day),'temp_max'].mean()

    latest = {"precip":td_precip,"temp_max":td_max,"temp_min":td_min,"temp_range":temp_range,"month_max":month_max,"month_day_max":month_day_max,"monthly_avg":monthly_avg,"day_of_year_avg":day_of_year_avg}

    df=pd.DataFrame(latest,index=[date])
    return df

def predictor(df):
    return model.predict(df)

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
