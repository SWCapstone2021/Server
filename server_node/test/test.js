require('dotenv').config();
import Koa from 'koa';
import Router from 'koa-router';
import bodyParser from 'koa-bodyparser';
import mongoose from 'mongoose';
import api from '../src/api';
import cors from '@koa/cors';
import { stream } from '../config/winston';
import morgan from 'koa-morgan';
import { assert } from 'console';
const should = require('should');
const http = require('http');
const { HTTP_PORT, MONGO_URI } = process.env;
const app = new Koa();
const router = new Router();
const request = require('supertest');
let server;

const video_id = '8LuyIt61cn0';
const video_id_err = '0GOBecqH4gY';
const video_id_arr = ['8LuyIt61cn0', '8LuyIt61cn0', '8LuyIt61cn0'];

const keyword = '물가';
const keyword_err = '그럼에도불구하고';
const question = '물가 상승이 일어날까';





router.use('/api', api.routes());
app.proxy = true;

//app.use( async (ctx, next) => {
//	stream.write(`Request from ${ctx.request.ip}`);
//	next();
//});
app.use(morgan('HTTP/:http-version :method :remote-addr :url :remote-user :status :res[content-length] :referrer :user-agent :response-time ms', { stream }));
app.use(bodyParser());
app.use(cors());
app.use(router.routes()).use(router.allowedMethods());


/* app.listen(HTTP_PORT, ()=> {
    console.log(`Listening to Port ${HTTP_PORT}..`);
});
 */
beforeAll(() => {
    mongoose.connect(MONGO_URI,
        {
            useNewUrlParser: true,
            useFindAndModify: false
        })
        .then(() => {
            console.log('DB connection success');
        })
        .catch(e => {
            console.log('DB connection fail');
        });


    const appCallback = app.callback();
    try {
        var httpServer = http.createServer(appCallback);
        server = httpServer
            .listen(HTTP_PORT, function (err) {
                if (err) {
                    console.error('HTTP server FAIL: ', err, (err && err.stack));
                }
                else {
                    console.log(`HTTP  server OK:`);
                }
            });
    }
    catch (ex) {
        console.error('Failed to start HTTP server\n', ex, (ex && ex.stack));
    }
});

describe('API TEST', () => {
    describe('POST /api/scripts/load', () => {
        it('자막을 찾았다면, 자막을 리턴한다.', async () => {
            return await request(server)
                .post('/api/scripts/load')
                .send({ video_id })
                .set('Accept', 'application/json')
                .expect('Content-Type', /json/)
                .expect(200)
                .then(res => {
                    assert(res.body.should.have.property('video_id'), true);
                    assert(res.body.should.have.property('scriptions'), true);
                });
        });

        it('자막이 없다면, 에러를 리턴한다.', async () => {
            return await request(server)
                .post('/api/scripts/load')
                .send({ video_id: video_id_err })
                .expect(500)
        })
    });


    describe('POST /api/scripts/find-word', () => {
        it('자막이 있는 영상에 검색어를 전달하면, 자막의 내용중에 검색어가 포함된 문장을 리턴한다.', async () => {
            return await request(server)
                .post('/api/scripts/find-word')
                .send({ video_id, keyword })
                .set('Accept', 'application/json')
                .expect('Content-Type', /json/)
                .expect(200)
                .then(res => {
                    assert(res.body.should.have.property('video_id'), true);
                    assert(res.body.should.have.property('result'), true);
                });
        });

        it('자막이 없다면 검색을 할 수 없다.', async () => {
            return await request(server)
                .post('/api/scripts/find-word')
                .send({ video_id: video_id_err, keyword })
                .expect(500)
        });
    });


    describe('POST /api/ml/qa', () => {
        it('자막이 있는 영상의 question을 보내면 그에 대한 answer를 받는다.', async () => {
            return await request(server)
                .post('/api/ml/qa')
                .send({ video_id, question })
                .set('Accept', 'application/json')
                .expect('Content-Type', /json/)
                .expect(200)
                .then(res => {
                    assert(res.body.should.have.property('video_id'), true);
                    assert(res.body.should.have.property('question'), true);
                    assert(res.body.should.have.property('answer'), true);
                });
        }, 1000 * 30);

        it('자막이 없다면 질문을 할 수 없다', async () => {
            return await request(server)
                .post('/api/ml/qa')
                .send({ video_id: video_id_err, question })
                .expect(500)
        }, 1000 * 30);
    });


    describe('POST /api/ml/summarization', () => {
        it('자막이 있는 영상의 video_id를 보내면 해당 영상에 대한 summarization 결과를 리턴', async () => {
            return await request(server)
                .post('/api/ml/summarization')
                .send({ video_id })
                .set('Accept', 'application/json')
                .expect('Content-Type', /json/)
                .expect(200)
                .then(res => {
                    assert(res.body.should.have.property('video_id'), true);
                    assert(res.body.should.have.property('summarization'), true);
                });
        });

        it('자막이 없다면 요약을 할 수 없다', async () => {
            return await request(server)
                .post('/api/ml/summarization')
                .send({ video_id: video_id_err })
                .expect(500)
        });
    });



    describe('POST /api/ml/association', () => {
        it('자막이 있는 동영상에서 검색어와 유사한 키워드를 자막에서 찾는다면, 그 키워드들이 포함된 문장을 리턴', async () => {
            return await request(server)
                .post('/api/ml/association')
                .send({ video_id, keyword })
                .set('Accept', 'application/json')
                .expect('Content-Type', /json/)
                .expect(200)
                .then(res => {
                    assert(res.body.should.have.property('video_id'), true);
                    assert(res.body.should.have.property('keyword'), true);
                    assert(res.body.should.have.property('result'), true);
                });
        });

        it('자막이 없다면 키워드 검색을 할 수 없다.', async () => {
            return await request(server)
                .post('/api/ml/association')
                .send({ video_id: video_id_err, keyword })
                .expect(500)
        });
    });

    describe('POST /api/ml/freq', () => {
        it('검색 결과로 나온 동영상의 신뢰도 계산', async () => {
            return await request(server)
                .post('/api/ml/freq')
                .send({ video_id: video_id_arr })
                .set('Accept', 'application/json')
                .expect('Content-Type', /json/)
                .expect(200)
                .then(response => {
                    const res = response.body;
                    const result = res.result;
                    expect(typeof result).toBe('object');
                    expect(result.length).not.toEqual(0);
                });
        });
    });

});

afterAll(() => {
    mongoose.disconnect();
    server.close();
});

