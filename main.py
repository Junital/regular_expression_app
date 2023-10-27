import os
import re
from tkinter import scrolledtext
import tkinter as tk
from tkinter import filedialog

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
    pattern = re.compile(r'{}'.format(query), re.IGNORECASE | re.DOTALL)

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

def on_enter_key(event):
    search_button_clicked()

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

# search module
search_frame = tk.Frame(app)
search_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

## head_frame
head_frame = tk.Frame(search_frame)
head_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

keyword_label = tk.Label(head_frame, text="Enter a Regular Expression pattern:")
keyword_label.pack()

keyword_entry = tk.Entry(head_frame)
keyword_entry.pack(side=tk.LEFT, padx=170, pady=5, ipadx=30)
keyword_entry.bind("<Return>", on_enter_key)

search_button = tk.Button(head_frame, text="Search", command=search_button_clicked)
search_button.place(x=400, y=22)

## result frame
result_frame = tk.Frame(search_frame)
result_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

result_text = scrolledtext.ScrolledText(result_frame, state=tk.DISABLED, wrap=tk.WORD)
result_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

## highlight frame
highlight_frame = tk.Frame(search_frame)
highlight_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

highlight_button = tk.Button(highlight_frame, text="Highlight", command=highlight_matches)
highlight_button.pack(side=tk.LEFT, padx=100, pady=5)

clear_button = tk.Button(highlight_frame, text="Clear Highlight", command=clear_highlight)
clear_button.pack(side=tk.LEFT, padx=100, pady=5)

result_text.tag_configure("highlight", background="yellow")

app.mainloop()