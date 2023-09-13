from socket import *
import webbrowser
import time

chrome_path = "C:/Program Files/Google/Chrome/Application/chrome.exe"

url1 = "https://maker.wiznet.io/"
url2 = "https://github.com/"
url3 = "https://www.google.com"
url4 = "https://www.raspberrypi.com/news/page/3/"

serverSock = socket(AF_INET, SOCK_STREAM)
serverSock.bind(('192.168.0.4', 5000))
serverSock.listen()

print(f"server waiting....")

try:
    while True:
        connectionSock, addr = serverSock.accept()
        print(f"Client connected: {addr}")

        while True:
            try:
                data = connectionSock.recv(1024)
                if not data:
                    break
                print(f"recv data: {data.decode('utf-8')}")

                data_int = int(data.decode('utf-8'))

                url = url1
                if data_int < 57402:
                    url = url2
                    if data_int < 49269:
                        url = url3
                        if data_int < 41136:
                            url = url4

                webbrowser.register('chrome', None, webbrowser.GenericBrowser(chrome_path))
                webbrowser.get('chrome').open(url)
                time.sleep(3)
                print("server closed1.")
            except ConnectionResetError:
                print("Client disconnected: {addr}")
                break

        connectionSock.close()
        time.sleep(3)
except KeyboardInterrupt:
    print("Server closed.")
    serverSock.close()
