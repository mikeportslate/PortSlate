$(document).ready(function() {

    plotBarChart();
    plotPieChart();

});	


function plotBarChart(labels, data1, data2) {

    var ctx = document.getElementById("AuMHistory");
    ctx.height = 300

    var config = {
        type: 'bar',
        data: {
            labels: [2014, 2015, 2016, 2017, 2018],
            datasets: [{
                label: 'AuM ($bn)',
                backgroundColor: "#26B99A",
                data: [108, 120, 148, 166, 194]
            }]
        },
        options: {
            maintainAspectRatio: false,
            responsive: true,
            scales: {
            yAxes: [{
                ticks: {
                beginAtZero: true
                }
            }]
            }
        }		
    }
    var mylineChart4 = new Chart(ctx, config);	

};

function plotPieChart(labels, data1, data2) {

    var ctx = document.getElementById("AUMType");
    ctx.height = 300

    var config = {
        type: 'pie',
        data: {
            labels: ['Pension Assets', 'Insurance', 'Soverign Wealth Funds','Charities','Family Office','Others'],
            datasets: [{
                label: 'AuM ($bn)',
                backgroundColor:[
                    "#455C73",
                    "#9B59B6",
                    "#BDC3C7",
                    "#26B99A",
                    "#3498DB",
                    "#26B99A"
                  ],
                data: [54,4 ,20, 0, 10,12]
            }]
        },
        options: {
            maintainAspectRatio: false,
            responsive: true,
            scales: {
            }
        }		
    }
    var mylineChart4 = new Chart(ctx, config);	

};

function plotStackBarChart1(labels, data1, data2) {

    var ctx = document.getElementById("AccountType1");
    ctx.height = 300

    var config = {
        type: 'bar',
        data: {
            labels: ['Discretionary'],
            datasets: [{
                label: 'Advisory',
                backgroundColor:["#455C73"],
                data: [10]
                },
                {
                label: 'Discretionary',
                backgroundColor:["#9B59B6"],
                data: [90]
                }
            ]
        },
        options: {
            maintainAspectRatio: false,
            responsive: true,
            scales: {
            }
        }		
    }
    var mylineChart4 = new Chart(ctx, config);	

};

function plotStackBarChart2(labels, data1, data2) {

    var ctx = document.getElementById("AccountType2");
    ctx.height = 300

    var config = {
        type: 'bar',
        data: {
            labels: ['Discretionary'],
            datasets: [{
                label: 'Pooled',
                backgroundColor:["#455C73"],
                data: [10]
                },
                {
                label: 'Discretionary',
                backgroundColor:["#9B59B6"],
                data: [90]
                }
            ]
        },
        options: {
            maintainAspectRatio: false,
            responsive: true,
            scales: {
            }
        }		
    }
    var mylineChart4 = new Chart(ctx, config);	

};