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
        action_methods = [ item.replace(prefix,'') for item in dir(self) if item.startswith(prefix) and callable(getattr(self,item)) ]

        parser = argparse.ArgumentParser(description='Log Analyzer')
        subparser = parser.add_subparsers(dest='action')
        for action in action_methods:
            subparser.add_parser(action,help=getattr(self,prefix+action).__doc__)

        parser.add_argument("-o","--output",nargs=1,dest='output_json',required=True)
        parser.add_argument("input",nargs='+',help='input files and/or directories')

        parser.parse_args(['--help'])

    def action_most_freq_ip(self,args):
        "compute the most frequent ip"
        pass
    def action_last_freq_ip(self,args):
        "compute the least frequent ip"
        pass
    def action_events_per_second(self,args):
        "compute the events per second ratio"
        pass
    def action_total_bytes(self,args):
        "compute the total bytes transferred"
        pass

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
