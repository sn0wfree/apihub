# coding=utf8

import requests

if __name__ == '__main__':
    data = {'file': ('hello.txt', 'hello, world!', "text/plain")}
    r = requests.post('http://0.0.0.0:8279/upload_file', files=data)

    print(r.text)
