import admin from "firebase-admin";
import credentials from "../../../credential.json";

//const Firebase_Auth = admin.initializeApp();
admin.initializeApp({
    credential: admin.credential.cert(credentials),
    databaseURL: "https://findyou.firebaseio.com"
    });

export const login = (ctx,next) => {

  const headerToken = ctx.request.headers.authorization;
  if (!headerToken) {
    return ctx.throw({ message: "No token provided" }).status(401);
  }

  if (headerToken && headerToken.split(" ")[0] !== "Bearer") {
      ctx.throw({ message: "Invalid token" }).status(401);
  }

  const token = headerToken.split(" ")[1];
    admin
    .auth()
    .verifyIdToken(token)
    .then(() => next())
    .catch(() => ctx.throw({ message: "Could not authorize" }).status(403));
}

export const logout = ctx => {

}

export const register = ctx => {

}

