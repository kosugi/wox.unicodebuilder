# -*- coding: utf-8 -*-

from wox import Wox, WoxAPI
import clipboard
import query

class Main(Wox):

    def query(self, q):
        results = []
        for i in query.do(q):
            data = i['data']
            title = i['title']
            text = i['subtitle']
            dummy = i['dummy']
            item = {
                'Title': title,
                'SubTitle': text,
                'IcoPath': 'icon.png',
            }
            if not dummy:
                item['JsonRPCAction'] = {
                    'method': 'copyToClipboard',
                    'parameters': [data],
                    'dontHideAfterAction': False
                }
            results.append(item)
        return results

    def copyToClipboard(self, text):
        clipboard.put(text)

if __name__ == '__main__':
    Main()
