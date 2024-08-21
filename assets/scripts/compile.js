$('body').on('change', '#compileas',function(){
    let compileas = $(this).find(":selected").text()
    console.log(compileas)
    if (compileas == 'LaTeX' | compileas == 'PDF'){
        console.log($('#withcompile'))
        $('#withcompile').css('display', 'block')
    }   $('#withcompile').html(`

        <option value='pgf'>pgf</option>

    `)

})

$('body').on('click', '#compile', function(){

    var selecteds = $('input:checked')
    $.each(selecteds, function(){
        var waitingimg = $(this).parent().parent().find('.waiting')
        waitingimg.css('visibility', 'visible')
        let compileas = $(this).parent().parent().find('#compileas').val()
        let withcompile = $(this).parent().parent().find('#withcompile').val()
        let contentPath = $(this).parent().parent().parent().find('textarea').attr('path')
        //let contentExt = contentPath.split('.')[1]
        let content = $(this).parent().parent().parent().find('textarea').val()
        
        

        eel.saveContent(`${contentPath}`, content)()

        if ($('.editor div textarea').length == 1){
            textarea = $('.editor div textarea')
            
        }else{
            textarea = $('.editor div[aria-hidden="false"] textarea')
        }
        $(`#${name_to_id(textarea.attr('path').split('\\').pop().split('/').pop())} a`).removeClass('notsaved')

        eel.compile(`${contentPath}`, withcompile, compileas)(function(result){
                waitingimg.css('visibility', 'hidden')
                openFolder()
                if (result.message != 'compile successful'){
                    notification('Derleme yapilirken bir hata meydana geldi')
                }
            
        })
    })


    


    //var contentName = $('li.editortabs[aria-selected="true"] a').html()
    //var contentExt = contentName.split('.')[1]



    /*
    if ($('.editor div[aria-hidden="true"]').length == 0){
        var textarea = $('.editor div textarea').val()
    }else{
        var textarea = $('.editor div[aria-hidden="true"] textarea').val()
    }

    eel.SaveContents
    */
    //if (contentExt != 'pdf' || contentExt != '.tex')

})