from fetch import *
from frame import capture
import subprocess
URLS={
28:'https://arxiv.org/pdf/2510.16786',
55:'https://users.encs.concordia.ca/~pcr/paper/Sofia_Change_Safety_Ratio.pdf',
64:'https://www.se.cs.uni-saarland.de/publications/docs/WSD%2B.pdf',
65:'https://arxiv.org/pdf/2509.14483',
72:'https://arxiv.org/pdf/2508.12285',
93:'https://sws.informatik.uni-leipzig.de/wp-content/uploads/2026/07/Productivity_of_Software_Developers_with_AI_tools_LitRev.pdf',
100:'https://arxiv.org/pdf/2605.23008',
127:'https://arxiv.org/pdf/2607.24601'}

def download(item):
    i,url=item; name=f'H{i:03}'; dest=BASE/'fulltexts'/(name+'.pdf'); dest.parent.mkdir(exist_ok=True)
    data=capture(url,dest); assert data.startswith(b'%PDF'),(i,url)
    subprocess.run(['pdftotext','-layout',str(dest),str(dest.with_suffix('.txt'))],check=True)
    return dict(id=name,url=url,path=dest.relative_to(BASE).as_posix(),sha256=sha256(data).hexdigest())
if __name__=='__main__':
    with ThreadPoolExecutor(7) as pool:result=list(pool.map(download,URLS.items()))
    tsv(BASE/'fulltext-sources.tsv',result)
