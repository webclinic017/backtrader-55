import os
import sys
import baostock as bs
import pandas as pd
from utils.Utils import GetStartDate
from utils.Utils import GetEndDate
from utils.Utils import GetModPath

modpath = GetModPath()
start_date = GetStartDate()
end_date = GetEndDate()

if __name__ == '__main__':
    # 登陆系统
    lg = bs.login()
    # 显示登陆返回信息
    print('login respond error_code:' + lg.error_code)
    print('login respond  error_msg:' + lg.error_msg)

    # 获取存款准备金率
    rs = bs.query_required_reserve_ratio_data(start_date=start_date, end_date=end_date)
    print('query_required_reserve_ratio_data respond error_code:' + rs.error_code)
    print('query_required_reserve_ratio_data respond  error_msg:' + rs.error_msg)

    # 打印结果集
    data_list = []
    while (rs.error_code == '0') & rs.next():
        # 获取一条记录，将记录合并在一起
        data_list.append(rs.get_row_data())
    result = pd.DataFrame(data_list, columns=rs.fields)

    # 结果集输出到csv文件
    file_name = "reserve_ratio.csv"
    datapath = os.path.join(modpath, '..\\datas\\' + file_name)
    result.to_csv(datapath)
    print("get deposit rate to reserve_ratio.csv done")

    # 登出系统
    bs.logout()
