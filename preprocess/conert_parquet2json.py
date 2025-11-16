import os
import pandas as pd

def convert_parquet_to_json(directory):
    for filename in os.listdir(directory):
        if filename.endswith(".parquet"):
            parquet_file = os.path.join(directory, filename)
            json_file = os.path.join(directory, filename.replace('.parquet', '.json'))

            try:
                # 读取Parquet文件
                df = pd.read_parquet(parquet_file)
            except Exception as e:
                print(f"Error reading {parquet_file}: {e}")
                continue

            # 保存为JSON文件
            with open(json_file, 'w', encoding='UTF-8', errors='ignore') as f:
                df.to_json(f, orient='records', lines=True, force_ascii=False)
            print(f"Converted {parquet_file} to {json_file}")

if __name__ == "__main__":
    directory = r"/data6/ftpdata/yilei4/math/data/train/org/STP_Lean"
    convert_parquet_to_json(directory)
