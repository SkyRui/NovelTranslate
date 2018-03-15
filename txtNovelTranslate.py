#coding=utf-8
import httplib
import md5
import urllib
import random
import json
import sys
#################################################
appid = '20180204000120849'			#keyID
secretKey = 'uc06bnLi6fNKg5WdUV63'	#secretKey
#################################################
def TransByBaidu(text,fromLang = 'auto',toLang = 'zh'):
    httpClient = None
    myurl = '/api/trans/vip/translate'
    q = text
    salt = random.randint(32768, 65536)
    sign = appid+q+str(salt)+secretKey

    m1 = md5.new()
    m1.update(sign)
    sign = m1.hexdigest()

    myurl = myurl+'?appid='+appid+'&q='+urllib.quote(q)+'&from='+fromLang+'&to='+toLang+'&salt='+str(salt)+'&sign='+sign
    try:
        httpClient = httplib.HTTPConnection('api.fanyi.baidu.com')
        httpClient.request('GET', myurl)
        #response是HTTPResponse对象
        response = httpClient.getresponse()        
        result = response.read()
        data = json.loads(result)
        return data["trans_result"][0]["dst"]
    except Exception, e:
        print e
    finally:
        if httpClient:
            httpClient.close()
#########################################
s_path = sys.argv[1]
s_file = open(s_path, 'r')

name = s_path.split('/')[-1] + ".ch.txt"
t_file = open(name, 'a')

lines = s_file.readlines()
lineslen = len(lines)

print "total lenght:"+str(lineslen)
v = 0
e = 0
while v < lineslen-1:
    try:
        for value , line in enumerate(lines[v:]):
            print "NO."+str(v+1)+"/"+str(lineslen)+" Line Translate OK!"
            if line == '\n':
            	t_file.write('\n')
                continue
            tran = TransByBaidu(line) + '\n'
            v+=1
            tran = tran.encode("utf-8")
            t_file.write(tran)
    except Exception ,a:
        print a
        e+=1
    finally:
        t_file.write(tran)
print "error: "+str(e)
s_file.close()
t_file.close()