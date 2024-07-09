

function placeToTreeView(files) {
    $('#openfolder').css('display', 'none')
    $('.treeview').prepend(treeTitle(files[0].path))
    $('.treeview .filesfolders').css('display', 'block')

    const appended = []


    for (let i = 0; i < files.length; i += 1) {
        //console.log(files[i].dir.split("\\").length == '2')
        //console.log(appended.includes(files[i].dir))
        if (files[i].dir == '') {
            $('.treeview .filesfolders').append(file(files[i]))
        }

        else if (files[i].dir.split("/").length == '2' && !appended.includes(files[i].dir)) {
            $('.treeview .filesfolders').append(folder(files[i]))
            appended.push(files[i].dir)
        }

        else if (files[i].dir.split("\\").length == '2' && !appended.includes(files[i].dir)) {
            $('.treeview .filesfolders').append(folder(files[i]))
            appended.push(files[i].dir)
        }


        else if (files[i].dir.split("/").length > '2') { // tüm alt indexler

            if (!appended.includes(files[i].dir)) {
                var dirs = files[i].dir.split('/') // mevcut olmayan klasörleri eklemek
                var res = []
                for (var j = 0; j <= dirs.length; j += 1) {
                    filename = dirs[1].replace('#', 'mcrpy35mcrpy').replace('.', 'mcrpy46mcrpy')
                    //console.log(filename)
                    if ($('#'+filename).length == 0) {
                        $('#'+res.join(' #')).append(subFolder(filename, j + 1))

                    }

                    res.push(filename)
                    dirs.shift()
                }

                appended.push(files[i].dir)
            }
            if (files[i].file != '') {
                const dir = files[i].dir.replace('#', 'mcrpy35mcrpy').replace('.', 'mcrpy46mcrpy')
                const file = files[i].file.replace('#', 'mcrpy35mcrpy').replace('.', 'mcrpy46mcrpy')
                $(`${dir.split('/').join(' #')}`).append(subFile(file, dir.split('/').length)) // alt dosyalar

            }
        }

        else if (files[i].dir.split("\\").length > '2') { // tüm alt indexler

            if (!appended.includes(files[i].dir)) {
                var dirs = files[i].dir.split('\\') // mevcut olmayan klasörleri eklemek
                var res = []
                for (var j = 0; j <= dirs.length; j += 1) {
                    filename = dirs[1].replace('#', 'mcrpy35mcrpy').replace('.', 'mcrpy46mcrpy')
                    //console.log(filename)
                    if ($(`#${filename}`).length == 0) {
                        $(`#${res.join(' #')}`).append(subFolder(filename, j + 1))

                    }

                    res.push(filename)
                    dirs.shift()
                }

                appended.push(files[i].dir)
            }
            if (files[i].file != '') {
                const dir = files[i].dir
                const file = files[i].file
                //const dir = files[i].dir.replace('#', 'mcrpy35mcrpy').replace('.', 'mcrpy46mcrpy')
                //const file = files[i].file.replace('#', 'mcrpy35mcrpy').replace('.', 'mcrpy46mcrpy')
                $(`${dir.split('\\').join(' #')}`).append(subFile(file, dir.split('\\').length)) // alt dosyalar

            }
        }

    }

}




function openFolder() {
    eel.openfolder()(function(path){
        if (path != ''){
            eel.getfiles(path)(function(files){
                $('.treeViewTitle').remove()
                $('.filesfolders').empty()
                placeToTreeView(files)
            })
        }
    })
}




function updateFolderAsync(){

    const openeds = $('.dir.opened')// > :first-child')


    if (!$('#new').length){
        eel.getWorkspaceFolder()(function(workspaceFolder){
            if (workspaceFolder != ''){
                eel.getfiles(workspaceFolder)(function(files){

                    $('.treeViewTitle').remove()
                    $('.filesfolders').empty()
                    placeToTreeView(files)
                    openeds.each(function(){
                        $("div#"+$(this).attr('id')).children(':first').click()
                    })
                })
            }
        })
    }

}


$('#openfolder button').on('click', function () {
    openFolder()
    //var updateFolder = setInterval(function(){
    //    updateFolderAsync()
    //}, 1000)
})

// Create file and folder structures
function treeTitle(title) {
    return `
    <div class='treeViewTitle'>
        <h3>~/${title}</h3>
        <div class='icons'>
            <img class='newfile' src='https://cdn-icons-png.flaticon.com/512/7163/7163764.png'>
            <img class='closeWorkspace' src='https://cdn-icons-png.flaticon.com/512/12503/12503635.png'>
        </div>
    </div>
    `
}
function folder(key) {
    return `<div class='dir closed' id='${name_to_id(key.dir.split('\\')[1])}'><a>~/${id_to_name(key.dir)}</a></div>`
}
function file(key) {
    return `<div class='file' id='${name_to_id(key.file)}'><a>${id_to_name(key.file)}</a> <img class='dots' src="https://cdn-icons-png.flaticon.com/512/2311/2311524.png"></div>`
}
function subFolder(key, layer) {
    return `<div class='dir closed' style='padding-left:${layer * 10}px' id='${name_to_id(key)}'><a>~/${id_to_name(key)}</a></div>`
}
function subFile(key, layer) {
    return `<div class='file' style='padding-left:${layer * 10}px' id='${name_to_id(key)}'><a>${id_to_name(key)}</a></div>`
}


$(document).ready(function() {
    $('.editor').tabs();
    $('.previewTabs').tabs();
});





$('body').on('click', '.file a', function (element) {
    var parentNode = $(this).parent().parent().parent()
    if (!$(this).html().includes('.pdf')){
        if ($(`.editor ul a`).length != 0){
            var id_ = ['tabs', Array.from($(`.editor ul a`)).reverse()[0]['href'].split('-')[1]]
        
        }else
        {
            var id_ = ['tabs', '0']
        }


    if (parentNode.hasClass('treeview')) {
        getFileContent($(this).parent().attr('id'), 'R0000T', id_)
    } else {
        //getFileContent($(this).parent().attr('id'), parentNode.attr('id'), id_)
        getFileContent($(this).parent().attr('id'), $(this).parent().parent().attr('id'), id_)

    }
    
    $('.editor ul').append(`
        <li class='editorTabs'>
            <a href="#${id_[0] + '-' + (parseInt(id_[1]) + 1)}" tabindex="-1" class="ui-tabs-anchor" id="ui-id-${parseInt(id_[1]) + 1}">${element.currentTarget.textContent}</a>
            <img class='closeTab' src='https://cdn-icons-png.flaticon.com/512/1828/1828665.png'>
        </li>
    `)
    const tab_index = Array.from(document.querySelectorAll('.editor ul li')).indexOf($('.editor ul .ui-state-active')[0])
    $('.editor').tabs('destroy')
    $('.editor').tabs({
        active: tab_index
        })

}else{
    if (parentNode.hasClass('treeview')){
        var path = '\\' + 'R0000T' + '\\' + $(this).parent().attr('id')
    }else{
        var path = '\\' + parentNode.attr('id') + '\\' + $(this).parent().attr('id')
    }
    console.log(path)
    preview(path).then(()=>{
        $('#the-canvas').addClass(path)
    })

}

})

$('body').on('click', '.closeTab', function(){
    const tabid = parseInt($(this)[0].previousElementSibling['href'].split('-')[1])

    $(`li[aria-controls='tabs-${tabid}']`)[0].remove()
    $(`div#tabs-${tabid}`)[0].remove()
    

})



$('body').on('click', '.dir a', function(){
    //console.log($(this).parent())
    if ($(this).parent().attr('class').includes('closed')){
        $(this).parent().removeClass('closed')
        $(this).parent().addClass('opened')
    }else{
        $(this).parent().addClass('closed')
        $(this).parent().removeClass('opened')
    }
})





async function getFileContent(file, parentdir, id) {
    if (parentdir!='R0000T'){
    var parent = parentdir
}else{
    var parent = 'R0000T'
}
    console.log(parent, id_to_name(file))
    const data = eel.getcontent(parent, id_to_name(file))(function(fileContent){
        var content = fileContent.content
        var fullpath = fileContent.fullpath
        if (id[1] != 0){
        $('.editor').append(`
        <div id='${id[0] + '-' + (parseInt(id[1]) + 1)}' style='display: none;'>
            <textarea spellcheck='false' path='${fullpath}'>${content}</textarea>
            <div class='Derlenecek'>
                <div class='Derle'>
                    <img class='waiting' src='https://i.gifer.com/XVo6.gif' height='50' width='50' style='visibility: hidden;'>
                    <select name="compileas" id="compileas">
                        <option value="novalue" selected disabled hidden>Bir Hedef Seçin</option>
                        <option value="latex">LaTeX</option>
                        <option value="pdf">PDF</option>
                    </select>
                    <select style='display: none;' name='withcompile' id='withcompile'></select>
                    <button id="compile">olarak derle</button>
                    <input id="willcompile" type="checkbox">
                </div>
            </div>
        </div>`)
        }else{
            $('.editor').append(`
            <div id='${id[0] + '-' + (parseInt(id[1]) + 1)}'>
                <textarea spellcheck='false' path='${fullpath}'>${content}</textarea>
                <div class='Derlenecek'>
                    <div class='Derle'>
                        <img class='waiting' src='https://i.gifer.com/XVo6.gif' height='50' width='50' style='visibility: hidden;'>
                        <select name="compileas" id="compileas">
                        <option value="novalue" selected disabled hidden>Bir Hedef Seçin</option>
                            <option value="latex">LaTeX</option>
                            <option value="pdf">PDF</option>
                        </select>
                        <select style='display: none;' name='withcompile' id='withcompile'></select>
                        <button id="compile">olarak derle</button>
                        <input id="willcompile" type="checkbox">
                    </div>
                </div>
            </div>`)
        }
    })
}


// Yeni Dosya Oluşturma

$('body').on('click', '.newfile', function(){
    if ($('.filesfolders #new').length === 0){
        $('.filesfolders').append(`
            <div id="new">
                <div>
                    <label>Yeni Dosya</label>
                    <img src='https://cdn-icons-png.flaticon.com/512/12503/12503635.png'>
                </div>
                <input type='text'>
            </div>
        `)
        $('#new input').focus()

    }
})

// Dosya Adı Girme Yeri Dışında Herhangi Bir Yere Tıklandığında Dosyayı Kaydet

$(document).on('click', function(event){
    if ($('.notopen').css('display') == 'none'){
        if (!$(event.target).closest('#new').length && $('#new input').val() != '' && $('#new input').length) {
            eel.saveFile($('#new input').val())()
            $('#new').remove()
        }
    }
})



$('body').on('click', 'div#new img', function(){
    $('#new').remove()
})


$('body').on('keydown', '#new input', function(event) {
                // 13 is the keycode for the Enter key
                console.log(event.keyCode)
                if (event.keyCode == 13) {
                    // Prevent the default action (if necessary)
                    event.preventDefault();
                    eel.saveFile($('#new input').val())()
                    $('#new').remove()
                } else if (event.keyCode == 27){
                    $('#new').remove()
                }
            });


// Çalışma alanını kapatma

$('body').on('click', '.closeWorkspace', function(){
    $('.notopen#openfolder').css('display', 'flex')
    $('.treeViewTitle').remove()
    $('.filesfolders').empty()
    $('.filesfolders').css('display', 'none')
    eel.clearWorkspace()()
})

$('body').on('click', '.dots', function(){
    console.log($(this))

})



function name_to_id(content){
    return content
    .replace('#', 'mcrpy35mcrpy')
    .replace('.', 'mcrpy46mcrpy')
}

function id_to_name(content){
    return content
    .replace('mcrpy35mcrpy', '#')
    .replace('mcrpy46mcrpy', '.')
}