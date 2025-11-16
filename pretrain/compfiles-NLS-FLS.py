#合成数据转换为无监督
import sys, json, re
from tqdm import tqdm
import hashlib
import random

input_p = '/data3/ftpdata/kmwang5/Lean-dataset/Lean-4/0_ori/compfiles-main/folded_data/compfiles-NLS-FLS.json'
output_p = '/data3/ftpdata/kmwang5/Lean-dataset/Lean-4/1_pretrain/compfiles-main/compfiles-NLS-FLS.json'
back_p = '/data3/ftpdata/kmwang5/Lean-dataset/Lean-4/1_pretrain/compfiles-main/backtrans_compfiles-NLS-FLS.json'
datasource = 'compfiles'
prompt_p = '/data3/ftpdata/kmwang5/Lean-dataset/instructions/NLS-FLS.json'
back_prompt_p = '/data3/ftpdata/kmwang5/Lean-dataset/instructions/FLS-NLS.json'

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
    # header = 'import Mathlib\nimport Aesop\n\nset_option maxHeartbeats 0\n\nopen BigOperators Real Nat Topology Rat\n\n'
    
    #instruction = 'Translate the following math problem of natural language into Lean4 statement.\nMath problem of natural language:\n{informal_problem}\n```Lean4\n'
    instructions = json2dict(prompt_p)
    response = '{target}'

    #back_instruct = 'Informalize the following Lean4 code into natural language problem.\nLean4 code:\n{target}\nNatural language problem:\n'
    back_instructions = json2dict(back_prompt_p)
    back_response = '{intarget}'
    indata = json2dict(input_p)
    data_lst = []
    back_lst = []
    for data in tqdm(indata):
        #print(data)
        NLS = data['input'].strip()
        instruction = random.choice(instructions)
        data['target'] = re.sub('end Imo.{5,7}$', '', data['target'].strip()).strip()
        if re.search(':=$', data['target'].strip()):
            data['target'] = data['target'].strip() + ' by'
        elif re.search('sorry$', data['target'].strip()):
            data['target'] = re.sub('sorry$', '', data['target']).strip()

        if instruction['position'] == 'head':
            if random.random() < 0.5: 
                context = add_ret(instruction['instruction'] + '\nNatural language:\n' + NLS) + add_ret(response.format(target=data['target']))
            else:
                context = add_ret(instruction['instruction'] + NLS) + add_ret(response.format(target=data['target']))
        else:
            if random.random() < 0.5: 
                context = add_ret('Natural language:\n' + NLS + '\n' + instruction['instruction']) + add_ret(response.format(target=data['target']))
            else:
                context = add_ret(NLS + '\n' + instruction['instruction']) + add_ret(response.format(target=data['target']))

        idx = get_md5(context)
        data_dump = convert_format(idx, context)
        data_lst.append(data_dump)
        
        back_instruct = random.choice(back_instructions)
        if back_instruct['position'] == 'head':
            if random.random() < 0.5:
                back_context = add_ret(back_instruct['instruction'] + '\nLean4 code:\n' + data['target']) + add_ret(back_response.format(intarget=NLS))
            else:
                back_context = add_ret(back_instruct['instruction'] + data['target']) + add_ret(back_response.format(intarget=NLS))
        else:
            if random.random() < 0.5:
                back_context = add_ret('Lean4 code:\n' + data['target'] + '\n' + back_instruct['instruction']) + add_ret(back_response.format(intarget=NLS))
            else:
                back_context = add_ret(data['target'] + '\n' + back_instruct['instruction']) + add_ret(back_response.format(intarget=NLS))

        back_idx = get_md5(back_context)
        back_dump = convert_format(back_idx, back_context)
        back_lst.append(back_dump)
    dict2json(output_p, data_lst)
    dict2json(back_p, back_lst)

if __name__ == '__main__':
    main()
