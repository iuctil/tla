
const keys = require('./keys');

exports.mag = {
  apiKey: keys.magApiKey,
}

//list of papers to show under reference section
//we can query for related papers, papers cited, etc from MAG, probably..

exports.papers = [
  {
    doi: "https://doi.org/10.1089/tmj.2014.9983",
    name: "Telemedicine and e-Health in Disaster Response",
    journal: "Telemedicine and e-Health",
    date: new Date("2012-06-27"),
  },

  {
    doi: "https://doi.org/10.1089/tmj.2017.0237",
    name: "Development and Validation of Telemedicine for Disaster Response: The North Atlantic Treaty Organization Multinational System",
    journal: "Telemedicine and e-Health",
    date: new Date("2018-09-14"),
  },
]
