
import requests
import json
import iptc        
import time

# a=iptc.easy.dump_chain('filter', 'INPUT', ipv6=False)
# print(a)  
BAN_LIST_ADDRESS='https://gcpud.net/api/blacklist-ip'
last_hash=''
chain = iptc.Chain(iptc.Table(iptc.Table.FILTER), "INPUT")
for i in chain.rules:
    print(i,'rule')
while True:

    ip_request=requests.get(BAN_LIST_ADDRESS).text
    new_hash=hash(ip_request)
    if last_hash != new_hash:
        last_hash=new_hash
        ips_list=json.loads(ip_request)['ips']

        banned_query=iptc.easy.dump_chain('filter', 'INPUT', ipv6=False)
        print(banned_query)
        banned_list=[]
        for ip in banned_query:
            try:
                range_ips=ip['src']
                banned_list.append(range_ips[0:range_ips.find('/')])
            except:
                pass
            
        print(banned_list,'banned_list',ips_list,'ips_list')
        for ip in ips_list:
            print(ip,'ip')
            if not ip in banned_list:
                print(ip,'to ban')
                rule = iptc.Rule()
                rule.protocol = "tcp"
                rule.src = ip
                rule.target = iptc.Target(rule, "DROP")
                
                chain.insert_rule(rule)
        for ip in banned_list:
            print(ip,'ip in banned_kist')
            if not ip in ips_list:
                print(ip,'not in ips list, need to delete rook')
                chain = iptc.Chain(iptc.Table(iptc.Table.FILTER), "INPUT")
                for rule in chain.rules:
                    
                    if ip in rule.src:
                        print(rule.src,'rule')
                        try:
                            chain.delete_rule(rule)
                        except Exception as e:
                            print(e)


    time.sleep(60)


