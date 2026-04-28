import os
import sys

# 导入咱们写好的核心模块
from src.linter import check_dead_links
from src.ingest import read_all_documents
from src.compiler import compile_knowledge_base, save_wiki_pages
from src.query_engine import chat_with_knowledge_base

def main_menu():
    """主菜单界面"""
    raw_dir = "raw"
    wiki_dir = "wiki"
    
    while True:
        print("\n" + "="*50)
        print("🚀 Karpathy 风格长上下文知识库系统 (完整版)")
        print("="*50)
        print("1. 重新编译知识库 (Ingest + Compile)")
        print("2. 进入问答系统 (Query)")
        print("3. 健康检查 (Auto-Lint 扫描死链) 🌟[进阶功能]")
        print("4. 退出程序 (Exit)")
        print("="*50)
        
        choice = input("请选择操作 (1/2/3/4): ").strip()
        
        if choice == '1':
            print("\n[阶段 1] 正在读取 raw 文件夹中的原始文档...")
            raw_text = read_all_documents(raw_dir)
            if not raw_text:
                print("读取失败，请检查 raw 文件夹里是否有文件！")
                continue
            
            print(f"成功读取！合并总字数: {len(raw_text)} 字。")
            print("\n[阶段 2] 正在呼叫大模型进行提炼与编译...")
            llm_result = compile_knowledge_base(raw_text)
            
            if llm_result:
                print("\n[阶段 3] 正在保存生成的 Wiki 词条...")
                save_wiki_pages(llm_result, wiki_dir)
            
        elif choice == '2':
            chat_with_knowledge_base()
            
        elif choice == '3':
            # 注意这里传入 wiki_dir 变量
            check_dead_links(wiki_dir) 
            
        elif choice == '4':
            print("👋 感谢使用，再见！")
            sys.exit(0)
            
        else:
            print("❌ 输入无效，请重新输入 1、2、3 或 4！")

if __name__ == "__main__":
    # 确保当前运行路径在项目根目录
    if not os.path.exists("src"):
        print("错误：请确你在 karpathy-kb 文件夹下运行此程序！")
    else:
        main_menu()