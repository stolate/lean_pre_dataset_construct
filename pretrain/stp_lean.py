import sys, json, os
from tqdm import tqdm
import hashlib
import random

input_p = '/data6/ftpdata/yilei4/math/data/train/org/STP_Lean'   #sys.argv[1]
output_p = '/data6/ftpdata/yilei4/math/data/train/pretrain_format/STP_lean.json'
dataset = 'STP'#sys.argv[3]
prompt_p = '/data6/ftpdata/yilei4/math/data/train/instructions/proof_instruction.json'

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

def main():
    #instruction = 'Translate the following informal math statement with proof into Lean4 code.\nNatural language statement:\n{informal_statement}\nproof:\n{informal_proof}\n```Lean4\n'
    #response = '{formal_proof}\n```'
    instructions = json2dict(prompt_p)
    indata = []

    for filename in os.listdir(input_p):
        if filename.endswith('.json'):
            pass
        else:
            continue
        path = os.path.join(input_p, filename)
        indata += json2dict(path)

    data_lst = []
    for data in tqdm(indata):
        instruction = random.choice(instructions)['instruction']
        text_instruct = instruction + '\n' +data['prompt'].split('```lean4')[1]
        text_response = data['target']
        datasource = dataset + '_' + data['tag']
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
