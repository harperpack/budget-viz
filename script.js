/*jslint es6:true*/
//let data = require("./budget.json")
//import data from "./budget.json"
//let d3 = require("https://d3js.org/d3.v5.min.js")

// import * as d3 from 'd3';
//
// let svgWidth = 1000;
// let svgHeight = 300;
//
// let svg = d3.select('svg')
//    .attr("width", svgWidth)
//    .attr("height", svgHeight)
//    .attr("class", "bar-chart");
//
// let dataset = [80, 100, 56, 120, 180, 30, 40, 120, 160];
//
// let JSON = {"revenue":{},"expense":{}};

let TYPE = "expense";

let URL = "https://raw.githubusercontent.com/harperpack/budget-viz/master/budget.json";

// let LEVELS = {"total":"Total","department":"Department","fund":"Fund","unit":"Unit","account":"Account","sub_account":"Item"};

// let LEVELS = [["total","Total"],["department","Department"],["fund","Fund"],["unit","Unit"],["account","Account"],["sub_account","Item"]];

//let LEVELS = {"names": ["total","department","unit","account","sub_account"],"pretty":{"total":"Total","department":"Department","unit":"Unit","account":"Account","sub_account":"Item"}};

// let CURRENT_LEVEL = ["x","Dept6","Dept5","Dept4","Dept3","Dept2","Dept1"];

let CURRENT_LEVEL = ["Dept1","Dept2","Dept3","Dept4","Dept5","Dept6"];

let X_AXIS = {
  "x": {
    "type": "category"
    }
  };

let GRID = {
  "y": {
    "lines": [
      {
        "value": 0
      }
    ]
  }
};

let CHART_ID = "#chart";

let DATA = {
  "x": "x",
  "columns":[
    ["x","Dept1","Dept2","Dept3","Dept4","Dept5","Dept6"],
    ["data1", -30, 200, 200, 400, -150, 250],
    // ["data2", 130, 100, -100, 200, -150, 50],
    // ["data3", -230, 200, 200, -300, 250, 250]
  ],
  "onclick": function(d, element) {
       // d - ex) {x: 4, value: 150, id: "data1", index: 4, name: "data1"}
       // element - <circle>
       console.log(d);
    },
  //groups:[["data1","data2"]],
  "type":"bar"
};


async function loadData(url) {
  const response = await fetch(url).then(response => response.json());
  console.log("Data are fetched.");
  // console.log(response.revenue.Evanston);
  // console.log(JSON);
  JSON = response;
  setSchema(JSON["schema"]);
  // SCHEMA = JSON["schema"]
  updateLevel(SCHEMA[0]);
};

function setSchema(schema) {
  // console.log(schema);
  select = document.getElementById('schema');
  schema.forEach(
    function(level) {
      let option = document.createElement("option");
      option.text = level;
      select.add(option);
      SCHEMA.push(level);
    }
  );
  // for (let i = 0; i < schema.length; i++) {
  //   console.log(schema[i]);
  //   console.log('--');
  //   let option = document.createElement("option");
  //   option.text = schema[i];
  //   select.add(option);
  //   SCHEMA.push(schema[i]);
  // }
}

function updateLevel(level) {
  if (typeof level == 'undefined') {
    let select = document.getElementById('schema');
    level = select.options[select.selectedIndex].text;
  }
  console.log(level);
  // console.log(TYPE);
  // console.log(JSON);
  // console.log(JSON[TYPE]);
  // console.log(level);
  let cols = [["x"],[level]];
  let pairs = [];
  // console.log(cols);
  for (const entry in JSON[TYPE]) {
    // console.log(entry);
    if (JSON[TYPE][entry]["type"] == level) {
      // console.log(cols);
      pairs.push([entry,JSON[TYPE][entry]["members"]["total"][0]]);
    }
    else {
      // console.log(JSON[TYPE][entry]["type"]);
    }
  }
  //console.log(pairs);
  pairs.sort(
    function(a, b) {
      // console.log(x[1]);
      if (a[1] < b[1]) {
        return 1;
      }
      if (a[1] > b[1]) {
        return -1;
      }
      else {
        return 0;
      }
    }
  );
  // console.log(pairs);
  // console.log(pairs[0])
  pairs.forEach(
    function(pair) {
      cols[0].push(pair[0]);
      cols[1].push(pair[1]);
    }
  );
      // cols[0].push(entry);
      // cols[1].push(JSON[TYPE][entry]["members"]["total"][0]);
    // } else {
    //   // console.log(level);
    // }
  DATA["columns"] = cols;
  displayChart();
  }

loadData(URL);
// // let data = loadData(url)
// // console.log(data.revenue.Evanston);
//
// let d = new Date();
// document.body.innerHTML = "<h1>Today's date is " + d + "</h1>"


function displayChart() {
  try {
    bb.generate({
      "data": DATA,
      "axis": X_AXIS,
      "grid": GRID,
      "bindto": CHART_ID
    });
  }
  catch (e) {
    console.log(e);
  }
  console.log("We built the chart.");
}
