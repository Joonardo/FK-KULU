function readFiles() {
    var promises = []
    $('#erittelyt').children().each(function() {
        var elem = $(this)
        promises.push(new Promise(function(resolve, reject) {
            var tosite = {}

            tosite.amount = elem.find('#summa')[0].value
            tosite.description = elem.find('#kuvaus')[0].value

            var file = elem.find('#file')[0].files[0]

            var reader = new FileReader()
            reader.onload = function(e) {
                tosite.content = e.target.result
                resolve(tosite)
            }
            reader.readAsDataURL(file)
        }))
    })
    return promises
}
