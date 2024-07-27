import cors from "cors";
import dotenv from "dotenv";
import express from "express";
import logger from "morgan";
import { driver } from "./neo4j";

dotenv.config();

var app = express();

app.use(logger("dev"));
app.use(express.json());
app.use(express.urlencoded({ extended: false }));
app.use(cors({ origin: ["http://localhost:4200", "https://wikisolver.laurensk.at"] }));

app.get("/search", async (req, res) => {
  const from = req.query.from;
  const to = req.query.to;

  if (from == null || to == null) {
    return res.status(400).json({ error: "Invalid param, we need 'from' and 'to'" });
  }

  const session = driver.session();

  try {
    const start = performance.now();

    const result = await session.run(
      `MATCH (start {id: $from}), 
            (end {id: $to}),
            p = shortestPath((start)-[:HAS_LINK_TO*]->(end))
       RETURN p`,
      { from, to }
    );

    const end = performance.now();

    if (result.records.length === 0) {
      return res.status(404).json({ error: "No path found" });
    }

    const path = result.records[0].get("p");
    const pathElements = [path.start.properties.id];

    path.segments.forEach((segment: any) => {
      pathElements.push(segment.end.properties.id);
    });

    return res.json({ path: pathElements, ms: end - start });
  } catch {
    return res.json({ error: "Query failed" });
  } finally {
    session.close();
  }
});

export default app;
