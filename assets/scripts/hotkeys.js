function checkCode(content) {

    const psBlocks = content.match(/\.PS([\s\S]*?)\.PE/);
    if (!psBlocks) {
        notification('Hiç .PS ve .PE blokları bulunamadı.', 'error');
        return;
    }

    const beforePS = content.split('.PS')[0].trim();
    const afterPE = content.split('.PE').pop().trim();
    
    if (!beforePS || !afterPE) {
        notification('.PS’den önce veya .PE’den sonra LaTeX kodu yok.', 'error');
        return;
    }

    const brackets = content.match(/[{}]/g);
    const stack = [];
    for (const char of brackets) {
        if (char === '{') {
            stack.push(char);
        } else if (char === '}') {
            if (stack.length === 0 || stack[stack.length - 1] !== '{') {
                notification('Eşleşmeyen kapalı parantez.', 'error');
                return;
            }
            stack.pop();
        }
    }
    
    if (stack.length > 0) {
        notification('Eşleşmeyen açık parantez.', 'error');
        return;
    }

    const begins = (content.match(/\\begin\{([^}]+)\}/g) || []).map(b => b.match(/\\begin\{([^}]+)\}/)[1]);
    const ends = (content.match(/\\end\{([^}]+)\}/g) || []).map(e => e.match(/\\end\{([^}]+)\}/)[1]);

    const beginSet = new Set(begins);
    const endSet = new Set(ends);

    if (beginSet.size === 0 || endSet.size === 0) {
        notification('En az bir \\begin ve bir \\end gereklidir.', 'error');
        return;
    }

    const missingEnds = [...beginSet].filter(begin => !endSet.has(begin));
    if (missingEnds.length > 0) {
        notification(`\\begin{${missingEnds[0]}} için eşleşen bir \\end{${missingEnds[0]}} bulunamadı.`, 'error');
        return;
    }

    notification('LaTeX kodu geçerli.');
}







document.addEventListener('keydown', function (event) {
    if (event.ctrlKey && event.key === 's') {
        event.preventDefault();  // Varsayılan "Sayfayı Kaydet" davranışını engelle

        // Burada kendi özelliğinizi ekleyin


        if ($(`.editor div[aria-hidden="false"] textarea`).length) {
            path = $(`.editor div[aria-hidden="false"] textarea`).attr('path')
            content = $(`.editor div[aria-hidden="false"] textarea`).val()
            //checkCode(content)
            eel.saveContent(path, content)(function (message) {
                if (message.message == 'success') {
                    notification(`${$('li.editorTabs.ui-tabs-active a').text()} dosyasi basariyla kaydedildi.`)
                }


                if ($('.editor div textarea').length == 1){
                    textarea = $('.editor div textarea')
                    
                }else{
                    textarea = $('.editor div[aria-hidden="false"] textarea')
                }
                $(`#${name_to_id(textarea.attr('path').split('\\').pop().split('/').pop())} a`).removeClass('notsaved')
        

            })
        } else {
            if ($(`.editor textarea`).length) {
                path = $(`.editor textarea`).attr('path')
                content = $(`.editor textarea`).val()
                //checkCode(content)
                eel.saveContent(path, content)(function (message) {
                    if (message.message == 'success') {
                        notification(`${$('li.editorTabs.ui-tabs-active a').text()} dosyasi basariyla kaydedildi.`)
                    }
                    if ($('.editor div textarea').length == 1){
                        textarea = $('.editor div textarea')
                        
                    }else{
                        textarea = $('.editor div[aria-hidden="false"] textarea')
                    }
                    $(`#${name_to_id(textarea.attr('path').split('\\').pop().split('/').pop())} a`).removeClass('notsaved')
            
                })


            }
        }



    }
});