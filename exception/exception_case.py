# coding=utf8
# import json


def request(taskid=None):
    # TODO
    # print("[ init ] accessor request %s %s %s" % (host, api, params))
    try:
        # taskid = self.request_post(host + api, params)
        if taskid is None:
            # print("taskid is none ")
            print("checkpoint 1")
            # return False
            raise ValueError  # 测试走到这里之后， 如果exception中写了pass, 那么后面的代码是否不会运行了。
        # res = self.request_get(host, taskid)
        # self.response = json.loads(res.decode('utf8'))
        # if self.response.get('task_result').get('status').get('ret_code') == 0:
        #     print("[ request done ] params=%s, api=%s, host=%s" % (params, api, host))
        #     # logger.info("request.ret_code=0")
        #     return True
        # else:
        #     err_msg = self.response.get('task_result').get('status').get('msg')
        #     print("[ response.err_msg ] params=%s, api=%s, host=%s, msg=%s" % (params, api, host, err_msg))
        #     # print("response.err_msg=%s,  %s, %s" % (err_msg, '', ''))
        #     # print("response.get('task_result').get('status').get('ret_code') != 0 %s, %s" % (api, params))
        #     raise ValueError
    except Exception as err:
        print("checkpoint 2")
        pass  # pass是否会直接返回， 不再执行下面的return false
        print("checkpoint 3")
        # print("[ request exception ] params=%s, api=%s, host=%s, err=%s" % ('', api, host, err))
        # print("request exception %s" % err)
    print("checkpoint final")
    return False


print(request())
