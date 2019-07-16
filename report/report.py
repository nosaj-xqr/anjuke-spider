import pymysql
import pandas as pda
import re
import numpy as np
import matplotlib.pylab as pyl
import matplotlib as mp

#设置能显示中文的图表字体
mp.rcParams['font.sans-serif'] = ['KaiTi']
mp.rcParams['font.serif'] = ['KaiTi']

conn=pymysql.connect(host='localhost',user='root',passwd='root',db='fangjia')
data=pda.read_sql('select * from chongqing1',con=conn)
df1=np.array(data)
df2=df1.T
list_all=df2.tolist()

list_loc=list_all[1]
for i in range(0,len(list_loc)):
    pat_loc='\[\xa0(.*?)\xa0'
    list_loc[i]=re.compile(pat_loc).findall(list_loc[i])
    list_loc[i]=str(list_loc[i])
#转为集合进行去重，获取重庆各个区名
list_loc_set=set(list_loc)

#部分楼盘使用的是万元/套的单位，于是采取总价除以面积的方法获得每平米的房价
list_size=list_all[4]
sum_size=[]
for j in range(0,len(list_size)):
    pat_size='建筑面积：(.*?)-'
    list_size[j]=re.compile(pat_size).findall(list_size[j])
    if list_size[j]==list(''):
        list_size[j]='0'
    list_size[j]=list(map(lambda x:float(x),list_size[j]))
    sum_size+=list_size[j]
    
list_price=list_all[2]
sum_price=[]
for k in range(0,len(list_price)):
    pat_price1='(\d*?)元'
    pat_price2='(\d*?)万元'
    price=re.compile(pat_price1).findall(list_price[k])
    if price==['']:
        price=re.compile(pat_price2).findall(list_price[k])
        if price != list('') and sum_size[k] != 0:
            price=list(map(lambda x:float(x),price))
            price=np.multiply(price,10000)
            price=np.divide(price,sum_size[k])          
    price=list(map(lambda x:float(x),price))
    if price==list(''):
        list_price[k]=[0]
    else:
        list_price[k]=price
    sum_price+=list_price[k]

#各区楼盘数量
list_price_sum=[]
#各区楼盘均值
list_price_average=[]
for city in list_loc_set:
    #各区楼盘价格
    list_price_loc=[]
    sum1=0
    sum2=0
    for n in range(0,len(list_loc)):
        if city==list_loc[n]:
            sum1 += 1
        #设置5万的原因是依照日常经验，去掉部分特殊楼盘以及异常房价
        if city==list_loc[n] and (sum_price[n] > 0 and sum_price[n] < 50000):
            list_price_loc.append(sum_price[n])
            sum2+=sum_price[n]
    list_price_sum.append(sum1)
    list_price_average.append(sum2/sum1)
    pyl.title(city+'楼盘价格分布')
    pyl.ylabel('价格')
    x=[t for t in range(0,len(list_price_loc))]
    list_price_loc.sort()
    y=list_price_loc
    pyl.plot(x,y,'o')
    pyl.show()
#统计楼盘分布
x1=[]
for city in list_loc_set:
    x1.append(city)
y1=list_price_sum
pyl.title('重庆楼盘分布')
pyl.bar(x1,y1,align='center')
pyl.show()

#统计各区楼盘均价
y2=list_price_average
pyl.title('重庆各区普通楼盘均价')
pyl.bar(x1,y2,align='center')
pyl.show()
