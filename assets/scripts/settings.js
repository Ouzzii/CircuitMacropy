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

    $('body').on('click', '.settings img:first-child', function () {
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