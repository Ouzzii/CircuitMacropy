$(document).ready(function(){

    eel.Is_there_an_update_available()(function(html){
        if (html != false){
            $('#ask_for_update').html(html)
        }

    })

    eel.getColorPalette("SunsetHarmony")(function(json){
        console.log(json)
        const newTreeviewBackground = json[0];
        const newFileForeground = json[1];
        const newFileHoverBackground = json[2];
        const newFileHoverForeground = json[3];
        const newTreeviewTitle = json[4];
    
        // CSS değişkenlerini güncelleme
        document.documentElement.style.setProperty('--treeviewBackground', newTreeviewBackground);
        document.documentElement.style.setProperty('--fileForeground', newFileForeground);
        document.documentElement.style.setProperty('--fileHoverBackground', newFileHoverBackground);
        document.documentElement.style.setProperty('--fileHoverForeground', newFileHoverForeground);
        document.documentElement.style.setProperty('--treeviewTitle', newTreeviewTitle);
    
    })


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


    eel.filesettings()(function(value){
        console.log(value)
        $('#junkfileentry').val(value)
    })

    eel.updatesettings()(function(value){
        console.log(value)
        if (value){
            $('#autoupdatecheckbox').click()
        }
    })


    eel.createCircuitMacros()(function(){
        $('iframe.waiting').css('display', 'none')
        $('.treeview button').css('display', 'block')
    })


    
})


