#合成数据转换为无监督
import sys, json, re
from tqdm import tqdm
import hashlib
import random

read_file_path = '/data3/ftpdata/kmwang5/Lean-dataset/Isabelle/0_ori/Isabelle-AFP-versions/split_results.jsonl'
save_file_path  = '/data3/ftpdata/kmwang5/Lean-dataset/Isabelle/1_pretrain/Isabelle-AFP-versions/Isabelle-AFP-versions.json'

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

with open(read_file_path, 'r', encoding='utf-8') as rf, open(save_file_path, 'w', encoding='utf-8') as sf:
    for line in rf:
        data = json.loads(line)
        content = add_ret(data['content'])
        idx = get_md5(content)
        current_data = {
            'id': idx,
            'text': content,
            'datasource': 'Isabelle-AFP-versions'
        }
        sf.write(json.dumps(current_data, ensure_ascii=False)+'\n')
        