var erittelyt = null
var erittelySkeleton = `
    <div class="form-group input-group tosite">
        <div class="input-group-prepend">
            <label id="label" class="input-group-text btn btn-outline-secondary" data-toggle="tooltip" title="Valitse PDF-tiedosto." ><span id="liitePh" class="fa fa-file-pdf-o"></span></span><input type="file" id="file" class="validate is-invalid" hidden/></label>
        </div>
        <input class="form-control validate" placeholder="Kuvaus" id="kuvaus" name="description" type="text" />
        <input class="form-control col-sm-2 text-right validate" placeholder="€" id="summa" name="amount" type="text" />
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

function sum(elem = undefined) {
    let sum = 0
    if(elem) elem.val(elem.val().replace(/[^\d.,]/g, '').split(/[,\.]/g, 2).join('.'))
    $("[id^=summa]").each(function() {
        $(this).val($(this).val().replace(/[^\d.,]/g, '').split(/[,\.]/g, 2).join('.'))
        var s = $(this).val().replace(',', '.').replace('€', '')
        sum += parseFloat(parseFloat(s) ? s : '0')
    })
    $("#total").text(sum.toFixed(2))
}

function AddTositeField() {
    var elem = $(erittelySkeleton)
    erittelyt.append(elem)

    elem.find("#file").change(function() {
        var parts = $(this)[0].value.split("\\")
        var fn = parts[parts.length-1]
        elem.find("#liitePh").text(fn.length > 0 ? " " + fn.slice(0,4) + '..' : "")
        elem.find("#label").prop("title", fn.length > 0 ? fn : "Valitse PDF-tiedosto.")
        var files = $(this)[0].files
        setValidation($(this), files.length > 0 && files[0].type === 'application/pdf')

        elem.find("#liitePh").removeClass("fa-file-pdf-o")

        if($(this).hasClass("is-invalid") && fn.length > 0) {
            elem.find("#liitePh").removeClass("fa-thumbs-o-up")
            elem.find("#liitePh").addClass("fa-thumbs-o-down")
        }else if(fn.length > 0){
            elem.find("#liitePh").removeClass("fa-thumbs-o-down")
            elem.find("#liitePh").addClass("fa-thumbs-o-up")
        }else{
            elem.find("#liitePh").addClass("fa-file-pdf-o")
        }
    })

    elem.on('input', () => sum(elem))

    sum(elem)

    elem.find("#poista").click(function() {
        elem.remove()
        sum()
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
    $("#submit").prop("disabled", true)
    $("#sbm-sp").removeClass("hidden")

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
                $("#submit").prop("disabled", false)
                $("#sbm-sp").addClass("hidden")
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
