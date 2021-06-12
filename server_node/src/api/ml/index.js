import Router from 'koa-router';
import * as mlCtrl from './ml.ctrl';

const ML = new Router();

ML.post('/qa', mlCtrl.QAsystem);
ML.post('/summarization', mlCtrl.Summarization);
ML.post('/freq', mlCtrl.cosinsimilar);
ML.post('/association', mlCtrl.wordEmbedding);
//ML.post('/stt')

export default ML;