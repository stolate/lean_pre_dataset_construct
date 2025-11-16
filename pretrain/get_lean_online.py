import json, os
import subprocess
from tqdm import tqdm

def json2dict_lean(inpath):
    data = []
    with open(inpath, 'r') as fr:
        for line in fr:
            line = json.loads(line)
            #print(line)
            repo_name = line['url'].split('.git')[0].split('.com/')[-1]

            data.append(repo_name)
    return data


inpath = '../../org/lean-github/lean-github.json'
repo_data = json2dict_lean(inpath)
lean_repo = list(set(repo_data))


def json2dict(inpath):
    data = []
    with open(inpath, 'r') as fr:
        for line in fr:
            line = json.loads(line)
            repo_name = line['repo_name']
            if repo_name in lean_repo:
                continue
            commit = line['branch_name']
            sub_path = line['path']

            prefix = 'https://raw.githubusercontent.com'
            
            path = prefix + '/' +repo_name + '/' + commit + '/' + sub_path
            
            #print(path)
            #print('https://raw.githubusercontent.com/kevinsullivan/cs2120f23/c2da7c4a6be769c6fca375a54e8c1fa31ba2854b/Instructor/Lectures/grad/vector_spaces.lean')
            
            data.append(path)
    return data

def dict2json(data, path):
    with open(path, 'w') as fw:
        for line in tqdm(data):
            fw.write(json.dumps(line, ensure_ascii=False) + '\n')

def download(url, dest_path):
    cmd = 'wget -P {} {}'.format(dest_path, url)
    try:
        result = subprocess.run(['wget', '-P', dest_path, url], capture_output=True, text=True, check=True)
        #print("命令输出:\n", result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"命令执行出错，错误信息: {e.stderr}")

def main():
    
    indir = '/data6/ftpdata/yilei4/math/data/train/org/stack-v2'
    outdir = '/data6/ftpdata/yilei4/math/data/train/org/stack-v2/download_leanfile'
    os.makedirs(outdir, exist_ok=True)

    for filename in os.listdir(indir):
        if filename.endswith('json'):
            pass
        else:
            continue
        print(filename)

        inpath = os.path.join(indir, filename)
        #print(inpath)
        path_data = json2dict(inpath)
        path_list = set(path_data)
        print(len(path_list))

        for index, url in enumerate(tqdm(path_list)):
            #dest_path = os.path.join('../repos')
            download(url, outdir)


if __name__ == '__main__':
    main()
