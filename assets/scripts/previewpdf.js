
var pdfDoc = null,
  pageNum = 1,
  pageRendering = false,
  pageNumPending = null,
  scale = 1,
  canvas = document.getElementById("the-canvas");
  ctx = canvas.getContext("2d");
  outputScale = window.devicePixelRatio || 1;


function renderPage(num) {
  pageRendering = true;
  pdfDoc.getPage(num).then((page) => {

    var viewport = page.getViewport({ scale: scale });
    //canvas.height = viewport.height
    //canvas.width = viewport.width

    canvas.width = Math.floor(viewport.width * outputScale);
    canvas.height = Math.floor(viewport.height * outputScale);
    canvas.style.minwidth = Math.floor(viewport.width) + "px";
    canvas.style.height = Math.floor(viewport.height) + "px";
    //console.log(Math.floor(viewport.width) + "px", Math.floor(viewport.height) + "px")
    console.log(
      Math.floor(viewport.width * outputScale),
      Math.floor(viewport.height * outputScale)
    );
    console.log($("#preview").css("height"));

    var renderContext = {
      canvasContext: ctx,
      viewport: viewport,
    };

    var renderTask = page.render(renderContext);

    renderTask.promise.then(() => {
      pageRendering = false;
      if (pageNumPending !== null) {
        renderPage(pageNumPending);
        pageNumPending = null;
      }
    });
  });

  document.getElementById("zoom").textContent = (scale - 1) * 100 + "%";
  // document.getElementById('page_num').textContent = num
}


// sync
/*function getAndPut() {
  fetch("/get_pdf")
    .then((response) => response.arrayBuffer())
    .then((arrayBuffer) => {
      pdfjsLib.getDocument({ data: arrayBuffer }).promise.then(function (pdf) {
        pdfDoc = pdf;
        renderPage(1);
      });
    });
}*/
// async
/*async function getAndPut(path){
    response = await fetch(path)
    content = await response.arrayBuffer()
    pdfjsLib.getDocument({ data: content }).promise.then(function (pdf) {
        pdfDoc = pdf;
        renderPage(parseInt($('#pageNum')[0].textContent));
      });
}*/

//async
async function preview(path){
  if(path!=''){
    console.log(id_to_name(path))
    eel.getpdf(id_to_name(path))(function(content){
      console.log(content)
      var PDFcontent = atob(content)
      pdfjsLib.getDocument({ data: PDFcontent }).promise.then(function (pdf) {
        pdfDoc = pdf;
        renderPage(parseInt($('#pageNum')[0].textContent));
      });
    })


  
  }
}









document.getElementById("zoomOut").addEventListener("click", function () {
  if (scale != 1) {
    scale -= 1;
    renderPage(parseInt($('#pageNum')[0].textContent));
    console.log(scale);
  }
});

document.getElementById("zoomIn").addEventListener("click", function () {
  scale += 1;
  renderPage(parseInt($('#pageNum')[0].textContent));
  console.log(scale);
});


// Derleme işlemi

function Derlenenecekler(){
  const derlenecek_girisler = $(`input[type='checkbox']:checked`)
  const derlenecekler = []
  if (derlenecek_girisler.length!=0){
    for (let i=0;i<derlenecek_girisler.length;i++){
      const path = derlenecek_girisler[i].parentNode.parentNode.parentNode.firstChild.nextElementSibling.getAttribute('path') 
      const elem = derlenecek_girisler[i].parentNode.parentNode.parentNode.firstChild.nextElementSibling
      if (path.endsWith('.tex')){
        derlenecekler.push({
          Path: path,
          Content: elem.value,
          Function: 'compileAsPdf'
        })
      }
      else if (!path.endsWith('.pdf')){
        derlenecekler.push({
          Path: path,
          Content: elem.value,
          Function: 'compileAsTex'
        })
       }
    }
  }

  return derlenecekler
}
  


function Derle(derlenecekler){
  $('.waiting').each(function(){
    $(this).css('visibility', 'visible')
  })

  fetch('/derle', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({Contents: derlenecekler})
  }).then(()=>{
    //$('.waiting').css('visibility', "visible")
    $('.treeview').empty()
    openFolder()
  }).then(()=>{
    //$('.waiting').css('visibility', "hidden")
    $('.waiting').each(function(){
      $(this).css('visibility', 'hidden')
    })
  }).then(()=>{
    preview($('#the-canvas')[0].className)
  })



}




$('body').on('click', ".Derle button", function(element){
  //$('#waiting').css('visibility', "visible")

  //Derle(Derlenenecekler())

  
  //$('#waiting').css('visibility', "hidden")
})

$('body').on('click', '.previousPage', function(){
  console.log('prev')
  if (parseInt($('#pageNum')[0].textContent) != 1){
    $('#pageNum')[0].textContent = parseInt($('#pageNum')[0].textContent)-1
    preview($('#the-canvas')[0].className)
  }


})

$('body').on('click', '.nextPage', function(){
  console.log('next')

    $('#pageNum')[0].textContent = parseInt($('#pageNum')[0].textContent)+1
    preview($('#the-canvas')[0].className)

})