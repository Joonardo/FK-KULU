$(document).ready(function() {
    $('*[id^="btn-"]').each(function() {
        id = $(this)[0].id.split('-')[1]
        $(this).click(function() {
            $.ajax({
                type: 'post',
                url: '/bills/' + id + '/accept',
                complete: function(ret) {
                    if(ret.status != 200) {
                        alert("Oho, jotain meni pieleen.")
                        return
                    }
                    $("#acc-" + id).html(
                        '<span style="font-size: 0.8cm;" class="fa fa-check-square-o"></span>'
                    )
                }
            })
        })
    })
})
