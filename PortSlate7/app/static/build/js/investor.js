$(document).ready(function() {

// Update the Investor Account Detail
$.ajax({
    url: '/api/investor/summary',
    type: 'POST',
    dataType: "json",
    data: {investor:localStorage.getItem('investor')},
    success: function(response){
        document.getElementById("InvestorDisplayName").innerHTML = response[0].InvestorDisplayName;
        document.getElementById("AccountID").innerHTML = response[0].InvestorID;
        document.getElementById("LegalName").innerHTML = response[0].InvestorLegalName;
        document.getElementById("EntityType").innerHTML = response[0].EntityType;
        document.getElementById("Group").innerHTML = response[0].InvestorGroup;
        document.getElementById("TaxID").innerHTML = response[0].TaxIDNumber;
        document.getElementById("InvestmentDate").innerHTML = response[0].InvestmentDate;
        document.getElementById("StockClass").innerHTML = response[0].StockClass;
        document.getElementById("PercentageInterest").innerHTML = response[0].PercentageInterest;
        document.getElementById("PricePerShare").innerHTML = response[0].PricePerShare;
        document.getElementById("TotalCommitment").innerHTML = response[0].TotalCommitment;
        document.getElementById("FundedToDate").innerHTML = response[0].FundedToDate;
        document.getElementById("PercentageLimit").innerHTML = response[0].PercentageLimit;
        document.getElementById("Certificated").innerHTML = response[0].Certificated;
        document.getElementById("FundingMethod").innerHTML = response[0].FundingPreference;
        document.getElementById("DeliveryMethod").innerHTML = response[0].DeliveryMethodPreference;
        document.getElementById("WithholdingFed").innerHTML = response[0].WithholdingFederal;
        document.getElementById("WithholdingState").innerHTML = response[0].WithholdingState;
    },
    error: function(e){

    }

});
    

// Update the charts



// Update Investor Transaction History Datatable
    $('#datatable_history').DataTable({
        "processing": true,
        "serverSide": false,
        "info": true,
        // "responsive": true,
        "bPaginate": false,
        "bFilter": false,
        "bAutoWidth": false,
        "ajax": {
            "url": "/api/investor/history",
            "type": "POST",
            "data": {investor:localStorage.getItem('investor')}
        },
        "columns": [
            {
                "data": "FundingDate", 
                "render": function(data, type, JsonResultRow, meta){
                    return moment(data).format('YYYY-MM-DD');
                }
            },
            {"data": "FolderName"},
            {"data": "Activity"},
            {"data": "FundingAmount", render: $.fn.dataTable.render.number(',', '.', 0, '$') }
        ],
        "order": [[0,"asc"]]
    
    });


});