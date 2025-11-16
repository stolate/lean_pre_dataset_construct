import sys, json, os
from tqdm import tqdm
import hashlib
import random

input_p = '/data6/ftpdata/yilei4/math/data/train/org/miniCTX/miniCTX-fullproof'
output_p = '/data6/ftpdata/yilei4/math/data/train/pretrain_format/miniCTX_fullproof.json'
dataset = 'miniCTX'   #sys.argv[3]
prompt_p = '/data6/ftpdata/yilei4/math/data/train/instructions/minictx_fullproof.json'

st_instr = [
    '{INSTRUCTION}\nThe given file contents are\n{CONTEXT}',
    '{INSTRUCTION}\nThe file contents are as below.\n{CONTEXT}',
    'Below are the given file contents.\n{CONTEXT}\n{INSTRUCTION}',
    'The file contents are\n{CONTEXT}\n{INSTRUCTION}',
    '{CONTEXT}\nAbove are the file contents.\n{CONTEXT}\n{INSTRUCTION}\n',
    '{INSTRUCTION}\nThe file contents including theorem statement as follows.\n{CONTEXT}',
    '{INSTRUCTION}\nFile contents are below.\n{CONTEXT}',
    ]


def indent_json2dict(inpath):
    with open(inpath, 'r') as fr:
        data = json.load(fr)
    return data

def json2dict(inpath):
    with open(inpath, 'r') as fr:
        data = []
        for line in tqdm(fr):
            #print(line)
            content = json.loads(line)
            data.append(content)
    return data

def add_ret(context):
    context = context.strip().replace("\n","<ret>")+"<ret> <end>"
    return context

def convert_format(idx, input_text, datasource):

    id = datasource + '-' + idx
        
    data_dump={
        "id":id,
        "text":input_text,
        "datasource":datasource,
        }
    return data_dump

def get_md5(input_string):
    # 创建一个md5哈希对象
    md5_hash = hashlib.md5()
    
    # 更新哈希对象，注意需要编码为字节
    md5_hash.update(input_string.encode('utf-8'))
    
    # 获取十六进制的MD5哈希值
    return md5_hash.hexdigest()


def dict2json(path, data):
    with open(path, "w", encoding="utf-8") as outpuf_f:
        for data_dump in tqdm(data):
            json.dump(data_dump, outpuf_f, ensure_ascii=False)
            outpuf_f.write("\n")

import re

def extract_string_between_tags(text, start_tag, end_tag):
    """
    该函数使用正则表达式从文本中提取指定开始和结束标签之间的内容，可处理标签前后有换行符的情况。
    :param text: 待处理的原始文本
    :param start_tag: 开始标签，例如 [STATE]
    :param end_tag: 结束标签，例如 [/STATE]
    :return: 标签之间的字符串，如果未找到匹配内容则返回 None
    """
    # 对开始和结束标签进行转义，避免特殊字符影响正则匹配
    escaped_start_tag = re.escape(start_tag)
    escaped_end_tag = re.escape(end_tag)
    # 构建正则表达式模式，允许标签前后有换行符，使用非贪婪匹配
    pattern = fr'\s*{escaped_start_tag}\s*(.*?)\s*{escaped_end_tag}\s*'
    # 在文本中搜索符合模式的内容，使用 re.DOTALL 标志使 . 能匹配换行符
    match = re.search(pattern, text, re.DOTALL)
    if match:
        # 返回捕获组中的内容，即标签之间的字符串
        return match.group(1)
    return None

def main():
    indata = []
    instructions = json2dict(prompt_p)
    for filename in os.listdir(input_p):
        path = os.path.join(input_p, filename)
        indata += json2dict(path)

    data_lst = []
    for data in tqdm(indata):
        #print(data)
        #print(data.keys())
        instruct = random.choice(instructions)['instruction']
        input_text = data['prompt'].split('-/', 1)[-1]
        #print(input_text)
        #state = extract_string_between_tags(input_text, "[STATE]", "[/STATE]")
        #print(input_text)
        context = extract_string_between_tags(input_text, "[CTX]", "[/CTX]")
        #print(state)
        
        text_instruct = random.choice(st_instr).format(INSTRUCTION=instruct, CONTEXT=context)
        #print(text_instruct)
        text_response = data['completion'].replace('[/PROOF]', '')
        #print(text_response)
        #raise
        datasource = dataset + '_' + 'fullproof' #data['prompt_name']
        context = add_ret(text_instruct) + add_ret(text_response)
        #print(context)
        #print(datasource)
        #raise
        
        idx = get_md5(context)
        data_dump = convert_format(idx, context, datasource)
        data_lst.append(data_dump)
    dict2json(output_p, data_lst)

if __name__ == '__main__':
    main()
