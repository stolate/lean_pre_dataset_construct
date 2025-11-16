import json
import hashlib
import re, sys
import os
from tqdm import tqdm

def split_lean_theorem(lean_code):
    """
    分割 Lean 4 定理中的声明部分和证明部分

    参数:
        lean_code (str): 包含 Lean 定理的字符串

    返回:
        dict: {"statement": 声明部分, "proof": 证明部分}
    """
    # 去掉多余的空格和换行
    lean_code = lean_code.strip()

    # 正则表达式查找声明部分到 `:=` 为止的部分（非贪婪匹配）
    #print(lean_code)
    #match = re.search(r'^(theorem|lemma)\s+[\s\S]+?:=', lean_code, re.DOTALL | re.MULTILINE)
    match = re.search(r'^(theorem|lemma)\s+[\s\S]+?:=', lean_code, re.DOTALL | re.MULTILINE)
    if match:
        # 提取声明部分
        statement = match.group().strip().removesuffix(":=").strip()

        # 提取证明部分
        proof_start = match.end()  # 找到 `:=` 后的起始位置
        proof = lean_code[proof_start:].strip()

        return statement, proof
    else:
        raise ValueError("无法解析提供的 Lean 定理。请检查输入格式是否正确。")

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

def extr_lean(intext):
    try:
        cot, code = intext.rsplit('Final Lean Formalization:', 1)
    except:
        try:
            cot, code = intext.split('```lean',1)
            code = '```lean' + code
            #print(code)
        except:
            print(intext)
            raise
    #print(cot)
    #print(code)
    #raise
    code = code.strip()
    if code.endswith('```') and code.startswith('```lean'):
        #print(code)
        code = re.search(r'```lean\n(.*?)```', code, re.DOTALL).group(1)
    elif code.startswith('```lean'):
        code = code.split('```lean')[-1]
    elif code.endswith('```'):
        code = code.split('```')[0]
    else:
        print( code)
        raise
    '''
    try:
        code = re.search(r'```lean\n(.*?)\n```', code, re.DOTALL).group(1)
    except:
        print( code)
        raise
    '''
    return cot, code

def extr_fls(fls_in):
    #print(fls_in)
    if ":=" in fls_in:
        try:
            FLS, _ = fls_in.rsplit(':=', 1)   #split_lean_theorem(item['output'])        
        except:
            print(fls_in)
            raise
            #print(fls_in)
            #print(FLS)
            #raise
    elif isinstance(fls_in, dict):
        cot, lean_code = extr_lean(fls_in['coT'])
        FLS = lean_code.rsplit(':=', 1)[0]
    else:
        FLS = fls_in
    #print(FLS)
    #raise
    return FLS


def convert_format(org_data, task, dataset):
    data = []
    for item in tqdm(org_data):
        #item = json.loads(line)
        #print(item.keys())
        #print(item)
        #raise
                
        try:
            NLS = item['input']
            #NLS = item['input'].lstrip("Statement in natural language:").rstrip("Translate the statement in natural language to Lean:").strip()
        except:
            NLS = None
        
        #item['output'] = item['accept']
        try:
            item['output']
        except:
            continue
        
        FLS = extr_fls(item['output'])
        #rej_FLS = extr_fls(item['reject'])
        
        idx = get_md5(FLS)
    
        data_w = {
            "id": task+"-" + dataset +'-' + idx,
            "NLS": NLS,
            "NLP": None,
            "FLS": FLS,
            "FLP": None,
        }
        data.append(data_w)
    return data

def dict2json(data, path):
    with open(path, 'w') as fw:
        for line in tqdm(data):
            fw.write(json.dumps(line, ensure_ascii=False) + '\n')

def main():
    # in_path = sys.argv[1]
    # out_path = sys.argv[2]
    #in_path = "../org/SJTU_LeanStatement_SFT/LeanStatement_Amplified.json"
    #out_path = "../processed/SJTU_LeanStatement_SFT_Amplified.json"
    indir = '../org/SJTU_LeanStatement'
    outdir = '../../pretrain_format'
    task = 'NLFLT'
    os.makedirs(outdir, exist_ok=True)

    for filename in os.listdir(indir):
        if filename.endswith('json'):
            pass
        else:
            continue
        print(filename)
        dataset = os.path.basename(indir) + '_' + filename.split('_')[-1].split('.')[0]
        print(dataset)
        inpath = os.path.join(indir, filename)
        #print(inpath)
        org_data = indent_json2dict(inpath)
        
        processed_data = convert_format(org_data, task, dataset)
        
        outpath = os.path.join(outdir, dataset+'.json')
        dict2json(processed_data, outpath)

if __name__ == '__main__':
    main()
