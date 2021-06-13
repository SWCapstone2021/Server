# Server

## Introduction



<br/>
<p align="center">
    <img src="./logo-com.svg"/>
    <br/>
  <h4 align="center">스크립트 기반 영상 검색 및 요약 서비스</h4>
</p>
  <br/>
  <p align = "center">
  <a href="https://github.com/SWCapstone2021/Server/actions/workflows/cd.yml">
    <img src = "https://github.com/SWCapstone2021/Server/actions/workflows/cd.yml/badge.svg">
    </a>
  <a href="https://github.com/SWCapstone2021/Server/actions/workflows/ci.yml">
    <img src = "https://github.com/SWCapstone2021/Server/actions/workflows/ci.yml/badge.svg">
    </a>
    <a href="https://github.com/SWCapstone2021/Server/issues">
        <img src="https://img.shields.io/github/issues/SWCapstone2021/Server"/>
    </a>
    <a href="https://github.com/SWCapstone2021/Server/pulls">
        <img src="https://img.shields.io/github/forks/SWCapstone2021/Server"/>
    </a>
    <a href="https://github.com/SWCapstone2021/Server/stargazers">
        <img src="https://img.shields.io/github/stars/SWCapstone2021/Server"/>
    </a>
    <a href="https://github.com/SWCapstone2021/Server/blob/m/LICENSE">
        <img src="https://img.shields.io/github/license/SWCapstone2021/Server"/>
    </a> <br/>
  </p>
<p align = "center">
<img src="https://img.shields.io/badge/Node.js-339933?style=flat-square&logo=nodejs&logoColor=white"/>
<img src="https://img.shields.io/badge/Docker-2496ED?style=flat-square&logo=docker&logoColor=white"/>
<img src="https://img.shields.io/badge/Nginx-009639?style=flat-square&logo=nginx&logoColor=white"/>
<img src="https://img.shields.io/badge/MongoDB-47A248?style=flat-square&logo=mongodb&logoColor=white"/>
<img src="https://img.shields.io/badge/flask-000000?style=flat-square&logo=flask&logoColor=white"/>
<img src="https://img.shields.io/badge/jest-C21325?style=flat-square&logo=jest&logoColor=white"/>
<img src="https://img.shields.io/badge/pm2-2B037A?style=flat-square&logo=pm2&logoColor=white"/>
</p>
<p align="center"> •
  <a href="#environments">Environments</a> • 
  <a href="#system-structure">System Structures</a> • 
  <a href="#contributor">Contributors</a> • 
  <a href="#license">License</a>
</p>
<br>

본 프로젝트는 2021년도 1학기 아주대학교 정보통신대학 소프트웨어학과에서 개설된 SW 캡스톤 디자인 과목을 수강하는 동안 개발했습니다. 찾아봐유는 유튜브에서 제공하는 자막을 이용하여, 동영상 내에서 사용자가 검색을 하면, 해당 내용이 포함된 위치를 알려주는 서비스입니다.

## Environments
- Linux-ubuntu LTS 16.04
- node v12.22.1
- python v3.6.9
- nginx/1.14.0
- Docker version 20.10.6


## system-structure

FindU의 대략적인 아키텍쳐입니다.

![구조도](https://user-images.githubusercontent.com/54361266/121766298-d044e200-cb8b-11eb-843e-7ea9ed13740d.PNG)

1.Reverse Proxy: Nginx

2.API Server: Nodejs(Koa)

3.ML Server: Flask

4.Database: MongoDB

*Chrome Browser는 Https를 강제하기 때문에 https 인증이 필요합니다. 따라서 FindU에서는 Nginx에서 https 인증을 처리하도록 했습니다.

*ML Server는 GPU를 사용하기 때문에, GPU를 가용하고 있는 자체 서버를 활용했습니다.

## Contributor

Maintainer : 허범수

Contributor : 강한결, 김수연, 남희수, 오승민


## License

This application is freely available for free non-commercial use, and may be redistributed under these conditions. Please, see the [license](https://github.com/Algostu/dodam-appserver/blob/master/LICENSE) for further details.
