$(function(){
    $('.btn-default').on('click',function(){
        $('#myModal').modal({backdrop: 'static', keyboard: false})
    });

    $('#myModal').on('hidden.bs.modal', function (e) {
        $('#edit_form')[0].reset();
    });
    

});


