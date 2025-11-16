#合成数据转换为无监督
import sys, json
from tqdm import tqdm
import hashlib
import random

input_p = '/data3/ftpdata/kmwang5/Lean-dataset/Lean-4/0_ori/mathlib_informal_v4.16.0/data.jsonl'
output_p = '/data3/ftpdata/kmwang5/Lean-dataset/Lean-4/1_pretrain/mathlib_informal_v4.16.0/mathlib_informal_v4.16.0.json'
back_p = '/data3/ftpdata/kmwang5/Lean-dataset/Lean-4/1_pretrain/mathlib_informal_v4.16.0/backtrans_mathlib_informal_v4.16.0.json'
datasource = 'mathlib_informal_v4.16.0'
prompt_p = '/data3/ftpdata/kmwang5/Lean-dataset/instructions/trans_statement.json'
back_prompt_p = '/data3/ftpdata/kmwang5/Lean-dataset/instructions/back_trans_statement.json'

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
    with open(output_p, "w", encoding="utf-8") as sf1, open(back_p, "w", encoding="utf-8") as sf2:
        for data_dump in tqdm(data):
            json.dump(data_dump, outpuf_f, ensure_ascii=False)
            outpuf_f.write("\n")

def main():
    # header = 'import Mathlib\nimport Aesop\n\nset_option maxHeartbeats 0\n\nopen BigOperators Real Nat Topology Rat\n\n'
    
    #instruction = 'Translate the following math problem of natural language into Lean4 statement.\nMath problem of natural language:\n{informal_problem}\n```Lean4\n'
    with open(output_p, "w", encoding="utf-8") as sf1, open(back_p, "w", encoding="utf-8") as sf2:
        indata = json2dict(input_p)
        for data in tqdm(indata):
            instructions = json2dict(prompt_p)

            header = ''
            for module_name in data['module_name']:
                header += 'import {module_name}\n'

            formal_statement = f"{data['kind']} {'.'.join(data['name'])} : {data['signature']} {data['value']}\n"

            response = header + formal_statement

            #back_instruct = 'Informalize the following Lean4 code into natural language problem.\nLean4 code:\n{formal_statement}\nNatural language problem:\n'
            back_instructions = json2dict(back_prompt_p)
            back_response = '{informal_statement}'
            #print(data)
            NLS = data['informal_description'].strip()
            instruction = random.choice(instructions)
            if instruction['position'] == 'head':
                context = add_ret(instruction['instruction'] + '\nNatural language:\n' + NLS) + add_ret(response)
            else:
                context = add_ret('Natural language:\n' + NLS + '\n' + instruction['instruction']) + add_ret(response)
            #print(context)
            #raise
            idx = get_md5(context)
            data_dump = convert_format(idx, context)
            sf1.write(json.dumps(data_dump, ensure_ascii=False)+'\n')
            
            back_instruct = random.choice(back_instructions)
            if back_instruct['position'] == 'head':
                back_context = add_ret(back_instruct['instruction'] + '\nLean4 code:\n' + response) + add_ret(back_response.format(informal_statement=NLS))
            else:
                back_context = add_ret('\nLean4 code:\n' + response + back_instruct['instruction']) + add_ret(back_response.format(informal_statement=NLS))
            #back_context = add_ret(back_instruct.format(formal_statement=data['output'])) + add_ret(back_response.format(informal_statement=NLS))
            #print(back_context)
            #raise
            back_idx = get_md5(back_context)
            back_dump = convert_format(back_idx, back_context)
            sf2.write(json.dumps(back_dump, ensure_ascii=False)+'\n')
        


if __name__ == '__main__':
    main()
