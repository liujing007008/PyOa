import threading
from random import random
from requests import utils
from time import time, sleep
from collections import deque
import requests
import json
from lxml import etree
import re


class OA:
    domain = 'http://10.111.240.12'
    pki_login = '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'
    userId = 'U=92f6fe1c/O=05000001'
    '''
    以下是用于登录的请求头
    '''
    cookie_login = {'__PLATFORM_SESSION_TIME_KEY': '{:.0f}'.format((time() * 1000))}
    url_login = 'http://10.111.240.12/appuiinteg/pc/pkiLogin/dl'
    postBody_login = {
        'JSESSIONID': '',
        'parm_c': 'admin',
        'parm_d': pki_login,
        'parm_e': userId,
        'parm_f': '',
        'parm_a': '',
        'parem_b': '',
    }
    header_login_g = {
        'Accept': 'image/gif, image/jpeg, image/pjpeg, application/x-ms-application, application/xaml+xml, application/x-ms-xbap, */*',
        'Referer': 'http://10.111.240.12/appuiinteg/pc/login',
        'Accept-Language': 'zh-Hans-CN,zh-Hans;q=0.5',
        'User-Agent': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 10.0; WOW64; Trident/7.0; .NET4.0C; .NET4.0E; .NET CLR 2.0.50727; .NET CLR 3.0.30729; .NET CLR 3.5.30729)',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept-Encoding': 'gzip, deflate',
        'Content-Length': '2238',
        'Host': '10.111.240.12',
        'Connection': 'Keep-Alive',
        'Pragma': 'no-cache',
    }

    def login(self):
        return self.__login_get_sess()

    def __login_get_cookie(self):
        try:
            session = requests.session()
            response = session.post(url=self.url_login, headers=self.header_login_g, data=self.postBody_login,
                                    cookies=self.cookie_login)
        except Exception as e:
            print('request error')
            return e
        else:
            if response.status_code == 200:
                cookies_dict = requests.utils.dict_from_cookiejar(session.cookies)
                return cookies_dict

    def __login_get_sess(self):
        try:
            session = requests.session()
            response = session.post(url=self.url_login, headers=self.header_login_g, data=self.postBody_login,
                                    cookies=self.cookie_login)
        except Exception as e:
            print("  ● 登陆失败")
            print(e)
            return e
        else:
            if response.status_code == 200:
                print("  ● 登陆成功")
                return session


class OaTaskQue(OA):
    '''
    以下是获取待办文件列表的请求头
    '''
    url_getQue = 'http://10.111.240.12/apptodone/pc/todolist/init'
    postBody_getQue = {'param': '{"op":"reload","serverCtrl":"","data":{"groupType":"1"}}'}
    header_getQue_p = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'X-Requested-With': 'XMLHttpRequest',
        'Referer': 'http://10.111.240.12/apptodone/pc/todolist/open',
        'Accept-Language': 'zh-Hans-CN,zh-Hans;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'User-Agent': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 10.0; WOW64; Trident/7.0; .NET4.0C; '
                      '.NET4.0E; .NET '
                      'CLR 2.0.50727; .NET CLR 3.0.30729; .NET CLR 3.5.30729)',
        'Content-Length': '110',
        'Host': '10.111.240.12',
        'Connection': 'Keep-Alive',
        'Pragma': 'no-cache',
    }
    '''
    以下是每份文件对象操作的请求头
    '''

    def __init__(self):
        self.doc_list = []
        self.task_queue = deque()
        self.sess = self.login()

    def get_doc_list(self, url=None, headers=None, data=None):
        '''
        发送请求获取待办文件清单
        :return:
        返回一个对象列表[{},{}]，每个对象就是一份文件的信息，同时将该对象列表绑定在实例身上
        '''
        url = url if url else self.url_getQue
        headers = headers if headers else self.header_getQue_p
        data = data if data else self.postBody_getQue
        try:
            response = self.sess.post(url=url, headers=headers, data=data)
        except Exception as e:
            print('  ● Unknown Error with request for getting doc map ')
            print(e)
            return None
        else:
            if response.status_code == 200:
                try:
                    res = response.json()
                except Exception as e:
                    print(e)
                    print(response)
                    print('  ● Response content is not expect for getting doc map!')
                else:
                    for i in res["result"][0]["data"]:
                        self.doc_list.extend(i["map"])
                return self.doc_list

    def enter_queue(self, li):
        try:
            for i in li:
                if i not in self.task_queue:
                    self.task_queue.append(i)
            return self.task_queue
        except Exception as e:
            print(e)
            return None

    def watch_task_queue(self):
        try:
            if not self.task_queue:
                print('  ● Task_queue is empty. Call function for getting doc list!')
                li = self.get_doc_list()
                return self.enter_queue(li)
            else:
                print('  ● Task_queue is not empty')
        except Exception as e:
            print(e)
            return None

    def daemon_task(self):
        while True:
            sleep(1)
            self.watch_task_queue()

    def test(self):
        return self.__login_get_sess()


class DocHandler(OA):
    header_detail_g = {
        'Accept': 'image/gif, image/jpeg, image/pjpeg, application/x-ms-application, application/xaml+xml, '
                  'application/x-ms-xbap, */*',
        'Accept-Language': 'zh-Hans-CN,zh-Hans;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'User-Agent': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 10.0; WOW64; Trident/7.0; .NET4.0C; '
                      '.NET4.0E; .NET CLR 2.0.50727; .NET CLR 3.0.30729; .NET CLR 3.5.30729)',
        'Host': '10.111.240.12',
        'Connection': 'Keep-Alive',
    }
    header_detail_p = {
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Accept': '*/*',
        'X-Requested-With': 'XMLHttpRequest',
        'Referer': '',
        'Accept-Language': 'zh-Hans-CN,zh-Hans;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'User-Agent': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 10.0; WOW64; Trident/7.0; .NET4.0C; '
                      '.NET4.0E; .NET CLR 2.0.50727; .NET CLR 3.0.30729; .NET CLR 3.5.30729)',
        'Host': '10.111.240.12',
        'Connection': 'Keep-Alive',
        'Pragma': 'no-cache',
    }

    def __init__(self):
        self.sess = self.login()

    def get_doc_detail(self, url, workId):
        url = self.domain + url
        payload = {'userId': self.userId, 'workItemId': workId}
        # print("  ● Let me have a rest. See you in 2 seconds. ZZzzzzzz..............")
        # time.sleep(2)
        # print("  ● I will start working now")
        try:
            print('  ● Getting detail page from: ', url)
            print('  ● The workItemId I am dealing is: ', workId)
            response = self.sess.get(headers=self.header_detail_g, url=url, params=payload)
            html = response.content.decode()
            if response.status_code == 200:
                # print('  ● Success to get detail page: ', response.status_code)
                return html
            else:
                print('  ● Failure to get detail page: ', response.status_code)
                return False
        except Exception as e:
            print('  ● Something was wrong with getting detail page')
            print(e)
            return False

    def send_cmt(self, pageobj, cmt):
        print('Will send requests to server for commenting "已阅"!')
        math_random = str(random() * 1000)
        self.header_detail_p['Referer'] = pageobj.refer_url
        url = pageobj.servePath + '/csg-front-framework/pc/component/form/csgcmtput/putCsgCmt' + '/?mathrandom=' + math_random
        pageobj.cmt_params['content'] = cmt
        response = self.sess.post(url, headers=self.header_detail_p, data=pageobj.cmt_params)
        try:
            if response.status_code == 200:
                if response.json():
                    res = response.json()
                    print('  ● Cmt_response:', res)
                    if res['nextOperationType'] == 'Reload':
                        return True
                    else:
                        print('  ● Something was wrong to send a comment 1. {}'.format(res['nextOperationType']))
                        return False
                else:
                    print('  ● Something was wrong to send a comment 2. {}'.format(None))
                    return False
            else:
                print('  ● Something was wrong to send a comment 3. {}'.format(response.status_code))
                return False
        except Exception as e:
            print(e)
            return False

    def send_end(self, pageobj):
        if pageobj.end_params_app:
            print('  ● Will send requests to server for ending by using app!')
            self.end_appaction(pageobj)

        if pageobj.end_params_flow:
            print('  ● Will send requests to server for ending by using flow!')
            self.end_flowaction(pageobj)

    def end_appaction(self, pageobj):
        url = pageobj.servePath + '/csg-front-framework/pc/component/form/csgtoolbar/callEngineAfterAppAction'
        for item in pageobj.end_params_app.values():
            if bool(item) is None:
                return [False, {'error': 'Some params is None with ending doc'}]
        try:
            payload = pageobj.end_params_app
            response = self.sess.get(url, headers=self.header_detail_g, params=payload)
            if response.status_code == 200:
                res_dict = response.json()
                print('  ● End_response by app:', res_dict)
                if res_dict.get('succeed') == 'true' or 'True':
                    print('  ● Push off doc from my ★app queue. Success!')
                    return [True, 'Success to wash out doc from que!']
                elif res_dict.get('data').get('nextOperationType') == 'Close':
                    print('  ● Push off doc from my ★app queue. Success!')
                    return [True, 'Success to wash out doc from que!']
                else:
                    print('  ● Server did not response right content by end_app')
                    return [False, 'Server did not response right content']
            else:
                print('  ● failure for wash out doc from que,because Server refuse! The statu code is {}'.format(
                    response.status_code))
                return [False, 'failure for wash out doc from que,because Server refuse! The statu code is {}'.format(
                    response.status_code)]
        except Exception as e:
            print('  ● End post has not sent successfully')
            print(e)
            return [False, 'End post has not sent successfully']

    def end_flowaction(self, pageobj):
        for item in pageobj.end_params_flow.values():
            if bool(item) is None:
                return [False, {'error': 'Some params is None with ending doc'}]
        send_pre = self.pre_end_flowaction(pageobj)
        if send_pre is True:
            url = pageobj.servePath + '/csg-front-framework/pc/component/form/csgflowautosend/csgflowautosend/autoSend'
            payload = pageobj.end_params_flow
            response = self.sess.post(url, headers=self.header_detail_p, data=payload)
            if response.status_code == 200:
                res_dict = response.json()
                sign_end = res_dict.get('postMsg')
                print('  ● End_response by flow:', res_dict)
                if sign_end == '发送成功!' or '发送成功！':
                    print(sign_end)
                    print('  ● Push off doc from my ★flow queue. Success!')
                    return [True, 'Success to wash out doc from que!']
                elif nextOperationType == 'Close':
                    print(sign_end)
                    print('  ● Push off doc from my ★flow queue. Success!')
                    return [True, 'Success to wash out doc from que!']
                else:
                    print(res_dict)
                    print('  ● Server did not response right content 1 by ★flow_end')
                    print(res_dict.get('postMsg'))
                    return [False, 'Server did not response right content']
            else:
                print('  ● failure for wash out doc from que,because Server refuse!statu code is {}'.format(
                    response.status_code))
                return [False, 'failure for wash out doc from que,because Server refuse! The statu code is {}'.format(
                    response.status_code)]
        else:
            print('  ● Server did not response right content by predeal failure')
            return [False, 'Server did not response right content']

    def pre_end_flowaction(self, pageobj):
        url = pageobj.servePath + '/csg-front-framework/pc/component/form/csgflowautosend/csgflowautosend/getAutoSendCtrl'
        header_post_pre = self.header_detail_p
        header_post_pre['Accept'] = 'application/json, text/javascript, */*; q=0.01'
        response = self.sess.post(url, headers=header_post_pre, data=pageobj.end_params_flow)
        if response.status_code == 200:
            if response.json():
                res = response.json()
                if res.get('confirmMsg') == "文件将送至：审计部文书（周南）进行办理":
                    print('  ● 文件将送至：文书进行办理')
                    return True
                else:
                    print('next not find {}'.format(res))
                    return False
            else:
                print('  ● pre_end_flowaction response is {}'.format(response.content.decode()))
                return False
        else:
            print('  ● pre_end_flowaction response_code is {}'.format(response.status_code))
            return False


class OaParse(OA):
    def __init__(self, html):
        self.html = html
        self.process = {}
        self.webcfg = {}
        self.servePath = ''
        self.hidden = {}
        self.cmt_params = {}
        self.workid = ''
        self.refer_url = ''
        self.end_params_app = {}
        self.end_params_flow = {}
        pass

    def parse_page(self):
        self._get_page_cfg(self.html)
        self._get_hidden(self.html)
        self._get_cmt_params()
        self._get_end_params()

    def _get_page_cfg(self, html=None):
        '''
        获取页面配置对象，webCfg、processObj、newAttachReadOnly，挂载到对象属性
        :param html:
        :return:
        '''
        if html is None:
            html = self.html
        # print("  ● Get_pagecfg(): Getting webCfg、processObj、newAttachReadOnly")
        pattern_p = re.compile(r'\s*(var\sprocessObj\s=\s)(.*);')
        pattern_w = re.compile(r'(\s*webCfg\s=\s)\{([\s\S]*)\};')
        html_obj = etree.HTML(html)
        html_list = html_obj.xpath("//script[not(@*)]/text()")
        for item in html_list:
            match_pro = pattern_p.match(item)
            if match_pro:
                self.process = json.loads(match_pro.group(2))
            match_web = pattern_w.match(item)
            if match_web:
                web_str = match_web.group(2)
                list_temp = web_str.strip(',').split(',')
                for i in list_temp:
                    i_str = i.replace("\r", "").replace("\t", "").replace("\n", "").replace(" ", "")
                    j_list = i_str.split(':"')
                    dict_temp = {j_list[0]: j_list[1].strip('"')}
                    self.webcfg.update(dict_temp)
        self.servePath = self.domain + self.webcfg[
            'servePath']
        self.flowActionAOList = self.process.get('flowProcessId')
        self.appActionAOList = ''
        print("  ● Get_pagecfg: Success")
        return

    def _get_hidden(self, html=None):
        if html is None:
            html = self.html
        html_obj = etree.HTML(html)
        html_list = html_obj.xpath("//input[@type='hidden'or'Hidden']")
        for item in html_list:
            try:
                _key = item.xpath('@id')
                _value = item.xpath('@value')
                _name = item.xpath('@name')
            except Exception as e:
                print(e)
            else:
                if len(_key) == 0:
                    continue
                else:
                    key = _key[0] if bool(_key) else ''
                    name = _name[0] if bool(_name) else ''
                    value = _value[0] if bool(_value) else ''
                temp_dict = {str(key): {'name': str(name), 'value': str(value)}}
                self.hidden.update(temp_dict)
        if self.hidden.get("toDoTitle"):
            self.title = self.hidden.get("toDoTitle").get('value')
        elif self.hidden.get("toDoTitle") is None:
            self.title = self.hidden.get('todoTitle').get('value')
        if self.hidden.get("toDoUrl"):
            self.refer_url = 'http://10.111.240.12' + self.hidden.get("toDoUrl").get('value')
        elif self.hidden.get("toDoUrl") is None:
            self.refer_url = 'http://10.111.240.12' + self.hidden.get('todoUrl').get('value')
        return self.hidden

    def _get_cmt_params(self):
        try:
            self.cmt_params['processId'] = self.process.get('flowProcessId')
            self.cmt_params['workItemId'] = self.process['curPerformerAO']['workItemId']
            self.workid = self.cmt_params['workItemId']
            self.cmt_params['setAgentDate'] = 'false'
            self.cmt_params['agentUserId'] = ''
            self.cmt_params['agentDate'] = ''
            self.cmt_params['sessionId'] = self.hidden['sessionId']['value']
            self.cmt_params['isEntrust'] = 'false'
        except Exception as e:
            return [False, {'Info': 'Failure to get_cmt_params', 'code': 0}]
        try:
            self.cmt_params['pluginId'] = self.process['commentActionAOList'][0][
                'cmtActionsPluginId']  # 这里如果获取不到意见操作对象，可能会报错。下一步应该考略忽略这里，在后续代码中判断是否获取到意见字典。
            self.cmt_params['cmtActionId'] = self.process['commentActionAOList'][0]['id']
        except Exception as e:
            return [False, {'Info': 'Failure to get_cmt_params', 'code': 1}]
        return [True, {'Info': 'Success to get_cmt_params', 'code': 0}]

    def _get_end_params(self):
        _flowActionAOList = self.process.get('flowActionAOList')
        _appActionAOList = self.process.get('appActionAOList')
        if _appActionAOList:
            print('  ● _appActionAOList is not None')
            self.end_params_app['processId'] = self.process.get('flowProcessId')
            self.end_params_app['sessionId'] = self.cmt_params['sessionId']
            self.end_params_app['workItemId'] = self.workid
            for item in _appActionAOList:
                if item.get('name') == "已阅":
                    print('  ● Get name which is "已阅" from _appActionAOList')
                    self.end_params_app['pluginId'] = item.get('appActionsPluginId')
                    self.end_params_app['appActionId'] = item.get('id')
                    return self.end_params_app

        if _flowActionAOList:
            # print('  ● _flowActionAOList is not None')
            self.end_params_flow['processId'] = self.process.get('flowProcessId')
            self.end_params_flow['sessionId'] = self.cmt_params['sessionId']
            self.end_params_flow['workItemId'] = self.workid
            self.end_params_flow['agenteUserCode'] = ''
            for item in _flowActionAOList:
                if item.get('name') in ['处理完毕', '阅办完毕', '办理完毕', '送文件归档']:
                    # print('  ● Get name which is "处理完毕', '阅办完毕', '送文件归档" from _flowActionAOList')
                    self.end_params_flow['pluginId'] = item.get('flowActionsPluginId')
                    self.end_params_flow['flowActionId'] = item.get('id')
                    return self.end_params_flow
        print('  ● Error:Both of flow and app are not found')
        return True


if __name__ == '__main__':
    OA = OaTaskQue()
    print('  ● The task que length:  ★', len(OA.task_queue))
    t_task_watch = threading.Thread(target=OA.daemon_task)
    t_task_watch.setDaemon(True)
    t_task_watch.start()
    handler = DocHandler()
    while True:
        if OA.task_queue:
            x = OA.task_queue.popleft()
            wid = x.get('workItemId')
            todoUrl = x.get('todoUrl')
            pageHtml = handler.get_doc_detail(url=todoUrl, workId=wid)
            x['html'] = pageHtml
            page = OaParse(pageHtml)
            page.parse_page()
            print('  ● Dealing doc: {}'.format(page.title))
            handler.send_cmt(page, "已阅")
            handler.send_end(page)
            print('  ● The task que length:  ★', len(OA.task_queue))
            sleep(10)
        else:
            continue
