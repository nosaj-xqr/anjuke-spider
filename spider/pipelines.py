# -*- coding: utf-8 -*-
import pymysql

class FangjiaPipeline(object):
    def process_item(self, item, spider):
        conn=pymysql.connect(host='localhost',user='root',passwd='root',db='fangjia')
        cursor=conn.cursor()
        for i in range(0,len(item['name'])):
            name=item['name'][i]
            #此处加了多个try方法来规避爬取时部分字段未爬取到内容，从而导致数组越界等异常，但感觉不太合理，目前没想到更好的解决方案
            try:
                loc=item['location'][i]
            except Exception as err:
                loc=''
            try:
                price=item['price'][i]
            except Exception as err:
                price=''
            try:
                tag=item['tag'][i]
            except Exception as err:
                tag=''
            try:
                size=item['size'][i]
            except Exception as err:
                size=''
            try:
                url=item['url'][i]
            except Exception as err:
                url=''
            sql="insert into chongqing1(name,loc,price,tag,size,url) values ('"+name+"','"+loc+"','"+price+"','"+tag+"','"+size+"','"+url+"');"
            cursor.execute(sql)
            conn.commit()
        cursor.close()
        conn.close()
        return item
