import pandas as pd
import numpy as np
import csv
from sklearn.metrics.pairwise import cosine_similarity
brfile = "F:/KGBL/BugReport/BugReport/AspectJBR/BRW2V_edit.csv"
triplefile = "F:/KGBL/ProjectKG/triple2embed111.csv"

# 读取缺陷报告向量
brvec = []
triplevec = []

df1 = pd.read_csv(brfile)
df2 = pd.read_csv(triplefile, engine='python')
num = 0
for i in df2['1'].values:
    num += 1
    if np.isnan(i):
        print(True)
        print(num)
# 提取缺陷报告嵌入
print("命名实体识别后的缺陷报告为：")
print(df1.iloc[2]["cleaned"])
a = df1.iloc[2]["embedding"]
brvec = a.replace("\n"," ").replace("]"," ").replace("["," ").split(" ")
brvec = [i for i in brvec if i != '' and i !='[']


for j in range(len(brvec)):
    brvec[j] = eval(brvec[j])
# 记录三元组所在位置和相似度
tripleLoc = []
sim = []

# 将缺陷报告嵌入与三元组嵌入计算相似度
print("正在计算相似度……")
for k in range(0,51400):
    for h in range(6,306):
        triplevec.append(df2.iloc[k][h])
    # print(triplevec)
    cossim = cosine_similarity([brvec,triplevec])
    if abs(cossim[0][1]) > 0.15:
        # print(df2.iloc[k][1] + " " + df2.iloc[k][4] + " " + df2.iloc[k][3])
        print(k)
        tripleLoc.append(k)
        # print(abs(cossim[0][1]))
        sim.append(abs(cossim[0][1]))
    triplevec = []

# 输出相似度排序
print("相似度排序为：")
sim = np.array(sim)
simSort = np.argsort(-sim)
for j in range(0,30):
    print(df2.iloc[tripleLoc[j]][1] + " " + df2.iloc[tripleLoc[j]][4] + " " + df2.iloc[tripleLoc[j]][3])




