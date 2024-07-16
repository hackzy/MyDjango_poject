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
        }});
        let table = $('#table').dataTable({
            language:{url:'static/js/zh.json'},
            ajax:{
                url:'get_inactive',
                dataSrc: 'data',
            },
            columns:[
                {data:'number'},
                {data:'type'},
                {data:'model'},
                {data:'depart_name'},
                {data:'pos'},
                {data:'status'},
                {data:'ip'},
                {data:'descr'}
            ],
            
            
        });

}

    );

    $('#zcdj').on('submit',function(event){
        event.preventDefault();
        var comment = new FormData(this);
        $.ajax({
            type: "POST",
            url: this.url,
            data: comment,
            processData:false,
            contentType:false,
            success: function (response) {
                $('.alert').text(response['message']).show();
            }
        });
        
    });
    $('#zcly').on('submit',function(event){
        event.preventDefault();
        var comment = new FormData(this);
        $.ajax({
            type: "POST",
            url: this.url,
            data: comment,
            processData:false,
            contentType:false,
            success: function (response) {
                $('.alert').text(response['message']).show();
            }
        });
        
    });
    $('#zcly').on('submit',function(event){
        event.preventDefault();
        var comment = new FormData(this);
        $.ajax({
            type: "POST",
            url: this.url,
            data: comment,
            processData:false,
            contentType:false,
            success: function (response) {
                $('.alert').text(response['message']);
            }
        });
        
    });
    $('#file_upload').on('change',function(event){
        const file = event.target.files[0];
        if (file){
            const fileType = ['application/vnd.openxmlformats-officedocument.spreadsheetml.sheet','application/vnd.ms-excel']
            if (!(fileType.includes(file.type))){
                $('.alert').text('请上传Excel文件！');
                return
            }
            var files = new FormData();
            files.append('file',this.files[0]);
            files.append('csrfmifflewaretoken','{{ csrf_token }}');
            $.ajax({
                type: "POST",
                url:'file_upload',
                data:files,
                processData:false,
                contentType:false,
                success:function(response){
                    $('.alert').text(response.message).show();


                }
            })
        }
    });
    $('tbody').on('click','tr',function(){
        var number = $(this).find('td:eq(0)').text();
        var model = $(this).find('td:eq(2)').text();
        var depart = $(this).find('td:eq(3)').text();
        var pos = $(this).find('td:eq(4)').text();
        $('input[name="number"]').val(number);
        $('input[name="model"]').val(model);
        $('label[name="old_depart"]').text(depart);
        console.log(depart)
        $('input[name="pos"]').val(pos);
    })
    
    

