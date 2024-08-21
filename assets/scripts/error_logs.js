// SELECT DISTRO POP-UP

$('body').on('click', 'div.enable', function() {
    $('div.enable').removeClass('selected-distro')
    $(this).addClass('selected-distro')
});




$('body').on('click', 'img#apply-distro-selection', function(){
    if ($('div.enable.selected-distro').length){

        eel.select_distro($('div.enable.selected-distro').text().split(':')[0])()
        notification(`Secilen tex dagitimi: ${$('div.enable.selected-distro').text().split(':')[0]}. Tex dagitimini daha sonradan LaTeX Ayarlari > Tex Dagitimini Seciniz kismindan degistirebilirsiniz`, 'success')
    }else{
        notification(`Hicbir tex dagitimi secilmedi, daha sonra ayarlar menusunden durumu degistirebilirsiniz. LaTeX Ayarlari > Tex Dagitimini Seciniz`, 'error');
    }

    $('#select-distros').css('display', 'none')
})
$('body').on('click', 'img#decline-distro-selection', function(){
    $('#select-distros').css('display', 'none')
    notification(`Hicbir tex dagitimi secilmedi, daha sonra ayarlar menusunden durumu degistirebilirsiniz. LaTeX Ayarlari > Tex Dagitimini Seciniz`, 'error');
})





// MAIN LOGS PAGE
$('body').on('click', '.error-label span', function(){
    mainpage = $(`
        <div class="error-logs-page">
            <div class="topbar">
            
                <div class="left-tools">
                </div>
                <div class="middle-tools">
                </div>                
                <div class="right-tools">
                    <img class="close-page" src="https://cdn-icons-png.flaticon.com/512/12503/12503635.png"></img>
                </div>
            </div>
        
        
        </div>`)

    $('body').prepend(mainpage)
})


$('body').on('click', '.error-logs-page .close-page', function(){
    $('.error-logs-page').remove()
})




$('body').on('click', 'button#compile', function(){
    if ($('select#compileas').val() == 'pdf'){
        if ($('.editor div textarea').length == 1){
            content = $('.editor div textarea').val()
            
        }else{
            content = $('.editor div[aria-hidden="false"] textarea').val()
        }
        console.log(content)


        if (!content.includes('begin{document}') & !content.includes('end{document}')){
            notification("Sozdizimi Hatasi: dosyalar pdf'e cevrilirken iceriginde latex kodlari olmalidir")
        }else if(!content.includes('usepackage')){
            notification("Sozdizimi Hatasi: dosyalar pdf'e cevrilirken iceriginde gerekli olan kutuphaneler usepackage ile ice aktarilmalidir")
        }

    }
})


$('body').on('change keyup', 'textarea', function() {

    /* 
    Zayif kod yazimi;

    textarea ogesinin kendi ozel idsi olarak path ozelligi verilmis ve bu ozellik ana makinadaki yolunu ifade eder
    ancak tree kismindaki dosya ismi yalnizca parenti olan div ve kendi id'si ile belirtilmistir

    textarea ogesinin path ozelligi su sekildedir -> C:/Users/ozank/Desktop/m4\devre.m4

    gorundugu gibi ana dosya yolu / ile ifade edilirken asil dosya ise sozdisiminde yasakli olan \ ile belirtilmistir
    
    */

    filename = $(this).attr('path').split('\\').pop().split('/').pop()

    $(`#${name_to_id(filename)} a`).addClass('notsaved')
  } );