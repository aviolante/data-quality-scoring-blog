import pandas as pd
import random
from faker import Faker
import numpy as np

def create_customer_data(rownum=10):
  """
  generate random customer data and introduce NaN values
  """
  fake = Faker()

  # empty arrays to add as dataframe columns
  firstname, lastname, email, state, city, job, salary, has_child_bin, shop_last_6_mnths = [], [], [], [], [], [], [], [], []

  for i in range(rownum+1):
    firstname.append(fake.first_name())
    lastname.append(fake.last_name())
    email.append(fake.email())
    state.append(fake.state())
    city.append(fake.city())
    job.append(fake.job())
    salary.append(random.randrange(50000, 350000, 12333))
    has_child_bin.append(fake.boolean(chance_of_getting_true=60))
    shop_last_6_mnths.append(fake.boolean(chance_of_getting_true=30))

  # create dataframe and map arrays to dataframe columns
  df = pd.DataFrame()

  df['firstname']         = firstname
  df['lastname']          = lastname
  df['email']             = email
  df['state']             = state
  df['city']              = city
  df['job']               = job
  df['salary']            = salary
  df['has_child_bin']     = has_child_bin
  df['shop_last_6_mnths'] = shop_last_6_mnths

  # randomly introduce NaN values to data
  for col in ['firstname','lastname','state','city','job','salary']:
    df[col] = df[col].sample(frac=0.8)

  return df


df = create_customer_data()
print(df.head())


def generate_survey_results(rownums=10):
  """
  Generate forced ranking results ranking our 8 features 1-8 with 1 being the
  most important and 8 being the least important
  """
  df_survey = pd.DataFrame(columns=df.columns)
  for i in range(rownums):
    gen_res = np.array([random.sample(range(1, 10), 9)])
    df_survey = df_survey.append(pd.DataFrame(gen_res, columns=df.columns))

  return df_survey


df_survey = generate_survey_results(rownums=15)
print(df_survey.head())


def create_rank_weights_df(survey_results):
  df_survey_res = pd.DataFrame(survey_results.mean(), columns=['avg_rating'])
  df_survey_res['feature_rank'] = df_survey_res['avg_rating'].rank()
  df_survey_res['rank_sum'] = len(df_survey_res) - df_survey_res['feature_rank'] + 1
  df_survey_res['rank_sum_weights'] = df_survey_res['rank_sum'] / df_survey_res['rank_sum'].sum()

  df_survey_res['feature_name'] = df_survey_res.index
  df_survey_res = df_survey_res.reset_index(drop=True)

  df_survey_res = df_survey_res[['feature_name', 'avg_rating', 'feature_rank', 'rank_sum', 'rank_sum_weights']]

  return df_survey_res


df_new = create_rank_weights_df(df_survey)
print(df_new)
