import Router from 'koa-router';
import * as paymentsCtrl from './payments.ctrl';

const payments = new Router();

// 1.결제 정보 생성(저장)
payments.post('/complete', paymentsCtrl.payment_complete);
payments.post('/request', paymentsCtrl.payment_request);
//payments.get('/', paymentsCtrl.test);

export default payments;