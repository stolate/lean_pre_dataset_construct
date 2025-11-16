#合成数据转换为无监督
import sys, json
from tqdm import tqdm
import hashlib
import random

input_p = '/data6/ftpdata/yilei4/math/data/train/org/herald/statement.json'   #sys.argv[1]
output_p = '/data6/ftpdata/yilei4/math/data/train/pred_proof_format/herald_statement.json'   #sys.argv[2]
datasource = 'herald_statement'#sys.argv[3]

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

    indata = json2dict(input_p)
    data_lst = []
    back_lst = []
    for data in tqdm(indata):
        
        NLS =data['informal_statement']
        FLS = data['formal_statement'].split('sorry')[0]

        #FLS_comments = '/--\n{nls}\n-/\n{fls}'.format(nls=NLS, fls=FLS)
        data_dump = {
                    'id': data['id'],
                    'NLS': NLS,
                    'FLS': FLS
                }
        data_lst.append(data_dump)

    dict2json(output_p, data_lst)

if __name__ == '__main__':
    main()
