// initialise mongodb database which is supposed to inside the docker container called "mongodb"
db = db.getSiblingDB("users");
db.createCollection("user_info");

db.user_info.insertOne({
  name: "Test",
  email: "test@gmail.com",
  password: "Test123",
});
