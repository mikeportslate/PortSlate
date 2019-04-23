function assetIRR() {

    $.ajax({
        type: 'POST',
        url: '/api/asset/irr',
        dataType: "json",
        data: {
            vehicle:localStorage.getItem('fund'),
            // assetID:localStorage.getItem('asset'),
            assetID:$('#IRR_form')['0']['0'].value, 
            exitCost:$('#IRR_form')['0']['1'].value, 
            exitYear:$('#IRR_form')['0']['2'].value, 
            exitCap:$('#IRR_form')['0']['3'].value, 
            exitNOIAdj:$('#IRR_form')['0']['4'].value,
            JV:$('#IRR_form')['0']['5'].value  
        },
        success: function(result) {
            createTable(result);
        },
        error:{}
    });

};

function createTable(result){
    
    $('#AssetCashFlow').append('<table id="jsonTable"><thead><tr></tr></thead><tbody></tbody></table>');
	
    $.each(Object.keys(result[0]), function(index, key){
        $('#jsonTable thead tr').append('<th>' + key + '</th>');
    });	
    
    $.each(result, function(index, jsonObject){     

        if(Object.keys(jsonObject).length > 0){
            var tableRow = '<tr>';
            $.each(Object.keys(jsonObject), function(i, key){
                tableRow += '<td>' + jsonObject[key] + '</td>';
            });
            tableRow += "</tr>";
            $('#jsonTable tbody').append(tableRow);
        }
	});
}
