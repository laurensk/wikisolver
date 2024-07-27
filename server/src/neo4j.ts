import { auth, driver as neo4jDriver } from "neo4j-driver";

export const driver = neo4jDriver(
  process.env.NODE_ENV == "production" ? "bolt://neo4j:7687" : "bolt://127.0.0.1:7687",
  auth.basic("neo4j", "securePassword123")
);
