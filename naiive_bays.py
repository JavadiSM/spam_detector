class NAIIVE_BAYS:
    def __init__(self,table,raw=False):
        """
        table should look like:
        {
            "lable": {"spam":0.4,"ham":0.6},
            # words
            "helllo": {"spam":{True:0.4,False:0.6},"ham":{True:0.26,False:0.74}},
            ... other words
        }
        otherwise, table is raw:
        ["spam fgbgbf","ham yo bro", ...]
        """

        
        self.table = NAIIVE_BAYS.preccess_raw(table) if raw else table


    def preccess_raw(table:list[str],smooth=False):
        """
        it is very inefficent for now, I plan to enhance it in future
        lable\ttext
        each line of data set shuold be in this format
        """
        # I'll keep counts for now, in order to regularize or use laplace smoothing
        formatted = {"lable": {"spam":0,"ham":0}}
        for line in table:
            lable,text = (line.strip().lower()).split('\t')
            formatted["lable"][lable] += 1
            for word in set(text.split()):
                if not word in formatted:
                    formatted[word] = {"spam":{True:0,False:0},"ham":{True:0,False:0}}
                formatted[word][lable][True] += 1
        hams = formatted["lable"]["ham"]
        spams = formatted["lable"]["spam"]
        words = list(formatted.keys())[1:]
        for word in words:
            formatted[word]["spam"][False] = spams - formatted[word]["spam"][True]
            formatted[word]["ham"][False] = hams - formatted[word]["ham"][True]

        if smooth: # laplace smoothing
            formatted["lable"]["ham"] += 1
            formatted["lable"]["spam"] += 1
            for word in words:
                formatted[word]["spam"][False] +=1
                formatted[word]["ham"][False] +=1
                formatted[word]["spam"][True] +=1
                formatted[word]["ham"][True] +=1

        # normalize
        summ = formatted["lable"]["spam"] + formatted["lable"]["ham"]
        formatted["lable"]["ham"] /= summ
        formatted["lable"]["spam"] /= summ
        for word in words:
            summ = formatted[word]["spam"][True] + formatted[word]["spam"][False]
            formatted[word]["spam"][False] /= summ
            formatted[word]["spam"][True] /= summ
            summ = formatted[word]["ham"][True] + formatted[word]["ham"][False]
            formatted[word]["ham"][False] /= summ
            formatted[word]["ham"][True] /= summ

        return formatted
    

if __name__=="__main__":
    path = "SMSSpamCollection.txt"
    lines = []
    with open(path,"r", encoding='utf-8') as fo:
        for line in fo:
            lines.append(line.strip())
    table = NAIIVE_BAYS.preccess_raw(lines,True)
    print(table)