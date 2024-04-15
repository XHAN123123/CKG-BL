#对缺陷报告进行批量命名实体识别
# Import generic wrappers
from transformers import AutoModel, AutoTokenizer,AutoModelForTokenClassification
from transformers import pipeline
import xml.dom.minidom
import xml.etree.ElementTree
import csv
import numpy as np

#方法定义将xmlfile中的缺陷报告读入csv
def writeTocsv(xmlfile,file):
    Dom = xml.dom.minidom.parse(xmlfile)
    root = Dom.documentElement
    BugIdList = root.getElementsByTagName('bug')
    SummaryList = root.getElementsByTagName('summary')
    DescrptionList = root.getElementsByTagName('description')
    with open(file, 'w', encoding='utf-8', newline='') as writer1:
        writer = csv.writer(writer1)
        writer.writerow(['BugId', 'Summary', 'Description', 'bugReportNER'])
        for i in range(len(BugIdList)):
            BugId = BugIdList[i].getAttribute('id')
            Summary = SummaryList[i].firstChild.data
            Description = DescrptionList[i].firstChild.data
            writer.writerow([BugId, Summary, Description])
        writer1.close()

#对csv进行实体标注，获得标注后的实体
def softner(file, fileNER):
    with open(file, 'rt', encoding='utf-8') as f:
        reader = csv.reader(f)
        sumdes = [row[1] + row[2] for row in reader]
        print(len(sumdes))
    # nerword = np.ones((len(sumdes),1),dtype=str)
    word1 = []
    nerword = ""
    with open(fileNER, 'a', newline='', encoding='utf-8') as writer2:
        writefile = csv.writer(writer2)
        for i in range(0, len(sumdes)-1):
            example = sumdes[i]
            # print(example)
            ner_results_before = SoftNER(example)
        # print(ner_results_before)
        # print(len(ner_results_before))
        # print(len(ner_results_before)-1)
            for k in range(0, len(ner_results_before)-1):
                ner_results_before[k]['word'] = ner_results_before[k]['word'].replace("Ġ", " ").replace("Ċ", "\n")
                nerword = nerword + ner_results_before[k]['word']
            nerword = nerword + "作为分隔符"+"\n"
    with open('F:/KGBL/BugReport/BugReport/ZXingBR/nerword.txt',"w",encoding="UTF-8") as f:
        f.write(nerword)

# Define the model repo
# Download pytorch model加载Pytorch模型
model_name = "mrm8488/codebert-base-finetuned-stackoverflow-ner"
model = AutoModelForTokenClassification.from_pretrained("mrm8488/codebert-base-finetuned-stackoverflow-ner")
tokenizer = AutoTokenizer.from_pretrained(model_name, add_prefix_space=False)
SoftNER = pipeline(task="ner", model=model, tokenizer=tokenizer)
# 读取xml对象（缺陷报告）
writeTocsv('F:/KGBL/BugReport/BugReport/ZXingBR/ZXingBugRepository.xml','F:/KGBL/BugReport/BugReport/ZXingBR/BugReportNER.csv')
# 对缺陷报告进行命名实体识别 获得标注后的词汇
softner('F:/KGBL/BugReport/BugReport/ZXingBR/BugReportNER.csv','F:/KGBL/BugReport/BugReport/ZXingBR/NERword.csv')



# F:/KGBL/BugReport/BugReport/AspectJBR/BugreportNER.csv
# 'F:/KGBL/BugReport/BugReport/AspectJBR/AspectJBugRepository.xml'

