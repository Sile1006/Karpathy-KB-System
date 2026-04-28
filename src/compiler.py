import os
import re
from openai import OpenAI
# 导入我们已经修改好的读取函数（支持PDF和MD）
from src.ingest import read_all_documents

# ==========================================
# 配置区（建议这些参数后续可以统一放进 config.py）
# ==========================================
API_KEY = "sk-b0cc9da9a85244ac87206bec308709a3"
BASE_URL = "https://api.deepseek.com/v1"
MODEL_NAME = "deepseek-chat"

# 初始化客户端
client = OpenAI(api_key=API_KEY, base_url=BASE_URL)

def compile_knowledge_base(raw_text):
    """
    向大模型发送原始文本，并利用 Prompt 工程生成支持双链的 Wiki 内容。
    """
    print("\n🚀 正在呼叫大模型进行全局编译，请稍候...")
    
    system_prompt = """
    你是一个硬核的“Karpathy风格”知识库自动编译器。
    你的任务是深度阅读用户提供的原始资料（包含电赛赛题 PDF、电机技术手册 PDF 以及个人开发笔记），提炼出核心概念。

    【核心任务】
    1. 实体识别：识别出如“JC4010电机”、“CAN通信协议”、“串级PID控制”、“FPGA_LCD”、“YOLOv8部署”等核心实体。
    2. 知识蒸馏：从技术手册中提取关键参数（如波特率、CAN ID、寄存器地址） [cite: 50, 754]。
    3. 自动关联：在内容中使用 [[实体名]] 建立双向链接。

    【强制输出格式】
    每个页面必须以 `### FILE: 实体名.md` 开头：
    
    ### FILE: 实体名.md
    ---
    title: 实体名
    tags: [电赛备赛, 嵌入式开发, 自动化]
    ---
    # 实体名
    内容（必须包含技术要点和应用说明。若涉及其他页面，请使用 [[ ]] 引用）。
    
   【要求】
    1. 只输出规定的 ### FILE: 格式内容。
    2. 针对技术手册，务必保留关键的 16 进制指令示例。
    3. ⚠️【强制数量要求】：你必须深度挖掘原文档中的细分技术点，强制生成【至少 10 个】以上的独立 Wiki 页面！
    (例如可以细分为：JC4010电机参数、CAN标准帧结构、PVT位置控制指令、电赛C题波形展示要求、紫外激光笔控制、STM32串口波特率配置...等等)
    """

    try:
        response = client.chat.completions.create(
            model=MODEL_NAME, 
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"以下是完整的原始资料：\n{raw_text}"}
            ],
            temperature=0.2 # 进一步调低，确保格式绝对稳定
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"❌ 调用 API 时发生错误: {e}")
        return None

def save_wiki_pages(llm_output, output_folder="wiki"):
    """
    将返回的长文本切割并强制以 UTF-8 编码保存，彻底杜绝乱码。
    """
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        
    # 利用正则切割文件块
    pages = re.split(r'### FILE:\s*(.+?\.md)', llm_output)
    
    saved_count = 0
    # re.split 产生的列表索引 1 是文件名，2 是内容，以此类推
    for i in range(1, len(pages), 2):
        filename = pages[i].strip()
        content = pages[i+1].strip()
        
        file_path = os.path.join(output_folder, filename)
        
        # 👉 强制使用 UTF-8 编码保存，解决 Obsidian 乱码问题
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ 已存入 Wiki: {filename}")
        saved_count += 1
        
    print(f"\n✨ 编译完成！共生成 {saved_count} 个技术词条。")

# 测试区
if __name__ == "__main__":
    # 使用最新的目录路径
    raw_dir = "raw"
    wiki_dir = "wiki"
    
    text = read_all_documents(raw_dir)
    if text:
        result = compile_knowledge_base(text)
        if result:
            save_wiki_pages(result, wiki_dir)