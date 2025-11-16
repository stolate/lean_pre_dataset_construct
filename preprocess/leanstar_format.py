import json
import hashlib
import re, sys
import os
from tqdm import tqdm

def get_md5(input_string):
    # 创建一个md5哈希对象
    md5_hash = hashlib.md5()
    
    # 更新哈希对象，注意需要编码为字节
    md5_hash.update(input_string.encode('utf-8'))
    
    # 获取十六进制的MD5哈希值
    return md5_hash.hexdigest()

def indent_json2dict(inpath):
    with open(inpath, 'r') as fr:
        data = json.load(fr)
    return data

def extr_lean_base(intext):
    #print(intext)
    
    try:
        match_str = re.search(r'Tactic state:\n---\n(.*?)\n---\nReasoning:', intext, re.DOTALL)
        code = match_str.group(1)
    except:
        print(intext)
        raise
    #print(code)
    #raise
    return code

def extr_lean(intext):
    try:
        match_str = re.search(r'```lean4\n(.*?)```', intext, re.DOTALL)
        code = match_str.group(1)
    except:
        print(intext)
        raise
    #print(code)
    
    return code

def convert_format(org_data, task, dataset):
    data = []
    for item in tqdm(org_data):
        #item = json.loads(line)
        #print(item.keys())
        #print(item)
        #raise
        cur_state = extr_lean_base(item['input'])
        next_tactic = extr_lean(item['output'])
        #print('cur_state:', cur_state)
        #print('======================')
        #print(next_tactic)
        
        #print(item['output'])
        
        CoT = item['output'].split("---\nNext tactic:")[0].strip()
        #print('========================')
        #print(CoT)
        #raise
        idx = get_md5(item['input']+item['output'])
    
        data_w = {
            "id": task+"-" + dataset +'-' + idx,
            "cur_state": cur_state,
            "CoT": CoT,
            "next_tactic": next_tactic,
        }
        #print(data_w)
        #raise
        data.append(data_w)
    return data

def dict2json(data, path):
    with open(path, 'w') as fw:
        for line in tqdm(data):
            fw.write(json.dumps(line, ensure_ascii=False) + '\n')

def main():
    indir = '../org/Lean_STaR_base'
    outdir = '../processed/'
    task = 'NLFLT'
    os.makedirs(outdir, exist_ok=True)

    for filename in os.listdir(indir):
        if filename.endswith('json'):
            pass
        else:
            continue
        print(filename)
        dataset = os.path.basename(indir) + '_' + filename.split('.')[0]
        print(dataset)
        inpath = os.path.join(indir, filename)
        #print(inpath)
        org_data = indent_json2dict(inpath)
        
        processed_data = convert_format(org_data, task, dataset)
        
        outpath = os.path.join(outdir, dataset+'.json')
        dict2json(processed_data, outpath)

if __name__ == '__main__':
    main()
