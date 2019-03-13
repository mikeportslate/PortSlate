

let table = $('#datatables').DataTable({
    "processing": true,
    "serverSide": true,
    "ajax": {
        "url": "/api/asset/list",
        "type": "GET"
    },
    "columns": [
        {"data": "id"},
        {"data": "property"},        
        {"data": "lender"},
        {"data": "loantype"},
        {"data": "ratetype"},
        {"data": "index"},
        {"data": "indexrate"},
        {"data": "indexspread"},
        {"data": "interestrate_initial"},
        {"data": "date_funding"},
        {"data": "date_maturityinitial"},
        {"data": "funding_total"},
        {
            "data": null,
            "defaultContent": '<button type="button" class="btn btn-info">Edit</button>' + '&nbsp;&nbsp' +
            '<button type="button" class="btn btn-danger">Delete</button>'
        }
    ]
});

$.ajaxSetup({
  data: {csrfmiddlewaretoken: '{{ csrf_token }}' },
});


$('#datatables tbody').on('click', 'button', function () {
    let data = table.row($(this).parents('tr')).data();
    let class_name = $(this).attr('class');
    if (class_name == 'btn btn-info') {
        // EDIT button
        $('#property').val(data['property']);
        $('#lender').val(data['lender']);
        $('#loantype').val(data['loantype']);
        $('#ratetype').val(data['ratetype']);
        $('#index').val(data['index']);
        $('#indexrate').val(data['indexrate'].slice(0,-1));
        $('#indexspread').val(data['indexspread'].slice(0,-1));
        $('#interestrate_initial').val(data['interestrate_initial'].slice(0,-1));
        $('#date_funding').val(data['date_funding']);
        $('#date_maturityinitial').val(data['date_maturityinitial']);
        $('#funding_total').val(data['funding_total']);
        $('#type').val('edit');
        $('#modal_title').text('EDIT');
        $("#myModal").modal();
    } else {
        // DELETE button
        $('#modal_title').text('DELETE');
        $("#confirm").modal();
    }

    id = data['id'];

});

$('#new').on('click', function (e) {
    $('#property').val('new');
    $('#lender').val('new');
    $('#loantype').val('new');
    $('#ratetype').val('new');
    $('#index').val('new');
    $('#indexrate').val('new');
    $('#indexspread').val('new');
    $('#interestrate_initial').val('new');
    $('#date_funding').val('new');
    $('#date_maturityinitial').val('new');
    $('#funding_total').val('new');
    $('#type').val('new');
    $('#modal_title').text('NEW');
    $("#myModal").modal();
});

$('form').on('submit', function (e) {
    e.preventDefault();
    let $this = $(this);
    let type = $('#type').val();
    let method = '';
    let url = '/api/asset/add';
    if (type == 'new') {
        // new
        method = 'POST';
    } else {
        // edit
        url = url + '/' + id;
        method = 'POST';
    }

    $.ajax({
        url: url,
        type: method,
        method: method,
        data: $this.serialize(),
        success: function(data, jqXHR) {
            $("#myModal").modal('hide');
            location.reload()
        },
        error: function() {
            console.log('error')
        }
    });
});

$('#confirm').on('click', '#delete', function (e) {
    $.ajax({
        url: '/api/asset/delete/' + id,
        type: 'POST',
        success: function(data, jqXHR) {
            $("#confirm").modal('hide');           
            location.reload();
            console.log('success')
        },
        error: function() {
            console.log('error')
        }
    });
});

