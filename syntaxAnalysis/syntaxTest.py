import io
import re

# Test_file_full_path='~/vimfiles/bundle/vim-shaderlab/test/CharactorSurface.shader'
Test_file_full_path = 'c:/Users/Administrator/vimfiles/bundle/vim-shaderlab/test/CharactorSurface.shader'

Test_StartLine = 73
Test_StartCol = 5

Struct_define_Dict = {}
Include_file_list = []
re_compare_include = re.compile(
    r'\s*(#include)\s+\"([_a-zA-Z0-9]+[_a-zA-Z0-9\.]*)\"')

re_compare_struct_define= re.compile(r'([_a-zA-Z0-9]+)\s+([_a-zA-Z0-9]+)\s*;')

def StartParse():
    with open(Test_file_full_path, 'r') as f:
        StructParse(f)
        print Struct_define_Dict
#         IncludeParse(f)


def StructParse(f):
    curStructName = ""
    for line in f.readlines():
        content = line.strip()
        if curStructName == "":
            list_str = re.split(r'\s+', content)
            if len(list_str) > 1 and list_str[0] == 'struct':
                curStructName = list_str[1]
                #                 print 'match struct, curStructName:%s'%curStructName
                if Struct_define_Dict.get(curStructName, '-1') != -1:
                    #                     print 'add curStructName:%s'%curStructName
                    Struct_define_Dict[curStructName] = []
        else:
            if re.match(r'}', content) != None:
                curStructName = ""

#                 print '--- curStructName end \n cur line:%s' % content
            else:
                matchRes = re_compare_struct_define.match(content)
                if matchRes != None and Struct_define_Dict.has_key(
                        curStructName):
                    var = matchRes.group(2)
                    #                     print 'line:%s'% content
                    #                     print 'append:%s'%var
                    Struct_define_Dict[curStructName].append(var)


def IncludeParse(f):
    for line in f.readlines():
        matchRes = re_compare_include.match(line)
        if matchRes != None:
            fileName = matchRes.group(2)
            if fileName not in Include_file_list:
                Include_file_list.append(fileName)
            print 'find include: %s' % fileName

def MatchVarDefine(var,line):
    comStr=r'.*?([_a-zA-Z]+[_a-zA-Z0-9]*)\s+'+var+'.*'
#     re_compare_var_define=re.compile(comStr)
    matchRes=re.match(comStr,line)
    if matchRes==None:
        print 'not match'
        return None
    else:
        res=matchRes.group(1)
#         print matchRes.groups()
#         print res
        return res

# StartParse()
# print re.match(r'}','};')
# print re_compare_include.match('#include \"UnityCG.cgine\"').groups()
MatchVarDefine('s','inline fixed4 LightingSelfLambert (SurfaceOutput s, fixed3 lightDir, half3 viewDir, fixed atten)')
