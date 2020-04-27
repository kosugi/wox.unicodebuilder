# -*- coding: utf-8 -*-

from wox import Wox
import clipboard

class Main(Wox):

    def __init__(self, worker):
        self.worker = worker
        super().__init__()

    def query(self, q):
        results = []
        for i in self.worker(q):
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
