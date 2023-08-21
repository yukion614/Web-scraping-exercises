#matplotlib inline
import lxml
import pandas
from io import StringIO
import pandas as pd
import requests
import datetime
import ipywidgets as widgets
import matplotlib.pyplot as plt
'''人生規劃==============================================='''
#def 人生規劃_輸入():#7比資料
print("輸入個人資訊: ")
    
起始資金 = int(input('輸入現有資金: '))
每月薪水 = int(input('輸入每月薪資: '))
每月開銷 = int(input('輸入每月開銷/不包含房租:'))
每月房租 = int(input('每月房租:'))
退休年齡 = int(input('預計退休年齡:'))
預測起始年齡 = int(input('起始年齡: '))
預測終點年齡 = int(input('終點年紀'))
預測時段 = range(預測起始年齡, 預測終點年齡, 1)
   

def 每年淨額計算():

    # 每年淨額
    每年淨額 = pd.Series(0, index=預測時段)
    每年淨額.iloc[0] = 起始資金
    每年淨額.loc[:退休年齡] += 每月薪水 * 12
    每年淨額 -= (每月開銷 + 每月房租) * 12
    #產生圖表
    print("每年淨額圖表:")
    每年淨額.plot()  #轉換資料為plot
    #淨額圖表
    每年淨額.show()

    # 無投資總資產
    print("無資產投資情況: ")
    無投資總資產 = 每年淨額.cumsum()
    無投資總資產.plot()#轉換資料為plot
    無投資總資產.show()
 
每年淨額計算()
   
'''考慮買房情況==========================================='''

#計算將來考慮買房時的[買房價格]
買房價格 = 300
買房頭期款 = 100
買房年紀 = 35
房貸利率 = 3
貸款年數 = 20

print('計算每年買房花費: ')
買房花費 = pd.Series(0, index=預測時段)
買房花費[買房年紀] = 買房頭期款
買房花費.loc[買房年紀:買房年紀+貸款年數-1] += (買房價格 - 買房頭期款) / 貸款年數
買房花費.plot()

#計算貸款利息
print('計算貸款利息: ')
# 先計算有多少欠款
欠款 = pd.Series(0, index=預測時段)
欠款[買房年紀] = 買房價格
欠款 = 欠款.cumsum()
欠款 = 欠款 - 買房花費.cumsum()
#欠款.plot()

利息 = 欠款.shift().fillna(0) * 房貸利率 / 100
利息.plot()

#計算繳交房租
房租年繳 = pd.Series(每月房租*12, index=預測時段)
房租年繳.loc[買房年紀:] = 0
房租年繳.plot()

每年淨額_買房 = pd.Series(0, index=預測時段)
每年淨額_買房.iloc[0] = 起始資金
每年淨額_買房.loc[:退休年齡] += 每月薪水 * 12
每年淨額_買房 -= (每月開銷*12 + 房租年繳 + 利息 + 買房花費)
每年淨額_買房.cumsum().plot()
#每年淨額_買房.plot()

#==========================
def asset_prediction(起始資金 ,起始年紀,
    每月薪水 ,
    每月開銷 ,
    每月房租 ,
    退休年齡 ,
    投資部位,
    投資年利率,
    買房價格,
    買房頭期款,
    買房年紀,
    房貸利率,
    貸款年數,):

    預測時段 = range(起始年紀, 100)
    每年淨額 = pd.Series(0, index=預測時段)
    每年淨額.iloc[0] = 起始資金
    每年淨額.loc[:退休年齡] += 每月薪水 * 12
    每年淨額 -= (每月開銷 + 每月房租) * 12
    
    
    def compound_interest(arr, ratio, return_rate):
        ret = [arr.iloc[0]]
        for v in arr[1:]:
            ret.append(ret[-1] * ratio * (return_rate/100 + 1) + ret[-1] * (1 - ratio) + v)
        return pd.Series(ret, 預測時段)
    
    買房花費 = pd.Series(0, index=預測時段)
    買房花費[買房年紀] = 買房頭期款
    買房花費.loc[買房年紀:買房年紀+貸款年數-1] += (買房價格 - 買房頭期款) / 貸款年數
    
    欠款 = pd.Series(0, index=預測時段)
    欠款[買房年紀] = 買房價格
    欠款 = 欠款.cumsum()
    欠款 = 欠款 - 買房花費.cumsum()
    利息 = 欠款.shift().fillna(0) * 房貸利率 / 100


    房租年繳 = pd.Series(每月房租*12, index=預測時段)
    房租年繳.loc[買房年紀:] = 0
    
    每年淨額_買房 = pd.Series(0, index=預測時段)
    每年淨額_買房.iloc[0] = 起始資金
    每年淨額_買房.loc[:退休年齡] += 每月薪水 * 12
    每年淨額_買房 -= (每月開銷*12 + 房租年繳 + 利息 + 買房花費)
    
    
    
    pd.DataFrame({
        'no invest, no house': 每年淨額.cumsum(),
        'invest, no house': compound_interest(每年淨額, 投資部位, 投資年利率),
        'no invest, house': 每年淨額_買房.cumsum(),
        'invest, house': compound_interest(每年淨額_買房, 投資部位, 投資年利率),
        
    }).plot()

    
    import matplotlib.pylab as plt
    plt.ylim(0, None)
    
    print('月繳房貸', (買房價格 - 買房頭期款) / 貸款年數 / 12)
    print('利息', 利息.sum() / 貸款年數)
    print('')


widgets.interact(asset_prediction, 
    起始資金=widgets.FloatSlider(min=0, max=100, step=10, value=20),
    起始年紀=widgets.IntSlider(min=0, max=100, step=1, value=30),
    每月薪水=widgets.FloatSlider(min=0, max=20, step=0.1, value=3),
    每月開銷=widgets.FloatSlider(min=0, max=20, step=0.2, value=1),
    每月房租=widgets.FloatSlider(min=0, max=20, step=0.5, value=1),
    退休年齡=widgets.IntSlider(min=0, max=100, step=1, value=60),
    投資部位=widgets.FloatSlider(min=0, max=1, step=0.1, value=0.7),
    投資年利率=widgets.FloatSlider(min=0, max=20, step=0.5, value=5),
    買房價格=widgets.IntSlider(min=100, max=2000, step=50, value=300),
    買房頭期款=widgets.IntSlider(min=100, max=2000, step=50, value=100),
    買房年紀=widgets.IntSlider(min=20, max=100, step=1, value=40),
    房貸利率=widgets.FloatSlider(min=1, max=5, step=0.1, value=2.4),
    貸款年數=widgets.IntSlider(min=0, max=40, step=1, value=20)
)




'''財報====================================================='''
number = str(input('輸入股票代號: '))
year = input("輸入年份: ")
month = input('輸入月: ')
day = input('輸入日: ')
sseason = str(input('輸入季: '))

url = f'https://mops.twse.com.tw/server-java/t164sb01?step=1&CO_ID={number}&SYEAR={year}&SSEASON={sseason}&REPORT_ID=C'  
table = pd.read_html(url)[2]

tb = pd.DataFrame(table)
print(tb)
print('='*30)
#print(tb.iat[#數字,#表格名])

'''抓取股價==============================================================='''
def crawl_price(date):
     # 將 date 變成字串 舉例：'20180525' 
    datestr = date.strftime('%Y%m%d')
    
    # 從網站上依照 datestr 將指定日期的股價抓下來
    r = requests.post('http://www.twse.com.tw/exchangeReport/MI_INDEX?response=csv&date=' + datestr + '&type=ALLBUT0999')
    
    # 將抓下來的資料（r.text），其中的等號給刪除
    content = r.text.replace('=', '')
    
    # 將 column 數量小於等於 10 的行數都刪除
    lines = content.split('\n')
    lines = list(filter(lambda l:len(l.split('",')) > 10, lines))
    
    # 將每一行再合成同一行，並用肉眼看不到的換行符號'\n'分開
    content = "\n".join(lines)
    
    # 假如沒下載到，則回傳None（代表抓不到資料）
    if content == '':
        return None
    
    # 將content變成檔案：StringIO，並且用pd.read_csv將表格讀取進來
    df = pd.read_csv(StringIO(content))
    
    # 將表格中的元素都換成字串，並把其中的逗號刪除
    df = df.astype(str)
    df = df.apply(lambda s: s.str.replace(',', ''))
    
    # 將爬取的日期存入 dataframe
    df['date'] = pd.to_datetime(date)
    
    # 將「證券代號」的欄位改名成「stock_id」
    df = df.rename(columns={'證券代號':'stock_id'})
    
    # 將 「stock_id」與「date」設定成index 
    df = df.set_index(['stock_id', 'date'])
    
    # 將所有的表格元素都轉換成數字，error='coerce'的意思是說，假如無法轉成數字，則用 NaN 取代
    df = df.apply(lambda s:pd.to_numeric(s, errors='coerce'))
    
    # 刪除不必要的欄位
    df = df[df.columns[df.isnull().all() == False]]
    
    return df

print(crawl_price(datetime.datetime(int(year),int(month),int(day))))


'''對應小資族所推薦的股價======================================='''