import mongoose, { Schema } from 'mongoose';
import bcrypt from 'bcrypt';
import jwt from 'jsonwebtoken';



const UserSchema = new Schema({
    email: {type: String, required: true, unique: true, lowercase: true},
    user_name: { type: String, required: true, trim: true},
    hashedPassword: {type: String, required: true, trim: true},
    phoneNumber: {type: String, required: true},
    Permission: { type: Number, required: true, default: 0}
});

UserSchema.methods.setPassword = async function(pw) {
    const hash = await bcrypt.hash(pw, 10);
    this.hashedPassword = hash;
};

UserSchema.methods.checkPassword = async function(pw) {
    const result = await bcrypt.compare(pw, this.hashedPassword);
    return result;
};

UserSchema.methods.serialize = function() {
    const data = this.toJSON();
    delete data.hashedPassword;
    return data;
};

UserSchema.methods.generateToken = function() {
  const token = jwt.sign(
      {
          _id: this.id,
          username: this.username,
      },
      process.env.JWT_SECRET,
      {
          expiresIn: '7d'
      },
  );
  return token;  
};

UserSchema.statics.findByUsername = function(username) {
    return this.findOne({username});
};

const User = mongoose.model('User', UserSchema);

export default User;