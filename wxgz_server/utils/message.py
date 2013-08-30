'''
Created on 2013-8-28

@author: yongtaoxing
'''
import hashlib
from wxgz_server.models import TextMessage
from datetime.datetime import now
from django.shortcuts import render_to_response

def check_signature(request_dict, token):
    '''检查消息是否是微信发过来的'''
    if request_dict.get('signature') and request_dict.get('timestamp') and request_dict.get('nonce') and request_dict.get('echostr'):
        signature = request_dict.get('signature')
        timestamp = request_dict.get('timestamp')
        nonce = request_dict.get('nonce')
        token = token
        tmplist = [token,timestamp,nonce]
        tmplist.sort()
        newstr = ''.join(tmplist)
        sha1result = hashlib.sha1()
        sha1result.update(newstr)
        if sha1result.hexdigest() == str(signature):
            return True
        else:
            return False
    else:
        return False     
    
def default_response(to_user_name, from_user_name):
    msg = TextMessage(to_user_name = to_user_name, from_user_name = from_user_name)
    msg.content='您好，您的消息系统已经收到，会马上处理，请耐心等待。'
    msg.create_time = now()    
    msg.save()
    return render_to_response('response/text_to_user.xml',{'msg':msg})

def subscribe_response(to_user_name, from_user_name):
    msg = TextMessage(to_user_name = to_user_name, from_user_name = from_user_name)
    msg.content='您好，欢迎订阅相亲助手！'
    msg.create_time = now()
    msg.save()
    return render_to_response('response/text_to_user.xml',{'msg':msg})
    
if __name__ == '__main__':
    pass