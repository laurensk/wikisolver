import { auth, driver as neo4jDriver } from "neo4j-driver";

export const driver = neo4jDriver("bolt://127.0.0.1:7687", auth.basic("neo4j", "securePassword123"));
