function addSubmit() {
  $.ajax({
    method: 'POST',
    url: {{ url_for('portal.submit_task')|tojson }},
    data: $('#service_form').serialize()
  }).done(addShow);
}

function addShow(data) {
  celery_task_id = data.celery_task_id
  autoPlay(celery_task_id)
}

function autoPlay(celery_task_id){
  time = setInterval(function(){
    $.ajax({
      url: {{ url_for('portal.monitor_task')|tojson }},
      data: {"celery_task_id": celery_task_id},
      type: "POST",
      success: function(obj){
        for (result of obj.results){
          $('#result').append("taskid: "+celery_task_id+" status: "+result.status+"\n");
          if (result.status=="SUCCESS"){
            $('#result').append("exit_code: "+result.exit_code+"\n")
            $('#result').append("stdout: "+result.stdout+"\n")
            $('#result').append("stderr: "+result.stderr+"\n")
            clearInterval(time), function(){
　　            autoPlay();
　　           }
          }else if(result.status=='FAILURE'){
            $('#result').append("traceback: "+result.traceback+"\n")
            clearInterval(time),function(){
　　            autoPlay();
　　           }　　
          }else{
            $('#result').append("result: "+result.result.progress+"\n")
          }
        }
        var textarea = document.getElementById('result');
        textarea.scrollTop = textarea.scrollHeight;
      }
    })
  },5000
  );
}

$("#submit").click(addSubmit)