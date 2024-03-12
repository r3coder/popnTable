/*
 Copyright (c) 2024 r3c0d3r.com
 Released under the MIT license
 https://opensource.org/licenses/mit-license.php
*/
/*
 Copyright (c) 2020 otoge-flow-flow.com
 Released under the MIT license
 https://opensource.org/licenses/mit-license.php
*/
/*
 Copyright (c) 2019 ケルパニ＠猫
 Released under the MIT license
 https://opensource.org/licenses/mit-license.php
*/

/* eslint-disable no-undef */
(() => {

	const DEBUG = false;

	// エラーチェック
	if (document.domain !== 'p.eagate.573.jp') {
		document.body.innerHTML = '<a href="https://p.eagate.573.jp/">https://p.eagate.573.jp/</a> 에서 코드를 실행해 주세요.<br>';
		return;
	}

	if (!ea_common_template.userstatus.state.login) {
		document.body.innerHTML = '로그인 해주세요.<br>';
		return;
	}

	if (!ea_common_template.userstatus.state.subscription) {
		document.body.innerHTML = 'e-amusement 베이직 코스 가입이 필요합니다.<br>';
		return;
	}

	if (!ea_common_template.userstatus.state.eapass) {
		document.body.innerHTML = 'e-amusement pass가 등록되어 있지 않습니다.<br>';
		return;
	}

	if (!ea_common_template.userstatus.state.playdata) {
		document.body.innerHTML = '플레이 데이터가 없습니다.<br>';
		return;
	}

	// 重複起動チェック
	if (window.BOOKMARKLET_TOOL_POPN) {
		document.body.insertAdjacentHTML('beforeend', '이미 실행이 끝났습니다.<br>');
		return;
	}

	window.BOOKMARKLET_TOOL_POPN = true;

	/**
	 * 頭文字リスト
	 */
	const initials = [
		'ｱ', 'ｲ', 'ｳ', 'ｴ', 'ｵ',
		'ｶ', 'ｷ', 'ｸ', 'ｹ', 'ｺ',
		'ｻ', 'ｼ', 'ｽ', 'ｾ', 'ｿ',
		'ﾀ', 'ﾁ', 'ﾂ', 'ﾃ', 'ﾄ',
		'ﾅ', 'ﾆ', 'ﾇ', 'ﾈ', 'ﾉ',
		'ﾊ', 'ﾋ', 'ﾌ', 'ﾍ', 'ﾎ',
		'ﾏ', 'ﾐ', 'ﾑ', 'ﾒ', 'ﾓ',
		'ﾔ', 'ﾕ', 'ﾖ',
		'ﾗ', 'ﾘ', 'ﾙ', 'ﾚ', 'ﾛ',
		'ﾜ', 'ｦ', 'ﾝ',
		'A', 'B', 'C', 'D', 'E', 'F', 'G',
		'H', 'I', 'J', 'K', 'L', 'M', 'N',
		'O', 'P', 'Q', 'R', 'S', 'T', 'U',
		'V', 'W', 'X', 'Y', 'Z',
		'0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
		'@', '*', '「', '↑'
	];

	/**
	 * Blob を UTF-8 文字列にパース
	 */
	const parseBlob = blob => {
		return new Promise(resolve => {
			const reader = new FileReader();
			reader.onload = () => {
				resolve(reader.result)
			};
			reader.readAsText(blob);
		});
	};

	/**
	 * HTML 文字列を DOM にパース
	 */
	const parseHTML = string => new DOMParser().parseFromString(string, 'text/html');

	/**
	 * プロフィールページをパース
	 */
	const parseProfilePage = dom => {

		const array = [];

		// 取得
		const table = dom.getElementsByClassName('st_box').item(0);

		if (table !== null) {
			const elements = table.getElementsByTagName('div');

			for (let i = 0; i < elements.length; i++) {
				const row = elements.item(i);
				if (row.className !== 'item_st') {
					continue;
				}

				const index = row.innerHTML.lastIndexOf('<br>')
				const childCount = row.childElementCount;
				let childTagName = '';
				if (1 <= childCount) {
					childTagName = row.firstElementChild.tagName;
				}
				if (index !== -1) {
					// キャラ名取得
					// console.log(row.innerHTML.substr(index + 4));
					array.push(row.innerHTML.substr(index + 4));
				} else if (childTagName === 'IMG') {
					// ex ramp
					// console.log('ex ramp');
				} else if (1 < childCount) {
					// option 
					// console.log('option');
				} else {
					// others
					// console.log(row.innerHTML);
					array.push(row.innerHTML);
				}
			}
		}

		return array;

	};

	/**
	 * ページをパース
	 */
	const parsePage = (dom, pageNumber) => {
		let array = [];

		// 取得
		const table = dom.getElementsByClassName('mu_list_table').item(0);

		let i = 0;
		let rowCount = 0;
		if (table !== null) {
			const elements = table.getElementsByTagName('li');

			for (i = 1; i < elements.length; i++) { // 見出しの行があるので i = 1 から
				const row = parseRow(elements.item(i), pageNumber * 20 + i);
				array.push(row);
				rowCount++;
			}
		}

		return {array, rowCount};

	};

	const toMedalOrdinalScale = pngName => {
		switch (pngName) {
		case 'meda_a.png':
			return 1;
		case 'meda_b.png':
			return 2;
		case 'meda_c.png':
			return 3;
		case 'meda_d.png':
			return 4;
		case 'meda_e.png':
			return 5;
		case 'meda_f.png':
			return 6;
		case 'meda_g.png':
			return 7;
		case 'meda_h.png':
			return 8;
		case 'meda_i.png':
			return 9;
		case 'meda_j.png':
			return 10;
		case 'meda_k.png':
			return 11;
		case 'meda_none.png':
			return -1;
		default:
			return -1;
		}
	};
	const toRankOrdinalScale = pngName => {
		switch (pngName) {
		case 'rank_s.png':
			return 1;
		case 'rank_a3.png':
			return 2;
		case 'rank_a2.png':
			return 3;
		case 'rank_a1.png':
			return 4;
		case 'rank_b.png':
			return 5;
		case 'rank_c.png':
			return 6;
		case 'rank_d.png':
			return 7;
		case 'rank_e.png':
			return 8;
		case 'rank_none.png':
			return -1;
		default:
			return -1;
		}
	};

	/**
	 * クエリ文字列をオブジェクトにパース
	 */
	const parseQuery = query => {
		const pairs = query.split('&');
		const object = {};
		pairs.forEach(pairString => {
			const pair = pairString.split('=');
			const key = decodeURIComponent(pair[0]);
			const value = decodeURIComponent(pair[1]);
			object[key] = value;
		});
		return object;
	};

	/**
	 * メダル・ランク画像パスパース
	 */
	const getExtention = src => /([^/]+)$/.exec(src)[1]; 
	const getMedal = src => toMedalOrdinalScale(getExtention(src))
	const getRank = src => toRankOrdinalScale(getExtention(src));
	const getScore = src => {
		if (src === '-') {
			return -1;
		}

		return Number(src);
	};

	/**
	 * 行パース
	 */
	const parseRow = (element, index) => {

		// 曲名・ジャンル名・ID
		const music = element.getElementsByClassName('col_music').item(0);

		const music_link = music.getElementsByTagName('a').item(0);
		const music_id = parseQuery(music_link.search.slice(1)).no;
		const music_title = music_link.textContent;
		const music_genre = music.getElementsByTagName('div').item(0).textContent;

		// メダル・スコア
		const column_easy = element.getElementsByClassName('col_5').item(0);
		const column_normal = element.getElementsByClassName('col_normal').item(0);
		const column_hyper = element.getElementsByClassName('col_hyper').item(0);
		const column_ex = element.getElementsByClassName('col_ex').item(0);

		const img_easy = column_easy.getElementsByTagName('img');
		const img_normal = column_normal.getElementsByTagName('img');
		const img_hyper = column_hyper.getElementsByTagName('img');
		const img_ex = column_ex.getElementsByTagName('img');

		const medal_easy = getMedal(img_easy.item(0).src);
		const medal_normal = getMedal(img_normal.item(0).src);
		const medal_hyper = getMedal(img_hyper.item(0).src);
		const medal_ex = getMedal(img_ex.item(0).src);

		const rank_easy = getRank(img_easy.item(1).src);
		const rank_normal = getRank(img_normal.item(1).src);
		const rank_hyper = getRank(img_hyper.item(1).src);
		const rank_ex = getRank(img_ex.item(1).src);

		const score_easy = getScore(column_easy.textContent);
		const score_normal = getScore(column_normal.textContent);
		const score_hyper = getScore(column_hyper.textContent);
		const score_ex = getScore(column_ex.textContent);

		const row = [
			music_id,
			music_genre,
			music_title,
			index,
			[
				[
					medal_easy,
					rank_easy,
					score_easy
				],
				[
					medal_normal,
					rank_normal,
					score_normal
				],
				[
					medal_hyper,
					rank_hyper,
					score_hyper
				],
				[
					medal_ex,
					rank_ex,
					score_ex
				]
			]
		];


		return row;
	};


	/*
	profile取得
	*/
	const loadProfile = () => {

		const url = 'https://p.eagate.573.jp/game/popn/unilab/playdata/';

		return fetch(url, {
				credentials: 'include'
			})
			.then(response => response.blob())
			.then(blob => parseBlob(blob))
			.then(string => {
				const array = parseProfilePage(parseHTML(string));
				return array;
			});

	};

	/**
	 * ジャンルで頭文字ごとに読み込み
	 */
	const loadScoreOfInitial = initial => loadScoreOfPage(initial, 0);

	const loadScoreOfPage = async (initial, page) => {

		const url = 'https://p.eagate.573.jp/game/popn/unilab/playdata/mu_top.html?page=' + page + '&genre=' + initial;

		await sleep(10);

		return fetch(url, {
				credentials: 'include'
			})
			.then(response => response.blob())
			.then(blob => parseBlob(blob))
			.then(string => {
				const {array, rowCount} = parsePage(parseHTML(string), page);
				if (rowCount === 20) {
					return loadScoreOfPage(initial, page + 1).then(arrayNext => array.concat(arrayNext));
				} else {
					return array;
				}
			});

	};

	/**
	 * ファイル保存ダイアログ表示
	 * 
	 * Chrome, Firefox, Edge 対応
	 */
	const showSaveFileDialog = (data, name, type) => {

		const a = document.createElement('a');
		a.href = URL.createObjectURL(new Blob([data], {
			'type': type
		}));
		a.download = name;

		a.style.display = 'none';
		document.body.appendChild(a);
		a.click();
		document.body.removeChild(a);

	};

	sleep = (msec) => {
		return new Promise(resolve => {
			setTimeout(() => {resolve()}, msec);
		})
	}

	const goScrollEnd = () => {
		// 最下部にスクロール
		var element = document.documentElement;
		var bottom = element.scrollHeight - element.clientHeight;
		window.scroll(0, bottom);
	};

	// post
	const post = (path, params) => {

		const form = document.createElement('form');
		form.method = 'POST';
		form.action = path;

		const hiddenField = document.createElement('input');
		hiddenField.type = 'hidden';
		hiddenField.name = 'datalist';
		hiddenField.value = encodeURIComponent(params);

		form.appendChild(hiddenField);

		document.body.appendChild(form);
		form.submit();
	};

	/**
	 * メイン
	 */
	const main = () => {

		// 取得開始
		document.body.innerHTML = '수집중...<br>';

		// 取得
		if (DEBUG) { // テスト

			loadProfile().then(
				array1 => {
				document.body.insertAdjacentHTML('beforeend', '프로필 수집 완료<br>');
				loadScoreOfInitial(initials[0]).then(array2 => {
					document.body.insertAdjacentHTML('beforeend', '수집 완료 (' + array2.length + ' 곡)<br>');
					const json = JSON.stringify({profile: array1, scores:array2}, null, '    ');
					showSaveFileDialog(json, 'score.json', 'application/json')
				});
			});


			/*

			*/

		} else { // 本番
			loadProfile().then(array1 => {
				document.body.insertAdjacentHTML('beforeend', '프로필 수집 완료<br>');

				// promise.allが速いが負荷が高いので逐次処理。
				initials.reduce(async (accumulator, currentArray) => {
					await sleep(10);
					await accumulator;
					document.body.insertAdjacentHTML('beforeend', '수집중 (' + currentArray + ')<br>');
					goScrollEnd();					

					return await loadScoreOfPage(currentArray, 0).then(arrays => {
						if (Array.isArray(accumulator)) {
							return accumulator.concat(arrays);
						}
						return accumulator.then(array =>{
							return array.concat(arrays);
						});
					});
				}, []).then(arrays => {
					const arrays2 = arrays
						// .reduce((accumulator, currentValue) => accumulator.concat(currentValue)) // Promise.all() の結果をまとめる
						.filter((x, i, a) => a.findIndex(x2 => x[0] === x2[0]) === i); // 重複削除
					const diff = arrays.length - arrays2.length; 
					document.body.insertAdjacentHTML('beforeend', '중복 삭제 (' + diff + ' 곡)<br>');
					document.body.insertAdjacentHTML('beforeend', '수집 완료 (' + arrays2.length + ' 곡)<br>');
					goScrollEnd();

					const information = [ new Date().toLocaleString() ];
					// 結果送付。
					const json = JSON.stringify({ profile: array1, info: information, scores: arrays2 });

          // const blob = new Blob([json], { type: 'application/json' });
          // const url = URL.createObjectURL(blob);
          // const a = document.createElement('a');
          // a.href = url;
          // a.download = `${json.profile[1]}.json`;
          // a.download = `data.json`;
          // a.click();
					post('http://r3c0d3r.mooo.com/submit', json);
				});
			});
		}
	};

	main();

})();
