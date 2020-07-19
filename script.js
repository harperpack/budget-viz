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

let SCHEMA = [];

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
  updateLevel(LEVELS["names"][1]);
  displayChart();
};



function updateLevel(level) {
  console.log("trumpet");
  // console.log(TYPE);
  // console.log(JSON);
  // console.log(JSON[TYPE]);
  let cols = [["x"],[LEVELS["pretty"][level]]];
  let pairs = [];
  // console.log(cols);
  for (const entry in JSON[TYPE]) {
    // console.log(entry);
    if (JSON[TYPE][entry]["type"] == level) {
      // console.log(cols);
      pairs.push([entry,JSON[TYPE][entry]["members"]["total"][0]]);
    }
  }
  console.log(pairs);
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
  console.log(pairs[0])
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
  }
  // console.log(cols);
  // DATA["columns"] = cols;
  // console.log(DATA["columns"]);
  //console.log(JSON.TYPE.Evanston);
// }
//
// function returnSelection(spec, level, source, format) {
//   // let outputValues = [];
//   // let outputLabels = [];
//   let output = [];
//   for (const name in json.spec) {
//     if (json.spec.name.type == level) {
//       for (const sourceName in json.spec.name.members) {
//         if (sourceName == source) {
//           let tuple = [json.spec.name.members.sourceName[format],sourceName];
//           output.push(tuple);
//           // outputValues.push(json.spec.name.members.sourceName[format]);
//           // outputLabels.push(sourceName);
//         }
//       }
//     }
//   }
//   return output;
// };
//
// // function printEvanston() {
// //   let data = loadData(url);
// //   console.log(data.revenue.Evanston);
// // }
//
// // printEvanston();
loadData(URL);
// // let data = loadData(url)
// // console.log(data.revenue.Evanston);
//
// let d = new Date();
// document.body.innerHTML = "<h1>Today's date is " + d + "</h1>"


function displayChart() {
  bb.generate({
    "data": DATA,
    "axis": X_AXIS,
    "grid": GRID,
    "bindto": CHART_ID
  });
  console.log("We built the chart.");
}

// let chart = bb.generate({
//   data: {
//     columns: [
// 	["data1", -30, 200, 200, 400, -150, 250],
// 	["data2", 130, 100, -100, 200, -150, 50],
// 	["data3", -230, 200, 200, -300, 250, 250]
//     ],
//     type: "bar",
//     groups: [
//       [
//         "data1",
//         "data2"
//       ]
//     ]
//   },
//   grid: {
//     y: {
//       lines: [
//         {
//           value: 0
//         }
//       ]
//     }
//   },
//   bindto: "#chart"
// });
