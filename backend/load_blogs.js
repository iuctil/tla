#!/usr/bin/env node
const fs = require('fs');
const Parser = require('rss-parser');
const parser = new Parser();

(async ()=>{
  const feed = await parser.parseURL("http://federaltelemedicine.com/?feed=rss2");
  console.dir(feed);
  /*
  {
  items: [
    {
      creator: 'Carolyn Bloch',
      title: 'Ideas to Advance Breakthroughs',
      link: 'http://federaltelemedicine.com/?p=9544',
      pubDate: 'Mon, 12 Jul 2021 09:19:56 +0000',
      'dc:creator': 'Carolyn Bloch',
      comments: 'http://federaltelemedicine.com/?p=9544#comments',
      content: 'The Presidents proposed FY 2022 budget requests $6.5 billion to create the Advanced Research Projects Agency for Health (ARPA-H) to be housed within NIH. The goal is to develop breakthroughs to prevent, detect, and treat diseases like Alzheimer’s, diabetes, and cancer.  In an article published in Science, White House Office of Science and Technology Policy [&#8230;]',
      contentSnippet: 'The Presidents proposed FY 2022 budget requests $6.5 billion to create the Advanced Research Projects Agency for Health (ARPA-H) to be housed within NIH. The goal is to develop breakthroughs to prevent, detect, and treat diseases like Alzheimer’s, diabetes, and cancer.  In an article published in Science, White House Office of Science and Technology Policy […]',
      guid: 'http://federaltelemedicine.com/?p=9544',
      categories: [Array],
      isoDate: '2021-07-12T09:19:56.000Z'
    },
  */
    feed.items.forEach(item=>{
        const pageid = item.link.split("?p=")[1]; //link: 'http://federaltelemedicine.com/?p=9544',
        const id = "federaltelemedicine."+pageid;
        const filepath = __dirname+"/../content/blog/"+id+".md";

        //if(fs.existsSync(filepath)) return; //don't write if it already exists

        //remove non ascii
        for(let key in item) {
            if(typeof item[key] == "string") {
                item[key] = item[key].replace(/[^\x00-\x7F]/g, "");
            }
            //TODO categories is an array.. we should handle array?
        }

        //replace trailing "[&#8230;]" with ...
        item.content = item.content.replace("[&#8230;]", "...");

        const content = `---
source: "http://federaltelemedicine.com"
title: "${item.title}"
description: "todo.."
lead: "${item.content}"
date: ${item.isoDate}
lastmod: ${item.isoDate}
draft: false
extlink: "${item.link}"
images: []
categories: [${item.categories.map(cat=>'"'+cat+'"')}]
contributors: ["${item.creator}"]
---
`;
        console.log("writing", id);
        console.log(content);
        fs.writeFileSync(filepath, content, {encoding: "ascii"});
    });
})();
