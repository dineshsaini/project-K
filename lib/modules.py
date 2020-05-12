__all__ = []

import random
import importlib
import argparse

class BaseModule:
    def __init__(self, proxy_list=[], ua_list=[], max_threads=1, verbosity=0):
        self.proxy_list = proxy_list
        self.ua_list = ua_list
        self.max_threads = max_threads
        self.verbosity = verbosity

    def call(self, args):
        self.getParser()
        self.defineArgs()
        self.parseArgs(args)
        self.main()

    def main(self):
        # * This method needs to be overridden in every module
        pass

    def getParser(self):
        if not hasattr(self, 'parser'): 
            self.parser = argparse.ArgumentParser()
        return self.parser 

    def defineArgs(self):
        # * This method needs to be overridden in every module
        pass

    def parseArgs(self, args):
        self.args = self.getParser().parse_args(args.split())

    def getArgs(self):
        return self.args
        
    def getProxyList(self):
        return self.proxy_list

    def getUAList(self):
        return self.ua_list

    def getRandomProxy(self):
        try:
            return random.choice(self.proxy_list)
        except IndexError:
            return ''

    def getRandomUserAgent(self):
        try:
            return random.choice(self.ua_list)
        except IndexError:
            return ''

    def getVerbosity(self):
        return self.verbosity

    def getMaxAllowedThreads(self):
        return self.max_threads

    def setProxyList(self, l=[]):
        self.proxy_list.append(l)

    def setUAList(self, ual=[]):
        self.ua_list.append(ual)

    def setMaxAllowedThreads(self, c):
        self.max_threads = c
    
    def serVerbosity(self, v):
        self.verbosity = v

    def addProxy(self, p=''):
        self.proxy_list.append(p)
    
    def addUserAgent(self, ua=''):
        self.ua_list.append(ua)


class ModuleLoader:
    def load(mod_name, **def_args):
        try:
            module = importlib.import_module('modules.{}'.format(mod_name))
        except ModuleNotFoundError:
            pass
        else:    
            if hasattr(module, mod_name):
                mod_class = getattr(module, mod_name)
                if issubclass(mod_class, BaseModule):
                    mod_obj = mod_class(**def_args)
                    return mod_obj
        raise Exception('Module "{}" not found or is incorrect.'.format(mod_name))
