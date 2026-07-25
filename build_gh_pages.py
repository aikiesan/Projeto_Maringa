import os
import shutil

def build_github_pages():
    base_dir = os.path.dirname(__file__)
    docs_dir = os.path.join(base_dir, 'docs')
    static_dir = os.path.join(base_dir, 'static')

    if os.path.exists(docs_dir):
        shutil.rmtree(docs_dir)

    shutil.copytree(static_dir, docs_dir)
    print("Diretório /docs/ gerado com sucesso para deploy no GitHub Pages!")

if __name__ == '__main__':
    build_github_pages()
