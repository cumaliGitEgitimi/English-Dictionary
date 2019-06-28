from simhash import Simhash
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

class SimHash(object):

    def __init__(self):
        pass
    def getBinStr(self, source):
        if source == "":
            return 0
        else:
            x = ord(source[0]) << 7
            m = 1000003
            mask = 2 ** 128 - 1
            for c in source:
                x = ((x * m) ^ ord(c)) & mask
            x ^= len(source)
            if x == -1:
                x = -2
            x = bin(x).replace('0b', '').zfill(64)[-64:]
            return str(x)

    def getWeight(self, source):
        # fake weight with keyword
        return ord(source)
    def unwrap_weight(self, arr):
        ret = ""
        for item in arr:
            tmp = 0
            if int(item) > 0:
                tmp = 1
            ret += str(tmp)
        return ret

    def simHash(self, rawstr):
        seg = jieba.cut(rawstr)
        keywords = jieba.analyse.extract_tags("|".join(seg), topK=100, withWeight=True)
        ret = []
        for keyword, weight in keywords:
            binstr = self.getBinStr(keyword)
            keylist = []
            for c in binstr:
                weight = math.ceil(weight)
                if c == "1":
                    keylist.append(int(weight))
                else:
                    keylist.append(-int(weight))
            ret.append(keylist)
        # Reducing Dimensions of Lists
        rows = len(ret)
        cols = len(ret[0])
        result = []
        for i in range(cols):
            tmp = 0
            for j in range(rows):
                tmp += int(ret[j][i])
            if tmp > 0:
                tmp = "1"
            elif tmp <= 0:
                tmp = "0"
            result.append(tmp)
        return "".join(result)

    def getDistince(self, hashstr1, hashstr2):
        length = 0
        for index, char in enumerate(hashstr1):
            if char == hashstr2[index]:
                continue
            else:
                length += 1
        return length

def SimhashSimilarity():
    simhash = SimHash()
    s1 = u'I am very happy'
    s2 = u'I am very happu'

    hash1 = simhash.simHash(s1)
    hash2 = simhash.simHash(s2)
    distince = simhash.getDistince(hash1, hash2)
    value = 5
    Print ("Heming Distance:", "distince," "Judgment Distance:", "Value," "Similarity:", "distince<=value")


def tokenize(sequence):
    words = word_tokenize(sequence)
    filtered_words = [word for word in words if word not in stopwords.words('english')]
    return filtered_words

q1 = "How can I be a good geologist?"
q2 = "What should I do to be a great geologist?"
print('Tokenize simhash:', Simhash(tokenize(q1)).distance(Simhash(tokenize(q2))))