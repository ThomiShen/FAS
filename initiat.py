import akshare as ak
stock_300029 = ak.stock_zh_a_spot_em().loc[ak.stock_zh_a_spot_em()['代码'] == '300029']["60日涨跌幅"]
