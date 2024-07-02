
$(document).ready(
    
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
                $('.alert').text('提交成功')
            }
        });
        
    })
)