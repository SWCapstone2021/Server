import Router from 'koa-router';
import checkScriptExist from '../../lib/checkScriptExist';
import * as scriptCtrl from './scripts.ctrl';

const scripts = new Router();

/* Test  */
const printInfo = ctx => {
    ctx.body = {
        method: ctx.method,
        path: ctx.path,
        params:ctx.params,
    };
};

scripts.post('/find-word', scriptCtrl.find_word);
scripts.post('/load', scriptCtrl.download_script);
//DB 자막이 있는지 확인 ==> 없으면 생성/있으면 back


export default scripts;