function placeToTreeView(files) {
    $('#openfolder').remove()
    $('.treeview').prepend(treeTitle(files[0].path))

    const appended = []


    for (let i = 0; i < files.length; i += 1) {
        if (files[i].dir == '') {
            $('.treeview').append(file(files[i]))
        }
        else if (files[i].dir.split("\\").length == '2' && !appended.includes(files[i].dir)) {
            $('.treeview').append(folder(files[i]))
            appended.push(files[i].dir)
        }

        else if (files[i].dir.split("\\").length > '2') { // tüm alt indexler

            if (!appended.includes(files[i].dir)) {
                var dirs = files[i].dir.split('\\') // mevcut olmayan klasörleri eklemek
                var res = []
                for (var j = 0; j <= dirs.length; j += 1) {

                    if ($(`#${dirs[1]}`).length == 0) {
                        $(`#${res.join(' #')}`).append(subFolder(dirs[1], j + 1))

                    }

                    res.push(dirs[1])
                    dirs.shift()
                }

                appended.push(files[i].dir)
            }
            if (files[i].file != '') {
                $(`${files[i].dir.split('\\').join(' #')}`).append(subFile(files[i].file, files[i].dir.split('\\').length)) // alt dosyalar

            }
        }

    }

}




async function openFolder() {
    
    eel.openfolder()(function(path){
        eel.getfiles(path)(function(files){
            placeToTreeView(files)
        })
    })
}



$('#openfolder button').on('click', function (element) {
    openFolder()
})

// Create file and folder structures
function treeTitle(title) {
    return `<p class='treeViewTitle'>~/${title}</p>`
}
function folder(key) {
    return `<div class='dir' id='${key.dir.split('\\')[1]}'><a>~/${key.dir}</a></div>`
}
function file(key) {
    return `<div class='file' id='${key.file}'><a>${key.file}</a></div>`
}
function subFolder(key, layer) {
    return `<div class='dir' style='padding-left:${layer * 10}px' id='${key}'><a>~/${key}</a></div>`
}
function subFile(key, layer) {
    return `<div class='file' style='padding-left:${layer * 10}px' id='${key}'><a>${key}</a></div>`
}


$(document).ready(function() {
    $('.editor').tabs();
    $('.previewTabs').tabs();
});





$('body').on('click', '.file', function (element) {
    if (!element.currentTarget.textContent.includes('.pdf')){
        if ($(`.editor ul a`).length != 0){
            var id_ = ['tabs', Array.from($(`.editor ul a`)).reverse()[0]['href'].split('-')[1]]
        
        }else
        {
            var id_ = ['tabs', '0']
        }


    if (element.currentTarget.parentNode.className == 'treeview') {
        getFileContent(element.currentTarget.id, 'R0000T', id_)
    } else {
        getFileContent(element.currentTarget.id, element.currentTarget.parentNode.id, id_)

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
    if (element.currentTarget.parentNode.className == 'treeview'){
        var path = '\\' + 'R0000T' + '\\' + element.currentTarget.id
    }else{
        var path = '\\' + element.currentTarget.parentNode.id + '\\' + element.currentTarget.id
    }

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




async function getFileContent(file, parentdir, id) {
    if (parentdir!='R0000T'){
    var parent = 'parentdir'
}else{
    var parent = 'R0000T'
}
    const data = eel.getcontent(parent, file)(function(fileContent){
        var content = fileContent.content
        var fullpath = fileContent.fullpath
        if (id[1] != 0){
        $('.editor').append(`
        <div id='${id[0] + '-' + (parseInt(id[1]) + 1)}' style='display: none;'>
            <textarea spellcheck='false' path='${fullpath}'>${content}</textarea>
            <div class='Derlenecek'>
                <div>Derle ve önizle: 
                    <input type='checkbox'>
                </div>
                <div class='Derle'>
                    <img class='waiting' src='https://i.gifer.com/XVo6.gif' height='50' width='50' style='visibility: hidden;'>
                    <button>Derle</button>
                </div>
            </div>
        </div>`)
        }else{
            $('.editor').append(`
            <div id='${id[0] + '-' + (parseInt(id[1]) + 1)}'>
                <textarea spellcheck='false' path='${fullpath}'>${content}</textarea>
                <div class='Derlenecek'>
                    <div>Derle ve önizle: 
                        <input type='checkbox'>
                    </div>
                    <div class='Derle'>
                        <img class='waiting' src='https://i.gifer.com/XVo6.gif' height='50' width='50' style='visibility: hidden;'>
                        <button>Derle</button>
                    </div>
                </div>
            </div>`)
        }
    })
}
