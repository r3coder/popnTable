
from util import CompareTitle
import json

def FindSongData(genre, title, userdata):
    isUpper = 0
    if "(UPPER)" in genre:
        isUpper = 1
        genre = genre.replace("(UPPER)", "")
    lvl = 0
    if "(EX)" in genre:
        lvl = 3
        genre = genre.replace("(EX)", "")
    elif "(H)" in genre:
        lvl = 2
        genre = genre.replace("(H)", "")
    elif "(N)" in genre:
        lvl = 1
        genre = genre.replace("(N)", "")
    for e in userdata["scores"]:
        if CompareTitle(e[2],title) and e[5] == isUpper: # Only name matching
            if e[4][lvl][0] == -1:
                return None
            return e[4][lvl]
    # print(f"Not found: genre='{genre}', title='{title}', difficulty={lvl}, isUpper={isUpper}")
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
