$.ajaxSettings.traditional = true;

verbose = true;
sleep = 10;

tracker = Object();

PopTracker = function(){
  // populates the tracker object with all of the info from each patch_div
  patch_divs = $('div.patch_div');
  patch_divs.each(function(){
    var patch_div = $(this);
    var computer_id = patch_div.prop("id");
    var ta = patch_div.find('textarea');
    var sinfo = patch_div.find('.sinfo');

    tracker[computer_id] = Object();
    tracker[computer_id].postargs = Object();
    tracker[computer_id].postargs.computer_id = computer_id;
    tracker[computer_id].postargs.substep = 1;
    tracker[computer_id].postargs.jobs = [];
    tracker[computer_id].patch_div = patch_div;
    tracker[computer_id].ta = ta;
    tracker[computer_id].sinfo = sinfo;
    tracker[computer_id].patchloop = 0;
  })
}

AppendVal = function(o, v){
  o.val(o.val() + v + "\n");
}

CheckVerboseAppend = function(o, v){
  if (~v.indexOf('status:') || ~v.indexOf('VERBOSE')){
    if (verbose) {AppendVal(o, v);}
  } else {
    AppendVal(o, v);
  }
}

StopPatchLoop = function(computer_id, t, reason){
  if (t.patchloop){
    var v = "Patch Process for " + computer_id + " stopped, reason: " + reason;
    AppendVal(t.ta, v);
    console.log(v);
    console.log(t);
    clearInterval(t.patchloop);
    t.patchloop = 0;
  } else {
    var v = "Patch Process for " + computer_id + " not stopped, not running";
    console.log(v);
  }
  ScrollDown(t.ta);
}

StopAllPatchLoops = function(reason){
  $.each(tracker, function(computer_id, t){
    StopPatchLoop(computer_id, t, reason);
  });
}

StartPatchLoop = function(computer_id, t){
  if (!t.patchloop){
    $.when(PatchProcess.run_step(computer_id))
    .then(PatchProcess.handle_data, PatchProcess.handle_fail);

    t.patchloop = setInterval(function(){
      $.when(PatchProcess.run_step(computer_id))
      .then(PatchProcess.handle_data, PatchProcess.handle_fail);
    }, 1000 * sleep);

    var v = "Patch Process for " + computer_id + " started, updating every " + sleep + " seconds";
    AppendVal(t.ta, v);
    console.log(v);
    console.log(t);
  } else {
    var v = "Patch Process for " + computer_id + " not started, already running";
    console.log(v);
  }
  ScrollDown(t.ta);
}

StartAllPatchLoops = function(){
  $.each(tracker, function(computer_id, t){
    StartPatchLoop(computer_id, t);
  });
}

ScrollDown = function(e){
  e.animate({scrollTop: e.prop("scrollHeight")}, 200);
}

PatchProcess = {
  run_step:function(computer_id){
    var url = "do_patch_process.py";
    console.log("++ Making AJAX request to " + url);
    console.log(tracker[computer_id].postargs);
    return $.ajax({
      url: url,
      data: tracker[computer_id].postargs,
      computer_id: computer_id,
      dataType: 'json',
      type: 'post',
    });
  },

  handle_data:function(data){
    var computer_id = this.computer_id;

    console.log("** Received AJAX response")
    console.log(data);

    $.extend(tracker[computer_id].postargs, data);

    console.log("** Current tracker for " + this.computer_id);
    console.log(tracker[computer_id]);

    if (data.computer_name){
        tracker[computer_id].sinfo.html(data.computer_name);
    }

    $.each(data.status, function(i, v){
      CheckVerboseAppend(tracker[computer_id].ta, v);
    });

    ScrollDown(tracker[computer_id].ta);

    if (data.error || data.finished){
      if (data.error){
        var reason = "Error encountered!";
      } else {
        var reason = "Finished succesfully!";
      }
      StopPatchLoop(computer_id, tracker[computer_id], reason);
    }
  },

  handle_fail:function(data){
    var computer_id = this.computer_id;
    StopPatchLoop(computer_id, tracker[computer_id], "AJAX failure!");
  }

}

// on dom ready
$().ready(function() {

  if(verbose){
    $('#verbose').prop('checked', true);
  } else {
    $('#verbose').prop('checked', false);
  }

  $('#verbose').change(function() {
    if($(this).is(':checked')) {
        verbose = true;
    } else {
        verbose = false;
    }
  });

  $('#stop').click(function(){
    StopAllPatchLoops("user pressed '" + $(this).val() + "'");
  });

  PopTracker();
  StartAllPatchLoops();

});
