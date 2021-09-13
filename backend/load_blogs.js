#!/usr/bin/env node
const fs = require('fs');
const Parser = require('rss-parser');
const parser = new Parser();

const cyrb53 = function(str, seed = 0) {
    let h1 = 0xdeadbeef ^ seed, h2 = 0x41c6ce57 ^ seed;
    for (let i = 0, ch; i < str.length; i++) {
        ch = str.charCodeAt(i);
        h1 = Math.imul(h1 ^ ch, 2654435761);
        h2 = Math.imul(h2 ^ ch, 1597334677);
    }
    h1 = Math.imul(h1 ^ (h1>>>16), 2246822507) ^ Math.imul(h2 ^ (h2>>>13), 3266489909);
    h2 = Math.imul(h2 ^ (h2>>>16), 2246822507) ^ Math.imul(h1 ^ (h1>>>13), 3266489909);
    return 4294967296 * (2097151 & h2) + (h1>>>0);
};

async function loadFeed(rssUrl, key) {
  //const feed = await parser.parseURL("http://federaltelemedicine.com/?feed=rss2");
  //const feed = await parser.parseURL("https://www.phe.gov/ASPRBlog/_layouts/15/listfeed.aspx?List=f59454e5-a08d-4a13-9abe-0d31ef99f1af");
  const feed = await parser.parseURL(rssUrl);
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
        //const pageid = item.link.split("?p=")[1]; //link: 'http://federaltelemedicine.com/?p=9544',
        //const id = key+"."+pageid;
        const id = cyrb53(item.guid);
        console.log(item.guid, id);
        const filepath = __dirname+"/../content/bplp/external/"+key+"/"+id+".md";

        //if(fs.existsSync(filepath)) return; //don't overwrite if it already exists

        //remove non ascii
        for(let key in item) {
            if(typeof item[key] == "string") {
                item[key] = item[key].replace(/[^\x00-\x7F]/g, "");
            }
            //TODO categories is an array.. we should handle array?
        }

        //replace trailing "[&#8230;]" with ...
        item.content = item.contentSnippet.replace("[&#8230;]", "...");

        const content = `---
source: "${key}"
title: "${item.title}"
description: "todo.."
lead: "${item.content}"
date: ${item.isoDate}
lastmod: ${item.isoDate}
draft: false
extlink: "${item.link}"
extcategories: [${item.categories.map(cat=>'"'+cat+'"')}]
contributors: ["${item.creator}"]
toc: false
#menu:
#  blog:
#    parent: "external"
---
`;
        console.log("writing", id);
        console.log(content);
        fs.writeFileSync(filepath, content, {encoding: "ascii"});
    });
}

loadFeed("https://tools.cdc.gov/api/v2/resources/media/404952.rss", "cdc");
//loadFeed("https://thedigitalresponder.wordpress.com/feed/", "thedigitalresponder");
//loadFeed("http://federaltelemedicine.com/?feed=rss2", "federaltelemedicine");
//loadFeed("https://www.phe.gov/ASPRBlog/_layouts/15/listfeed.aspx?List=f59454e5-a08d-4a13-9abe-0d31ef99f1af", "phe-aspr");


