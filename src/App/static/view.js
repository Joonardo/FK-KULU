bill_skeleton = `<tr title="{sum}€: {description}">
    <td>{submitter}</th>
    <td>{date}</th>
    <td id="accepted-{id}">{accepted_visual}</th>
    <td>
        <a href="/api/pdf/{id}?token={token}" class="btn btn-primary" role="button">
            <span class="fa fa-file-pdf-o"></span>
        </a>
        <button id="btn-{id}" class="btn btn-success" role="button">
            <span class="fa fa-check-square-o"></span>
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

page = 1

function search(ev) {
    ev.preventDefault()

    var queryObj = []

    var subm = $("#name").val()
    var date = $("#date").val()
    var acc = $("#accepted").val()

    if(subm != "") {
        queryObj.push({
            'name': 'submitter',
            'op': 'like',
            'val': '%' + subm + '%'
        })
    }

    if(date != "") {
        // Dirty hack to make search by date work
        var d0 = (new Date(date)).toISOString()
        var d1 = new Date(date)
        d1.setDate(d1.getDate() + 1)
        d1 = d1.toISOString()

        queryObj.push({
            'name': 'date',
            'op': '<=',
            'val': d1
        })

        queryObj.push({
            'name': 'date',
            'op': '>=',
            'val': d0
        })
    }

    if(acc != "Kaikki") {
        queryObj.push({
            'name': 'accepted',
            'op': '==',
            'val': acc === 'Hyväksytyt'
        })
    }

    download({'q': JSON.stringify({'filters': queryObj})})
}

function render_bill(bill) {
    bill.submitter = escapeHtml(bill.submitter)
    bill.date = (new Date(bill.date)).toLocaleDateString()
    bill.accepted_visual = '<span class="fa fa-2x fa-' + (bill.accepted ? "thumbs-o-up" : "thumbs-o-down") + '"></span>'
    bill.sum = 0

    for(i in bill.receipts) {
        bill.sum += parseInt(bill.receipts[i].amount)
    }

    m_bill = bill_skeleton

    for(key in bill) {
        m_bill = m_bill.replace(new RegExp('{' + key + '}', 'g'), bill[key])
    }
    m_bill = m_bill.replace(/{token}/g, localStorage.token)
    $("#table-body").append(m_bill)

    console.log(bill.accepted);
    if(bill.accepted) {
        $('#btn-' + bill.id).prop('hidden', true)
    }

    $('#btn-' + bill.id).click(function() {
        $('#modal').modal()
        $('#submit-accept').off('click')
        $('#submit-accept').on('click', function() {
            console.log(bill.id);
            $.ajax({
                type: 'post',
                url: '/api/accept/' + bill.id,
                data: JSON.stringify({
                    description: $('#info').val()
                }),
                contentType: 'application/json',
                headers: {
                    'Auth': localStorage.token
                },
                success: function() {
                    $('#btn-' + bill.id).prop('hidden', true)
                    $('#accepted-' + bill.id).html('<span class="fa fa-2x fa-thumbs-o-up"></span>')
                },
                error: function() {
                    alert("Hyväksyminen ei onnistunut.")
                }
            })
            $('#modal').modal('toggle')
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

function download(query) {
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
        download({page: page - 1})
    })

    $('.next').click(function() {
        download({page: page + 1})
    })

    $('#cancel-accept').click(function() {
        $('#modal').modal('hide')
    })

    $('#modal').on('hide', function() {
        $('#info').val('')
    })

    $('button').prop('disabled', true)
    console.log('Session: ' + localStorage.token);
    download({})
})
