import os
import re
from tkinter import scrolledtext
import tkinter as tk

def get_column_count(line_number):
    line_start = f"{line_number}.0"
    line_end = f"{line_number + 1}.0"
    line_text = result_text.get(line_start, line_end)
    return len(line_text)  # 减去换行符

def highlight_matches():
    query = keyword_entry.get()
    text_content = result_text.get("1.0", "end")
    result_text.tag_remove("highlight", "1.0", "end")

    # print(result_text.index("end"))

    pattern = re.compile(r'{}'.format(re.escape(query)), re.IGNORECASE | re.DOTALL)
    matches = pattern.finditer(text_content)

    for match in matches:
        start = match.start()
        end = match.end()
        # print(f"1.{start}", f"1.{end}", "\n")
        line = 1
        start_line = 1
        end_line = 1
        while(True):
            column_num = get_column_count(line)
            if(start <= column_num and end <= column_num):
                break
            if(start > column_num):
                start -= column_num
                start_line += 1
            if(end > column_num):
                end -= column_num
                end_line += 1
            line += 1
        # print(start_line, start, end_line, end)
        result_text.tag_add("highlight", f"{start_line}.{start}", f"{end_line}.{end}")

def clear_highlight():
    result_text.tag_remove("highlight", "1.0", "end")

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
def search_button_clicked():
    query = keyword_entry.get()

    if not query:  # 检查输入是否为空
        return

    results = search_files(directory, query)
    result_text.config(state=tk.NORMAL)
    result_text.delete(1.0, tk.END)
    if results:
        for result in results:
            result_text.insert(tk.END, f"File: {result[0]}\n")
            result_text.insert(tk.END, f"Context: {result[1]}\n")
        highlight_matches()
    else:
        print("No results found.")

directory = 'D:\D\Logseq\journals'  # 指定搜索的目录

app = tk.Tk()
app.title("Regular Expression App")

keyword_label = tk.Label(app, text="Enter a Regular Expression pattern:")

keyword_label.pack()

keyword_entry = tk.Entry(app)
keyword_entry.pack()

search_button = tk.Button(app, text="Search", command=search_button_clicked)
search_button.pack()

result_text = scrolledtext.ScrolledText(app, state=tk.DISABLED, wrap=tk.WORD)
result_text.pack()

highlight_button = tk.Button(app, text="Highlight", command=highlight_matches)
highlight_button.pack()

clear_button = tk.Button(app, text="Clear Highlight", command=clear_highlight)
clear_button.pack()

result_text.tag_configure("highlight", background="yellow")

app.mainloop()