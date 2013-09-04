#!/usr/bin/env python
# -*- coding: UTF -*-
# Create your views here.
import logging
logger = logging.getLogger(__name__)
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from wxgz_server.utils import message
from xiangqinzhushou.settings import TOKEN
from wxgz_server.utils.parser import Parser
@csrf_exempt  
def home(request):
    if request.method == 'GET':
        # get方法的时候返回验证字符串
        myresponse = HttpResponse()
        if message.check_signature(request.GET, TOKEN):
            myresponse.write(request.GET.get('echostr'))
            return myresponse
        else:
            myresponse.write('不提供直接访问！')
            return myresponse
        # 处理微信发过来的post请求
    if request.method == 'POST':
        received_msg = Parser(request.body)
        logger.info('收到一条来自 %s 的 %s 消息: %s',
                    received_msg.from_user_name,
                    received_msg.msg_type,
                    received_msg.content)
        msg = message.build_message(received_msg)
        logging.info("msg = %s", msg)
        if received_msg.msg_type=='event' and received_msg.event == 'subscribe':
            return message.subscribe_response(to_user_name=received_msg.from_user_name,
                                            from_user_name=received_msg.to_user_name)
        elif received_msg.msg_type=='event' and received_msg.event == 'unsubscribe':
            return HttpResponse('成功取消关注！')
        else:
            return message.default_response(to_user_name=received_msg.from_user_name,
                                            from_user_name=received_msg.to_user_name)
            
