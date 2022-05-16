import nltk
#nltk.download('punkt')
#nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize
import os
import math
import pandas as pd


class irSystem:
    path = r"D:\ir\Book\DocumentCollection"
    collctionPath = []  # Here we store documents paths as indexes in a list
    collectionInfo = []  # Here we stor documents data as string indexes
    docs = dict()  # Here we make dictionary
    collect = []
    # similartyquery=[]
    # takequery=[]
    docId = []  # Here we store docs id
    possetional = {}  # possetional index dictionary
    stopwords = set(stopwords.words('english'))
    marks = ['.', ',', '?', ';', ':', '<', '>', '&', '&&', '| ', '||', '/', '\\', '{', '}', '[', ']', '(', ')', '!',
             '~', '|', '_', '-', '+', '*']

    def __init__(self):  # initialization constructor
        '''self.collctionPath.append(open("D:\Disktop\FCAL_Books\level 3\IR\project\Documentcollection\\1.txt","r"))
        self.collctionPath.append(open("D:\Disktop\FCAL_Books\level 3\IR\project\Documentcollection\\2.txt", "r"))
        self.collctionPath.append(open("D:\Disktop\FCAL_Books\level 3\IR\project\Documentcollection\\3.txt", "r"))
        self.collctionPath.append(open("D:\Disktop\FCAL_Books\level 3\IR\project\Documentcollection\\4.txt", "r"))
        self.collctionPath.append(open("D:\Disktop\FCAL_Books\level 3\IR\project\Documentcollection\\5.txt", "r"))
        self.collctionPath.append(open("D:\Disktop\FCAL_Books\level 3\IR\project\Documentcollection\\6.txt", "r"))
        self.collctionPath.append(open("D:\Disktop\FCAL_Books\level 3\IR\project\Documentcollection\\7.txt", "r"))
        self.collctionPath.append(open("D:\Disktop\FCAL_Books\level 3\IR\project\Documentcollection\\8.txt", "r"))
        self.collctionPath.append(open("D:\Disktop\FCAL_Books\level 3\IR\project\Documentcollection\\9.txt", "r"))
        self.collctionPath.append(open("D:\Disktop\FCAL_Books\level 3\IR\project\Documentcollection\\10.txt", "r"))
        #self.Read()#This Function reading data from collectionPaths and storing it at collectionInfo'''
        self.readdoc()
        self.tokinization(self.collectionInfo)  # This function tokenizing docs and printing the token's word in a list
        self.stop_word()  # This function clear list from stopwords : (a,the,the who ,etc)
        self.phase2()  # Just for design
        self.BuildPositionalIndex()
        self.printPossetional()
        self.get_query()
        self.phase3()
        matrex = self.tfIdfMatrex(self.tf_and_idf())
        self.sem(matrex)

    print("--" * 10)
    print("    phase 1 :")
    print("--" * 10)

    # samir amin
    def readdoc(self):
        os.chdir(self.path)  # choose direction
        x = []  # temp list to append file no. 10
        for file in os.listdir():
            if file.endswith('0.txt'):  # this condition before others becuase function don't read ten's numbers
                file_path = f"{self.path}/{file}"
                with open(file_path, "r") as file:
                    x.append(file.read())  # append file no. 10 in x
            elif file.endswith('.txt'):  # this condition is general for all one's files 1->9
                file_path = f"{self.path}/{file}"
                with open(file_path, "r") as file:
                    self.collectionInfo.append(file.read())  # append files in collectionInfo
        if len(x) > 0:  # here we append the 10's file withe collectionInfo
            self.collectionInfo += x
            print("")
            print(self.collectionInfo)

    def tokinization(self, collctionInfo):
        count = 1  # document number
        for i in collctionInfo:
            self.docs.update({count: self.qTokenization(
                i)})  # put number of documents as a key in dictionary and value will be dtat comes from qtokenization
            count += 1
        print("After tokinization : ")
        print("**" * 10)
        print(self.docs)
        print("__" * 30)

    def qTokenization(self,
                      document):  # This function is using word_tokinize to cut words and return every word as index in a list
        document = document.lower()
        token = word_tokenize(document)
        storeTokes = []
        for i in token:
            if i not in self.marks:
                storeTokes.append(i)
        return storeTokes

    def stop_word(self):
        tokensList = []
        for key in self.docs:
            for value in self.docs[key]:
                if value not in self.stopwords:
                    tokensList.append(value)
            self.docs[key] = tokensList
            tokensList = []
        print("After stop words : ")
        print("**" * 10)
        print(self.docs)
        print("__" * 30)

    def Qstop_word(self, q):
        tokenList = []
        for i in q:
            if i not in self.stopwords:
                tokenList.append(i)
        return tokenList

    # tarek
    def phase2(self):
        print("--" * 10)
        print("    phase 2 :")
        print("--" * 10)

    def BuildPositionalIndex(self):
        for document in self.docs:
            self.buildP(document, self.possetional)

    def buildP(self, document, possitional):
        counter = 0
        for word in self.docs[document]:  # docs[1]
            counter += 1
            if word in possitional:
                if document in possitional[word]:
                    possitional[word][document].append(counter)
                else:
                    possitional[word].update({document: [counter]})
            else:
                possitional.update({word: {document: [counter]}})

    def printPossetional(self):
        print(self.possetional)
        for i in self.possetional:
            print("<" + str(i) + ',' + str(len(self.possetional[i])) + ';')
            for j in self.possetional[i]:
                print(str(j) + ":" + str(self.possetional[i][j]) + ';')
            print('>')

    # magdy
    def get_query(self):
            query = input("Enter Query : ") #get query from user
            query = self.qTokenization(query) # apply query tokenization function
            query = self.Qstop_word(query)    # apply query stopword function
            self.search(query)       # send query after processing as parameter to search

    def search(self, query):
        print(query)
        if len(query) == 1: #if user enter one word
            if query[0] in self.possetional: #hold that word and searching for it in possetional
                print("Matches with documents : {}".format(self.possetional[query[0]].keys())) #if word is founded
            else:
                print("not match0")
        elif len(query) == 0: #if user enter no query
            print("there is no query entered")
        else: #if user enter more than one word
            res = []
            for i in range(len(query)): #looping for each word and search untile length = number of words
                if i + 1 == len(query):  # دا معناه انه عدى على الكويرى كله ف يقف
                    break # if second word == length of query stop loop
                else:
                    print("turn {} qi {} qi+1 {}".format(i, query[i], query[i + 1])) # print the iterats with query
                    x = self.compare(query[i], query[i + 1])  # x will be false or value
                    print("i {} x {}".format(i, x))
                    if x:                                  #if x != false
                        res = res + x                      # put x in result
            # 1,2,3  &&  1,2,4,7 && 1,2,5,8=1,2

            res2 = []
            for i in res:
                if res.count(i) == len(query) - 1: # if number of document exist len query-1 that mens the query match with document
                    if i not in res2: # to not make doblecates like result []
                        res2.append(i)  # if i is not in res2
            if len(res2) == 0:
                print("not match5")   # after comparing all words in query and not matching
            else:
                print("res {}:::res2 {}".format(res, res2)) # if matching

    def compare(self, i1, i2):
        if i1 not in self.possetional or i2 not in self.possetional:
            return False
        else:
            matchDoc = []
            for d in self.possetional[i1]: # hold keys of word then comparing with the next key
                if d not in self.possetional[i2]:
                    continue
                else:
                    if self.compareList(self.possetional[i1][d], self.possetional[i2][d]):
                        matchDoc.append(d)
            return matchDoc

    def compareList(self, l1, l2):
        for i in l1:
            if i + 1 in l2:
                return True
        return False

    # samir mohamed ahmed
    def phase3(self):
        print("--" * 10)
        print("    phase 3 :")
        print("--" * 10)

    def tf_and_idf(self):  # tf valew and idf value
        t = self.possetional  # new temp dictionary
        print("t=:  {}".format(t))
        for i in self.docs:  # Here this loop print all documents number in docId
            self.docId.append(i)
        for i in t:
            for j in t[i]:
                t[i][j] = len(t[i][j])
        for i in t:
            t[i].update({-1: float(
                format(math.log10((len(self.docId)) / (len(t[i]))), ".3f"))})  # computes TF & IDF for each term
            for j in self.docId:
                if j not in t[i]:  # check if the term is not in dictionary
                    t[i].update({j: 0})

            t[i] = dict(sorted(t[i].items()))
        print("IDF & TF for each term is (-1=idf):")
        print("**" * 10)
        print("idf &tf values: \n{}".format(
            pd.DataFrame.from_dict(t, orient='index', columns=([-1, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]))))
        return t

    def tfIdfMatrex(self, t):  # tf.idf value (tf weight)
        matrex = {}
        for i in t:
            matrex.update({i: []})
            idf = 0
            for j in t[i]:
                if j == -1:
                    idf = t[i][j]
                    continue
                matrex[i].append(float(format((math.log10(1 + t[i][j])) * idf, ".3f")))
        self.print(matrex)
        return matrex

    import pandas as pd
    def print(self, matrex):
        print("-" * 80)
        print("TF.IDF Matrex\n")
        df = pd.DataFrame.from_dict(matrex, orient='index', columns=[self.docId])
        print(df)
        print("-" * 80)
        # print("         {}".format(*self.docId))
        '''for i in matrex:
            print("{}  {}".format(i,matrex[i]))'''

    # Hussein
    def sem(self, matrex):  # دى زى المين كدا هى الى بتنادى الباقى

        takeQuery = input("enter query : ")
        takeQuery = self.qTokenization(takeQuery)  # تةكينايزيشن للكويرى
        takeQuery = self.Qstop_word(takeQuery)  # شيل الاستوب ورد من الكويرى
        print("\nMatrex befor norm befor add q")
        print(matrex)
        print("---" * 20)
        matrex = self.getQNorm(takeQuery, matrex)  # بتاخد الكويرى تحسبله الtf.idf وتحطه ف اخر الليست بتاعت الماتريكس
        print("Entered Query is : ")
        print(takeQuery)
        matrex = self.getNorm(matrex)  # اعمل نورماليزيشن للماتريكس بعد ما حطيت الكويرى
        rank = self.getRank(matrex)  # الترتيب حسب السيميلاريتى
        flag =0
        for i in rank:  # بتطبع الدوكيومنات الى ظاهر فيهم الكويرى بس بالترتيب
            if rank[i] != 0:
                if flag==0:
                    print("Best Ranked :{}".format(i))
                    flag=1
                    continue
                print(i)

    def getNorm(self, matrex):
        l = []
        print("\nMatrex befor norm after add q")
        print(matrex)
        for i in range(len(self.docId) + 1):
            sum = 0
            for j in matrex:
                sum += float(matrex[j][i]) ** 2  # get sum of word wieght & make it of power 2
            l.append(math.sqrt(sum))  # append squre root for sum in list
        for i in matrex:
            for j in range(len(matrex[i])):
                if l[j] == 0:
                    matrex[i][j] = 0
                else:
                    matrex[i][j] = float(format(matrex[i][j] / l[j], ".3f"))
        print("lenghth every doc: {}".format(l))
        print("\nMatrex after norm")
        print(matrex)
        '''for i in matrex:
            print("{}:{}".format(i, matrex[i]))
        print("finish")'''
        print(pd.DataFrame.from_dict(matrex, orient='index', columns=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, -1]))
        return matrex

    def getQNorm(self, query, matrex):
        qTfIdf = {}  # ديكشينارى هيكون جواه كل كلمه فالكويرى وقدامها ليست فيها الtfوالidf
        '''
            qTfIdf={
            "word1":[tf,idf]
            "word2":[tf,idf]
            }

        '''
        for i in query:  # بيجيب ال tfويحطها فالدكشنارى
            qTfIdf.update({i: [query.count(i)]})  # عدد تكرار الكلمه فالكويرى
        for i in range(len(query)):
            if query[i] not in query[:i]:  # دى عشان لو الكلمه عدى عليها قبل كدا ميحطهاش تانى
                if query[i] in matrex:
                    qTfIdf[query[i]].append(len(matrex[query[i]]) - matrex[query[i]].count(0.0))
                else:
                    qTfIdf[query[i]].append(0)
        print("query [tf,df]: {}".format(qTfIdf))
        print("###"*20)
        for i in qTfIdf:
            if qTfIdf[i][1] > 0:
                qTfIdf[i] = float(
                    format((math.log10(1 + qTfIdf[i][0])) * (math.log10((len(self.docId)) / (qTfIdf[i][1]))),
                           ".3f"))  # tf-idf=log(1+tf)*log(N/df)

        print("query wieght[tf.idf]: {}".format(qTfIdf))
        print("###"*20)
        for i in matrex:  # هنا بضيف قيم الكويرى بحيث تبقى ف اخر الليست بتاعت كل كلمه
            if i in qTfIdf:
                matrex[i].append(qTfIdf[i])
            else:
                matrex[i].append(0)
        return matrex

    def getRank(self, matrex):
        rank = {}
        for i in range(len(self.docId)):
            sum = 0
            for j in matrex:
                sum += matrex[j][i] * matrex[j][-1]
            rank.update({i + 1: float(format(sum, ".3f"))})
        print(rank)
        rank = dict(sorted(rank.items(), key=lambda x: x[1], reverse=True))
        print(rank)
        return rank


inst = irSystem()