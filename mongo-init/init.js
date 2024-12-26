db = db.getSiblingDB("users");
db.createCollection("user_info");

db.user_info.insertOne({
  name: "Test",
  email: "test@gmail.com",
  password: "Test123",
});
