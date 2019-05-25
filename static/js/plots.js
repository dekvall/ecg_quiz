$("#submit_answer").on("click",function(){
    $.ajax({
        url: "/answer",
        type: "GET",
        contentType: 'application/json;charset=UTF-8',
        data: {
            'selected': document.getElementById("answers").value
        },
        dataType:"json",
        success: function (data) {
            //Print if the answer is correct or not here
            $("#answer_comment").html(data)
        }
    });
})
