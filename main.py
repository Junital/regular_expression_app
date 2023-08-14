import os
import re

# 搜索关键词
def search_files(directory, query):
    results = []
    pattern = re.compile(r'{}'.format(query), re.IGNORECASE)

    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                matches = pattern.finditer(content)
                for match in matches:
                    context_start = max(0, match.start() - 30)
                    context_end = min(len(content), match.end() + 30)
                    context = content[context_start:context_end]
                    results.append((file_path, context))
    
    return results

# 主程序
def main():
    directory = 'D:\D\Logseq\journals'  # 指定搜索的目录

    while True:
        query = input("Enter a keyword to search (or 'exit' to quit): ")
        if query == 'exit':
            break
        results = search_files(directory, query)
        if results:
            print("Search results:")
            for result in results:
                print(f"file:{result[0]}\n")
                print(f"context:{result[1]}\n")
        else:
            print("No results found.")

if __name__ == "__main__":
    main()
