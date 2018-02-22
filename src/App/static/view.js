bill_skeleton = `<tr>
    <th>{submitter}</th>
    <th>{date}</th>
    <th>
        <a href="/api/bills/{id}/pdf" class="btn btn-primary" role="button">
            Lataa&nbsp;<span class="fa fa-file-pdf-o"></span>
        </a>
        <button id="btn" class="btn btn-success" role="button">
            <span class="fa fa-check-square-o"></span>
        </a>
    </th>
</tr>`

function render_bill(bill) {
    bill.date = (new Date(bill.date)).toLocaleDateString()
    m_bill = bill_skeleton
    for(key in bill) {
        m_bill = m_bill.replace(new RegExp('{' + key + '}', 'g'), bill[key])
    }
    $("#table-body").append(m_bill)
}

function render(resp) {
    $("#table").show()
    bills = resp.responseJSON.objects
    for(var i = 0; i < bills.length; i++) {
        render_bill(bills[i])
    }
}

function download(query) {
    $.ajax({
        type: 'get',
        headers: {
            'Auth': localStorage.token
        },
        url: '/api/bills',
        complete: function(ret) {
            // TODO error handling
            if(ret.responseJSON.num_results == 0) {
                $("#empty").show()
                return
            }
            render(ret)
        }
    })
}


$(document).ready(function() {
    download("")
})
