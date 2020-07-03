/*jslint es6:true*/
//let data = require("./budget.json")
//import data from "./budget.json"
//let d3 = require("https://d3js.org/d3.v5.min.js")
//
//let svgWidth = 500;
//let svgHeight = 300;
//
//let svg = d3.select('svg')
//    .attr("width", svgWidth)
//    .attr("height", svgHeight)
//    .attr("class", "bar-chart");

function loadData(url) {
    fetch(url).then(response => response.json());
    return response.json();
}

let data = loadData("http://0.0.0.0:8888/budget.json")

let d = new Date();
document.body.innerHTML = "<h1>Today's date is " + d + "</h1>"
