function readFiles() {
    var res = []
    var status = []
    $('#erittelyt').children().each(function() {
        var tosite = {}

        tosite.summa = $(this).find('#summa')[0].value
        tosite.kuvaus = $(this).find('#kuvaus')[0].value

        var file = $(this).find('#file')[0].files[0]

        var reader = new FileReader()
        reader.onload = function(e) {
            tosite.tiedosto = e.target.result
        }
        reader.readAsDataURL(file)

        res.push(tosite)
    })
    return res
}
