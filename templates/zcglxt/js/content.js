$(document).ready(function(){
    $.ajax({
        type: "GET",
        url: "get_options",
        success: function (response) {
            var depart = response.depart_names
            var type = response.type_names
            var depart_select = $('select[name="depart_name"]');
            depart_select.empty();
            depart_select.append('<option value="">请选择部门</option>');
            var type_select = $('select[name="type_name"]');
            type_select.empty();
            type_select.append('<option value="">请选择分类</option>');
            $.each(depart,function(index,dict){
                var option = $('<option></option>').attr('value',dict.id).text(dict.name);
                depart_select.append(option);
            });
            $.each(type,function(index,dict){
                var types = $('<option></option>').attr('value',dict.id).text(dict.name);
                type_select.append(types);
            })
            
        }
})
}

    
    );
    $('#zcdj').on('submit',function(event){
        event.preventDefault();
        var comment = new FormData(this)
        $.ajax({
            type: "POST",
            url: this.url,
            data: comment,
            processData:false,
            contentType:false,
            success: function (response) {
                $('.alert').text('提交成功');
            }
        });
        
    })