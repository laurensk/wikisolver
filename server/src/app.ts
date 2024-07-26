import dotenv from "dotenv";
import express from "express";
import logger from "morgan";

dotenv.config();

var app = express();

app.use(logger("dev"));
app.use(express.json());
app.use(express.urlencoded({ extended: false }));

app.get("/", (req, res) => {
  return res.json({ hi: "works" });
});

export default app;
