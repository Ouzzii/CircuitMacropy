$('body').on('click', '.settings img:first-child', function(){
    $('#settings').toggleClass('hidden')
})

$('body').on('click', '.apply button', function(){
    eel.applySettings(
        $('#junkfileentry').val()
    )
})


/*
$('.textInfo').hover(
    function(){
        console.log($(this).attr('id'))
        eel.getinfo($(this).attr('id'))(function(info){
            console.log(info)
        })
    },
    function(){

    }
)
*/