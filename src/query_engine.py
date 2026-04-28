import os
from openai import OpenAI

# ==========================================
# ⚠️ 填入你刚才使用的 API Key 和 Base URL
# ==========================================
API_KEY = "sk-b0cc9da9a85244ac87206bec308709a3"
BASE_URL = "https://api.deepseek.com/v1" # 如果用的是别家，请保持和之前一样

client = OpenAI(api_key=API_KEY, base_url=BASE_URL)

def load_entire_wiki(wiki_folder):
    """
    把 wiki 文件夹里所有编译好的知识点，全部加载到内存里，作为全局上下文。
    """
    wiki_content = []
    if not os.path.exists(wiki_folder):
        print("找不到 wiki 文件夹，请先运行 step2_compile.py")
        return ""
        
    for filename in os.listdir(wiki_folder):
        if filename.endswith(".md"):
            file_path = os.path.join(wiki_folder, filename)
            with open(file_path, 'r', encoding='utf-8') as f:
                text = f.read()
                # 附加上文件名，方便 AI 引用
                wiki_content.append(f"【文件名: {filename}】\n{text}\n")
                
    return "\n".join(wiki_content)

def chat_with_knowledge_base():
    """
    启动一个交互式的终端问答系统
    """
    print("正在加载知识库...")
    wiki_folder = "wiki"
    global_context = load_entire_wiki(wiki_folder)
    
    if not global_context:
        return

    print("知识库加载完毕！我们可以开始对话了。（输入 'quit' 退出）")
    print("-" * 50)
    
    # 构造系统提示词，强制要求它根据知识库回答，并带上引用
    system_prompt = f"""
    你是一个智能知识库助手。以下是用户个人的所有 Wiki 知识库内容：
    
    <knowledge_base>
    {global_context}
    </knowledge_base>
    
    【你的任务与规则】
    1. 你只能基于 <knowledge_base> 里的内容来回答用户的问题。
    2. 如果知识库里没有相关信息，请直接回答“根据当前知识库，我无法回答这个问题”，绝不能瞎编。
    3. 在你的回答中，如果引用了某个知识点，必须在句子末尾加上 Obsidian 风格的引用来源，格式为：[[文件名.md]]。
    4. 尽量综合多个文档的内容来回答复杂问题。
    """

    # 存储对话历史，实现“多轮对话” (这也属于进阶功能的加分项哦！)
    chat_history = [{"role": "system", "content": system_prompt}]

    while True:
        user_input = input("\n🧑 你的问题: ")
        if user_input.lower() in ['quit', 'exit', 'q']:
            print("👋 再见！")
            break
            
        if not user_input.strip():
            continue

        # 把用户的新问题加入历史记录
        chat_history.append({"role": "user", "content": user_input})
        
        print("🤖 AI 正在思考...")
        try:
            response = client.chat.completions.create(
                model="deepseek-chat", # 根据你的实际模型修改
                messages=chat_history,
                temperature=0.1 # 回答事实性问题，温度调低
            )
            
            answer = response.choices[0].message.content
            print(f"\n💡 回答:\n{answer}")
            
            # 把 AI 的回答也加入历史记录，这样它就能记住上下文了
            chat_history.append({"role": "assistant", "content": answer})
            
        except Exception as e:
            print(f"调用 API 时发生错误: {e}")

# ====== 测试运行区 ======
if __name__ == "__main__":
    chat_with_knowledge_base()