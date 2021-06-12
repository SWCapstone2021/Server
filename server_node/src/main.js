require('dotenv').config();
import Koa from 'koa';
import Router from 'koa-router';
import bodyParser from 'koa-bodyparser';
import mongoose from 'mongoose';
import api from './api';
import payments from './payments';
import cors from '@koa/cors';
import koaLogger from 'koa-logger-winston';
import { logger, stream } from '../config/winston';
import morgan from 'koa-morgan';

/*fire base---- */


//const https = require('https');
const http = require('http');
const { HTTP_PORT, MONGO_URI } = process.env;
const app = new Koa();
const router = new Router();
const fs = require('fs');
let server;
let DB;

DB = mongoose.connect(MONGO_URI,
  {
    useNewUrlParser: true,
    useFindAndModify: false
  })
  .then(() => {
    console.log("DB connection success");
  })
  .catch(e => {
    console.log(e);
  });

router.use('/api', api.routes());
router.use('/payments', payments.routes());
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
export { server, DB };
