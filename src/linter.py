import os
import re

def check_dead_links(wiki_folder="../wiki"):
    """
    扫描 wiki 文件夹下的所有 Markdown 文件，找出不存在的 [[死链]]
    """
    print("\n🔍 开始进行知识库健康检查 (Auto-Lint)...")
    
    if not os.path.exists(wiki_folder):
        print("❌ 找不到 wiki 文件夹！")
        return

    # 获取当前 wiki 文件夹下所有真实的 .md 文件名
    existing_files = [f for f in os.listdir(wiki_folder) if f.endswith('.md')]
    
    dead_links_count = 0
    
    # 遍历每一个 .md 文件，检查它里面的链接
    for filename in existing_files:
        file_path = os.path.join(wiki_folder, filename)
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # 使用正则表达式找出所有 [[xxx]] 格式的文字
        links = re.findall(r'\[\[(.*?)\]\]', content)
        
        for link in links:
            # 有些链接可能自带 .md，有些没有，我们统一处理加上 .md
            target_filename = link if link.endswith('.md') else f"{link}.md"
            
            # 如果链接指向的文件不存在于我们的文件夹里，就是死链！
            if target_filename not in existing_files:
                print(f"⚠️ [死链警告] 在 '{filename}' 中发现孤立概念: [[{link}]]")
                dead_links_count += 1
                
    if dead_links_count == 0:
        print("✅ 完美！知识库非常健康，所有双向链接均闭环！")
    else:
        print(f"\n❌ 扫描完毕：共发现 {dead_links_count} 个死链！")
        print("提示: 可以在 Obsidian 中手动创建这些缺失的页面，或者下次让 AI 补充。")

# 测试区
if __name__ == "__main__":
    check_dead_links("../wiki")