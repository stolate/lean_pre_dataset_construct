import sys, json, os
import hashlib
import random
from tqdm import tqdm

input_p = '../../org/deepseek_v1/dataset.jsonl'    #sys.argv[1]
output_p = '../../pretrain_format/deepseek_v1.json'   #sys.argv[2]
datasource = 'deepseek_v1'   #sys.argv[3]
prompt_p = '/data6/ftpdata/yilei4/math/data/train/instructions/proof_instruction.json'

def json2dict(inpath):
    data = []
    with open(inpath, 'r') as fr:
        for line in fr:
            line = json.loads(line)           
            data.append(line)
    return data


def readlean(path):
    with open(path, 'r', encoding='utf-8') as fr:
        lean_context = fr.read()
    return lean_context

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


org_data = json2dict(input_p)
#instruct_in = 'Complete the following Lean 4 code:\n```Lean4\n{header}\n{formal_state}\n'
#instruct_response = '{formal_proof}\n```'
ins_lst = json2dict(prompt_p)

with open(output_p, "w", encoding="utf-8") as outpuf_f:
    for data in tqdm(org_data):
        #print(data)
        instruction = random.choice(ins_lst)['instruction']
        context = add_ret(instruction + '\n' + data['header'] + '\n' + data['formal_statement']) + add_ret(data['formal_proof'])
        #print(context)
        #raise
        idx = get_md5(context)
        data_dump = convert_format(idx, context)
        #print(data_dump)
        json.dump(data_dump, outpuf_f, ensure_ascii=False)
        outpuf_f.write("\n")

