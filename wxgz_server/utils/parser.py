'''
Created on 2013-8-29

@author: yongtaoxing
'''
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET
try:
    import cStringIO as StringIO
except:
    import StringIO

class Parser(object):
    '''
    classdocs
    '''
    def __init__(self, xml_strs):
        '''传入一个xml字符串来初始化类，自动生成一个文档树，
        并调用get_object函数获得一个包含消息各个属性的对象'''
        xml_file = StringIO.StringIO(xml_strs)
        xml_tree = ET.ElementTree(file=xml_file)
        root = xml_tree.getroot()
        msgtype = xml_tree.find('MsgType').text
        if msgtype == 'text':
            self.get_text_msg(root)
        elif msgtype == 'image':
            self.get_img_msg(root)
        elif msgtype == 'location':
            self.get_location_msg(root)
        elif msgtype == 'link':
            self.get_link_msg(root)
        elif msgtype == 'event':
            self.get_event_msg(root)
        
    def get_text_msg(self, root):
        '''文本消息'''
        self.to_user_name = root[0].text
        self.from_user_name = root[1].text
        self.create_time = root[2].text
        self.msg_type = root[3].text
        self.content = root[4].text
        self.msg_id = root[5].text
        
    def get_img_msg(self, root):
        '''图片消息'''
        self.to_user_name = root[0].text
        self.from_user_name = root[1].text
        self.create_time = root[2].text
        self.msg_type = root[3].text
        self.pic_url = root[4].text
        self.msg_id = root[5].text
    def get_location_msg(self, root):
        '''地理位置消息'''
        self.to_user_name = root[0].text
        self.from_user_name = root[1].text
        self.create_time = root[2].text
        self.msg_type = root[3].text
        self.location_x = root[4].text
        self.location_y = root[5].text
        self.scale = root[6].text
        self.label = root[7].text
        self.msg_id = root[8].text
    def get_link_msg(self, root):
        '''链接消息推送'''
        self.to_user_name = root[0].text
        self.from_user_name = root[1].text
        self.create_time = root[2].text
        self.msg_type = root[3].text
        self.title = root[4].text
        self.description = root[5].text
        self.url = root[6].text
        self.msg_id = root[7].text
    def get_event_msg(self, root):
        '''事件推送'''
        self.to_user_name = root[0].text
        self.from_user_name = root[1].text
        self.create_time = root[2].text
        self.msg_type = root[3].text
        self.event = root[4].text
        self.event_key = root[5].text
