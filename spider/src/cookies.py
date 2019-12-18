from random import randint

cookies = [{
    'Cookie': '__uuid=1476718999772.16; _uuid=D34FB9D1FFA8420C15157A9C17482E83; gr_user_id=53427bcd-f337-4a67-abd8-6cea3885fb65; _fecdn_=1; verifycode=6fa6e5af690a4c3a882e6be4adb2a02d; JSESSIONID=B5C4C3E0D35B3F2F72C7A3575835765E; __tlog=1477208983609.41%7C00000000%7CR000000075%7Cs_o_009%7Cs_o_009; __session_seq=39; __uv_seq=39; _mscid=00000000; Hm_lvt_a2647413544f5a04f00da7eee0d5e200=1476719001,1477208985,1477212163; Hm_lpvt_a2647413544f5a04f00da7eee0d5e200=1477212761'
}]


idx = randint(0, len(cookies)-1)
cookie = cookies[idx]