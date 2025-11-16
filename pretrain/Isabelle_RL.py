#合成数据转换为无监督
import sys, json, re
from tqdm import tqdm
import hashlib
import random

input_p = '/data3/ftpdata/kmwang5/Lean-dataset/Isabelle/0_ori/Isabelle_RL/folded_data/train.json'
output_p = '/data3/ftpdata/kmwang5/Lean-dataset/Isabelle/1_pretrain/Isabelle_RL/Isabelle_RL-NLS-FLS.json'
back_p = '/data3/ftpdata/kmwang5/Lean-dataset/Isabelle/1_pretrain/Isabelle_RL/backtrans_Isabelle_RL-NLS-FLS.json'
datasource = 'Isabelle_RL'
prompt_p = '/data3/ftpdata/kmwang5/Lean-dataset/Isabelle-instruction/NLS-FLS.json'
back_prompt_p = '/data3/ftpdata/kmwang5/Lean-dataset/Isabelle-instruction/FLS-NLS.json'

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
    header = '''
    theory thorem_{j}
        imports Main
        begin
            {FLS} + by
        end
    '''
    
    instructions = json2dict(prompt_p)
    response = '{target}'

    back_instructions = json2dict(back_prompt_p)
    back_response = '{intarget}'
    indata = json2dict(input_p)
    data_lst = []
    back_lst = []
    j = 0
    for data in tqdm(indata):
        #print(data)
        NLS = data['natural_language_statement'].strip()
        FLS = header.replace('{FLS}', data['isabelle_translation']).replace('{j}', str(j))
        instruction = random.choice(instructions)

        if instruction['position'] == 'head':
            if random.random() < 0.5: 
                context = add_ret(instruction['instruction'] + '\nNatural language:\n' + NLS) + add_ret(response.format(target=FLS))
            else:
                context = add_ret(instruction['instruction'] + NLS) + add_ret(response.format(target=FLS))
        else:
            if random.random() < 0.5: 
                context = add_ret('Natural language:\n' + NLS + '\n' + instruction['instruction']) + add_ret(response.format(target=FLS))
            else:
                context = add_ret(NLS + '\n' + instruction['instruction']) + add_ret(response.format(target=FLS))

        idx = get_md5(context)
        data_dump = convert_format(idx, context)
        data_lst.append(data_dump)
        
        back_instruct = random.choice(back_instructions)
        if back_instruct['position'] == 'head':
            if random.random() < 0.5:
                back_context = add_ret(back_instruct['instruction'] + '\nIsabelle code:\n' + FLS) + add_ret(back_response.format(intarget=NLS))
            else:
                back_context = add_ret(back_instruct['instruction'] + FLS) + add_ret(back_response.format(intarget=NLS))
        else:
            if random.random() < 0.5:
                back_context = add_ret('Isabelle code:\n' + FLS + '\n' + back_instruct['instruction']) + add_ret(back_response.format(intarget=NLS))
            else:
                back_context = add_ret(FLS + '\n' + back_instruct['instruction']) + add_ret(back_response.format(intarget=NLS))

        back_idx = get_md5(back_context)
        back_dump = convert_format(back_idx, back_context)
        back_lst.append(back_dump)
        j += 1
    dict2json(output_p, data_lst)
    dict2json(back_p, back_lst)

if __name__ == '__main__':
    main()
