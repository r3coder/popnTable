
import numpy as np

# Class for store element
class SongDataElem:
    def __init__(self, series, level, genre, title, diffJP, diffKR, image, labelKR, isHJudge, isHGauge, score, medal, rank, popc):
        self.series = series
        self.level = level
        self.genre = genre
        self.title = title
        self.diffJP = diffJP
        self.diffKR = diffKR
        self.image = image
        self.labelKR = labelKR
        self.isHJudge = isHJudge
        self.isHGauge = isHGauge
        self.score = score
        self.medal = medal
        self.rank = rank
        self.popclass = popc
        self.is_filtered = False
    
    def IsUpper(self):
        if "(UPPER)" in self.genre:
            return True
        return False
    def __str__(self):
        return f"{self.series} {self.level} {self.genre} {self.title} {self.diffJP} {self.diffKR} {self.image} {self.labelKR} {self.isHJudge} {self.isHGauge} {self.score} {self.medal} {self.rank} {self.popclass}"


def GetPopClass(score, medal, level):
    clearbonus = 0
    if medal in [1, 2, 3, 4]:
        clearbonus = 5000
    elif medal in [5, 6, 7, 8]:
        clearbonus = 3000
    popc = (10000*level+score-50000+clearbonus)/5440
    # round from second decimal point
    return int(popc*100+0.5)/100

def GetDiffText(genre):
    x = "" if "(UPPER)" not in genre else "[UPPER]"
    if "(EX)" in genre:
        return x
    elif "(H)" in genre:
        return x+"ⓗ"
    elif "(N)" in genre:
        return x+"ⓝ"
    else:
        return x+""

def CompareTitle(a, b):
    rep = {"“":'"', "”":'"', "　":" ", "…":"...", "＠":"@", "～":"~", "(EX)":"", "〜":"~",
        "Ａ":"A", "Ｂ":"B", "Ｃ":"C", "Ｄ":"D", "Ｅ":"E", "Ｆ":"F", "Ｇ":"G", "Ｈ":"H", "Ｉ":"I", "Ｊ":"J", "Ｋ":"K", "Ｌ":"L", "Ｍ":"M", "Ｎ":"N", "Ｏ":"O", "Ｐ":"P", "Ｑ":"Q", "Ｒ":"R", "Ｓ":"S", "Ｔ":"T", "Ｕ":"U", "Ｖ":"V", "Ｗ":"W", "Ｘ":"X", "Ｙ":"Y", "Ｚ":"Z", "ａ":"a", "ｂ":"b", "ｃ":"c", "ｄ":"d", "ｅ":"e", "ｆ":"f", "ｇ":"g", "ｈ":"h", "ｉ":"i", "ｊ":"j", "ｋ":"k", "ｌ":"l", "ｍ":"m", "ｎ":"n", "ｏ":"o", "ｐ":"p", "ｑ":"q", "ｒ":"r", "ｓ":"s", "ｔ":"t", "ｕ":"u", "ｖ":"v", "ｗ":"w", "ｘ":"x", "ｙ":"y", "ｚ":"z", "０":"0", "１":"1", "２":"2", "３":"3", "４":"4", "５":"5", "６":"6", "７":"7", "８":"8", "９":"9", "＠":"@", "＃":"#", "＄":"$", "％":"%", "＾":"^", "＆":"&", "＊":"*", "（":"(", "）":")", "＿":"_", "＋":"+", "－":"-", "＝":"=", "｛":"{", "｝":"}", "｜":"|", "［":"[", "］":"]", "：":":", "；":";", "＂":'"', "’":"'", "，":",", "．":".", "／":"/", "＜":"<", "＞":">", "？":"?", "！":"!", " ":""}

    for k, v in rep.items():
        a = a.replace(k, v)
        b = b.replace(k, v)
    if a.lower() == b.lower():
        return True


def GetRankColor(rank):
    if rank == 1: # Gold BGR
        return (0, 215, 255, 255)
    elif rank == 2: # Light Red BGR
        return (140, 70, 255, 255)
    elif rank == 3:
        return (110, 40, 220, 255)
    elif rank == 4:
        return (70, 20, 190, 255)
    else: # Green ~ Black
        return (200 - (rank-5)*30, 0, 0, 255)

def GetSizeText(text, size, max_width):
    sz = 0
    for i in text:
        sz += 1 if ord(i) < 128 else 2
    if sz <= max_width:
        return size
    else:
        return int(size * max_width / sz)

def GetAbsIndex(text, ind):
    sz = 0
    for i in range(len(text)):
        sz += 1 if ord(text[i]) < 128 else 2
        if sz >= ind:
            return i

def MergeImageAlpha(img1, img2):
    a_b = img1[:,:,3] / 255.0
    a_f = img2[:,:,3] / 255.0
    for color in range(0, 3):
        img1[:,:,color] = img1[:,:,color] * a_b * (1.0 - a_f) + img2[:,:,color] * a_f
    return img1
