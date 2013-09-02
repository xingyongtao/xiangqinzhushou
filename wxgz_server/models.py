from django.db import models
import time

# Create your models here.
class WeixinUser(models.Model):
    name = models.CharField(max_length=100, primary_key=True, verbose_name='OpenID')
    publish_message = models.BooleanField(default=False)
    first_login_time = models.DateTimeField(auto_now_add=True)
    last_login_time = models.DateTimeField(auto_now=True)

class BaseMessage(models.Model):
    MESSAGE_TYPES = (
                     ('text', '文本消息'),
                     ('image', '图片消息'),
                     ('location', '地理位置消息'),
                     ('link', '链接消息'),
                     ('event', '事件推送'),
                     ('music', '音乐消息'),
                     ('news', '图文消息'),
                     )
    from_user_name = models.CharField(max_length=100, verbose_name='OpenID')
    to_user_name = models.CharField(max_length=100, verbose_name='OpenID')
    message_type = models.CharField(max_length=8, verbose_name='消息类型', choices=MESSAGE_TYPES)
    create_time = models.DateTimeField()

    class Meta:
        abstract = True
        
    def createtime(self):
        return time.mktime(self.create_time.timetuple())
        
class TextMessage(BaseMessage):
    message_id = models.IntegerField()
    content = models.TextField()
    
class ImageMessage(BaseMessage):
    message_id = models.IntegerField()
    picture_url = models.CharField(max_length=500)
    
class LocationMessage(BaseMessage):
    message_id = models.IntegerField()
    location_x = models.CharField(max_length=20, verbose_name='地理位置纬度')
    location_y = models.CharField(max_length=20, verbose_name='地理位置经度')
    scale = models.CharField(max_length=10, verbose_name='地图缩放大小')
    label = models.CharField(max_length=50, verbose_name='地理位置信息')
    
class LinkMessage(BaseMessage):
    message_id = models.IntegerField()
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=100)
    url = models.CharField(max_length=500)
    
class EventMessage(BaseMessage):
    EVENT_TYPES = (
                   ('subscribe', '订阅'),
                   ('unsubscribe', '取消订阅'),
                   ('CLICK', '自定义菜单点击事件')
                   )
    event = models.CharField(max_length=15, verbose_name='事件类型', choices=EVENT_TYPES)
    event_key = models.CharField(max_length=20, verbose_name='事件KEY值，与自定义菜单接口中KEY值对应')

class MusicMessage(BaseMessage):
    music_url = models.CharField(max_length=500, verbose_name='音乐链接')
    hq_music_url = models.CharField(max_lengh=500, verbose_name='高质量音乐链接，WIFI环境下优先使用该链接播放音乐')
    
class NewsMessage(BaseMessage):
    article_count = models.SmallIntegerField()
    
class SubNewsMessage(NewsMessage):
    parent_news = models.ForeignKey(NewsMessage)
    index = models.SmallIntegerField(verbose_name='消息的索引位置，从0开始')
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=100)
    picture_url = models.CharField(max_length=500)
    url = models.CharField(max_length=500)
