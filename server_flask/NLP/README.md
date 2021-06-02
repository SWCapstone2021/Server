# FindU NLP
이 프로젝트는 2021 Ajou University Spring SW capstone design 과목의 일환으로 진행되었습니다.

해당 repository는 찾아봐유의 **NLP** 소스코드를 저장하고 있습니다. 



## Features

### STT

**찾아봐유**를 사용하기 위해서는 영상의 script가 필요하다. 하지만 유튜브에서는 script가 없는 영상이 많고 '자막 자동 생성 기능'이 있지만 한국어의 경우 제대로 자막 생성이 이루어지지 않아 ***한국어에 맞는 STT model을 제작***하여 사용하고자 한다.

Dataset : ClovaCall, AIHub

Model : [ClovaCall](https://github.com/clovaai/ClovaCall)

Period : Iteration 1~3

### script추출하기
from basefunction.FindUMethod import MakeVttFile를 해야하며 MakeVttFile 메소드를 사용하여 subtitle을 추출한다. 파라미터로는  subtitle를 추출하고자하는 동영상의 URL을 넣어주면 된다. 기본적으로  script는 
"WEBVTT
Kind: captions
anguage: ko "
로 시작하며 5번째 줄부터 해당 동영상의 script내용이 담겨있다.
업로더가 직접 업로드한 script를 추출하면 "시작시간 --> 종료시간\n 해당시간의 대사\n\n"형식으로 구성되어 있고 유튜브에서 자동생성한 script를 추출한 경우, "시작시간\n해당시간의 대사\n"형식으로 구성되어 있다.  

### Ctrl+F기능
from basefunction.FindUMethod import Ctrl_F를 해야하며 Ctrl_F메소드를 사용하여 해당 키워드가 동영상의 어떤 구간에 있는지 찾아준다. 파라미터로는 찾고자하는 키워드와 동영상의 URL를 넣어주면 된다. 키워드를 입력하면 키워드가 속해있는 대사가 시작하는 시간을 리스트형식으로 return한다.(ex. 00:00:00.00)

### 신뢰도 기능
from basefunction.FindUMethod import Frequency를 해야하며 Frequency메소드를 사용하여 TF-IDF를 사용한다. '찾아봐유'는 Tf-idf를 변형하여 사용하였다. 본래의 TF-IDF는 TF * (log(N/df)) TF:단어 빈도수, N: 문서개수, IDF: 단어가 포함된 문서개수로 계산을 진행하는데 이 기능에서는 N:총 문장의 개수, ILF: 단어가 포함된 문장의 개수로 계산을 진행한다. return할 경우 TF-ILF에 해당하는 값이 나온다.
### Word Embedding

### QA System

### Summarization



## Contributor

Maintainer : 남희수, 오승민

Contributor : 강한결, 김수연, 허범수



## License
MIT License