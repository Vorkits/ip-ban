import requests
import json
import iptc        
import time
                                                                                                     
# a=iptc.easy.dump_chain('filter', 'INPUT', ipv6=False)
# print(a)  
BAN_LIST_ADDRESS='https://gcpud.net/api/blacklist-ip'
last_hash=''
while True:
    try:
        ip_request=requests.get(BAN_LIST_ADDRESS).text
        new_hash=hash(ip_request)
        if last_hash != new_hash:
            last_hash=new_hash
            ips_list=json.loads(ip_request)['ips']
            banned_query=iptc.easy.dump_chain('filter', 'INPUT', ipv6=False)
            banned_list=[]
            for ip in banned_query:
                range_ips=ip['src']
                banned_list.append(range_ips[0:range_ips.find('/')])
            print(banned_list)
            for ip in ips_list:
                if not ip in banned_list:
                    print(ip)
                    rule = iptc.Rule()
                    rule.protocol = "tcp"
                    rule.src = ip
                    rule.target = iptc.Target(rule, "DROP")
                    chain = iptc.Chain(iptc.Table(iptc.Table.FILTER), "INPUT")
                    chain.insert_rule(rule)
    except Exception as e:
        print(e)
    time.sleep(60)
