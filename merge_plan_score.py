import pandas as pd
import json

df1 = pd.read_csv('data/2021模拟_普通类平行计划1_普通类平行录取_物理化学生物.csv')
df2 = pd.read_csv('data/2021模拟_普通类平行计划1_普通类平行录取_政治历史地理.csv')

d2020 = pd.read_csv("data/2020投档线.csv", index_col='序号')

def query_score(school_number, major_number):
  try:
    res = d2020.loc[(d2020['学校代号']==school_number)&(d2020['专业代号']==major_number)]
    # print(school_number, major_number)
    # print(res)
    return int(res.iloc[0]['分数线']), int(res.iloc[0]['位次'])
  except:
    return 0, 10000000

options = []
unique = set()

def is_unique(row):
  identifier = int(row['院校代码']) * 0x66CCFF + int(row['专业代码'])
  if identifier in unique:
    return False
  unique.add(identifier)
  return True

def addDf(df):
  for index, row in df.iterrows():
    if not is_unique(row):
      continue
    option = dict((key, row[key]) for key in ["院校名称","专业名称","省","城市","计划数","选考科目要求", "备注"])
    option["分数线"], option["位次"] = query_score(row['院校代码'], row['专业代码'])
    options.append(option)


addDf(df1)
addDf(df2)

print(json.dumps(options, ensure_ascii=False))

# 院校代码,院校名称,专业代码,专业名称,学制,省,城市,本专科,计划数,选考科目要求,收费标准,备注
