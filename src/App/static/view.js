bill_skeleton = `
<tr title="{sum}€: {description}">
    <td>{submitter}</th>
    <td>{date}</th>
    <td id="accepted-{id}">{accepted_visual}</th>
    <td>
        <a href="/api/pdf/{id}?token={token}" class="btn btn-primary" role="button">
            <span class="fa fa-file-pdf-o"></span>
        </a>
        <button id="btn-{id}" class="btn btn-success" role="button">
            <span class="fa fa-search"></span>
        </a>
    </td>
</tr>`

var entityMap = {
  '&': '&amp;',
  '<': '&lt;',
  '>': '&gt;',
  '"': '&quot;',
  "'": '&#39;',
  '/': '&#x2F;',
  '`': '&#x60;',
  '=': '&#x3D;'
};

function escapeHtml (string) { // Move to backend
  return String(string).replace(/[&<>"'`=\/]/g, function (s) {
    return entityMap[s];
  });
}

receipt_skel = `
<div class="row" style="margin-bottom: 10px;">
    <div class="col-sm-2">
        <strong>{amount}€</strong>
    </div>

    <div class="col-sm-10">
        {description}
    </div>
</div>
`

function show(bill) {
    $("#modal-header").text("Kulukorvauslomake #" + bill.id)
    $("#modal-submitter").text(escapeHtml(bill.submitter))
    $("#modal-date").text((new Date(bill.date)).toLocaleDateString('fi-FI'))
    $("#modal-iban").text(escapeHtml(bill.iban))
    $("#modal-description").text(escapeHtml(bill.description))
    $("#modal-accepted-at").text(bill.accepted_at)
    $("#submit-toggle-hide").text(bill.hidden ? "Palauta." : "Piilota.")

    $("#submit-toggle-hide").off('click')
    $("#submit-toggle-hide").click(function() {
        $.ajax({
            type: "post",
            url: "/api/toggleHide/" + bill.id,
            contentType: 'application/json',
            headers: {
                'Auth': localStorage.token
            },
            success: function(ret) {
                alert(bill.hidden ? "Palautettu." : "Piilotettu.")
            }
        })
    })

    $("#modal-receipts").empty()

    for(i in bill.receipts) {
        r = bill.receipts[i]
        rec = receipt_skel
            .replace(/{description}/g, escapeHtml(r.description))
            .replace(/{amount}/g, escapeHtml(r.amount))
        $("#modal-receipts").append(rec)
    }

    $('#modal').modal()

    if(bill.accepted) {
        $("#modal-accept-form").addClass('hidden')
        $("#modal-accepted").removeClass('hidden')
        $("#submit-accept").hide()
        $("#modal-accepted-at").text(bill.accepted_at)
    }else{
        $("#modal-accept-form").removeClass('hidden')
        $("#modal-accepted").addClass('hidden')
        $("#submit-accept").show()
    }

    if(bill.paid && bill.paid.length) {
        $("#modal-paid").removeClass('hidden')
        $("#modal-paid-form").addClass('hidden')
        $("#submit-pay").hide()
        $("#modal-paid-at").text(bill.paid)
    }else{
        $("#modal-paid").addClass('hidden')
        $("#modal-paid-form").removeClass('hidden')
        $("#submit-pay").show()
    }
}

page = 1

function search(ev, page=1) {
    if(ev)
        ev.preventDefault()

    var queryObj = []

    var subm = $("#name").val()
    var sdate = $("#sdate").val()
    var edate = $("#edate").val()
    var acc = $("#accepted").val()

    if(subm != "") {
        queryObj.push({
            'name': 'submitter',
            'op': 'like',
            'val': '%' + subm + '%'
        })
    }

    if(sdate != "") {
        var d0 = (new Date(sdate)).toISOString()

        queryObj.push({
            'name': 'date',
            'op': '>=',
            'val': d0
        })
    }

    if(edate != "") {
        var d1 = (new Date(edate)).toISOString()

        queryObj.push({
            'name': 'date',
            'op': '<=',
            'val': d1
        })
    }

    switch (acc) {
        case "Kaikki":
            queryObj.push({
                'name': 'hidden',
                'op': '==',
                'val': false
            })
            break;
        case "Hyväksytyt":
            queryObj.push({
                'name': 'accepted',
                'op': '==',
                'val': true
            })
            queryObj.push({
                'name': 'hidden',
                'op': '==',
                'val': false
            })
            break;
        case "Hyväksymättömät":
            queryObj.push({
                'name': 'accepted',
                'op': '==',
                'val': false
            })
            queryObj.push({
                'name': 'hidden',
                'op': '==',
                'val': false
            })
            break;
        case "Piilotetut":
            queryObj.push({
                'name': 'hidden',
                'op': '==',
                'val': true
            })
            break;
    }
    download({'q': JSON.stringify({'filters': queryObj}), 'page': page})
}

function render_bill(bill) {
    bill.date = (new Date(bill.date)).toLocaleDateString('fi-FI')
    accepted_visual = '<span class="fa fa-2x fa-' + (bill.accepted ? "thumbs-o-up" : "thumbs-o-down") + '"></span>'
    if(bill.paid && bill.paid.length) {
        accepted_visual += '&nbsp;<span class="fa fa-2x fa-money"></span>'
    }
    bill.sum = 0

    for(i in bill.receipts) {
        bill.sum += parseInt(bill.receipts[i].amount)
    }

    m_bill = bill_skeleton

    for(key in bill) {
        m_bill = m_bill.replace(new RegExp('{' + key + '}', 'g'), escapeHtml(bill[key]))
    }
    m_bill = m_bill.replace(/{accepted_visual}/g, accepted_visual)
    m_bill = m_bill.replace(/{token}/g, localStorage.token)
    $("#table-body").append(m_bill)

    $('#btn-' + bill.id).click(function() {
        show(bill)
        $('#submit-accept').off('click')
        $('#submit-accept').on('click', function() {
            $.ajax({
                type: 'patch',
                url: '/api/bills/' + bill.id,
                data: JSON.stringify({
                    accepted: true,
                    accepted_at: $('#info').val()
                }),
                contentType: 'application/json',
                headers: {
                    'Auth': localStorage.token
                },
                success: function() {
                    $('#accepted-' + bill.id).html('<span class="fa fa-2x fa-thumbs-o-up"></span>')
                    alert("Kulukorvauslomake hyväksytty.")
                },
                error: function() {
                    alert("Hyväksyminen ei onnistunut.")
                }
            })
            $('#modal').modal('toggle')
            reload()
        })

        $('#submit-pay').off('click')
        $('#submit-pay').on('click', function() {
            $.ajax({
                type: 'patch',
                url: '/api/bills/' + bill.id,
                data: JSON.stringify({
                    paid: $('#pvm').val()
                }),
                contentType: 'application/json',
                headers: {
                    'Auth': localStorage.token
                },
                success: function() {
                    $('#accepted-' + bill.id).html('<span class="fa fa-2x fa-thumbs-o-up"></span>&nbsp;<span class="fa fa-2x fa-money"></span>')
                    alert("Merkitty maksetuksi.")
                },
                error: function() {
                    alert("Maksetuksi merktseminen ei onnistunut.")
                }
            })
            $('#modal').modal('toggle')
            reload()
        })
    })
}

function render(resp) {
    $("#table").prop('hidden', false)
    $("#empty").prop('hidden', true)
    bills = resp.responseJSON.objects
    for(var i = 0; i < bills.length; i++) {
        render_bill(bills[i])
    }

    $('.page').text(resp.responseJSON.page + '/' + resp.responseJSON.total_pages)
    page = resp.responseJSON.page

    if(page >= resp.responseJSON.total_pages) {
        $(".next").prop('disabled', true)
    }
    if(page === 1){
        $('.prev').prop('disabled', true)
    }
}

var last_query = undefined

function reload() {
    download(last_query)
}

function download(query) {
    last_query = query
    $('#table-body').empty()
    $('button').prop('disabled', true)
    $.ajax({
        type: 'get',
        headers: {
            'Auth': localStorage.token
        },
        url: '/api/bills?' + $.param(query),
        complete: function(ret) {
            $('button').prop('disabled', false)
            if(ret.status === 400) {
                window.location.href = "/login"
            }
            if(ret.responseJSON.num_results == 0) {
                return
            }
            render(ret)
        }
    })
}

$(document).ready(function() {
    if(!localStorage.token) {
        window.location.href = '/login'
    }

    $('#search').click(search)

    $('.prev').click(function() {
        search(undefined, page - 1)
    })

    $('.next').click(function() {
        search(undefined, page + 1)
    })

    $('#cancel-accept').click(function() {
        $('#modal').modal('hide')
    })

    $('#modal').on('hide', function() {
        $('#info').val('')
    })

    $('button').prop('disabled', true)

    search(undefined)
})
