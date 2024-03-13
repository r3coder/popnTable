import os

# sort method ["series", "title", "score"]
# Columns [4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
# Filter by medal (e.g. 0=None, 1=Perfect, 2~4=FC, 5~7=Clear, 8=EasyClear, 9~11=Failed, 12=Noplay')
# Filter by score (e.g. 0=None, 1=Perfect, 2~4=FC, 5~7=Clear, 8=EasyClear, 9~11=Failed, 12=Noplay')
# Filter by rank (e.g. 0=None, 1=S, 2=AAA, 3=AA, 4=A, 5=B, 6=C, 7=D, 8=E, 9=F')
# filter method ['none', 'darken', 'disable']

RANK = ["err", "S", "AAA", "AA", "A", "B", "C", "D", "E", "F"]

MEDAL = ["err", "퍼펙트", "은별", "은다이아", "풀콤보", "동별", "동다이아", "클리어", "이지클리어", "흑별", "흑다이아", "흑동그라미", "미플레이"]

DIFFJP = ["弱", "中", "強", "詐"]

DIFFKR = ["보스", "최상", "상", "중상", "중", "중하", "하", "최하", "개인", "?"]

DIFFJP = ["보스\n~+1.0", "최상\n+1.0\n~+.66", "상\n+.66\n~+.33", "중상\n+.33\n~+0.0", "중\n-0.0\n~-.33", "중하\n-.33\n~-.66", "하\n-.66\n~-1.0", "최하\n-1.0~", "개인", "미배정"]

from util import GetDiffText, SongDataElem, GetPopClass
from userdatautil import GetUserData, FindSongData

import numpy as np
import cv2
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from util import GetRankColor, GetSizeText, GetAbsIndex, MergeImageAlpha

# Load medal images
MEDAL_IMAGES = []
MEDAL_IMAGES.append([])
for i in range(1, 13):
    if os.path.exists(f'./medal/{i}.png'):
        medal_image = cv2.imread(f'./medal/{i}.png', cv2.IMREAD_UNCHANGED)
    else:
        medal_image = cv2.imread(f'./medal/0.png', cv2.IMREAD_UNCHANGED)
    # remove alpha channel

    medal_image = cv2.resize(medal_image, (60, 60))
    # TODO : Why black background?
    MEDAL_IMAGES.append(medal_image)

UPPER_IMAGE = cv2.imread(f'./image/_UPPER.png', cv2.IMREAD_UNCHANGED) # 87x60

WIDTH = 336
HEIGHT = 120

def GetElement(lvd, filtered=False, use_kr_label=True):
    img = np.zeros((HEIGHT, WIDTH, 4), dtype=np.uint8)
    # Fill image with gray, alpha=255
    img[:, :, 0:3] = 140
    img[:, :, 3] = 255
    # Load image from lv.image and place it to 70,0
    if len(lvd.image) > 0 and os.path.exists(f'image/{lvd.image}'):
        song_image = cv2.imread(f'image/{lvd.image}', cv2.IMREAD_UNCHANGED)
        # Add alpha channel if not exists
        if song_image.shape[2] == 3:
            song_image = cv2.cvtColor(song_image, cv2.COLOR_BGR2BGRA)
    else:
        song_image = cv2.imread(f'image/_base.png', cv2.IMREAD_UNCHANGED)
    song_image = cv2.resize(song_image, (246, 60)) # resize song_image to 246x60 (for in case)
    margin = 10
    if lvd.isHJudge and lvd.isHGauge:
        img[margin-5:60+margin+5, 70+margin-5:70+margin+123] = [0, 255, 255, 255]
        img[margin-5:60+margin+5, 70+margin+123:70+246+margin+5] = [0, 0, 255, 255]
    elif lvd.isHJudge:
        img[margin-5:60+margin+5, 70+margin-5:70+246+margin+5] = [0, 255, 255, 255]
    elif lvd.isHGauge:
        img[margin-5:60+margin+5, 70+margin-5:70+246+margin+5] = [0, 0, 255, 255]

    img[margin:60+margin, 70+margin:70+246+margin] = song_image
    if lvd.IsUpper():
        img_part = img[margin:UPPER_IMAGE.shape[0]+margin, 70+246+margin-87:70+246+margin]
        img[margin:UPPER_IMAGE.shape[0]+margin, 70+246+margin-87:70+246+margin] = MergeImageAlpha(img_part, UPPER_IMAGE)

    
    if lvd.score >= 0:
        # Add alpha, fxxk this crazy shit
        img_medal = MEDAL_IMAGES[lvd.medal]
        img_part = img[margin:img_medal.shape[0]+margin, margin+3:img_medal.shape[1]+margin+3]
        img[margin:img_medal.shape[0]+margin, margin+3:img_medal.shape[1]+margin+3] = MergeImageAlpha(img_part, img_medal)

    ## Text drawing
    img_pil = Image.fromarray(img)
    draw = ImageDraw.Draw(img_pil)

    # Write Song Title
    if len(lvd.labelKR) > 0 and use_kr_label:
        titletext = lvd.labelKR + GetDiffText(lvd.genre)
        sz = GetSizeText(titletext, 40, 16)
        minS = 20
        
        if sz < minS: # split text to half
            font = ImageFont.truetype("font/KR.TTF", minS)
            
            p = GetAbsIndex(titletext, 600//minS)
            draw.text((10, 75), titletext[:p], font=font, fill=(255, 255, 255, 255), stroke_width=1, stroke_fill='black')
            draw.text((10, 75+minS), titletext[p:], font=font, fill=(255, 255, 255, 255), stroke_width=1, stroke_fill='black')
        else:
            font = ImageFont.truetype("font/KR.TTF", sz)
            draw.text((10, 75), titletext, font=font, fill=(255, 255, 255, 255), stroke_width=2, stroke_fill='black')
    else:
        titletext = lvd.title + GetDiffText(lvd.genre)
        sz = GetSizeText(titletext, 40, 16)
        minS = 20
        if sz < minS: # split text to half
            font = ImageFont.truetype("font/JP.TTC", minS)
            p = GetAbsIndex(titletext, 600//minS)
            ttx = titletext[:p] + "\n" + titletext[p:]
            draw.text((10, 75), ttx, font=font, fill=(255, 255, 255, 255), stroke_width=1, stroke_fill='black')
        else:
            font = ImageFont.truetype("font/JP.TTC", sz)
            draw.text((10, 75), titletext, font=font, fill=(255, 255, 255, 255), stroke_width=2, stroke_fill='black')
    
    if lvd.score >= 0:
        # Write Score
        font = ImageFont.truetype("font/KR.TTF", 35)
        draw.text((220, 10), f"{lvd.score}", font=font, fill=(100, 255, 100, 255), stroke_width=2, stroke_fill='black')
        # Rank
        font = ImageFont.truetype("font/RANK.TTF", 40)
        col = GetRankColor(lvd.rank)
        w = 36-lvd.rank*9 if lvd.rank == 2 or lvd.rank == 3 else 0
        draw.text((32-w, 15), RANK[lvd.rank], font=font, fill=col, stroke_width=2, stroke_fill='black')
    
    img = np.array(img_pil)
    
    if filtered:
        # darken image
        img = cv2.addWeighted(img, 0.5, np.zeros(img.shape, img.dtype), 0, 0)
        img[:, :, 3] = 255
    return img

def GenerateTable(tomoID, level, columns = 8, filter_method = "none", filter_medal = 0, filter_score = 0, filter_rank = 0, output_path = None, use_diffkr = True, use_info = True, use_kr_label = True, title = None, sort_method = "series"): 


    print("=====================================")
    print(f" -- Table Generation Start")

    userdata = GetUserData(tomoID)

    print(f" -- Loaded User Data")

    leveldata = []
    with open(f'leveldata/{level}.tsv', encoding='utf-8') as f:
        levelline = f.read()
        isFirst = True
        for line in levelline.split('\n'):        
            if isFirst:
                isFirst = False
                continue
            line = line.split('\t')
            isHardJudge, isHardGauge = False, False
            if len(line[11]) > 0:
                isHardJudge = True
            if int(line[6]) > 1537:
                isHardGauge = True
            # Find user data
            sd = FindSongData(line[2], line[3], userdata)
            if sd is not None: # Medal Rank Score
                score = sd[2]
                medal = sd[0]
                rank = sd[1]
                popc = GetPopClass(score, medal, level)
            else:
                score = -1
                medal = -1
                rank = -1
                popc = -1
            lv = SongDataElem(line[0], level, line[2], line[3], line[7], line[9], line[10], line[8], isHardJudge, isHardGauge, score, medal, rank, popc)
            leveldata.append(lv)

    print(f" -- Songdata Parsed: {len(leveldata)} songs found and matched userinfo for level table")

    lv_cnt = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    lv_threshold = [0.7, 0.7, 0.7, 0.7, 0.7, 0.8, 0.7, 0.6, 0.5, 0.6] # 41, 42, 43, 44, 45, 46, 47, 48, 49, 50
    def ParseDiffJP(diffJP, lv):
        if len(diffJP) == 0:
            return 9
        # split bt ( and ±
        dv = diffJP.split("(")[1].split("±")
        abso = float(dv[0])
        rela = float(dv[1].split(")")[0])
        if rela >= lv_threshold[lv-41]:
            return 8
        if abso >= 1:
            return 0
        elif abso <= -1:
            return 7
        else:
            return int(4 - abso*3)

    for lvd in leveldata:
        if filter_method != 'none':
            if filter_medal >= lvd.medal:
                lvd.is_filtered = True
            if filter_score >= lvd.score:
                lvd.is_filtered = True
            if filter_rank >= lvd.rank:
                lvd.is_filtered = True
        if lvd.score < 0:
            lvd.is_filtered = False
        if filter_method == 'disable' and lvd.is_filtered:
            continue
        if use_diffkr:
            if lvd.diffKR in DIFFKR:
                lvd.diff = DIFFKR.index(lvd.diffKR)
            else:
                lvd.diff = 9
        else:
            lvd.diff = ParseDiffJP(lvd.diffJP, level)

        lvd.subIndex = lv_cnt[lvd.diff]
        lv_cnt[lvd.diff] += 1

    # if sort method is not sort_method, sort again
    if sort_method != "series": # sort by each diff
        elems = [None] * 12
        for lvd in leveldata:
            if elems[lvd.diff] is None:
                elems[lvd.diff] = []
            elems[lvd.diff].append(lvd)
        leveldata = []
        for elem in elems:
            k = 0
            if elem is None:
                continue
            if sort_method == "title":
                elem.sort(key=lambda x: x.title)
            elif sort_method == "score":
                elem.sort(key=lambda x: x.score, reverse=True)
            elif sort_method == "medal":
                elem.sort(key=lambda x: x.medal, reverse=True)
            for e in elem:
                # assign sub-index
                e.subIndex = k
                k += 1
            leveldata += elem


    v_total = len(leveldata)
    v_filtered = len([lvd for lvd in leveldata if lvd.is_filtered])

    if filter_method == 'disable':
        leveldata = [lvd for lvd in leveldata if not lvd.is_filtered]

    # full_image = np.zeros((HEIGHT * (len(leveldata)//columns+1), WIDTH * columns, 4), dtype=np.uint8)

    print(f" -- Data Loaded, {v_total} songs found, {v_filtered} songs filtered out")

    FRAME = 20
    TABLESTARTV = 340
    TABLESTARTH = 100
    BORDER = 20
    MARGIN_LINE = 20
    partStart = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    h = TABLESTARTV + BORDER
    for i in range(len(lv_cnt)):
        if lv_cnt[i] == 0:
            continue
        partStart[i] = h
        h += HEIGHT * ((lv_cnt[i]-1)//columns+1)
        h += FRAME

    h += BORDER - FRAME
    full_image = np.zeros((h, WIDTH * columns + TABLESTARTH + BORDER*2, 4), dtype=np.uint8)
    full_image[:, :, 0:3] = 50
    full_image[:, :, 3] = 255
    # DrawTitle
    img_pil = Image.fromarray(full_image)
    draw = ImageDraw.Draw(img_pil)
    font = ImageFont.truetype("font/KR.TTF", 90)
    if title is not None and len(title) > 0:
        draw.text((40, 50), title, font=font, fill=(255, 255, 255, 255), stroke_width=2, stroke_fill='black')
    else:
        draw.text((40, 50), f"챱챱뮤직 {level}렙 도표", font=font, fill=(255, 255, 255, 255), stroke_width=2, stroke_fill='black')
    font = ImageFont.truetype("font/KR.TTF", 60)
    n = userdata['profile'][0]
    draw.text((40, 150), f"유저:{n}", font=font, fill=(255, 255, 255, 255), stroke_width=2, stroke_fill='black')
    txt = "필터링: "
    if filter_method == 'none':
        txt += f"없음 (총 {v_total}개)"
    else:
        if filter_medal > 0:
            txt += f"메달 {MEDAL[filter_medal]} 이상 "
        if filter_score > 0:
            txt += f"점수 {filter_score} 이상 "
        if filter_rank > 0:
            txt += f"랭크 {RANK[filter_rank]} 이상 "
        if filter_method == 'darken':
            txt += f"어둡게 ({v_filtered}/{v_total})"
        elif filter_method == 'disable':
            txt += f"미표시 ({v_filtered}/{v_total})"

    draw.text((40, 220), txt, font=font, fill=(255, 255, 255, 255), stroke_width=2, stroke_fill='black')
    font = ImageFont.truetype("font/KR.TTF", 40)
    # tx = "[]: 제목 첫 글자,  (): 별명/장르명,  ⓗ: 하이퍼,  "
    tx = "():장르명,  테두리(빨:짠게, 노랑:짠판),  "
    if level <= 48:
        tx += "ⓗ:하이퍼,  "
    if use_diffkr:
        tx += f"기준 서열표: @popnmusic10"
    else:
        tx += f"기준 난이도값: popn.wiki"
    draw.text((40, 290), tx, font=font, fill=(255, 255, 255, 255), stroke_width=2, stroke_fill='black')
    # today date as YY-MM-DD
    # import datetime
    # t = datetime.datetime.now()
    font = ImageFont.truetype("font/KR.TTF", 32)
    fin_d = userdata['profile'][6].replace('時頃','시')
    draw.text((1000, 60), f"최종갱신 {fin_d}", font=font, fill=(255, 255, 255, 255), stroke_width=2, stroke_fill='black')
    font = ImageFont.truetype("font/KR.TTF", 28)
    draw.text((10, 10), f"곡 이미지: remywiki.com / popnmusic.fandom.com, 한국 서열표: @popnmusic10, 난이도값: popn.wiki", font=font, fill=(180, 180, 180, 255), stroke_width=2, stroke_fill='black')
    font = ImageFont.truetype("font/KR.TTF", 40)
    if use_info:
        creds = int(userdata['profile'][3]) + int(userdata['profile'][4]) + int(userdata['profile'][5])
        draw.text((500, 170), f"크레딧: {creds},   팝토모 ID: {userdata['profile'][1]}", font=font, fill=(255, 255, 255, 255), stroke_width=2, stroke_fill='black')

    full_image = np.array(img_pil)

    # Draw 10px line for each part
    for i in range(len(partStart)):
        if partStart[i] == 0:
            continue
        full_image[partStart[i]-13:partStart[i]-7, MARGIN_LINE:full_image.shape[1]-MARGIN_LINE] = [0, 0, 0, 255]
        # Draw LevelText
        img_pil = Image.fromarray(full_image)
        draw = ImageDraw.Draw(img_pil)
        if use_diffkr:
            font = ImageFont.truetype("font/KR.TTF", 50)
            draw.text((20, partStart[i]+10), DIFFKR[i], font=font, fill=(255, 255, 255, 255), stroke_width=2, stroke_fill='black')
        else:
            font = ImageFont.truetype("font/KR.TTF", 30)
            draw.text((20, partStart[i]+10), DIFFJP[i], font=font, fill=(255, 255, 255, 255), stroke_width=2, stroke_fill='black')
        full_image = np.array(img_pil)

    for lvd in leveldata:
        im = GetElement(lvd, lvd.is_filtered, use_kr_label)
        # Add image to full_image
        row = (lvd.subIndex // columns)*HEIGHT + partStart[lvd.diff]
        col = (lvd.subIndex % columns)*WIDTH + TABLESTARTH + BORDER
        full_image[row:row+HEIGHT, col:col+WIDTH] = im

    if output_path is not None:
        f_out = 'output/' + output_path + '.png'
    else:
        f_out = f'output/{tomoID}_L{level}_C{columns}'
        if filter_method != 'none':
            f_out += f'_{filter_method}'
            if filter_medal > 0:
                f_out += f'_medal{filter_medal}'
            if filter_score > 0:
                f_out += f'_score{filter_score}'
            if filter_rank > 0:
                f_out += f'_rank{filter_rank}'
        else:
            pass
        if use_diffkr:
            f_out += '_kr'
        f_out += '.png'

    cv2.imwrite(f_out, full_image)
    print(f" -- Table generated, and output to {f_out}")
    return f_out