# -*- coding: utf-8 -*-
# @Time    : 19/12/2017 9:54 AM
# @Author  : 伊甸一点
# @FileName: clusters.py
# @Software: PyCharm
# @Blog    : http://zpfbuaa.github.io

from math import pow
def readfile(file_name):
    lines = [line for line in file(file_name)]
    colnames = lines[0].strip().split('\t')[1:]
    rownames = []
    data = []
    for line in lines[1:]:
        p = line.strip().split('\t')
        rownames.append(p[0]) # First column in each row is the rowname
        data.append([float(x) for x in p[1:]]) # The data for this row is the remainder of the row
    return rownames, colnames, data

def pearson(v1, v2):
    sum1 = sum(v1)
    sum2 = sum(v2)
    sum1Pow = sum([pow(x,2) for x in v1])
    sum2Pow = sum([pow(x,2) for x in v2])

    pSum = sum([v1[i] * v2[i] for i in range(len(v1))])

    num = pSum - sum1*sum2/len(v1)
    den = (sum1Pow - pow(sum1,2)/len(v1)) * (sum2Pow - pow(sum2,2)/len(v1))
    if den == 0:
        return 0

    return 1.0 - num/den # the closer to 1, the more similar between v1 and v2


class bicluster:
    def __init__(self,vec,left=None,right=None,distance=0.0,id=None):
        self.left = left
        self.right = right
        self.vec = vec
        self.id = id
        self.distance = distance

def hcluster(rows, distance=pearson):
    distances = {}
    currentclustid = -1
    clust = [bicluster(rows[i],id=i) for i in range(len(rows))]
    while len(clust)>1:
        lowestpair=(0,1)
        clostest = distance(clust[0].vec,clust[1].vec)

        for i in range(len(clust)):
            for j in range(i+1,len(clust)):
                if (clust[i].id, clust[j].id) not in distances:
                    distances[(clust[i].id,clust[j].id)] = distance(clust[i].vec,clust[j].vec)

                d = distances[(clust[i].id,clust[j].id)]
                if d < clostest:
                    clostest = d
                    lowestpair=(i,j)

        mergevec = [ (clust[lowestpair[0]].vec[i] + clust[lowestpair[1]].vec[i])/2.0
                     for i in range(len(clust[0].vec))]
        newcluster = bicluster(mergevec,left = clust[lowestpair[0]], right = clust[lowestpair[1]],distance=clostest,id=currentclustid)
        currentclustid -=1
        del clust[lowestpair[1]]
        del clust[lowestpair[0]]
        clust.append(newcluster)
    return clust[0]

def printclust(clust, labels = None,n=0,save_path = 'data/cluster_result.txt', save_flag = 1):

    fw = open(save_path,'a')
    for i in range(n):
        print ' ',
        if save_flag == 1:
            fw.write(' ')
    if clust.id < 0:
        print '-'
        if save_flag == 1:
            fw.write('-'+'\n')
    else:
        if labels==None:
            print clust.id
            fw.write(str(clust.id)+'\n')
        else:
            print labels[clust.id]
            fw.write(labels[clust.id]+'\n')
    fw.close()
    if clust.left != None:
        printclust(clust.left,labels=labels,n=n+1)
    if clust.right != None:
        printclust(clust.right, labels=labels,n=n+1)


blognames, words, data = readfile('data/blogdata.txt')

clust = hcluster(data)

printclust(clust,labels=blognames,save_flag=1)