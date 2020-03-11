import requests
import traceback
import logging
import json

logger = logging.getLogger("default")

# def get_session(login_url,username,password,session):
#     def decorator(func):
#         @wraps(func)
#         def inner(*args,**kwargs):
#             data = {"principal":username,"password":password}
#             session.post(login_url,data=data)
#             res = func(*args,**kwargs)
#             return res
#         return inner
#     return decorator


class HarBorApi(object):
    def __init__(self,url,username,password,project_id):
        self.url = url
        self.username = username
        self.password = password
        self.header = {"Content-Type":"application/json"}
        self.project_id = project_id
        self.login_url = "{}/login".format(self.url)
        self.session = self.get_session()
    def get_session(self):
        session = requests.session()
        data = {"principal":self.username,"password":self.password}
        session.post(self.login_url,data=data,verify=True)
        return session
    def get_projects(self):
        project_url = "{}/api/repositories?project_id={}".format(self.url,self.project_id)
        try:
            req = self.session.get(project_url,headers=self.header,verify=True)
            if req.status_code != 200:
                raise Exception("响应异常，状态码是{}".format(req.status_code))
            return json.loads(req.text)
        except Exception:
            logger.error("[ERROR] " + traceback.format_exc())
        finally:
            self.session.close()
    def get_tag(self,repo_name):
        tag_url = "{}/api/repositories/{}/tags".format(self.url,repo_name)
        try:
            req = self.session.get(tag_url,headers=self.header,verify=True)
            if req.status_code != 200:
                raise Exception("响应异常，状态码是{}".format(req.status_code))
            tag_list = json.loads(req.text)
            tag_list.remove("latest")
            tag_list.sort(reverse=True)
            return tag_list[0]
        except Exception:
            logger.error("[ERROR] " + traceback.format_exc())
        finally:
            self.session.close()





