//页面加载集==================================
$(document).ready(function(){
    $.ajax({
        //获取下拉框数据
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
    });
    // 创建一个新的Date对象，它将包含当前日期和时间
    var today = new Date();
    // 获取年、月、日
    var year = today.getFullYear();
    var month = String(today.getMonth() + 1).padStart(2, '0'); // 月份是从0开始的
    var day = String(today.getDate()).padStart(2, '0');
    // 组合成YYYY-MM-DD格式
    var todayString = `${year}-${month}-${day}`;
    console.log(todayString);
    $('#start_date').val(todayString);
    $('#end_date').val(todayString);

    $('#table').dataTable({
        //动态加载表格数据
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

});

//页面监听集=============================
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
            $('#djAlert').text(response['message']).show();
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
            var alert = $('.alert')
            alert.empty()
            alert.append(response['message'] + response['link']).show();
        },
        error:function(xhr){
            $('.alert').text(xhr.responseJSON.error).show()
        }
        
    });
});
$('#file_upload').on('change',function(event){
    const file = event.target.files[0];
    if (file){
        const fileType = ['application/vnd.openxmlformats-officedocument.spreadsheetml.sheet','application/vnd.ms-excel']
        if (!(fileType.includes(file.type))){
            $('#uploadAlert').text('请上传Excel文件！').show();
            $('#file_upload').empty()
            return
        }
        var files = new FormData();
        var csrfmiddlewaretoken = $('[name="csrfmiddlewaretoken"]').val();
        files.append('csrfmiddlewaretoken',csrfmiddlewaretoken);
        files.append('file',this.files[0]);
        $.ajax({
            type: "POST",
            url:'file_upload',
            data:files,
            processData:false,
            contentType:false,
            success:function(response){
                $('#uploadAlert').text(response.message).show();
                $('#file_upload').empty()
            }
        })
    }
});
$('tbody').on('click','tr',function(){
    var number = $(this).find('td:eq(0)').text();
    var model = $(this).find('td:eq(2)').text();
    var depart = $(this).find('td:eq(3)').text();
    var pos = $(this).find('td:eq(4)').text();
    var ip = $(this).find('td:eq(6)').text();
    var descr = $(this).find('td:eq(7)').text();
    var type = $(this).find('td:eq(1)').text();
    $('input[name="number"]').val(number);
    $('.model').val(model);
    $('.type_name').val(type);
    $('input[name="pos"]').val(pos);
    $('input[name="ip"]').val(ip);
    $('input[name="dedcr"]').val(descr);
    $('#depart_name').find('option:contains('+ depart +')').attr("selected",true);
});
$("#number").on('blur',function(){
    var table = $('#table').DataTable();
    var indata = this.value;
    if (indata == ""){
        return false
    }
    table.rows().every(function(){
        var data = this.data();
        if(data['number'].includes(indata)){
            $('.model').val(data['model']);
            $('.type_name').val(data['type']);
            $('input[name="pos"]').val(data['pos']);
            $('input[name="ip"]').val(data['ip']);
            $('input[name="descr"]').val(data['descr']);
            $('#depart_name').find('option:contains('+ data['depart_name'] +')').attr("selected",true);
            return false
        }
    });
});
$('#data_5 input').datepicker({
    todayBtn: "linked",
    language: "zh-CN",
});
$('#zcbb').on('submit',function(event){
    event.preventDefault();
    var comment = new FormData(this);
    table = $('#exceltable tbody');
    table.empty();
    $.ajax({
        type: "POST",
        url: this.url,
        data: comment,
        processData:false,
        contentType:false,
        success: function (response) {
            $.each(response['data'], function(index, item) {
                // 创建新行
                var newRow = $('<tr></tr>');
                // 创建单元格并填充数据
                var index = $('<td></td>').text(item.index);
                var number = $('<td></td>').text(item.number);
                var type = $('<td></td>').text(item.type);
                var model = $('<td></td>').text(item.model);
                var pos = $('<td></td>').text(item.pos);
                var ip = $('<td></td>').text(item.ip);
                var depart_name = $('<td></td>').text(item.depart_name);
                var descr = $('<td></td>').text(item.descr);
                // 将单元格添加到行中
                newRow.append(index);
                newRow.append(number);
                newRow.append(type);
                newRow.append(model);
                newRow.append(pos);
                newRow.append(ip);
                newRow.append(depart_name);
                newRow.append(descr);
                // 将行添加到表格的主体
                $('#exceltable tbody').append(newRow);
            });
            var depart = response['depart_name'];
            var version = response['version'];
            var depart_info = $('#depart_info');
            var version_info = $('#version_info');
            depart_info.empty();
            version_info.empty();
            depart_info.append("<h5>使用机构："+ depart +"</h5>");
            version_info.append("<h5>版本："+ version +"</h5>");
            $("#tableBox").show();
        },
        error:function(xhr){
            $('.alert').text(xhr.responseJSON.error).show()
        }
    });

});
$('#download').on('click',function(){
    var old_html = window.document.body.innerHTML;
    var print_html = $('#print').html();
    window.document.body.innerHTML = print_html;
    window.print();
    window.document.body.innerHTML = old_html;
    
});
$('#export').on('click',function(){
    var start_date = $("#start_date").val()
    var end_date = $("#end_date").val()
    var depart_name = $("#depart_name").val()
    var uri = '/bgdc?type=bb&start_date='+start_date+'&end_date='+end_date+'&depart_name='+depart_name
    let link = document.createElement("a");
    link.href = uri;
    //对下载的文件命名
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
});


