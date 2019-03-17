$(document).ready(function() {

    $('#datatable-buttons').DataTable({
        "processing": true,
        "serverSide": true,
        "ajax": {
            "url": "/api/portfolio/assets",
            "type": "GET"
        },
        "columns": [
            { "data": null, defaultContent: "" },
            {"data": "AssetName"},
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
        ]


    });

});