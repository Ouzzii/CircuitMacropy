$(document).ready(function () {
    let notificationQueue = [];
    let isProcessing = false;
    
    function notification(message, type = 'info', duration = 5000) {
        // Bildirim divini oluştur
        let notification = $('<div class="notification"></div>')
            .addClass(type)
            .html(`
                <p>${message}</p>
                <button class="close-icon">❌</button>
            `);
    
        // Kapatma ikonuna tıklama olayı
        notification.find('.close-icon').on('click', function () {
            closeNotification(notification);
        });
    
        // Bildirimleri sayfaya ekle
        $('body').append(notification);
    
        // Bildirimlerin işlenmesini başlat
        notificationQueue.push({ element: notification, duration: duration });
    
        // Bildirimlerin işlenmesini başlat
        if (!isProcessing) {
            processNotifications();
        }
    }
    
    function closeNotification(notification) {
        notification.removeClass('show').addClass('hide');
        setTimeout(() => {
            notification.remove();
            notificationQueue = notificationQueue.filter(n => n.element[0] !== notification[0]);
            updateNotificationPositions(); // Update positions after removal
            processNotifications();
        }, 500);
    }
    
    function updateNotificationPositions() {
        let position = 30; // Initial position from the bottom
        $('.notification').each((index, element) => {
            $(element).css('bottom', `${position}px`);
            position += $(element).outerHeight() + 10; // Add height of each notification plus gap
        });
    }
    
    function processNotifications() {
        if (notificationQueue.length === 0) {
            isProcessing = false;
            return;
        }
    
        isProcessing = true;
    
        // İlk bildirim al
        let { element: currentNotification, duration } = notificationQueue[0];
    
        // İlk bildirim tamamlandıktan sonra diğer bildirimlerin sürelerini ayarla
        setTimeout(() => {
            closeNotification(currentNotification);
        }, duration);
    
        // Ensure that notifications are displayed one at a time
        setTimeout(() => {
            updateNotificationPositions();
            processNotifications();
        }, 500);
    }
        
    window.notification = notification





















    /* Detect tex distros */

    eel.detect_tex_distros()(function ([distros, boxdims]) {
        if (typeof distros == 'object') {
            let distrosEntries = Object.entries(distros['pdflatex-paths']);
            let distrosHtml = distrosEntries.map(([index]) => {
                let status = boxdims[index] ? '✓ Boxdims kurulu' : 'x Boxdims kurulumunda hata meydana geldi';
                let additionalClass = boxdims[index] ? 'enable' : '';
                return `<div class="${additionalClass}">${index}: ${status}</div>`;
            }).join('');

            // False olan değerleri kontrol et
            let hasError = Object.values(boxdims).some(value => !value);

            if (hasError) {
                distrosHtml += `
                    <div class="error-label" style="color: red; margin-top: 20px;">
                        boxdims kurulumunda bir hata ile karşılaşıldı, detaylı ayrıntı için <span>hata kayıtlarına</span> bakabilirsiniz.
                    </div>`;
            }

            $('#select-distros').html(`
                <div>
                    <label>Bilgisayarınızda aşağıdaki tex dağıtımları bulundu, lütfen bır dağıtım seçiniz:</label>
                    ${distrosHtml}
                </div>
                <div class='distro-selection-buttons'>
                    <img id='decline-distro-selection' src="https://cdn-icons-png.flaticon.com/512/12503/12503575.png">
                    <img id='apply-distro-selection' src="https://cdn-icons-png.flaticon.com/512/12503/12503570.png">
                </div>
            `);
            $('#select-distros').css('display', 'block')

        } else if(typeof distros == 'string')(
            notification(`Daha onceden ${distros} dagitiminin secildigi tespit edildi. Daha sonra ayarlar menusunden durumu degistirebilirsiniz; Dosya Ayarlari > Tex Dagitimini Seciniz`)
        )
    });






    eel.Is_there_an_update_available()(function (html) {

        if (html.message == 'update available') {
            $('#ask_for_update').html(html.html_content)
            $('#ask_for_update').css('display', 'block')
        } else if (html.message == 'already up to date') {

        } else if (html.message == 'no internet connection') {
            notification(`İnternet bağlantısı bulunmadığından versiyon kontrolü yapılamadı`, `error`)
            //$('#no-internet-connection').html(html.html_content)
            //$(".no-connection-alert").fadeOut(7500, function () {
            //    $(this).remove();
            //});
        }

    })

    eel.getColorPalette("SunsetHarmony")(function (json) {
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


    /*eel.getSettings()(function (html) {
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
        console.log(value)
        $('#junkfileentry').val(value)
    })

    eel.updatesettings()(function (value) {
        console.log(value)
        if (value) {
            $('#autoupdatecheckbox').click()
        }
    })*/


    eel.createCircuitMacros()(function () {
        $('iframe.waiting').css('display', 'none')
        $('.treeview button').css('display', 'block')
    })



})


