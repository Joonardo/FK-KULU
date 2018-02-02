var erittelyt = null
var erittelySkeleton = `
    <div id={tosite} class="form-group input-group tosite">
        <div class="input-group-prepend">
            <label class="input-group-text btn btn-outline-secondary"> <span id="{liitePh}"><span class="fa fa-file"></span></span><input type="file" id="{liite}" name="{liite}" class="validate is-invalid" hidden/></label>
        </div>
        <input class="form-control validate" placeholder="Kuvaus" id="{kuvaus}" name="{kuvaus}" type="text" />
        <input class="form-control col-sm-1 text-right validate" placeholder="€" id="{summa}" name="{summa}" type="text" />
        <div class="input-group-append">
            <button id={poista} class="btn btn-warning btn-outline-secondary" type="button"><span class="fa fa-trash-o"></span></button>
        </div>
    </div>`

function checkValidations() {
    var isV = true
    $('#form').find('.validate').each(function() {
        isV &= $(this).hasClass('is-valid')
    })

    $('#submit').prop('disabled', !isV)
}

function setValidation(sel, isValid) {
    if(isValid) {
        $(sel).addClass('is-valid')
        $(sel).removeClass('is-invalid')
    }else{
        $(sel).addClass('is-invalid')
        $(sel).removeClass('is-valid')
    }

    if(!isValid) {
        $('#submit').prop('disabled', true)
        return
    }

    checkValidations()
}

function validateIBAN() {
    var iban = $("#iban")[0].value
    setValidation("#iban", IBAN.isValid(iban))
}

function validateNotEmpty(sel) {
    return function() {
        var val = $(sel)[0].value
        setValidation(sel, val.length != 0)
    }
}

function AddTositeField() {
    var id = Math.floor(Math.random() * 1e6)
    var elem = $(erittelySkeleton
        .replace(/{tosite}/g, id)
        .replace(/{kuvaus}/g, "kuvaus" + id)
        .replace(/{liite}/g, "liite" + id)
        .replace(/{liitePh}/g, "liitePh" + id)
        .replace(/{summa}/g, "summa" + id)
        .replace(/{poista}/g, "poista" + id)
    )
    erittelyt.append(elem)

    $("#liite" + id).change(function() {
        var parts = $("#liite" + id)[0].value.split("\\")
        var fn = parts[parts.length-1]
        $("#liitePh" + id).text(fn)
        setValidation("#liite" + id, true)
    })

    $("#summa" + id).on('input', function() {
        var sum = 0
        $("[id^=summa]").each(function() {
            var s = $(this)[0].value.replace(',', '.').replace('€', '')
            sum += parseFloat(parseFloat(s) ? s : '0')
        })
        $("#total").text(sum)
    })

    $("#poista" + id).click(function() {
        $("#" + id).remove()
        checkValidations()
    })

    // Validations

    $("#summa" + id).on('input', function(){
        var s = $("#summa" + id)[0].value.replace(',', '.').replace('€', '')
        setValidation("#summa" + id, s.length != 0 && parseFloat(s))
    })
    $("#kuvaus" + id).on('input', validateNotEmpty("#kuvaus" + id))

    $("#submit").prop('disabled', true)
}

function submit() {
    var formData = new FormData($("#form")[0])

    var ids = []
    $('.tosite').each(function() { ids.push($(this)[0].id) })
    formData.append('ids', ids)

    console.log($('#form').serializeArray())

    $.ajax({
        type: 'post',
        url: '/',
        data: formData,
        processData: false,
        contentType: false,
        complete: function(ret) {
            alert(ret.responseText); //TODO
            console.log(ret);
        }
    })
}

$(document).ready(function() {
    erittelyt = $("#erittelyt")

    AddTositeField()

    $("#add").click(AddTositeField)
    $("#submit").click(submit)
    $("#iban").on('input', validateIBAN)
    $("#nimi").on('input', validateNotEmpty("#nimi"))
    $("#peruste").on('input', validateNotEmpty("#peruste"))
})
