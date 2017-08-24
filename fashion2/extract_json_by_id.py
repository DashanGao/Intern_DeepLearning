import json
import sys

broken_img = sys.argv[2]
js = sys.argv[1]
out_file = sys.argv[3]
js_record = {}
broken_record = {}
with open(js, "r") as js:
    jss = js.readlines()
    for j in jss:
        j = eval(j.strip())
        js_record.update({j["_id"]["$oid"]: j})
with open(broken_img, "r") as br:
    lines = br.readlines()
for line in lines:
    line.replace(".jpg", "").strip()
    if line in js_record:
        with open(out_file, "a") as out:
            out.write(str({line: js_record[line]})+"\n")
    else:
        print line
        # broken_record.update()
