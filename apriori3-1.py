# -*- coding: utf-8 -*-

from numpy import *


def getDataSet(args): 
    f = open(args,'r')  
    source = f.readlines()  
    f.close()  
    dataSet = []  
    for line in source:  
        temp1 = line.strip('\n')  #获得各行数据
        temp2 = temp1.split('\t')  #将行数据（字符串）转换成列表
        dataSet.append(temp2)     #dataset是由上述列表构成的列表
    return dataSet


def createC1(dataSet):
    C1 = []
    for transaction in dataSet:
        for item in transaction:
            if not [item] in C1:
                C1.append([item]) 

    C1.sort()
    
    return list(map(frozenset, C1))
	

def scanD(D,Ck,minSupport):

    ssCnt={}
    for tid in D:
        for can in Ck:
            if can.issubset(tid):
                #if not ssCnt.has_key(can): 
                if not can in ssCnt:
                    ssCnt[can]=1 
                else: ssCnt[can]+=1
    numItems=float(len(D))
    retList = []
    supportData = {}
    for key in ssCnt:
        support = ssCnt[key]/numItems
        if support >= minSupport:
            retList.insert(0,key)
        supportData[key] = support
    return retList, supportData


def aprioriGen(Lk, k): 
    
    retList = []
    lenLk = len(Lk)
    for i in range(lenLk):
        for j in range(i+1, lenLk): 
            L1 = list(Lk[i])[:k-2]; L2 = list(Lk[j])[:k-2]
            L1.sort(); L2.sort()
            if L1==L2: 
                retList.append(Lk[i] | Lk[j]) 
    return retList


def apriori(dataSet, minSupport = 0.5):
    C1 = createC1(dataSet)
    D = list(map(set, dataSet)) 
    L1, supportData = scanD(D, C1, minSupport)
    L = [L1]
    k = 2
    while (len(L[k-2]) > 0):
        Ck = aprioriGen(L[k-2], k)
        Lk, supK = scanD(D, Ck, minSupport)
        supportData.update(supK)
        L.append(Lk)
        k += 1
    return L, supportData
	
#生成关联规则
def generateRules(L, supportData, minConf=0.7):    
    bigRuleList = []
    for i in range(1, len(L)):  
        for freqSet in L[i]:
            H1 = [frozenset([item]) for item in freqSet]            
            if (i > 1):
                rulesFromConseq(freqSet, H1, supportData, bigRuleList, minConf)
            else:
                calcConf(freqSet, H1, supportData, bigRuleList, minConf)
    return bigRuleList


def calcConf(freqSet, H, supportData, brl, minConf=0.7):
    prunedH = []
    for conseq in H:
        conf = supportData[freqSet]/supportData[freqSet-conseq]
        if conf >= minConf and ('1') in conseq:
            print (freqSet-conseq,'-->',conseq,'conf:',conf)
            brl.append((freqSet-conseq, conseq, conf))
            prunedH.append(conseq)
        if conf >= minConf and ('-1') in conseq:
            print (freqSet-conseq,'-->',conseq,'conf:',conf)
            brl.append((freqSet-conseq, conseq, conf))
            prunedH.append(conseq) 
    return prunedH


def rulesFromConseq(freqSet, H, supportData, brl, minConf=0.7):
    
    m = len(H[0])
    if m == 1:
        calcConf(freqSet, H, supportData, brl, minConf)
        Hmp1 = aprioriGen(H, m+1)
        Hmp1 = calcConf(freqSet, Hmp1, supportData, brl, minConf)
    elif (len(freqSet) > (m + 1)): 
        Hmp1 = aprioriGen(H, m+1)
        Hmp1 = calcConf(freqSet, Hmp1, supportData, brl, minConf)
        if (len(Hmp1) > 1):    
            rulesFromConseq(freqSet, Hmp1, supportData, brl, minConf)

if __name__=='__main__':
    dataSet = getDataSet('test2.txt')
    L,suppData = apriori(dataSet,minSupport = 0.1)#这里设置最小支持度         
    rule = generateRules(L,suppData,minConf = 0.2)#这里设置最小置信度
