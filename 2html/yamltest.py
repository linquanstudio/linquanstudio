import yaml
import pprint
import re

with open('test.md', 'r') as f: md = [ l.strip() for l in f.readlines() ]
# yamlのブロックとmarkdownを分ける
ym = []
if md[0] == '---':
    md.pop(0)
    while md[0] != '---':
        ym.append(md.pop(0))
    md.pop(0)
ym = yaml.safe_load('\n'.join(ym))
print('[yaml]')
print(ym)
print('[markdown')
print(md)
