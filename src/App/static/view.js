bill_skeleton = `<tr>
    <th>{submitter}</th>
    <th>{date}</th>
    <th>
        <a href="/api/pdf/{id}?token={token}" class="btn btn-primary" role="button">
            Lataa&nbsp;<span class="fa fa-file-pdf-o"></span>
        </a>
        <button id="btn" class="btn btn-success" role="button">
            <span class="fa fa-check-square-o"></span>
        </a>
    </th>
</tr>`

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
    bill.date = (new Date(bill.date)).toLocaleDateString()
    m_bill = bill_skeleton
    for(key in bill) {
        m_bill = m_bill.replace(new RegExp('{' + key + '}', 'g'), bill[key])
    }
    m_bill = m_bill.replace(/{token}/g, localStorage.token)
    $("#table-body").append(m_bill)
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
                //window.location.href = "/login"
                console.log(400);
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
        page -= 1
        download({page: page})
    })

    $('.next').click(function() {
        page += 1
        download({page: page})
    })

    $('button').prop('disabled', true)
    console.log('Session: ' + localStorage.token);
    download({})
})
