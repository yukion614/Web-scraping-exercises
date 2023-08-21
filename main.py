#%matplotlib inline
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt



    #輸入人生規劃 參數
起始資金 = input('輸入起資: ')#30
每月薪水 = input('輸入每月月薪: ') #3
每月開銷 = input('輸入每月開銷#不包含房租') #1 不含房租
每月房租 = input('輸入每月房租') #1
退休年齡 = input('輸入預計退休年齡: ')#65
'''range(start, stop[, step])'''
起始年紀 = input('輸入起始年紀: ')
退休年紀 = input('輸入預計退休年齡: ')
預測時段 = range(起始年紀, 退休年齡, 1) #起始年紀 跟 退休年紀 


def 每年淨值計算():
    每年淨額 = pd.Series(0, index=預測時段)
    每年淨額.iloc[0] = 起始資金
    每年淨額.loc[:退休年齡] += 每月薪水 * 12
    每年淨額 -= (每月開銷 + 每月房租) * 12
  
    %matplotlib inline
    每年淨額.plot()

每年淨值計算()


# 將dfs中，row長度介於5~11的table合併（這些才是我們需要的table，其他table不需要）
df = pd.concat([df for df in dfs if df.shape[1] <= 11 and df.shape[1] > 5])

# 設定column名稱
df.columns = df.columns.get_level_values(1)

# 將 df 中的當月營收用 .to_numeric 變成數字，再把其中不能變成數字的部分以 NaN 取代（errors='coerce'）
df['當月營收'] = pd.to_numeric(df['當月營收'], 'coerce')

# 再把當月營收中，出現 NaN 的 row 用 .dropna 整行刪除
df = df[~df['當月營收'].isnull()]

# 刪除「公司代號」中出現「合計」的行數，其中「～」是否定的意思
df = df[df['公司代號'] != '合計']

# 將「公司代號」與「公司名稱」共同列為 df 的 indexes
df = df.set_index(['公司代號', '公司名稱'])

df.head()