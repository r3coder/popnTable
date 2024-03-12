
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
    print(f"Not found: genre='{genre}', title='{title}', difficulty={lvl}, isUpper={isUpper}")
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

IGNORESONGS = ["virkatoの主題によるperson09風超絶技巧変奏曲", "ma plume", "Popperz Chronicle"]

class SongDataU:
    def __init__(self, genre, songName, origVer, upperVer):
        self.genre = genre
        self.songName = songName
        self.origVer = origVer
        self.upperVer = upperVer

def _GetUserData(tomoID):
    # Parsing Userdata
    import json
    with open(f'userdata/{tomoID}.json', encoding='utf-8') as result:
        result = result.read()
        userdata = json.loads(result, strict=False)
    print("Userdata parsed, length:", len(userdata["playdataInputDtos"]))


    ## UPPER fix (temporary)
    dataU = []
    # UpperDB
    with open(f'leveldata/UPPER.tsv', encoding='utf-8') as f:
        level = f.read()
        isFirst = True
        for line in level.split('\n'):
            if isFirst:
                isFirst = False
                continue
            if line == "":
                continue
            data = line.split('\t')
            s = SongDataU(data[0], data[1], 0, int(data[2]))
            dataU.append(s)
        
    song_set = []
    fixcount = 0
    for data in userdata["playdataInputDtos"]:
        if data["songName"] in IGNORESONGS:
            continue
        for sn in dataU:
            if CompareTitle(sn.songName, data["songName"]):
                if data["version"] == sn.upperVer:
                    data["isUpper"] = True
                    fixcount += 1
                    break

    print("Upper chart data fixed:", fixcount)
    return userdata
