#合成数据转换为无监督
import sys, json
from tqdm import tqdm
import hashlib
import random

input_p = '/data2/xyzhou15/数学合成数据/LEAN4/Lean-Workbook/0_ori/lean_workbook.json'
output_p = '/data6/ftpdata/yilei4/math/data/train/pretrain_format/lean_workbook_proof.json'
datasource = 'lean_workbook'

def get_file_line_count(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return sum(1 for _ in file)
total_lines = get_file_line_count(input_p)

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
    header = 'import Mathlib\nimport Aesop\nimport ProofWidgets\n\nset_option maxHeartbeats 0\n\nopen BigOperators Real Nat Topology Rat\n\n'
    
    indata = indent_json2dict(input_p)
    data_lst = []
    back_lst = []
    for data in tqdm(indata):
        if data['proof'] == []:
            continue
        #print(data)
        for proof in data['proof']:
            context = add_ret(header + data['formal_statement'].rstrip("sorry").strip() + '\n' + proof.strip())
            #print(context)
            #raise
            idx = get_md5(context)
            data_dump = convert_format(idx, context)
            data_lst.append(data_dump)
    dict2json(output_p, data_lst)

if __name__ == '__main__':
    main()
