import axios from 'axios';
import { admin,  database} from '../../firebase';
import Orders from '../model/Orders';


const firebase_DB = admin.database();

/* 결제 정보 저장 */
/*  export const test = async (ctx) => {
  const userRef = database.ref('/users').child("lrYDv8ANtPMrG0lsRaPLJM3qviG2");
  const a = "1";
  const b = "2";
  const c = "3";
  userRef.update({ set: { a, b, c }});
  console.log('hi')
}  */

export const payment_request = async (ctx) => {
  const {
    pg,
    pay_method,
    merchant_uid,
    user_uid,
    name,
    amount,
    buyer_email,
    buyer_name,
    buyer_tel
  } = ctx.request.body;

  const new_order = new Orders({
    pg,
    pay_method,
    merchant_uid,
    user_uid,
    name,
    amount,
    buyer_email,
    buyer_name,
    buyer_tel
});

try {
    await new_order.save();
    ctx.status = 200;
    ctx.body = "Order information successfully created.";
} catch (e) {
    ctx.throw(500, e);
}
}

/* 결제 진행 */
export const payment_complete = async (ctx) => {

    try {
      const { imp_uid, merchant_uid } = ctx.request.body; // req의 body에서 imp_uid, merchant_uid 추출
      // 액세스 토큰(access token) 발급 받기
      const getToken = await axios({
        url: "https://api.iamport.kr/users/getToken",
        method: "post", // POST method
        headers: { "Content-Type": "application/json" }, // "Content-Type": "application/json"
        data: {
          imp_key: "imp_apikey", // REST API키
          imp_secret: "ekKoeW8RyKuT0zgaZsUtXXTLQ4AhPFW3ZGseDA6bkA5lamv9OqDMnxyeB9wqOsuO9W3Mx9YSJ4dTqJ3f" // REST API Secret
        }
      });
      const { access_token } = getToken.data.response; // 인증 토큰
      
      // imp_uid로 아임포트 서버에서 결제 정보 조회
      const getPaymentData = await axios({
        url: `https://api.iamport.kr/payments/${imp_uid}`, // imp_uid 전달
        method: "get", // GET method
        headers: { "Authorization": access_token } // 인증 토큰 Authorization header에 추가
      });

      const paymentData = getPaymentData.data.response; // 조회한 결제 정보
      
      // DB에서 결제되어야 하는 금액 조회
      const order = await Orders.findById(paymentData.merchant_uid);
      const {user_id} = order;
      const amountToBePaid = order.amount; // 결제 되어야 하는 금액
      
      // 결제 검증하기
      const { amount, status } = paymentData;
      if (amount === amountToBePaid) { // 결제 금액 일치. 결제 된 금액 === 결제 되어야 하는 금액
        await Orders.findByIdAndUpdate(merchant_uid, { $set: paymentData }); // DB에 결제 정보 저장
        
        switch (status) {
          case "ready": // 가상계좌 발급
            // DB에 가상계좌 발급 정보 저장
            {
                const { vbank_num, vbank_date, vbank_name } = paymentData;
                const userRef = database.ref('/users').child(user_id/* user_id */);
                await userRef.update({ set: { vbank_num, vbank_date, vbank_name }});

               // await Users.findByIdAndUpdate("/* 고객 id */", { $set: { vbank_num, vbank_date, vbank_name }});
                // 가상계좌 발급 안내 문자메시지 발송
                /* SMS?
                SMS.send({ text: `가상계좌 발급이 성공되었습니다. 계좌 정보 ${vbank_num} \${vbank_date} \${vbank_name}`}); 
                 */
                ctx.body = ({ status: "vbankIssued", message: "가상계좌 발급 성공" });
                break;
            }
          case "paid": // 결제 완료
            {
                ctx.status = 200;
                ctx.body = ({ status: "success", message: "일반 결제 성공" });
                break;
            }
        }
      } else { // 결제 금액 불일치. 위/변조 된 결제
        ctx.throw(400, new Error({ status: "forgery", message: "위조된 결제시도" }));
      }
    } catch (e) {
      ctx.throw(400, e);
    }
}