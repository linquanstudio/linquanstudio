import yaml
import pprint
import re

with open('test.md', 'r') as f: md = f.readlines()

# yamlのブロックを抽出

joined = ''.join(md)
m = re.match(r'^-+$(.*)', joined, flags=re.MULTILINE)
print(m.groups())


#for l in md:
#    m = re.match(r'title:(.+)\n', l)
#    if m is not None:
#        print(m.groups())

    
                  
#s = 'aaa@xxx.com'
#m = re.match(r'([a-z]+)@([a-z]+)\.([a-z]+)', s)
#print(m)
# <re.Match object; span=(0, 11), match='aaa@xxx.com'>
#print(m.groups())
