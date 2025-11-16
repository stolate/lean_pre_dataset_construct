import os, json

generalize_prompt = '请将以下指令泛化为50条不同的指令，一半英文一半中文，均保持意思不变.请以python list的格式返回，每个元素是一条指令字符串.\n原始指令：'
direct_translate_prompt = [
    'You are an expert in Lean4 theorem prover and you will be given a theorem in natural language, and you must translate it into the correct formal statement in Lean4.',
    'Translate the following natural language problem into Lean4 code.',
    'Translate the following natural language problem into Lean4 statement with the potential proof replaced by \"sorry\"',
    'You will be given a math problem in natural language. Please translate it into correct Lean4 statement.',
    'Please translate the following natural language theorem into Lean4 format.'
    ]

cot_prompt = [
        'You will be given a math problem in natural language. Please translate it into correct Lean4 statement with thinking step by step.',
        'You are an expert in Lean4 theorem prover and you will be given a theorem in natural language, and you must translate it into the correct formal statement in Lean4 step by step.',
        'Translate the following natural language problem into Lean4 code with thinking steps.',
        'Translate the given natural language theorem into Lean4 statement with CoT.'
        ]

direct_complete_prompt = [
    '给定一个lean4命题，请你写出对应的lean4证明过程。',
    '你是一个lean4专家，请续写以下lean4代码，完成命题的证明。'
    ]

trans_state_proof = [
    'Translate the following informal math statement with proof into Lean4 code.',
    '请将下列数学问题形式化为带有证明过程的lean4代码。'
    '请将下列自然语言描述的题目翻译为Lean4代码。',
    '给定一个自然语言描述的数学问题，请给出对应的Lean4形式化命题及证明。',
    '请将下述问题翻译为Lean4代码，并证明。'    
    ]

informal_leandojo = [
    'Informalize the above Lean4 traced state-tactic sequence into natural language.',
    '请将上述形式化的状态-策略数据对，翻译为自然语言。',
    ]

minictx_st = [
    'You are proving a theorem in Lean 4 and given the current proof state, please generate the next tactic in the proof.',
    'You are an expert in Lean 4. Predict the next tactic for the given proof state.',
    'Generate the next tactic for the given Lean 4 proof state.'
    ]

minictx_context = [
    'You are proving a theorem in Lean 4 and given the current proof state and context, please generate the next tactic in the proof.',
    'You are an expert in Lean 4. Predict the next tactic for the given proof state.',
    'Given a Lean 4 proof state and the context, please generate the next tactic for the state.'
    ]

minictx_fullproof = [
    'You are proving a theorem in Lean 4 and given the current file contents up to and including the theorem statement.',
    'Complete the Lean 4 proof, given the file contents including the theorem statement.',
    'Given the current Lean 4 file contents up to and including the theorem statement, please generate the proof.'
    ]

results = [
    "You are proving a theorem in Lean 4 and given the current file contents up to and including the theorem statement.",
    "You're proving a theorem in Lean 4 and provided with the current file contents up to and including the theorem statement.",
    "You are engaged in proving a theorem in Lean 4 and given the current file contents up to and including the theorem statement.",
    "You are working on proving a theorem in Lean 4 and given the current file contents up to and including the theorem statement.",
    "You are in the process of proving a theorem in Lean 4 and given the current file contents up to and including the theorem statement.",
    "You are attempting to prove a theorem in Lean 4 and given the current file contents up to and including the theorem statement.",
    "You are tasked with proving a theorem in Lean 4 and given the current file contents up to and including the theorem statement.",
    "You are supposed to prove a theorem in Lean 4 and given the current file contents up to and including the theorem statement.",
    "You are required to prove a theorem in Lean 4 and given the current file contents up to and including the theorem statement.",
    "You are going to prove a theorem in Lean 4 and given the current file contents up to and including the theorem statement.",
    "You are about to prove a theorem in Lean 4 and given the current file contents up to and including the theorem statement.",
    "You are set to prove a theorem in Lean 4 and given the current file contents up to and including the theorem statement.",
    "You are on the way to prove a theorem in Lean 4 and given the current file contents up to and including the theorem statement.",
    "You are in the course of proving a theorem in Lean 4 and given the current file contents up to and including the theorem statement.",
    "You are busy proving a theorem in Lean 4 and given the current file contents up to and including the theorem statement.",
    "You are occupied with proving a theorem in Lean 4 and given the current file contents up to and including the theorem statement.",
    "You are focused on proving a theorem in Lean 4 and given the current file contents up to and including the theorem statement.",
    "You are dedicated to proving a theorem in Lean 4 and given the current file contents up to and including the theorem statement.",
    "You are committed to proving a theorem in Lean 4 and given the current file contents up to and including the theorem statement.",
    "You are determined to prove a theorem in Lean 4 and given the current file contents up to and including the theorem statement.",
    "You are striving to prove a theorem in Lean 4 and given the current file contents up to and including the theorem statement.",
    "You are trying to prove a theorem in Lean 4 and given the current file contents up to and including the theorem statement.",
    "You are making an effort to prove a theorem in Lean 4 and given the current file contents up to and including the theorem statement.",
    "You are exerting yourself to prove a theorem in Lean 4 and given the current file contents up to and including the theorem statement.",
    "You are using your skills to prove a theorem in Lean 4 and given the current file contents up to and including the theorem statement.",
    "You are leveraging your knowledge to prove a theorem in Lean 4 and given the current file contents up to and including the theorem statement.",
    "You are applying your expertise to prove a theorem in Lean 4 and given the current file contents up to and including the theorem statement.",
    "You are demonstrating your ability to prove a theorem in Lean 4 and given the current file contents up to and including the theorem statement.",
    "You are showing your proficiency in proving a theorem in Lean 4 and given the current file contents up to and including the theorem statement.",
    "You are exhibiting your talent in proving a theorem in Lean 4 and given the current file contents up to and including the theorem statement.",
    "你正在Lean 4中证明一个定理，并且已获得包含定理陈述在内的当前文件内容。",
    "你正在Lean 4里证明一个定理，同时得到了包含定理陈述在内的当前文件内容。",
    "你正着手在Lean 4中证明一个定理，还拿到了包含定理陈述在内的当前文件内容。",
    "你正忙于在Lean 4中证明一个定理，并且被给予了包含定理陈述在内的当前文件内容。",
    "你正专注于在Lean 4中证明一个定理，同时获知了包含定理陈述在内的当前文件内容。",
    "你正致力于在Lean 4中证明一个定理，而且得到了包含定理陈述在内的当前文件内容。",
    "你正努力在Lean 4中证明一个定理，并且拥有了包含定理陈述在内的当前文件内容。",
    "你正尝试在Lean 4中证明一个定理，同时拿到了包含定理陈述在内的当前文件内容。",
    "你正打算在Lean 4中证明一个定理，并且得到了包含定理陈述在内的当前文件内容。",
    "你正要在Lean 4中证明一个定理，同时获知了包含定理陈述在内的当前文件内容。",
    "你准备在Lean 4中证明一个定理，并且拥有了包含定理陈述在内的当前文件内容。",
    "你处于在Lean 4中证明一个定理的过程中，并且得到了包含定理陈述在内的当前文件内容。",
    "你在Lean 4中承担着证明一个定理的任务，并且被给予了包含定理陈述在内的当前文件内容。",
    "你应该在Lean 4中证明一个定理，同时获知了包含定理陈述在内的当前文件内容。",
    "你需要在Lean 4中证明一个定理，并且拥有了包含定理陈述在内的当前文件内容。",
    "你正在为在Lean 4中证明一个定理而努力，同时拿到了包含定理陈述在内的当前文件内容。",
    "你正在用自己的技能在Lean 4中证明一个定理，并且得到了包含定理陈述在内的当前文件内容。",
    "你正在利用自己的知识在Lean 4中证明一个定理，同时获知了包含定理陈述在内的当前文件内容。",
    "你正在运用自己的专业知识在Lean 4中证明一个定理，并且拥有了包含定理陈述在内的当前文件内容。",
    "你正在展示自己在Lean 4中证明一个定理的能力，同时拿到了包含定理陈述在内的当前文件内容。",
    "你正在展现自己在Lean 4中证明一个定理的熟练度，并且得到了包含定理陈述在内的当前文件内容。",
    "你正在显露自己在Lean 4中证明一个定理的天赋，同时获知了包含定理陈述在内的当前文件内容。",

    "Complete the Lean 4 proof, given the file contents including the theorem statement.",
"Finish the Lean 4 proof, considering the file contents with the theorem statement.",
"Accomplish the Lean 4 proof, taking into account the file contents having the theorem statement.",
"Carry out the Lean 4 proof, based on the file contents that include the theorem statement.",
"Execute the Lean 4 proof, given the information in the file with the theorem statement.",
"Fulfill the Lean 4 proof, according to the file contents containing the theorem statement.",
"Finalize the Lean 4 proof, given the file details including the theorem statement.",
"Achieve the Lean 4 proof, in light of the file contents with the theorem statement.",
"Wrap up the Lean 4 proof, considering the data in the file including the theorem statement.",
"Conclude the Lean 4 proof, based on the file contents which include the theorem statement.",
"Do the Lean 4 proof, given the file contents that have the theorem statement.",
"Make the Lean 4 proof, considering the file's information including the theorem statement.",
"Perform the Lean 4 proof, taking the file contents with the theorem statement into consideration.",
"Undertake the Lean 4 proof, given the file contents incorporating the theorem statement.",
"Work on the Lean 4 proof, based on the file details including the theorem statement.",
"Conduct the Lean 4 proof, given the information in the file that includes the theorem statement.",
"Effect the Lean 4 proof, according to the file contents with the theorem statement included.",
"Realize the Lean 4 proof, considering the file data with the theorem statement.",
"Bring about the Lean 4 proof, based on the file contents having the theorem statement.",
"Produce the Lean 4 proof, given the file details that include the theorem statement.",
"Given the file contents with the theorem statement, complete the Lean 4 proof.",
"Considering the file contents including the theorem statement, finish the Lean 4 proof.",
"Taking into account the file contents having the theorem statement, accomplish the Lean 4 proof.",
"Based on the file contents that include the theorem statement, carry out the Lean 4 proof.",
"Given the information in the file with the theorem statement, execute the Lean 4 proof.",
"According to the file contents containing the theorem statement, fulfill the Lean 4 proof.",
"Given the file details including the theorem statement, finalize the Lean 4 proof.",
"In light of the file contents with the theorem statement, achieve the Lean 4 proof.",
"Considering the data in the file including the theorem statement, wrap up the Lean 4 proof.",
"Based on the file contents which include the theorem statement, conclude the Lean 4 proof.",
"给定包含定理陈述的文件内容，完成 Lean 4 证明。",
"考虑到包含定理陈述的文件内容，完成 Lean 4 的证明。",
"鉴于包含定理陈述的文件内容，完成 Lean 4 证明。",
"依据包含定理陈述的文件内容来完成 Lean 4 证明。",
"根据含有定理陈述的文件信息完成 Lean 4 证明。",
"按照包含定理陈述的文件内容完成 Lean 4 的证明工作。",
"鉴于包含定理陈述的文件详情，完成 Lean 4 证明。",
"根据包含定理陈述的文件内容达成 Lean 4 证明。",
"考虑到包含定理陈述的文件数据，完成 Lean 4 证明。",
"依据包含定理陈述的文件内容结束 Lean 4 证明。",
"给定有定理陈述的文件内容，完成 Lean 4 证明。",
"考虑到文件中包含定理陈述的信息，完成 Lean 4 证明。",
"把包含定理陈述的文件内容考虑在内，完成 Lean 4 证明。",
"给定包含定理陈述的文件内容，着手完成 Lean 4 证明。",
"基于包含定理陈述的文件细节，完成 Lean 4 证明。",
"根据文件中包含定理陈述的信息，完成 Lean 4 证明。",
"按照包含定理陈述的文件内容来实现 Lean 4 证明。",
"考虑到包含定理陈述的文件数据，做完 Lean 4 证明。",
"依据包含定理陈述的文件内容实现 Lean 4 证明。",
"给定包含定理陈述的文件细节，完成 Lean 4 证明。",

"Given the current Lean 4 file contents up to and including the theorem statement, please generate the proof.",
"Given the contents of the current Lean 4 file up to and including the theorem statement, kindly generate the proof.",
"Given the current Lean 4 file's contents up to and including the theorem statement, please create the proof.",
"Given the contents of the current Lean 4 file up to and including the theorem statement, generate the proof.",
"Given the current Lean 4 file contents up to the theorem statement (inclusive), please generate the proof.",
"Given the current Lean 4 file's contents up to the theorem statement (inclusive), generate the proof.",
"Given the contents of the current Lean 4 file up to the theorem statement (inclusive), kindly generate the proof.",
"Given the current Lean 4 file contents up to and including the theorem statement, produce the proof.",
"Given the contents of the current Lean 4 file up to and including the theorem statement, create the proof.",
"Given the current Lean 4 file's contents up to and including the theorem statement, please come up with the proof.",
"Given the current Lean 4 file contents up to the theorem statement (inclusive), produce the proof.",
"Given the contents of the current Lean 4 file up to the theorem statement (inclusive), create the proof.",
"Given the current Lean 4 file's contents up to the theorem statement (inclusive), come up with the proof.",
"Given the current Lean 4 file contents up to and including the theorem statement, formulate the proof.",
"Given the contents of the current Lean 4 file up to and including the theorem statement, formulate the proof.",
"Given the current Lean 4 file's contents up to and including the theorem statement, please devise the proof.",
"Given the current Lean 4 file contents up to the theorem statement (inclusive), formulate the proof.",
"Given the contents of the current Lean 4 file up to the theorem statement (inclusive), devise the proof.",
"Given the current Lean 4 file's contents up to the theorem statement (inclusive), please frame the proof.",
"Given the current Lean 4 file contents up to and including the theorem statement, construct the proof.",
"Given the contents of the current Lean 4 file up to and including the theorem statement, construct the proof.",
"Given the current Lean 4 file's contents up to and including the theorem statement, please build the proof.",
"Given the current Lean 4 file contents up to the theorem statement (inclusive), construct the proof.",
"Given the contents of the current Lean 4 file up to the theorem statement (inclusive), build the proof.",
"Given the current Lean 4 file's contents up to the theorem statement (inclusive), please fashion the proof.",
"根据当前 Lean 4 文件中直至定理陈述（包含该陈述）的内容，请生成证明。",
"依据当前 Lean 4 文件中直至定理陈述（包含该陈述）的内容，生成证明。",
"按照当前 Lean 4 文件中直至定理陈述（包含该陈述）的内容，请生成证明。",
"根据当前 Lean 4 文件里直至定理陈述（包含该陈述）的内容，来生成证明。",
"基于当前 Lean 4 文件中直至定理陈述（包含该陈述）的内容，生成证明。",
"鉴于当前 Lean 4 文件中直至定理陈述（包含该陈述）的内容，请生成证明。",
"根据当前 Lean 4 文件的内容，直至定理陈述（包含该陈述），请生成证明。",
"按照当前 Lean 4 文件的内容，直至定理陈述（包含该陈述），生成证明。",
"依据当前 Lean 4 文件的内容，直至定理陈述（包含该陈述），请生成证明。",
"根据当前 Lean 4 文件内容，到定理陈述（包含该陈述）为止，请生成证明。",
"基于当前 Lean 4 文件内容，到定理陈述（包含该陈述）为止，生成证明。",
"鉴于当前 Lean 4 文件内容，到定理陈述（包含该陈述）为止，请生成证明。",
"根据当前 Lean 4 文件里的内容，直至定理陈述（包含该陈述），请构建证明。",
"依据当前 Lean 4 文件里的内容，直至定理陈述（包含该陈述），构建证明。",
"按照当前 Lean 4 文件里的内容，直至定理陈述（包含该陈述），请构建证明。",
"根据当前 Lean 4 文件的内容，到定理陈述（包含该陈述）为止，构建证明。",
"基于当前 Lean 4 文件的内容，到定理陈述（包含该陈述）为止，请构建证明。",
"鉴于当前 Lean 4 文件的内容，到定理陈述（包含该陈述）为止，构建证明。",
"根据当前 Lean 4 文件内容，直至定理陈述（包含该陈述），请拟定证明。",
"依据当前 Lean 4 文件内容，直至定理陈述（包含该陈述），拟定证明。",
"按照当前 Lean 4 文件内容，直至定理陈述（包含该陈述），请拟定证明。",
"根据当前 Lean 4 文件内容，到定理陈述（包含该陈述）为止，拟定证明。",
"基于当前 Lean 4 文件内容，到定理陈述（包含该陈述）为止，请拟定证明。",
"鉴于当前 Lean 4 文件内容，到定理陈述（包含该陈述）为止，拟定证明。",
"根据当前 Lean 4 文件中直至定理陈述（包含该陈述）的内容，请设计证明。",
"依据当前 Lean 4 文件中直至定理陈述（包含该陈述）的内容，设计证明。",
"按照当前 Lean 4 文件中直至定理陈述（包含该陈述）的内容，请设计证明。",
"根据当前 Lean 4 文件内容，到定理陈述（包含该陈述）为止，设计证明。",
"基于当前 Lean 4 文件内容，到定理陈述（包含该陈述）为止，请设计证明。",
"鉴于当前 Lean 4 文件内容，到定理陈述（包含该陈述）为止，设计证明。"
]


print(len(results))
with open('../../instructions/minictx_fullproof.json', 'w') as fw:
    for ins in results:
        data_dump = {'instruction': ins}
        fw.write(json.dumps(data_dump, ensure_ascii=False) + '\n')


