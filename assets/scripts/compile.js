$('body').on('click', '.Derle button', function(){
    var contentExt = $('li.editortabs[aria-selected="true"] a').html().split('.')[1]
    if ($('.editor div[aria-hidden="true"]').length == 0){
        var textarea = $('.editor div textarea').val()
    }else{
        var textarea = $('.editor div[aria-hidden="true"] textarea').val()
    }

    
})