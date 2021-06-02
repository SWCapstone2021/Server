import mongoose from 'mongoose';

const { Schema } = mongoose;
const OrderSchema = new Schema({
    pg: String,
    pay_method: String,
    merchant_uid: String,
    user_uid: String,
    name: String,
    amount: Number,
    buyer_email: String,
    buyer_name: String,
    buyer_tel: String,
});

const Orders = mongoose.model('Orders', OrderSchema);
export default Orders;