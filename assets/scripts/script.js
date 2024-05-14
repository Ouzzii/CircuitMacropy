$(document).ready(function(){
    eel.getSettings()(function(html){
        $('#settings').html(html)

        $('.settingTabs').tabs().removeClass('ui-widget ui-widget-content ui-widget-header ui-tabs-panel')
        $('.settingTabs ul').removeClass('ui-widget-header')

        $('#junkfiles').on('mouseenter', function(){
            eel.getinfo($(this).attr('id'))(function(info){
                console.log(info)
            })
        }).on('mouseleave', function(){

        })
        

    })

    eel.getJunkFiles()(function(value){
        console.log(value)
        $('#junkfileentry').val(value)
    })


    eel.createCircuitMacros()(function(){
        $('iframe.waiting').css('display', 'none')
        $('.treeview button').css('display', 'block')
    })


    
})


