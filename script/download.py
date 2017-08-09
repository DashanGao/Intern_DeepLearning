import sys
sys.path.append('.')
from dltool.multi_thread import MultiThreadWrap
from dltool.util import parse_json
import os
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--json', nargs='?', type=str, help="json")
parser.add_argument('--save_root', nargs='?', type=str)
parser.add_argument('--url_path', nargs='?', type=str)
parser.add_argument('--num_worker', nargs='*', type=int, default=10)
args = parser.parse_args()

save_root = args.save_root
with open(args.json, "r") as f:
    lines = [x.strip() for x in f]
p = parse_json(lines, args.url_path)

k = []
for i in p:
    k.append([i, save_root])

def write_success(ssss):
    pass

def work_func(url):
    cmd = "wget " + url[0] + " -t 2 -T 5 -nv -N -P "  + url[1]
#    cmd = "wget " + url[0] + " -t 2 -T 5 -nv -N -O " + url[2] + url[1]
    print(cmd)
    os.system(cmd)


mt = MultiThreadWrap(args.num_worker, k, write_success, work_func)
mt.start()
