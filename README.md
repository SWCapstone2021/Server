# Server

## Introduction


![image](https://user-images.githubusercontent.com/54361266/121766250-a25f9d80-cb8b-11eb-9702-b5cdd0e66913.png)

본 프로젝트는 2021년도 1학기 아주대학교 정보통신대학 소프트웨어학과에서 개설된 SW 캡스톤 디자인 과목을 수강하는 동안 개발했습니다. 찾아봐유는 유튜브에서 제공하는 자막을 이용하여, 동영상 내에서 사용자가 검색을 하면, 해당 내용이 포함된 위치를 알려주는 서비스입니다.

## Service Architecture

FindU의 대략적인 아키텍쳐입니다.

![구조도](https://user-images.githubusercontent.com/54361266/121766298-d044e200-cb8b-11eb-843e-7ea9ed13740d.PNG)

1.Reverse Proxy: Nginx

2.API Server: Nodejs(Koa)

3.ML Server: Flask

4.Database: MongoDB

*Chrome Browser는 Https를 강제하기 때문에 https 인증이 필요합니다. 따라서 FindU에서는 Nginx에서 https 인증을 처리하도록 했습니다.

*ML Server는 GPU를 사용하기 때문에, GPU를 가용하고 있는 자체 서버를 활용했습니다.



## License

This application is freely available for free non-commercial use, and may be redistributed under these conditions. Please, see the [license](https://github.com/Algostu/dodam-appserver/blob/master/LICENSE) for further details.
