$(document).ready(function() {

    document.getElementById("PageTitle").innerHTML='<h3><b>Investor Portal - '+localStorage.getItem('fund') + '</b></h3>'

    $('#datatable_history').DataTable({
        "processing": true,
        "serverSide": false,
        "info": true,
        // "responsive": true,
        "bPaginate": false,
        "bFilter": false,
        "bAutoWidth": false,
        "ajax": {
            "url": "/api/investors/history",
            "type": "POST",
            // "data": {vehicle:localStorage.getItem('fund'), asofdate:localStorage.getItem('asofdate')}
        },
        "columns": [
            {
                "data": "FolderName",
                "render": function(data, type, JsonResultRow, meta){
                    return '<a href="#">'+ data + '</a>';
                }
            },            
            {
                "data": "DeclarationDate", 
                "render": function(data, type, JsonResultRow, meta){
                    return moment(data).format('YYYY-MM-DD');
                }
            },
            {"data": "Activity"},
            {"data": "FolderAmount", render: $.fn.dataTable.render.number(',', '.', 0, '$') }
        ],
        "order": [[0,"asc"]]
    
    });


    $('#datatable_investors').DataTable({
        "processing": true,
        "serverSide": false,
        "info": true,
        // "responsive": true,
        "bPaginate": false,
        "bFilter": false,
        "ajax": {
            "url": "/api/investors/database",
            "type": "POST",
            // "data": {vehicle:localStorage.getItem('fund'), asofdate:localStorage.getItem('asofdate')}
        },
        "columns": [
            {
                "data": "InvestorDisplayName",
                "render": function(data, type, JsonResultRow, meta){
                    return '<a href="/investors/' + JsonResultRow.InvestorID + '">' + data + '</a>';
                }

            },
            {"data": "InvestorGroup"},
            {"data": "TotalCommitment", render: $.fn.dataTable.render.number(',', '.', 0, '$') },
            {"data": "FundedToDate", render: $.fn.dataTable.render.number(',', '.', 0, '$') },
            {"data": "Redemption" ,render: $.fn.dataTable.render.number(',', '.', 0, '$')},
            {"data": "CapitalBalance" ,render: $.fn.dataTable.render.number(',', '.', 0, '$')},
            {"data": "Shares", render: $.fn.dataTable.render.number(',', '.', 0, '')},
            {
                "data": "PctFunded", 
                "render": function(data, type, JsonResultRow, meta){
                    return parseFloat(data*100).toFixed(0)+"%";
                }
            }
        ],
        "order": [[0,"asc"]]
    
    });


});