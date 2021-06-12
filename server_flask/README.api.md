# REST API_LIST

진입점: https://202.30.30.3:5678

** http가 아니라 https입니다.
** jquery에서 GET으로 데이터 전달이 가능하지만 파싱이 번거로워져 모두 POST로 바꿨습니다.
** 우선 모든 기능을 flask로 옮겼습니다.


** jquery의 post를 사용하시면 보내실 데이터를 두번째 인자로 전달하시면 됩니다.
EX)
if (loc.substring(0, 29) == 'https://www.youtube.com/watch') {
        var videoID=loc.substring(32, loc.length)
		await $.post(`https://202.30.30.3:5678/scripts-load`,
		{ "video_id": videoID },
		function(data){
			console.log(data);
		});

## 1. ctrl+F

POST: /unit-find

methods: POST
location: /unit-find
body: {
    "video_id": string(유튜브 영상의 url중 id),
    "keyword": string(영상 시청시 검색 내용)
}

return ==> 각 검색어를 포함하는 구절과 시간을 리턴.

요약: 
Input: 시청중인 영상의 video_id와 검색 내용을 보내시면
Output: 각 검색어를 포함하는 구절과 시간을 리턴받을 수 있습니다.

## 2. 신뢰도 계산

POST: /ml/freq

methods: POST
location: /ml/freq
body: {
    "video_id": [string] (유튜브 검색창에 나오는 영상들의 video_id 배열. 개수는 5~10개 정도로..?)
    "keyword": string(유튜브 검색창에서의 검색 내용)
}

return ==> 각 영상의 video_id에 대응하는 신뢰도 리턴.

요약:
Input: 유튜브 검색창에서 검색한 결과로 나오는 영상들의 id(5~10개)와 검색한 내용(키워드)을 보내시면
Output: 각 영상에 대한 신뢰도를 리턴받을 수 있습니다.


## 3. 영상 로드 및 다운

methods: POST:
location: /scripts-load

body: {
    "video_id": string
}

return ==> 요청한 영상의 자막을 리턴.

영상이 없으면 영상을 다운 받아서 보내주고,
영상이 있다면 영상을 그냥 보내줍니다.

요약:
Input: 동영상의 id를 전달하면
Output: 해당 영상의 자막을 받을 수 있습니다.


