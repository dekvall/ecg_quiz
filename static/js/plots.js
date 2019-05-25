$('#answers').on('change',function(){
    $.ajax({
        url: "/answer",
        type: "GET",
        contentType: 'application/json;charset=UTF-8',
        data: {
            'selected': document.getElementById('answer').value

        },
        dataType:"json",
        success: function (data) {
            //Print if the answer is correct or not here
            Plotly.newPlot('bargraph', data );
        }
    });
})
