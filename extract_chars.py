import os
import argparse

def extract_chars(input_paths, output_path):
    unique_chars = set()
    
    for path in input_paths:
        if not os.path.exists(path):
            print(f"跳过: 文件或目录不存在 -> {path}")
            continue
            
        # 如果是目录，递归处理
        if os.path.isdir(path):
            for root, dirs, files in os.walk(path):
                for file in files:
                    file_path = os.path.join(root, file)
                    process_file(file_path, unique_chars)
        else:
            process_file(path, unique_chars)
            
    # 按 Unicode 排序
    sorted_chars = sorted(list(unique_chars))
    
    # 写入结果
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("".join(sorted_chars))
        
    print(f"\n提取完成！")
    print(f"输入路径: {input_paths}")
    print(f"总计唯一字符数: {len(sorted_chars)}")
    print(f"结果已保存至: {output_path}")

def process_file(file_path, char_set):
    # 常见的文本后缀
    text_extensions = {'.txt', '.json', '.lua', '.py', '.c', '.cpp', '.h', '.js', '.xml', '.resx', '.yaml', '.yml'}
    
    _, ext = os.path.splitext(file_path)
    if ext.lower() not in text_extensions:
        # 如果后缀不在列表内，尝试读取前几个字节判断是否为文本（简单处理）
        pass 

    print(f"正在读取: {file_path}")
    
    # 尝试多种编码读取
    encodings = ['utf-8', 'utf-16', 'shift_jis', 'gbk', 'utf-8-sig']
    content = None
    
    for enc in encodings:
        try:
            with open(file_path, 'r', encoding=enc) as f:
                content = f.read()
                break
        except (UnicodeDecodeError, LookupError):
            continue
            
    if content:
        for char in content:
            if char not in '\r\n\t':
                char_set.add(char)
    else:
        print(f"  [跳过] 无法以文本方式解码: {file_path}")

def main():
    parser = argparse.ArgumentParser(description="从文本文件中提取所有唯一字符并按 Unicode 排序。")
    parser.add_argument("input", nargs="+", help="输入文件或文件夹路径（支持多个）")
    parser.add_argument("-o", "--output", default="chars.txt", help="输出文件名 (默认: chars.txt)")
    
    args = parser.parse_args()
    
    extract_chars(args.input, args.output)

if __name__ == "__main__":
    main()
