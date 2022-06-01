#!/usr/bin/env python3
import re
import argparse
import sys
import os

pattern = re.compile('\s+')

class Analyzer:
    TIMESTAMP_INDEX=0
    CLIENT_IP_INDEX=2
    HEADER_SIZE_INDEX=1
    RESPONSE_SIZE_INDEX=4
    def __init__(self, args):
        prefix='action_'
        methods_name = [ item for item in dir(self) if item.startswith(prefix) and callable(getattr(self,item)) ]
        action_methods = [ item.replace(prefix,'') for item in methods_name ]
        help_text = [ getattr(self,item).__doc__ for item in methods_name ]
        #print(help_text)
        action_help_map = { action_methods[i]:help_text[i] for i in range(len(action_methods)) }
        #print(action_help_map)
        help_for_each = [ am + " - " + action_help_map[am] for am in action_methods ]
        #print('\n'.join(help_for_each))

        parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter,description='Log Analyzer',epilog="\n".join(help_for_each))
        parser.add_argument("-a","--action",required=True,dest='action_name',choices=action_methods)

        parser.add_argument("-o","--output",nargs=1,dest='output_json',required=True)
        parser.add_argument("-i","--input",nargs='+',dest='input',required=True,action='append',help='input files and/or directories')

        val = parser.parse_args()
        self.prepare_list(val.input)
        self.json=val.output_json[0]
        #print(self.files)
        #print(self.json)

        json_info = getattr(self,prefix+val.action_name)(self)
        print(json_info)

    def prepare_list(self,input_array):
        self.files = []
        for arr in input_array:
            for item in arr:
                if os.path.isfile(item):
                    self.files.append(item)
                elif os.path.isdir(item):
                    # list all dir contents
                    self.files += Analyzer.get_list_recursively(item)
    @staticmethod
    def get_list_recursively(path):
        ret = []
        if os.path.isdir(path):
            items = os.listdir(path)
            for item in items:
                new_path = path+os.sep+item
                if os.path.isdir(new_path):
                    ret += Analyzer.get_list_recursively(new_path)
                elif os.path.isfile(new_path):
                    ret.append(new_path)

        return ret

    def read_line_by_line(self,fname,method):
        f = open(fname,'rt')
        while True:
            line = f.readline()
            if not line:
                return method(None) # the end of file
                break
            line = line.strip()
            if len(line) == 0:
                continue
            array = re.split(pattern,line.strip())
            method(array)
        f.close()

    # to add a new action follow the patter below
    def action_most_freq_ip(self,args):
        "compute the most frequent ip"
        results = []
        for f in self.files:
            self.ip_count_map = {}
            info_map = self.read_line_by_line(f,self.find_most_freq_ip)
            info_map["file"] = f
            results.append(info_map)
        result_json = { "results" : results }
        return result_json

    def find_most_freq_ip(self,split_line):
        if split_line == None:
            # EOF, return the result
            count = 0
            ip = '0.0.0.0'
            for k,v in self.ip_count_map.items():
                if v > count:
                    count = v
                    ip = k
            return { "ip" : ip, "count" : count }

        client_ip = split_line[self.__class__.CLIENT_IP_INDEX]
        if client_ip in self.ip_count_map:
            self.ip_count_map[client_ip] += 1
        else:
            self.ip_count_map[client_ip] = 1

    def action_least_freq_ip(self,args):
        "compute the least frequent ip"
        results = []
        for f in self.files:
            self.ip_count_map = {}
            info_map = self.read_line_by_line(f,self.find_least_freq_ip)
            info_map["file"] = f
            results.append(info_map)
        result_json = { "results" : results }
        return result_json

    def find_least_freq_ip(self,split_line):
        if split_line == None:
            # EOF, return the result
            count = None
            ip = '0.0.0.0'
            for k,v in self.ip_count_map.items():
                if count is None or v < count:
                    count = v
                    ip = k
            return { "ip" : ip, "count" : count }

        client_ip = split_line[self.__class__.CLIENT_IP_INDEX]
        if client_ip in self.ip_count_map:
            self.ip_count_map[client_ip] += 1
        else:
            self.ip_count_map[client_ip] = 1

    def action_events_per_second(self,args):
        "compute the events per second ratio"
        print("C")

    def action_total_bytes(self,args):
        "compute the total bytes transferred"
        results = []
        for f in self.files:
            self.bytecount = 0
            info_map = self.read_line_by_line(f,self.add_total_bytes_transferred)
            info_map["file"] = f
            results.append(info_map)
        result_json = { "results" : results }
        return result_json

    def add_total_bytes_transferred(self,split_line):
        if split_line == None:
            return { "bytecount" : self.bytecount }
        header_size = int(split_line[self.__class__.HEADER_SIZE_INDEX])
        response_size = int(split_line[self.__class__.RESPONSE_SIZE_INDEX])
        self.bytecount += header_size + response_size

    def action_nothing(self,args):
        "do nothing"
        print("E")

i = Analyzer(sys.argv)
sys.exit(0)


argparser = argparse.ArgumentParser(description='Log processor')
argparser.add_argument


