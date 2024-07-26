const { writeFileSync } = require("node:fs");

const main = async () => {


    const res = await fetch("https://dumps.wikimedia.org/index.json");
    const json = await res.json();

    const jobs = json.wikis.dewiki.jobs;
    const sub = jobs.articlesdumprecombine ?? jobs.articlesdump;

    const file = sub.files[Object.keys(sub.files)[0]];
    const url = file.url;

    const fullUrl = "https://dumps.wikimedia.org" + url;
    const fileName = fullUrl.split("/").reverse()[0];

    console.log(fullUrl)

    // console.log(file.size);
    // console.log("Downloading " + fileName + " - please wait...")

    // const fileRes = await fetch(fullUrl);
    // const buffer = await fileRes.arrayBuffer();

    // fs.writeFileSync(fileName, Buffer.from(buffer))

    // console.log("Done!")

};

main();
