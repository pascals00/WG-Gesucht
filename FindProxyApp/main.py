from common.proxy_manager import * 

def main(): 
    proxy_manager = ProxyManager()
    numberOfProxies = 0

    while numberOfProxies < 100:
        proxy_manager.find_proxies_FreeProxy()
        numberOfProxies =+ 1
        
if __name__ == "__main__":
    main()