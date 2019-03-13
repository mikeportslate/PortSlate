	   
	$(document).ready(function() {
			
		init_dashboard();
				
		$.ajax({
				datatype: 'json',
				url: '/api/dashboard/summary',
				type: 'POST',
				data: '',
				success: function(response){
					updateTop(response);
					plotpieChart1(response);
					updateRateSummary(response);
				},
				error: function(e) {
					console.log(e)
				}
		});

		$.ajax({
			datatype: 'json',
			url: '/api/dashboard/timeseries',
			type: 'POST',
			data: '',
			success: function(response){
				var labels = [];
				var MarketValue = [];
				var NAV = [];
				var LTV = [];
				var DSCR = [];
				var labels_maturity = [];
				var MaturityInitial = [];
				var MaturityExt = [];

				for (var e = 0; e < Object.keys(response["Monthly Figures"]["Period"]).length; e++) {
					var d = new Date(response["Monthly Figures"]["Period"][e]);
					labels.push(d.getMonth()+1 + '/' + d.getFullYear());
					MarketValue.push(response["Monthly Figures"]["MarketValue"][e]/1000000);
					NAV.push(response["Monthly Figures"]["NAV"][e]/1000000);
					LTV.push((response["Monthly Figures"]["LTV"][e]*100).toFixed(0));
					DSCR.push((response["Monthly Figures"]["DSCR"][e]).toFixed(1));
				};
				labels_maturity = Object.keys(response['Maturity Initial']);
				MaturityInitial = Object.keys(response['Maturity Initial']).map(function(e) { return(response['Maturity Initial'][e])/1000000})
				MaturityExt = Object.keys(response['Maturity Extended']).map(function(e) { return(response['Maturity Extended'][e])/1000000})

				plotlineChart2(labels, MarketValue, NAV);
				plotlineChart3(labels, LTV);
				plotlineChart4(labels, DSCR);
				plotBarChart2(labels_maturity, MaturityInitial, MaturityExt);
				plotBarChart3(labels_maturity, MaturityInitial, MaturityExt);
			},
			error: function(e) {
				console.log(e)
			}
		});


			
	});	

	function updateTop(data) {

		document.getElementById("TopMarketValue").innerHTML = "$" + (data.MarketValue / 1000000).toFixed(0) + "mm"
		document.getElementById("TopNAV").innerHTML = "$" + (data.NAV / 1000000).toFixed(0) + "mm"
		document.getElementById("TopLTV").innerHTML = (data.LTV * 100).toFixed(0) + "%"
		document.getElementById("TopEffectiveRate").innerHTML = (data.EffectRate ).toFixed(2) + "%"
		document.getElementById("TopFloating").innerHTML = ((1-data.Loans_Fixed) * 100).toFixed(0) + "%"
		document.getElementById("TopMaturity").innerHTML = "2.5yrs"
	};

	function updateRateSummary(data) {

		var myTable = document.getElementById("RateSummaryTable");
		myTable.rows[0].cells[1].innerHTML = data.EffectRate.toFixed(2) + "%";
		myTable.rows[1].cells[1].innerHTML = data.EffectRate_Fixed.toFixed(2) + "%";
		myTable.rows[2].cells[1].innerHTML = data.EffectRate_Floating.toFixed(2) + "%";
		myTable.rows[3].cells[1].textContent = data.LoanSpread.toFixed(0) + "bps";
	};
	
	function plotpieChart1(data) {

		var ctx = document.getElementById("mypieChart");

		var config = {
			type: 'pie',
			data: {
				datasets: [{
					data: [data.Loans_Fixed.toFixed(2)*100, data.Loans_Floating_Cap.toFixed(2)*100, data.Loans_Floating_NoCap.toFixed(2)*100],
					backgroundColor: [
						"#455C73",
						"#9B59B6",
						"#BDC3C7"
					],
					label: 'Interest Rate Type' 
				}],
				labels: [
					"Fixed Rate Loan",
					"Floating Rate Loan (with Cap)",
					"Floating Rate Loan (no Cap)"
				]
			},
			options: {
				maintainAspectRatio: false,
				responsive: true,
			}
		}
		var mypieChart = new Chart(ctx, config);	

	};

	function plotlineChart2(labels, data1, data2) {

		var ctx = document.getElementById("mylineChart2");

		var config = {
			type: 'line',
			data: {
				labels: labels,
				datasets: [{
					label: 'Gross Asset Value',
					backgroundColor: "rgba(38, 185, 154, 0.31)",
					borderColor: "rgba(38, 185, 154, 0.7)",
					pointBorderColor: "rgba(38, 185, 154, 0.7)",
					pointBackgroundColor: "rgba(38, 185, 154, 0.7)",
					pointHoverBackgroundColor: "#fff",
					pointHoverBorderColor: "rgba(220,220,220,1)",
					pointBorderWidth: 1,
				data: data1
				}, {
					label: 'Net Asset Value',
					backgroundColor: "rgba(3, 88, 106, 0.3)",
					borderColor: "rgba(3, 88, 106, 0.70)",
					pointBorderColor: "rgba(3, 88, 106, 0.70)",
					pointBackgroundColor: "rgba(3, 88, 106, 0.70)",
					pointHoverBackgroundColor: "#fff",
					pointHoverBorderColor: "rgba(151,187,205,1)",
					pointBorderWidth: 1,
					data: data2
				}]
			},
			options: {
				scales: {
				yAxes: [{
					ticks: {
					beginAtZero: true
					}
				}]
				},
				xAxes: {
					interval: 10
				}
			}			
		}
		var mylineChart2 = new Chart(ctx, config);	

	};

	function plotlineChart3(labels, data1, data2) {

		var ctx = document.getElementById("mylineChart3");

		var config = {
			type: 'line',
			data: {
				labels: labels,
				datasets: [{
					label: 'LTV',
					backgroundColor: "rgba(150, 202, 89, 0.12)",
					borderColor: "#3f3f3f",
					pointBorderColor: "#fff",
					pointBackgroundColor: "#3f3f3f",
					pointHoverBackgroundColor: "#fff",
					pointHoverBorderColor: "rgba(220,220,220,1)",
					pointBorderWidth: 1,
				data: data1
				}]
			},
			options: {
				scales: {
				yAxes: [{
					ticks: {
					beginAtZero: true
					}
				}]
				},
				axisX: {
					interval: 10
				}
			}			
		}
		var mylineChart2 = new Chart(ctx, config);	

	};

	function plotlineChart4(labels, data1, data2) {

		var ctx = document.getElementById("mylineChart4");

		var config = {
			type: 'line',
			data: {
				labels: labels,
				datasets: [{
					label: 'DSCR',
					backgroundColor: "#3498DB",
					borderColor: "rgba(38, 185, 154, 0.7)",
					pointBorderColor: "#fff",
					pointBackgroundColor: "rgba(38, 185, 154, 0.7)",
					pointHoverBackgroundColor: "#fff",
					pointHoverBorderColor: "rgba(220,220,220,1)",
					pointBorderWidth: 1,
				data: data1
				}]
			},
			options: {
				scales: {
				yAxes: [{
					ticks: {
					beginAtZero: true
					}
				}]
				},
				axisX: {
					interval: 10
				}
			}			
		}
		var mylineChart4 = new Chart(ctx, config);	

	};

	function plotBarChart2(labels, data1, data2) {

		var ctx = document.getElementById("mybarChart2");

		var config = {
			type: 'bar',
			data: {
				labels: labels,
				datasets: [{
					label: 'Loans Matured ($mm)',
					backgroundColor: "#26B99A",
					data: data1
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

	function plotBarChart3(labels, data1, data2) {

		var ctx = document.getElementById("mybarChart3");

		var config = {
			type: 'bar',
			data: {
				labels: labels,
				datasets: [{
					label: 'Loans Matured ($mm)',
					backgroundColor: "#03586A",
					data: data1
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



    function init_dashboard() {



			if ($('#mystackbarChart').length ){
					
			var ctx = document.getElementById("mystackbarChart");
			var myChart = new Chart(ctx, {
				type: 'bar',
				data: {
				labels: ["Red"],
				datasets: [{
					label: 'Asset 1',
					data: [10],
					backgroundColor: 'rgba(255, 99, 132, 0.2)',
					borderColor:     'rgba(255,99,132,1)',
					borderWidth: 2
					},
					{
					label: 'Asset 2',
					data: [15],
					backgroundColor: 'rgba(255, 159, 64, 0.2)',
					borderColor:     'rgba(255, 159, 64, 1)',
					borderWidth: 2
					}
				]
				},
				options: {
				scales: {
					yAxes: [{
					stacked: true,
					ticks: {
						beginAtZero: true
					}
					}],
					xAxes: [{
					stacked: true,
					ticks: {
						beginAtZero: true
					}
					}]
			
				}
				}
			});
			
			}		


    };