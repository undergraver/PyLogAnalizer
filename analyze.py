#!/usr/bin/env python3
import re
import argparse
import sys

pattern = re.compile('\s+')

f = open('access.log','rt')
count=None

class Analyzer:
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
        print(val)

        getattr(self,prefix+val.action_name)(self)

    # to add a new action follow the patter below


    def action_most_freq_ip(self,args):
        "compute the most frequent ip"
        print("A")

    def action_last_freq_ip(self,args):
        "compute the least frequent ip"
        print("B")
    def action_events_per_second(self,args):
        "compute the events per second ratio"
        print("C")
    def action_total_bytes(self,args):
        "compute the total bytes transferred"
        print("D")
    def action_nothing(self,args):
        "do nothing"
        print("E")

i = Analyzer(sys.argv)

sys.exit(0)


argparser = argparse.ArgumentParser(description='Log processor')
argparser.add_argument


while True:
    line = f.readline()
    if not line:
        break
    line = line.strip()
    if len(line) == 0:
        continue
    array = re.split(pattern,line.strip())
    new_count=len(array)
    if count is None and count != new_count:
        print(new_count)
        count=new_count
f.close()
