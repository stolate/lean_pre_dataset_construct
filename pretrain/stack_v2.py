import sys, json, os
import hashlib
from tqdm import tqdm

input_p = '../../org/stack-v2/download_leanfile'    #sys.argv[1]
output_p = '../../pretrain_format/stack_v2.json'   #sys.argv[2]
datasource = 'stack_v2'   #sys.argv[3]

compare_p = '/data6/ftpdata/yilei4/math/data/train/org/lean-github/repos'

def json2dict(inpath):
    data = []
    with open(inpath, 'r') as fr:
        for line in fr:
            line = json.loads(line)
            lean = line['text'].replace('<ret>', '\n').replace('<end>', '').strip()
            #print(lean)
            
            idx = get_md5(lean)
            data.append(idx)
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


leangit = {}

for filename in os.listdir(compare_p):
    path = os.path.join(compare_p, filename)
    try:
        context = readlean(path).strip()
    except:
        print(filename)
        continue
    idx = get_md5(context)
    leangit[idx] = context


data_dict = {}
with open(output_p, "w", encoding="utf-8") as outpuf_f:
    for filename in tqdm(os.listdir(input_p)):
        path = os.path.join(input_p, filename)
        try:
            context = readlean(path).strip()
        except:
            print(path)
            continue
        idx = get_md5(context)

        if idx in leangit.keys():
            print(filename)
            continue
        if idx in data_dict.keys():
            print(filename)
            continue
        data_dict[idx] = context
        data_dump = convert_format(idx, context, datasource)
        #print(data_dump)

        json.dump(data_dump, outpuf_f, ensure_ascii=False)
        outpuf_f.write("\n")
print(len(data_dict.keys()))

