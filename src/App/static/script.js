var erittelyt = null
var erittelySkeleton = `
    <div class="form-group input-group tosite">
        <div class="input-group-prepend">
            <label class="input-group-text btn btn-outline-secondary"> <span id="liitePh"><span class="fa fa-file"></span></span><input type="file" id="file" class="validate is-invalid" hidden/></label>
        </div>
        <input class="form-control validate" placeholder="Kuvaus" id="kuvaus" name="description" type="text" />
        <input class="form-control col-sm-1 text-right validate" placeholder="€" id="summa" name="amount" type="text" />
        <div class="input-group-append">
            <button id="poista" class="btn btn-warning btn-outline-secondary" type="button"><span class="fa fa-trash-o"></span></button>
        </div>
    </div>`

function checkValidations() {
    var isV = true
    $('#form').find('.validate').each(function() {
        isV &= $(this).hasClass('is-valid')
    })

    $('#submit').prop('disabled', !isV)
}

function setValidation(elem, isValid) {
    if(isValid) {
        elem.addClass('is-valid')
        elem.removeClass('is-invalid')
    }else{
        elem.addClass('is-invalid')
        elem.removeClass('is-valid')
    }

    if(!isValid) {
        $('#submit').prop('disabled', true)
        return
    }

    checkValidations()
}

function validateIBAN() {
    var iban = $("#iban")[0].value
    setValidation($("#iban"), IBAN.isValid(iban))
}

function validateNotEmpty(elem) {
    return function() {
        var val = elem[0].value
        setValidation(elem, val.length != 0)
    }
}

function AddTositeField() {
    var elem = $(erittelySkeleton)
    erittelyt.append(elem)

    elem.find("#file").change(function() {
        var parts = $(this)[0].value.split("\\")
        var fn = parts[parts.length-1]
        elem.find("#liitePh").text(fn)
        setValidation($(this), true)//$(this)[0].files[0].type === 'application/pdf')
    })

    elem.find("#summa").on('input', function() {
        var sum = 0
        $("[id^=summa]").each(function() {
            var s = $(this)[0].value.replace(',', '.').replace('€', '')
            sum += parseFloat(parseFloat(s) ? s : '0')
        })
        $("#total").text(sum)
    })

    elem.find("#poista").click(function() {
        elem.remove()
        checkValidations()
    })

    // Validations

    elem.find("#summa").on('input', function(){
        var s = $(this)[0].value.replace(',', '.').replace('€', '')
        setValidation($(this), s.length != 0 && parseFloat(s))
    })
    elem.find("#kuvaus").on('input', validateNotEmpty(elem.find("#kuvaus")))

    $("#submit").prop('disabled', true)
}

function submit() {
    Promise.all(readFiles())
    .then(function(liitteet) {

        var data = {
            submitter: $('#nimi')[0].value,
            iban: $('#iban')[0].value,
            description: $('#peruste')[0].value,
            receipts: liitteet
        }

        $.ajax({
            type: 'post',
            url: '/api/bills',
            data: JSON.stringify(data),
            contentType: 'application/json',
            complete: function(ret) {
                console.log(ret.status === 400);
                if(ret.status === 400) {
                    alert(ret.responseText)
                }else{
                    alert('Lähetetty onnistuneesti.')
                }
            }
        })
    })
}

$(document).ready(function() {
    erittelyt = $("#erittelyt")

    AddTositeField()

    $("#add").click(AddTositeField)
    $("#submit").click(submit)
    $("#iban").on('input', validateIBAN)
    $("#nimi").on('input', validateNotEmpty($("#nimi")))
    $("#peruste").on('input', validateNotEmpty($("#peruste")))
})
