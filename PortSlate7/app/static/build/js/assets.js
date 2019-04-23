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
            "type": "POST",
            "data": {vehicle:localStorage.getItem('fund'), assetid:localStorage.getItem('asset'),asofdate:localStorage.getItem('asofdate')}
        },
        "columns": [
            { "render": function(data, type, JsonResultRow, meta){
                return '<img src="../static/images/'+JsonResultRow.Img+'" width=100%>';
            }},
            {
                "data": "AssetName",
                "render": function(data, type, JsonResultRow, meta){
                    return '<a href="/portfolio/asset/' + JsonResultRow.AssetID + '/'+ localStorage.getItem('asofdate') +'">' + data + '</a>';
                }
            },
            {"data": "PropertyType"},
            {
                "data": "PurchaseDate", 
                "render": function(data, type, JsonResultRow, meta){
                    return moment(data).format('YYYY-MM-DD');
                }
            },
            {"data": "Sqft_Unit", render: $.fn.dataTable.render.number(',', '.', 0, '') },
            {
                "data": "Occupancy", 
                "render": function(data, type, JsonResultRow, meta){
                    return parseFloat(data*100).toFixed(0)+"%";
                }
            },
            {"data": "Cost", render: $.fn.dataTable.render.number(',', '.', 0, '$') },
            {"data": "GAV", render: $.fn.dataTable.render.number(',', '.', 0, '$') },
            {"data": "NAV", render: $.fn.dataTable.render.number(',', '.', 0, '$') },
            {"data": "LoanBalance", render: $.fn.dataTable.render.number(',', '.', 0, '$') },
            {
                "data": "LTV", 
                "render": function(data, type, JsonResultRow, meta){
                    return parseFloat(data*100).toFixed(0)+"%";
                }
            },
            {"data": "InterestRate" },
            {"data": "RateType"},
            {
                "data": "Maturity",
                "render": function(data, type, JsonResultRow, meta){
                    return moment(data).format('YYYY-MM-DD');
                }
            }
        ],
        "order": [[0,"asc"]]
    
    });

});