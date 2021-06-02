import Router from 'koa-router';
import * as authAPI from './auth.ctrl';

const auth = new Router();

auth.get('/login', authAPI.login);

export default auth;