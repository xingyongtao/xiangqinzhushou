# Create your views here.
import logging
logger = logging.getLogger(__name__)
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.shortcuts import render_to_response
from wxgz_server.utils import message
from xiangqinzhushou.settings import TOKEN
from wxgz_server.utils.parser import Parser
@csrf_exempt  
def home(request):
    if request.method == 'GET':
        #get方法的时候返回验证字符串
        myresponse = HttpResponse()
        if message.check_signature(request.GET, TOKEN):
            myresponse.write(request.GET.get('echostr'))
            return myresponse
        else:
            myresponse.write('不提供直接访问！')
            return myresponse
        #处理微信发过来的post请求
    if request.method == 'POST':
        received_msg = Parser(request.body)
        logger.info('收到一条来自 %s 的 %s 消息: %s', received_msg.from_user_name, received_msg.msg_type, received_msg.content)
        #在用户没有会话的情况下进行正常的文字消息处理
        if received_msg.msg_type == 'text': #处理文字类型的消息
            return default_response(received_msg)
            #收到事件推送的处理
        elif received_msg.msg_type == 'event':
            if received_msg.event == u'subscribe':
                msg = TextMsg()
                msg_init(msg,received_msg)
                msg.content = DEFAULT_MSG
                return render_to_response('response/text_to_user.xml',locals())
            else :
                return HttpResponse('成功取消关注！')