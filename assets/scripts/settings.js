eel.getSettings()(function (html) {
    $('#settings').html(html)

    $('.settingTabs').tabs().removeClass('ui-widget ui-widget-content ui-widget-header ui-tabs-panel')
    $('.settingTabs ul').removeClass('ui-widget-header')

    $('#junkfiles').on('mouseenter', function () {
        eel.getinfo($(this).attr('id'))(function (info) {
            console.log(info)
        })
    }).on('mouseleave', function () {

    })


})


eel.filesettings()(function (value) {
    $('#junkfileentry').val(value)
})

eel.getLaTeXSettings()(function (value) {
    
    if (value.message = 'success') {

        if (value.availableTexDistros.length != 0) {
            $('#tabs-3 ul.tex-distros').html('')
            value.availableTexDistros.forEach(item => {
                $('#tabs-3 ul.tex-distros').append(`<li>${item}</li>`)
            })
        }
        if (value.availablePdflatexPaths.length != 0) {
            // Önce select içeriğini temizleyin ve disabled özniteliğini kaldırın
            $('#tabs-3 .pdflatex-path select').html('').removeAttr('disabled');

            // Eğer daha önce seçilmiş bir distro varsa, bunu listenin başına ekleyin
            if (value.selectedPdflatexPath != '') {
                $('#tabs-3 .pdflatex-path select').append(`<option selected>${value.selectedPdflatexPath}</option>`);
            }

            // Daha sonra mevcut pdflatex yollarını ekleyin
            value.availablePdflatexPaths.forEach((item, index) => {
                // Eğer item zaten seçilmiş distro ile aynıysa, atlayın
                if (item === value.selectedPdflatexPath) return;

                // İlk öğe için selected özelliğini ekleyin
                const isSelected = index === 0 && value.selectedTexDistro === '' ? ' selected' : '';
                $('#tabs-3 .pdflatex-path select').append(`<option${isSelected}>${item}</option>`);
            });

        }




    }
})

eel.updatesettings()(function (value) {
    if (value) {
        $('#autoupdatecheckbox').click()
    }
}) *

    $('body').on('click', '.settings img#settingsIcon', function () {
        $('#settings').toggleClass('hidden')
    })

$('body').on('click', '.apply button', function () {


    eel.applySettings(
        $('#junkfileentry').val(),
        $('#autoupdatecheckbox').is(':checked'),
        $('#tabs-3 .pdflatex-path select option:selected').text()

    )


})




$('body').on('click', '#ask_for_update .buttons img', function () {
    if ($(this).attr('id') == 'applyupdate') {
        eel.update_()()
    } else {
        $('body div#ask_for_update').remove()
    }
})

/*
Error Logs
*/
$('body').on('click', '#settingsIcon', function(){
    eel.getSessionLogs()(function(logs){
        $('.logName').empty()
        logs.forEach((item)=>{
            const logRow = document.createElement('option')
            logRow.textContent = item
            $('.logName').append(logRow)
        })


        /*logs.forEach((item)=>{

            const errorRow = document.createElement('div')
            errorRow.className = 'errorRow'
            const time = document.createElement('a')
            const module = document.createElement('a')
            const errorLevel = document.createElement('a')
            const message = document.createElement('a')


            time.textContent =  item[0]
            time.className = 'time'
            module.textContent = item[1]
            module.className = 'module'
            errorLevel.textContent = item[2]
            errorLevel.className = 'errorLevel'
            message.textContent = item[3]
            message.className = 'message'

            errorRow.appendChild(time)
            errorRow.appendChild(module)
            errorRow.appendChild(errorLevel)
            errorRow.appendChild(message)

            $('#errorLogsShowDivision').append(errorRow)
            
        })*/

    })
})



$('body').on('click', '#getLog', function(){
    $('#errorLogsShowDivision').empty()
    eel.getSessionLog($('select.logname').find(":selected").val())(function(logs){
        logs.forEach((item)=>{

            const errorRow = document.createElement('div')
            errorRow.className = 'errorRow'
            const time = document.createElement('a')
            const module = document.createElement('a')
            const errorLevel = document.createElement('a')
            const message = document.createElement('a')


            time.textContent =  item[0] + ' '
            time.className = 'time'
            module.textContent = item[1] + ' '
            module.className = 'module'
            errorLevel.textContent = item[2] + ' '
            if (item[2] == 'INFO'){
                errorLevel.className = 'INFOo'
            }else if (item[2] == 'DEBUG'){
                errorLevel.className = 'DEBUG'
            }else if (item[2] == 'ERROR'){
                errorLevel.className = 'ERROR'
            }
            
            
            message.textContent = item[3] + ' '
            message.className = 'message'

            errorRow.appendChild(time)
            errorRow.appendChild(module)
            errorRow.appendChild(errorLevel)
            errorRow.appendChild(message)

            $('#errorLogsShowDivision').append(errorRow)
            
        })
    })
})