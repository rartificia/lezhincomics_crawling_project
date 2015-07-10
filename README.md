# lezhincomics_crawling_project

리드미 겸 주석파일

레진코믹스의 만화 이미지 url형식은 다음과 같다. 이는 레진코믹스 만화창에서 개발자 도구 등으로 쉽게 확인할 수 있다.

url = http://2cdn.lezhin.com/episodes/#{만화 제목}/#{에피소드 번호}/contents/#{해당 에피소드 이미지 번호}?access_token=#{액세스 토큰}

oauth를 사용하는 레진 코믹스 특성상, 유효한 #{액세스 토큰}값을 알고있으면 해당 계정의 주인처럼 행세하는 것이 가능하다. 물론, 레진코믹스에는 어느정도 무료로 제공되는 만화도 있으므로, 자신의 계정의 #{액세스 토큰}을 사용해도 무방하다. 긴 말 않겠다. 가장 중요한것은, #{액세스 토큰}이다. 별도의 인증 과정 없이 #{액세스 토큰}만 있다면 해당 만화 이미지에 해당하는 url을 입력하여 이미지에 접근할 수 있다.

#{액세스 토큰}의 형식은 다음과 같다.

access_token=00000000-0000-0000-0000-00000000000c9&purchased=true

각 '0'에는 16진수가 들어간다. 해킹을 하든지 구글링을 하든지 아니면 자신의 계정의 것을 사용해도 무방하다. 그리고 purchased=true와 purchased=false가 있는데, 무과금 유저라면(즉, 해당 {#액세스 토큰}의 계정으로 구입하지 않은 만화라면) purchased=false옵션을 사용하라.

여기에 for문등으로 #{만화 제목}, #{에피소드 번호}, #{해당 에피소드 이미지 번호}를 잘 조작하면 해당 이미지에 접근할 수 있다. (e-hentai.org처럼 #{해당 에피소드 이미지 번호}를 랜덤해쉬값으로 지정해 놓은게 아니라 이미지 차례대로 정수값으로 되어있기 때문에 가능하다.)

그리고, 해당 에피소드의 이미지파일을 긁어올때 #{해당 에피소드에 포함된 이미지의 총 개수}등의 추가 정보가 필요하다. SQL Injection（엄밀히 말하면 아니다. 이렇게 말하기도 부끄러워질 정도이다.)으로 얻을 수 있다.

http://2cdn.lezhin.com/episodes/#{만화 제목}/;/contents/#{해당 에피소드 이미지 번호}?access_token=#{액세스 토큰}

위와 같이 #{에피소드 번호}에 해당되는 칸에 세미콜론을 넣어주면 된다. 그러면 다음과 같이 json파일 형식으로 해당 만화의 상세 정보를 알 수 있다.

[{"episodeId":"sweetguy/p0","seq":1,"comicId":"sweetguy","name":"p0","displayName":"예고편","title":"예고편","artists":"2wonsik2/comictool","description":"","cover":"http://cdn.lezhin.com/episodes/sweetguy/p0/cover","banner":"http://cdn.lezhin.com/episodes/sweetguy/p0/banner","social":"http://cdn.lezhin.com/episodes/sweetguy/p0/social","cut":8,"page":0,"type":"p","coin":0,"point":0,"created":1417416185093,"updated":0,"publishDate":"2014-12-01 00:00:00","free":true,"freeDate":"2014-12-01 00:00:00","up":false,"dDay":0,"artistComment":"재밌게 보셨다면 피드백 부탁드립니다~ ^^<br>글작가: <a href=\"https://www.facebook.com/2wonsik2\" target=\"_blank\">https://www.facebook.com/2wonsik2</a><br>그림 작가: <a href=\"https://www.facebook.com/santagoonstudio \" target=\"_blank\">https://www.facebook.com/santagoonstudio </a>","direction":"","published":1417359600000,"freed":1417359600000},{"episodeId":"sweetguy/1","seq":2,"comicId":"sweetguy","name":"1","displayName":"01","title":"1화","artists":"2wonsik2/comictool","description":"","cover":"http://cdn.lezhin.com/episodes/sweetguy/1/cover","banner":"http://cdn.lezhin.com/episodes/sweetguy/1/banner","social":"http://cdn.lezhin.com/episodes/sweetguy/1/social","cut":26,"page":0,"type":"","coin":3,"point":0,"created":1417348840158,"updated":1417416127612,"publishDate":"2014-12-01 00:00:00","free":true,"freeDate":"2014-12-01 00:00:00","up":false,"dDay":0,"artistComment":"재밌게 보셨다면 피드백 부탁드립니다~ ^^<br>글작가: <a href=\"https://www.facebook.com/2wonsik2\" target=\"_blank\">https://www.facebook.com/2wonsik2</a><br>그림 작가: <a href=\"https://www.facebook.com/santagoonstudio \" target=\"_blank\">https://www.facebook.com/santagoonstudio </a>","direction":"","published":1417359600000,"freed":1417359600000}

여기서 "comicId" == #{만화 제목}, "name" == #{에피소드 번호}, "cut" == #{해당 에피소드에 포함된 이미지의 총 개수}와 같은 관계가 있다.

lezhincrawl.py의 get_episode_info()는 바로 이 json파일을 파싱하는 함수이다. "cut"과 "name"을 담은 리스트들을 딕셔너리에 담아 return한다.

			중요 - lezhincrawl.py와 같은 디렉토리내에 Injection으로 얻은 json 내용을 복사하여 comicID.json와 같은 형식으로 저장해두어야한다.


get_image_links()는 get_episode_info()를 토대로 다운로드받을 이미지들의 링크를 for문으로 생성하고, 리스트에 담아 download_images()로 넘기는 함수이다.

download_images()는 get_image_links()에서 생성한 이미지 링크들을 wget으로 다운로드받고 각 episode별로 압축하는 함수이다.
