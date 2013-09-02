'''
Created on 2013-8-28

@author: yongtaoxing
'''
import logging
logger = logging.getLogger(__name__)

import hashlib
from wxgz_server.models import TextMessage, ImageMessage, LinkMessage, LocationMessage, EventMessage
from datetime.datetime import now
from django.shortcuts import render_to_response
from datetime import datetime

def check_signature(request_dict, token):
    '''检查消息是否是微信发过来的'''
    if request_dict.get('signature') and request_dict.get('timestamp') and request_dict.get('nonce') and request_dict.get('echostr'):
        signature = request_dict.get('signature')
        timestamp = request_dict.get('timestamp')
        nonce = request_dict.get('nonce')
        token = token
        tmplist = [token, timestamp, nonce]
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

def build_message(parsed_message):
    if parsed_message.msg_type == 'text':
        msg = TextMessage()
        msg.from_user_name = parsed_message.from_user_name
        msg.to_user_name = parsed_message.to_user_name
        msg.message_type = parsed_message.msg_type
        msg.create_time = datetime.fromtimestamp(parsed_message.create_time)
        
        msg.message_id = parsed_message.msg_id
        msg.content = parsed_message.content
        
        msg.save()
        return msg
        
    elif parsed_message.msg_type == 'image':
        msg = ImageMessage()
        msg.from_user_name = parsed_message.from_user_name
        msg.to_user_name = parsed_message.to_user_name
        msg.message_type = parsed_message.msg_type
        msg.create_time = datetime.fromtimestamp(parsed_message.create_time)
        
        msg.message_id = parsed_message.msg_id
        msg.picture_url = parsed_message.pic_url
        
        msg.save()
        return msg
    
    elif parsed_message.msg_type == 'location':
        msg = LocationMessage()
        msg.from_user_name = parsed_message.from_user_name
        msg.to_user_name = parsed_message.to_user_name
        msg.message_type = parsed_message.msg_type
        msg.create_time = datetime.fromtimestamp(parsed_message.create_time)
        
        msg.message_id = parsed_message.msg_id
        msg.location_x = parsed_message.location_x
        msg.location_y = parsed_message.location_y
        msg.scale = parsed_message.scale
        msg.label = parsed_message.label
        
        msg.save()
        return msg
    
    elif parsed_message.msg_type == 'link':
        msg = LinkMessage()
        msg.from_user_name = parsed_message.from_user_name
        msg.to_user_name = parsed_message.to_user_name
        msg.message_type = parsed_message.msg_type
        msg.create_time = datetime.fromtimestamp(parsed_message.create_time)
        
        msg.message_id = parsed_message.msg_id
        msg.title = parsed_message.title
        msg.description = parsed_message.description
        msg.url = parsed_message.url
        
        msg.save()
        return msg
    
    elif parsed_message.msg_type == 'event':
        msg = EventMessage()
        msg.from_user_name = parsed_message.from_user_name
        msg.to_user_name = parsed_message.to_user_name
        msg.message_type = parsed_message.msg_type
        msg.create_time = datetime.fromtimestamp(parsed_message.create_time)
        
        msg.event = parsed_message.event
        msg.event_key = parsed_message.event_key
        
        msg.save()
        return msg
        
    else:
        logging.info("unknown message: %s", parsed_message)
        return None
    
    
def default_response(to_user_name, from_user_name):
    msg = TextMessage(to_user_name=to_user_name, from_user_name=from_user_name)
    msg.content = '您好，您的消息系统已经收到，会马上处理，请耐心等待。'
    msg.create_time = now()    
    msg.save()
    return render_to_response('response/text_to_user.xml', {'msg':msg})

def subscribe_response(to_user_name, from_user_name):
    msg = TextMessage(to_user_name=to_user_name, from_user_name=from_user_name)
    msg.content = '您好，欢迎订阅相亲助手！'
    msg.create_time = now()
    msg.save()
    return render_to_response('response/text_to_user.xml', {'msg':msg})
    
if __name__ == '__main__':
    pass
