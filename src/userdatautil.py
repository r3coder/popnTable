
import json

def CompareTitle(a, b):
    if a.lower().replace("　"," ").replace(" ", "")== b.lower().replace("　"," ").replace(" ", ""): #Simple
        return True
    rep = {"“":'"', "”":'"', "　":" ", "…":"...", "＠":"@", "～":"~", "(EX)":"", "〜":"~",
        "Ａ":"A", "Ｂ":"B", "Ｃ":"C", "Ｄ":"D", "Ｅ":"E", "Ｆ":"F", "Ｇ":"G", "Ｈ":"H", "Ｉ":"I", "Ｊ":"J", "Ｋ":"K", "Ｌ":"L", "Ｍ":"M", "Ｎ":"N", "Ｏ":"O", "Ｐ":"P", "Ｑ":"Q", "Ｒ":"R", "Ｓ":"S", "Ｔ":"T", "Ｕ":"U", "Ｖ":"V", "Ｗ":"W", "Ｘ":"X", "Ｙ":"Y", "Ｚ":"Z", "ａ":"a", "ｂ":"b", "ｃ":"c", "ｄ":"d", "ｅ":"e", "ｆ":"f", "ｇ":"g", "ｈ":"h", "ｉ":"i", "ｊ":"j", "ｋ":"k", "ｌ":"l", "ｍ":"m", "ｎ":"n", "ｏ":"o", "ｐ":"p", "ｑ":"q", "ｒ":"r", "ｓ":"s", "ｔ":"t", "ｕ":"u", "ｖ":"v", "ｗ":"w", "ｘ":"x", "ｙ":"y", "ｚ":"z", "０":"0", "１":"1", "２":"2", "３":"3", "４":"4", "５":"5", "６":"6", "７":"7", "８":"8", "９":"9", "＠":"@", "＃":"#", "＄":"$", "％":"%", "＾":"^", "＆":"&", "＊":"*", "（":"(", "）":")", "＿":"_", "＋":"+", "－":"-", "＝":"=", "｛":"{", "｝":"}", "｜":"|", "［":"[", "］":"]", "：":":", "；":";", "＂":'"', "’":"'", "，":",", "．":".", "／":"/", "＜":"<", "＞":">", "？":"?", "！":"!", " ":""}
    for k, v in rep.items():
        a = a.replace(k, v)
        b = b.replace(k, v)
    if a.lower() == b.lower():
        return True
    return False

def FindSongData(genre, title, userdata):
    isUpper = True if "(UPPER)" in genre else False
    lvl = 0
    if "(EX)" in genre:
        lvl = 3
    elif "(H)" in genre:
        lvl = 2
    elif "(N)" in genre:
        lvl = 1
    for e in userdata["scores"]:
        if CompareTitle(e[2],title) and e[5] == isUpper: # Only name and upper matching
            if e[4][lvl][0] == -1:
                return None
            return e[4][lvl]
    return None

def GetUserData(tomoID):
    dup = []
    with open(f'userdata/{tomoID}.json', encoding='utf-8') as result:
        result = result.read()
        userdata = json.loads(result, strict=False)
    for d in userdata["scores"]:
        if d[2] in dup:
            d.append(True)
        else:
            d.append(False)
            dup.append(d[2])
    return userdata
