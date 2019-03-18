$(document).ready(function() {

    $('#datatable').DataTable({
        "processing": true,
        "serverSide": false,
        "info": true,
        // "responsive": true,
        "bPaginate": false,
        "bFilter": false,
        "bAutoWidth": true,
        "ajax": {
            "url": "/api/portfolio/assets",
            "type": "GET"
        },
        "columns": [
            { "render": function(data, type, JsonResultRow, meta){
                return '<img src="../static/images/'+JsonResultRow.Img+'" width=100%>';
            }},
            {
                "data": "AssetName",
                "render": function(data, type, JsonResultRow, meta){
                    return '<a href="/portfolio/asset/' + JsonResultRow.AssetID + '">' + data + '</a>';
                }
            },
            {"data": "PropertyType"},
            {"data": "TransactionDate"},
            {"data": "Sqft_Unit"},
            {"data": "Occupancy"},
            {"data": "Cost"},
            {"data": "GAV"},
            {"data": "NAV"},
            {"data": "LoanBalance"},
            {"data": "LTV"},
            {"data": "InterestRate"},
            {"data": "RateType"},
            {"data": "Maturity"}
        ],
        "order": [[0,"asc"]]

    });

});