#合成数据转换为无监督
import sys, json, os
from tqdm import tqdm
import hashlib
import random

input_p = '/data2/xyzhou15/数学合成数据/LEAN4/OpenBootstrappedTheorem/0_ori/data'
output_p = '/data6/ftpdata/yilei4/math/data/train/pretrain_format/OpenBootstrappedTheorem_lean.json'
formal_p = '/data6/ftpdata/yilei4/math/data/train/pretrain_format/OpenBootstrappedTheorem_formalize.json'
back_p = '/data6/ftpdata/yilei4/math/data/train/pretrain_format/OpenBootstrappedTheorem_interptet.json'
datasource = 'OpenBootstrappedTheorem'

prompt_p = '/data6/ftpdata/yilei4/math/data/train/instructions/openboots_trans.json'
back_prompt_p = '/data6/ftpdata/yilei4/math/data/train/instructions/openboots_backtrans.json'

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

def dir_json2dict(indir):
    data = []
    for filename in os.listdir(indir):
        if filename.endswith('json'):
            pass
        else:
            continue
        data += json2dict(os.path.join(indir, filename))
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
    header = 'import Mathlib\nimport Aesop\n\nset_option maxHeartbeats 0\n\nopen BigOperators Real Nat Topology Rat\n\n'
    
    instructions = json2dict(prompt_p)
    #instruct = 'Formalize the following theorem and proof of natural language into Lean4 code.\nTheorem and proof:\n{informal}\n```Lean4:\n'
    response = '{formal}\n```'
    
    back_instructions = json2dict(back_prompt_p)
    #back_instruct = 'Explain the following Lean4 code in natural language.\nLean4 code:\n{formal}\nNatural language explanation:\n'
    back_response = '{informal}'
    
    indata = dir_json2dict(input_p)
    data_lst = []
    formal_lst = []
    back_lst = []
    for data in tqdm(indata):
        #print(data)
        context = add_ret(header + data['Commented_proof'])
        #print(context)
        #raise
        idx = get_md5(context)
        data_dump = convert_format(idx, context)
        data_lst.append(data_dump)
        
        instruct = random.choice(instructions)['instruction']
        formal_context = add_ret(instruct + '\nNatural language:\n' + data['Generated_informal_statement_and_proof']) + add_ret(response.format(formal=data['Proof']))
        #print(formal_context)
        #raise
        formal_idx = get_md5(formal_context)
        formal_dump = convert_format(formal_idx, formal_context)
        formal_lst.append(formal_dump)

        back_instruct = random.choice(back_instructions)['instruction']
        back_context = add_ret(back_instruct + '\nLean4 code:\n' +data['Proof']) + add_ret(back_response.format(informal=data['Generated_informal_statement_and_proof']))
        #print(back_context)
        #raise
        back_idx = get_md5(back_context)
        back_dump = convert_format(back_idx, back_context)
        back_lst.append(back_dump)
    dict2json(output_p, data_lst)
    dict2json(back_p, back_lst)
    dict2json(formal_p, formal_lst)

if __name__ == '__main__':
    main()
