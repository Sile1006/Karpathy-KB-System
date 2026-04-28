import os
# 引入我们刚刚安装的 PDF 解析库
import PyPDF2

def read_pdf(file_path):
    """专门用来榨干 PDF 文本的解析器"""
    text = f"\n--- 来源文件: {os.path.basename(file_path)} (PDF) ---\n"
    try:
        with open(file_path, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
    except Exception as e:
        print(f"❌ 读取 PDF 失败 {file_path}: {e}")
    return text

def read_markdown(file_path):
    """原有的 Markdown 读取器"""
    text = f"\n--- 来源文件: {os.path.basename(file_path)} (Markdown) ---\n"
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            text += f.read() + "\n"
    except Exception as e:
        print(f"❌ 读取 Markdown 失败 {file_path}: {e}")
    return text

def read_all_documents(raw_folder):
    """
    终极融合引擎：自动识别 .md 和 .pdf 文件并全部吞入
    """
    if not os.path.exists(raw_folder):
        print(f"找不到文件夹: {raw_folder}")
        return ""

    all_text = []
    
    for filename in os.listdir(raw_folder):
        file_path = os.path.join(raw_folder, filename)
        
        # 遇到 Markdown 文件
        if filename.endswith(".md"):
            print(f"📄 成功读取 Markdown 文件: {filename}")
            all_text.append(read_markdown(file_path))
            
        # 遇到 PDF 文件
        elif filename.endswith(".pdf"):
            print(f"📕 成功解析 PDF 文件: {filename}")
            all_text.append(read_pdf(file_path))

    return "\n".join(all_text)

# 测试区
if __name__ == "__main__":
    content = read_all_documents("../raw")
    print(f"\n读取完成！合并后的总字数: {len(content)}")