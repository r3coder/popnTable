# popnTable
팝픈뮤직 서열표에 자신의 기록을 더해서 표기하는 프로그램입니다.

[이 링크](https://popntable.mooo.com:3000)에서 직접 테스트 해 볼 수 있습니다.

# 사전 설정

## 1. 이미지 데이터 저장

image 내부에 곡의 자켓 이미지를 받아야 합니다. [레미위키](https://remywiki.com/) / [팝픈위키팬덤](https://popnmusic.fandom.com/) 에 보통 있습니다.

위 도메인에서는 직접 하나하나 이미지를 저장했습니다. 본 레포지토리에는 업로드하지 않았습니다. 만약 필요하신 분은 별도로 연락 부탁드립니다.

## 2. 레벨 데이터 저장

`leveldata` 폴더 내부에는 각 레벨별 데이터를 tsv 형식으로 series / / genre / title / bpm / length / notes / diff_jp / label_kr / diff_kr / image_path / hardjudge 로 구분되어 저장하면 됩니다. [팝픈위키](popn.wiki)의 형식을 따르고 있습니다.

예시: `[5]		レッスン(EX)	POP-STEP-UP	32～260	1:33	1008	強(+0.978±0.4)	팝 스텝 업	개인		o`

[여기](https://docs.google.com/spreadsheets/d/1j9F6k-x06xxlOvE_IURBmjLPLHtiiiLHU2rDVpSPPCY)에서 최신 데이터를 업데이트 후, 각 레벨을 tsv 형태로 저장해 해당 폴더에 넣으면 됩니다.

## 3. 폰트 저장

`font` 폴더 내부에는 한글/일본어/랭크 폰트를 각각 `KR.TTF`, `JP.TTC`, `RANK.TTF`로 넣어야 합니다.

# 프로그램 실행

## 호스트 설정

실행 전, 자신의 컴퓨터가 제대로 환경 설정이 되었는지 확인할 필요가 있습니다.

`src/main.py`의 9번, 10번 줄에 `hostName`과 `serverPort`를 원하는 환경에 맞게 설정해 주세요.

`hostName`은 만약 도메인을 받지 않았다면 자신의 IP 주소를 입력하면 됩니다.

`serverPort`는 적당히 큰 값을 쓰셔도 되고, 할 줄 안다면 http 포트인 80이나 https 포트인 443을 사용해도 됩니다.

## 도메인 설정

도메인은 자신이 받을 수 있는 방법을 잘 사용하시면 됩니다. 저는 https://freedns.afraid.org/ 에서 그냥 무료 도메인을 사용했습니다.

## https 보안 인증 받기

certbot과 같은 것을 사용해서 설정하면 됩니다.

# 레포지토리 파일 설명

`src/collect.js`: 팝픈 홈페이지에서 데이터 긁어오는 코드입니다. `https://otoge-flow-flow.com/` 여기 코드를 수정해 사용중입니다. (MIT License)

`main.py`: 웹서버 기동하는 코드입니다.

`tablegen.py`: 이미지를 생성해주는 코드인데 대충짜서 부끄러우니까 보지 마세요 😥

`util.py`: 기타 유틸리티 코드입니다.

`userdatautil.py`: 유저 데이터 불러와서 파싱하는 코드입니다.

`medal/*.png` 팝픈뮤직 각 메달 이미지입니다.

# 이미지만 생성하고 싶을 때
`tablegen.py` 안의 `GenerateTable` 함수를 호출하면 됩니다. 그럼 output 폴더 안에 들어갑니다.

# Requirements
`python 3.10+`
`Pillow+`
`opencv-python`

# License

본 프로그램에 포함된 소스 코드 및 메달 이미지는 [MIT License](https://opensource.org/license/mit) 를 사용하고 있습니다.

요약하면, 다음과 같은 권한을 가집니다.

- 상업적 이용, 수정, 배포, 개인적 이용 모두 가능합니다.

- 제작자는 법적인 책임을 지지 않으며, 보증하지 않습니다.

- 본 프로그램의 일부 혹은 전부를 사용할 경우 라이선스 및 저작권을 고지해야 합니다.

## Mit License

The MIT License (MIT)

Copyright (c) 2024 R3C0D3r

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
