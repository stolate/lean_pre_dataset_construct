import sys, json, random, os
from tqdm import tqdm
input_p = r"/data6/ftpdata/yilei4/math/data/train/processed/Lean_CoT_plus_gpt4_gen_train.json"
output_p = r"/data6/ftpdata/yilei4/math/data/train/1_prompt/Lean_CoT_plus_gpt4_gen_train.json"
sample_p = r"/data6/ftpdata/yilei4/math/data/train/1_prompt/Lean_CoT_plus_shuff50.json"
os.makedirs(os.path.dirname(output_p), exist_ok=True)
# input_p = sys.argv[1]
# output_p = sys.argv[2]
STYLES = {
"translate_direct":
"""你现在是一个基于LEAN4和自然语言的推理专家，请根据下面的<当前状态-下一策略>LEAN4代码数据对，生成准确严谨的自然语言命题和证明过程，算式、公式等请用标准latex表示。
# LEAN4代码
### 当前状态: <命题> ###
### 下一策略: <证明> ###
请根据上述lean数据对，按照如下json格式生成自然语言描述的命题和证明:
{"命题": <NL statement>,"证明": <NL Proof>}
注意，输出的内容可参考lean的方法用自然语言（包含标准latex）进行推理，但不要直接使用lean中的函数。
""",
}
sample_num = 50

STYLES_backup = {
"translate_direct":
"""你现在是一个基于LEAN4和自然语言的推理专家，请根据下面的<命题-证明>LEAN4代码数据对，生成准确严谨的自然语言命题和证明过程，算式、公式等请用标准latex表示。
# LEAN4代码
### 命题: <命题> ###
### 证明: <证明> ###
请根据上述lean数据对，按照如下json格式生成自然语言描述的命题和证明:
{"命题": <NL statement>,"证明": <NL Proof>}
注意，输出的内容可参考lean的方法用自然语言（包含标准latex）进行推理，但不要直接使用lean中的函数。
""",
}

file_size = os.path.getsize(input_p)
with open(input_p, "r", encoding="utf-8") as inpuf_f, \
    open(output_p, "w", encoding="utf-8") as outpuf_f, \
    open(sample_p, "w", encoding="utf-8") as sample_f, \
    tqdm(total=file_size, unit='B', unit_scale=True, desc=input_p) as pbar:
    lines = inpuf_f.readlines()
    idx_lst = random.sample(range(0, len(lines)), sample_num)
    for index, line in enumerate(lines):
        pbar.update(len(line.encode('utf-8')))
        data_json = json.loads(line)
        if data_json['next_tactic'] == None:
            continue
        items = list(STYLES.items())
        # 随机选择一个键值对
        #FLP = '\n'.join(data_json['FLP']).strip()
        for k, v in items:
            
            try:
                query = v.replace("<当前状态>", data_json['cur_state']).replace("<下一策略>", data_json['next_tactic'])
            except:
                print(data_json['FLS'])
                print(data_json['FLP'])
                raise
            data_json["style"] = k
            data_json["query"] = query
                           
            json.dump(data_json, outpuf_f, ensure_ascii=False)
            outpuf_f.write("\n")
            #if index in idx_lst:
            #    json.dump(data_json, sample_f, ensure_ascii=False)
            #    sample_f.write("\n")


