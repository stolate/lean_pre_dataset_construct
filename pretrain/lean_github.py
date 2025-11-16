import sys, json, os
import hashlib
from tqdm import tqdm

input_p = '../../org/stack-v2/download_leanfile/'    #sys.argv[1]
output_p = '../../pretrain_format/stack_v2.json'   #sys.argv[2]
datasource = 'stack_v2'   #sys.argv[3]

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

def convert_format(idx, context, datasource):
    input_text=context.strip().replace("\n","<ret>")+"<ret> <end>"
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


with open(output_p, "w", encoding="utf-8") as outpuf_f:
    for filename in tqdm(os.listdir(input_p)):
        path = os.path.join(input_p, filename)
        context = readlean(path)
        idx = get_md5(context)
        data_dump = convert_format(idx, context, datasource)
        #print(data_dump)
        json.dump(data_dump, outpuf_f, ensure_ascii=False)
        outpuf_f.write("\n")

