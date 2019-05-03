import MeCab
import copy
import itertools

def wakati(text):
    t = MeCab.Tagger("-Owakati");
    m = t.parse(text);
    return m.rstrip().split(" ");

#英語だけの全文と日本語だけの全文をそれぞれでリスト化する
def jatoen(filename):
    src=open(filename, "r", encoding="utf-8_sig");
    line=src.readline();#最初の一行読み込む
    i=0;#ファイルの今から読み込む行番号
    wordlist_j=wakati(line)
    i=i+1;
    wordlist_e=['NULL']#英単語リスト初期化

    while line:
        if(i%2==0):#日本語のリスト化
            line=src.readline();
            wordlist_j.extend(wakati(line));
            i=i+1;
        else:#英語のリスト化
            line=src.readline();
            wordlist_e.extend(line.rstrip().split(" "));
            i=i+1;
    wordlist_j.pop();
    src.close();
    return  list(set(wordlist_j)), list(set(wordlist_e));
def makejaen_3(wordlist_j, wordlist_e):
    dic_p={}
    len_j=len(wordlist_j);
    for i in wordlist_j:
        dic_p[i]={};
        for j in wordlist_e:
            dic_p[i][j]=1/len_j;
    return dic_p;

#リストの中身を表示する
def print_str(max_gram, input_data):
    str="";
    for i in max_gram:
        str+=i+" ";
    print("原文："+input_data);
    print("目標文："+str);

#辞書型一個一個にアクセス
filename="内山コーパス.txt"
src=open(filename, "r", encoding="utf-8_sig")
dic={}#日本語単語と英単語の対応辞書型
i=0#カウント変数
#ファイルを一行ずつ読み込む
line=src.readline()
wordlist=wakati(line)#一行目は、日本文なので、分かち書き
wordlist_p=[]#日本語と重みを要素としたリスト型
for k in range(len(wordlist)):#最初の日本語リストに単語と重みを初期化
    wordlist_p.append([wordlist[k], 0.0]);
i=i+1
key=1#辞書型のキー初期化
#英単語と日本語対応の辞書型作成(初期化)重みは0.0で初期化
while line:
    if(i%2 == 0):#偶数のとき、その行は日本文
        line=src.readline();
        wordlist=wakati(line);
        wordlist_p=[]#wordlist_p初期化
        for k in range(len(wordlist)):
            wordlist_p.append([wordlist[k], 0.0]);
        i=i+1;
    else:#奇数のとき、その行は英文
        line=src.readline();
        list_english=['NULL']#英単語のリスト型最初の要素はNULLとする
        list_english.extend(line.rstrip().split(" "));
        dic[key]={};#キーの要素を辞書型で初期化
        for j in range(len(list_english)):
                if(key==0):
                    print(id(wordlist_p[0]));
                dic[key][list_english[j]]=copy.deepcopy(wordlist_p);#wordlist_pを直接代入すると、同じIDが入るため、copyを用いる。
        i=i+1;
        key=key+1;
wordlist_j, wordlist_e=jatoen(filename)
dic_p={}
#dic_p=makejaen(wordlist_j, wordlist_e)
dic_p=makejaen_3(wordlist_j, wordlist_e)
#ibm-model1実装
#print(dic_p);

kkkk=0;

#ibm-model1実装
for i in range(0, 5, +1):
    for j in dic:
        for k in dic[j]:#j番目の英単語kの重み設定
            for l in dic[j][k]:#j番目の英単語kのリストの要素にアクセス要素lの0番目は日本語単語 1番目は重み
                deno=0;#分母
                bunshi=0;#分子
                japa=l[0];
                bunshi=dic_p[japa][k];
                for m in dic_p[japa]:
                    if(m in dic[j]):
                        deno+=dic_p[japa][m];
                l[1]=bunshi/deno;
    for i in dic_p:
        for j in dic_p[i]:
            deno=0;
            bunshi=0;
            japa=i;
            for k in dic:#dicのキーは0,1,2,....
                if(j in dic[k]):
                    for l in dic[k][j]:
                        deno+=l[1];
                        if(l[0]==japa):
                            bunshi+=l[1];
            dic_p[i][j]=bunshi/deno;
    kkkk=kkkk+1
    print(kkkk)
    print(" -----")
    for i in dic_p:
        print(i)
        for j in dic_p[i]:
            print(j)
            print(dic_p[i][j])
    print(dic_p);
    print("------")
#print(dic_p)

#n-gram実装

#ngram初期化
ngram={}

filename="内山_test.txt"
#filename="英語コーパス_test_s.txt"
src=open(filename, "r", encoding="utf-8_sig")

#ファイルを一行読み込む
line=src.readline()
line_e=line.rstrip()

#英語コーパスのすべてに対して、ngram

while line:
    line=src.readline();
    line_e+=" "+line.rstrip();

wordlist=line_e.rstrip().split(" ");
#辞書型ngramにwordlistの要素をどんどん追加
#2-gram実装
#2-gramの表作り<s>:文頭 </s>:文末
for i in range(len(wordlist)):
    if(not(wordlist[i] in ngram)):
        ngram[wordlist[i]]={};
    if(wordlist[i] == "</s>"):
        ngram[wordlist[i]]={"NULL" : -1};
    else:
        for j in range(i+1, len(wordlist), +1):
            #任意の文字の後の<s>は0
            if(wordlist[j] == "<s>"):
                break;
            #iのキーの中にjという単語存在しないとき登録
            elif((i+1==j) and not(wordlist[j] in ngram[wordlist[i]]) ):
                ngram[wordlist[i]][wordlist[j]]=1;
            elif(i+1==j):
                ngram[wordlist[i]][wordlist[j]]+=1;
            elif(not(wordlist[j] in ngram[wordlist[i]])):
                ngram[wordlist[i]][wordlist[j]]=0;

wordlist_num=list(set(wordlist));
print("よう");
print(wordlist_num);
wordlist_num.remove("<s>");
wordlist_num.remove("</s>");
print(wordlist_num);
#英単語の異なり語数
len_english=len(wordlist_num)

#加算スムージング
for i in ngram:
    for j in wordlist_num:
        if(not(j in ngram[i])):
           ngram[i][j]=0;
print(ngram)

alpha=0.1;


#2gramの確率実装
ngram_p={}
for i in ngram:
    ngram_p[i]={}
    count_self=0;
    for j in ngram[i]:
        count_self+=ngram[i][j];
    for k in ngram[i]:
        ngram_p[i][k]=(ngram[i][k]+alpha)/(alpha*len_english+count_self);

print("加算スムージング後の")
print(ngram_p);

#print(dic_p);

#for i in dic_p:
#    print(i+",",max([(v, k) for k, v in dic_p[i].items()])[1]);

input_data=""
input_data=input(">>");
input_list=wakati(input_data);

#input_listの要素をそれぞれ対応する英単語に変換
for i in range(len(input_list)):
    input_list[i]=max([(v, k) for k, v in dic_p[input_list[i]].items()])[1];
for i in input_list:
    if(i=='NULL'):
        input_list.remove('NULL');

wordlist_english=copy.copy(input_list);
print(wordlist_english);
wordlist_list=[]
for i in itertools.permutations(wordlist_english):
    wordlist_list.append(list(i));
print(wordlist_list)
for i in wordlist_list:
    i.insert(0, '<s>');
    i.append('</s>');
print(wordlist_list)
input_list.insert(0, '<s>');
input_list.append('</s>');
gram=copy.copy(input_list);
#<s>に続く確率の高い単語を求める
#ngramによる確率最大となる文生成
max_p=0;
max_p_temp=1;
max_gram=[];
for gram in wordlist_list:
    max_p_temp=1;
    for i in range(0, len(gram)-1, +1):
        max_p_temp*=ngram_p[gram[i]][gram[i+1]];
    if(max_p < max_p_temp):
        max_p = max_p_temp;
        max_gram = copy.copy(gram);
print(max_gram);
max_gram.remove("<s>");
max_gram.remove("</s>");

#リストの中身を表示する
print_str(max_gram, input_data);