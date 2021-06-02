import Router from 'koa-router' ;
import scripts from './scripts';
import auth from './auth';
import ML from './ml';

const api = new Router();

api.use('/scripts', scripts.routes());
api.use('/auth',auth.routes());
api.use('/ml', ML.routes());


export default api;