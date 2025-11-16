#合成数据转换为无监督
import sys, json
from tqdm import tqdm
import hashlib
import random

input_p = '../../org/leandojo_informal/informalized_leandojo_clean.json'
output_p = '/data6/ftpdata/yilei4/math/data/train/pretrain_format/leandojo_informal.json'
datasource = 'leandojo_informal'
prompt_p = '/data6/ftpdata/yilei4/math/data/train/instructions/leandojo_informal.json'

def indent_json2dict(inpath):
    with open(inpath, 'r') as fr:
        data = json.load(fr)
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
    #ist_1 = '{formal}\nInformalize the above Lean4 traced state-tactic sequence into natural language.\nInformalization:\n'
    instructions = json2dict(prompt_p)
    ist_2 = '{informal}'
    indata = indent_json2dict(input_p)
    data_lst = []
    for data in tqdm(indata):
        ist_1 = random.choice(instructions)['instruction']
        context = add_ret(str(data['traced_tactics']) + '\n' + ist_1) + add_ret(ist_2.format(informal=data['informalization']))

        #print(context)
        
        idx = get_md5(context)
        data_dump = convert_format(idx, context)
        data_lst.append(data_dump)
    dict2json(output_p, data_lst)

if __name__ == '__main__':
    main()
