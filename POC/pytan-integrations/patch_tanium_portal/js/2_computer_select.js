// find each tr.search_row
// get the question_id that was started from span.q_id
// every 3 seconds perform an ajax call to get the results of question_id
// if question_id is not done yet, update span.q_status with progress
// if question_id is done, delete this tr and add new trs based on the results

function newRow($table,cols){
    $row = $('<tr/>');
    for(i=0; i<cols.length; i++){
        $col = $('<td/>', {'class' : 'c' + i});
        $col.append(cols[i]);
        $row.append($col);
    }
    $table.append($row);
}

var FindSearchRows = function(){
  var search_rows = $('tr.search_row');
  return search_rows;
}

var UpdateSearchRows = function(){
  search_rows = FindSearchRows();
  search_rows.each(function(){
    var search_row = $(this);
    var mytable = search_row.parent();
    var q_id = search_row.find('span.q_id').text();
    var q_status = search_row.find('span.q_status');

    // console.log(q_id)
    $.ajax({
      url: 'get_question_progress.py',
      data: { question_id: q_id},
      dataType: 'json',
      cache: true,
      timeout: 30000,
      success: function(data) {
        console.log("Received data from ajax call");
        console.log(data);
        q_status.html(data.status);
        if (data.finished){
          if (data.error) {
            // change class so that it doesnt get found by FindSearchRows any longer
            search_row.attr('class', 'failed_search');
          } else {
            // console.log(data.result_data);

            // remove the row
            search_row.remove();

            // for each item in result data, add a new row to mytable
            $.each(data.result_data, function(i, val){
              var is_windows = val['Is Windows'];
              if (is_windows === "False"){
                var cb_disabled = true;
              } else {
                var cb_disabled = false;
              }

              var td0 = $('<input />', {
                'class': 'checkbox',
                'disabled': cb_disabled,
                // 'required': true,
                // 'minlength': 1,
                'name': 'server',
                'type': 'checkbox',
                'value': val['Computer ID']
              });
              var td1 = val['Computer Name'];
              var td2 = val['IP Address'];
              var td3 = val['Operating System'];
              var td4 = val['Is Windows'];
              newRow(mytable, [td0, td1, td2, td3, td4]);

              // tell tablesort that table has been modded
              mytable.trigger("update");

            });

            // enable the next button
            $('input#next').prop('disabled', false);
          };
        };
      }
    });
  });
  return true;
};


var thisloop = setInterval(UpdateSearchRows, 1000 * 3);

$().ready(function() {
  $("table").tablesorter({sortList: [[1,1]]});

  $("form").validate({
    rules: {
      server: {
        required: true,
        minlength: 1
      }
    },
    messages: {
        server: {
          required: "You must select at least one server",
          minlength: "You must select at least one server"
      }
    }
  });

  $('#select_all').change(function() {
      var checkboxes = $(this).closest('form').find(':checkbox:not(:disabled)');
      if($(this).is(':checked')) {
          checkboxes.prop('checked', true);
      } else {
          checkboxes.prop('checked', false);
      }
  });
});
