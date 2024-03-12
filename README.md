# popnTable
팝픈뮤직 서열표에 자신의 기록을 더해서 표기하는 프로그램입니다.

# Preset (Dataset download)

image 내부에 곡의 자켓 이미지를 받아야 합니다. [https://remywiki.com/](레미위키) / [https://popnmusic.fandom.com/](팝픈위키팬덤) 에 보통 있습니다

medal 내부에는 `1.png ~ 12.png` 의 형태로 메달 이미지를 금별부터 미플레이까지 넣어야 합니다.

font 폴더 내부에는 한글/일본어/랭크 폰트를 각각 `KR.TTF`, `JP.TTC`, `RANK.TTF`로 넣어야 합니다.

leveldata 내부에는 각 레벨별 데이터를 tsv 형식으로 series / / genre / title / bpm / length / notes / diff_jp / label_kr / diff_kr / image_path / hardjudge 로 구분되어 저장하면 됩니다. [popn.wiki](팝픈위키)의 형식을 따르고 있습니다.

예시: `[5]		レッスン(EX)	POP-STEP-UP	32～260	1:33	1008	強(+0.978±0.4)	팝 스텝 업	개인		o`

# Files
`src/collect.js`: 팝픈 홈페이지에서 데이터 긁어오는 코드입니다. `https://otoge-flow-flow.com/` 여기 코드를 수정해 사용중입니다. (MIT License)
`main.py`: 웹서버 기동하는 코드입니다.
`tablegen.py`: 이미지를 생성해주는 코드인데 대충짜서 부끄러우니까 보지 마세요 😥
`util.py`: 기타 유틸리티 코드입니다.
`userdatautil.py`: 유저 데이터 불러와서 파싱하는 코드입니다.

# 이미지만 생성하고 싶을 때
`tablegen.py` 안의 `GenerateTable` 함수를 호출하면 됩니다. 그럼 output 폴더 안에 들어갑니다.

# Requirements
`python 3.10+`
`Pillow+`
`opencv-python`
