from random import randint

headers = [{
    'Cookie': 'yfx_c_g_u_id_10000042=_ck18012900250116338392357618947; VISITED_MENU=%5B%228528%22%5D; yfx_f_l_v_t_10000042=f_t_1517156701630__r_t_1517314287296__v_t_1517320502571__r_c_2',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.119 Safari/537.36',
    'Referer': 'http://www.sse.com.cn/assortment/stock/list/share/'
},{
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 '
                  'Safari/537.36',
    'DNT': '1',
    'Host': 'campus.liepin.com',
    'Pragma': 'no-cache',
    'Upgrade-Insecure-Requests': '1'
}
]

idx = randint(0, len(headers)-1)
header = headers[idx]
