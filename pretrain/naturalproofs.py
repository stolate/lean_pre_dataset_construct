#合成数据转换为无监督
import sys, json
from tqdm import tqdm
import hashlib
import random, re

input_p = '/data3/ftpdata/kmwang5/Lean-dataset/自然语言证明题/0_ori/naturalproofs-master/naturalproofs_folded_data_all.json'
output_p = '/data3/ftpdata/kmwang5/Lean-dataset/自然语言证明题/1_pretrain/naturalproofs/naturalproofs.json'
datasource = 'naturalproofs'

def get_file_line_count(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return sum(1 for _ in file)
total_lines = get_file_line_count(input_p)

def indent_json2dict(inpath):
    data = []
    with open(inpath, 'r') as fr:
        for line in fr:
            data.append(json.loads(line))
    return data

def json2dict(inpath):
    with open(inpath, 'r') as fr:
        data = []
        for line in fr:
            #print(line)
            content = json.loads(line)
            data.append(content)
    return data

def add_ret(context):
    context = context.strip().replace("\n","<ret>")+"<ret> <end>"
    return context

def convert_format(idx, input_text):
    #input_text=context.strip().replace("\n","<ret>")+"<ret> <end>"
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

def main():
    indata = indent_json2dict(input_p)
    data_lst = []
    for data in tqdm(indata):
        pattern = r'\[\[Definition:([^|]+)\|([^\]]+)\]\]'
        data['informal_statement'] = re.sub('^:', '', data['informal_statement'])
        data['informal_statement'] = re.sub(pattern, r'\2', data['informal_statement'])
        data['informal_statement'] = re.sub('\{\{Defof\t?\s?\|(.*?)\}\}', r'\1', data['informal_statement'])
        data['informal_statement'] = re.sub('\{\{eqn\t?\s?\|(.*?)\}\}\}', r'\1', data['informal_statement'])

        data['informal_proof'] = re.sub('^:', '', data['informal_proof'])
        data['informal_proof'] = re.sub(pattern, r'\2', data['informal_proof'])
        data['informal_proof'] = re.sub('\{\{Defof\t?\s?\|(.*?)\}\}', r'\1', data['informal_proof'])
        data['informal_proof'] = re.sub('\{\{eqn\t?\s?\|(.*?)\}\}\}', r'\1', data['informal_proof'])
        
        inputtext = data['informal_statement']
        context = add_ret(inputtext + '\n') + add_ret(data['informal_proof'])
        idx = get_md5(context)
        data_dump = convert_format(idx, context)
        data_lst.append(data_dump)
    dict2json(output_p, data_lst)

if __name__ == '__main__':
    main()
