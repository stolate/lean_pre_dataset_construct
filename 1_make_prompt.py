import sys, json, random, os
from tqdm import tqdm
input_p = r"/data2/xyzhou15/数学合成数据/LEAN4/mathlib_related/0_seed/leandojo_train.json"
output_p = r"/data6/ftpdata/yilei4/math/data/train/1_prompt/leandojo_train.json"

# input_p = sys.argv[1]
# output_p = sys.argv[2]
STYLES = {
"college":
"""Write an educational piece suited for college students about explaining the following LEAN4 proof process. Explain the entire proof process in natural language rather than LEAN language.:
<problem>

Do not just list concepts, but develop each one in detail before moving to the next, as we prioritize depth of understanding and comprehensive exploration of the subject matter over breadth. Focus on:
- Rigor: Ensure in-depth coverage of the concepts/sections.
- Application: Incorporate specific, practical examples, such as explaining advanced knowledge through some basic knowledge.
Do not include a title or an introduction, simply write the content without headlines and introductory phrases.""",

"college_zh":
"""针对大学生群体，撰写一篇关与解释如下LEAN4证明过程相关的教材文章，用自然语言而不是LEAN语言解释一下整个证明过程：
# LEAN4代码
<problem>

不要只是罗列概念，而是在进入下一个概念之前详细阐述每一个概念，因为我们更注重对主题的深度理解以及全面探索，而非广度。重点关注：
严谨性：确保对概念/部分进行深入的覆盖
应用性：融入具体的、实际的例子，比如通过一些初级知识来解释高级知识
不要包含标题或引言，直接写内容，无需标题和开头的引语。
注意，输出的内容可参考lean的方法用自然语言（包含标准latex）进行推理，但不要直接使用lean中的函数。""",
}
file_size = os.path.getsize(input_p)
with open(input_p, "r", encoding="utf-8") as inpuf_f, \
    open(output_p, "w", encoding="utf-8") as outpuf_f, \
    tqdm(total=file_size, unit='B', unit_scale=True, desc=input_p) as pbar:
    for index, line in enumerate(inpuf_f):
        pbar.update(len(line.encode('utf-8')))
        data_json = json.loads(line)
        
        items = list(STYLES.items())
        # 随机选择一个键值对
        # random_items = random.choice(items)
        # random_items = random.sample(items, 1)
        for k, v in items:
            data_dump = {"id": data_json["name"], "style": k}
            str_w = data_json["main_code"]+"\n"
            for index, step in enumerate(data_json["traced_tactics"]):
                str_w += f"# 步骤 {index}: {step['tactic']}\n"
                str_w += f"## 步骤{index}执行前状态: \n{step['state_before']}\n"
                for pre in step["premises"]:
                    str_w += f"## 前提: {pre['name']}\n"
                    str_w += pre["code"].strip()+"\n"
                str_w += f"## 步骤{index}执行后状态: \n{step['state_after']}\n"
                str_w += "\n"
                
            data_dump["query"] = v.replace("<problem>", str_w.strip())
            json.dump(data_dump, outpuf_f, ensure_ascii=False)
            outpuf_f.write("\n")
