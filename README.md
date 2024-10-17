
# CircuitMacropy Nedir?

CircuitMacropy en basit tanımı ile m4 programlama dilini kullanarak çizimleri LaTeX ve PDF biçimine dönüştürmek için alternatif bir editördür.

# Nasıl Kullanılır?

CircuitMacropy python yazılım dilini kullanarak yazılmıştır ve bundan dolayı kullanılabilmesi için cihazınızda python 3.10 versiyonu bulunması gerekmektedir. Ayrıca otomatik güncelleme işlemleri için git uygulamasının cihazınızda bulunması gerekmektedir.

git: https://git-scm.com/downloads/win
Python3.10: https://www.python.org/downloads/release/python-31011/

## İlgili sürümün yüklenmesi

Yukarıda da bahseildiği gibi proje gereksinimlerinden dolayı Python yazılım dilinin 3.10 versiyonu bulunması gerekmektedir, ilgili versiyonu [buradaki linkten](https://www.python.org/downloads/release/python-3100/) kullandığınız platformu seçerek indirip kurabilirsiniz.

## Programın Başlatılması

Programın Windows cihazlarda kolayca başlatılması için run_windows.bat isminde bir çalıştırılabilir dosya mevcut, bu dosya bilgisayarınızdaki 3.10 sürümündeki python programını arar ve gerekli kütüphaneleri yükleyerek programı başlatır. Karşılaşılabilecek hatalar dosya çalıştırıldıktan sonraki ekranda görülebilir ve alınan hataya göre hata giderilebilir.

## Program Kullanımı

Program başlatıldığında ilk olarak sizden bir çalışma klasörü seçmeniz istenecektir, sol tarafta bulunan panelde buton kullanılarak çalışma klasörü belirlenir. Çalışma klasörü seçildikten sonra klasördeki dosyaların üzerine tıklanarak değişiklikler yapılabilir

## Dosya Düzenleme İşlemleri

Bir dosya seçildikten sonra dosya ortada gözüken panelde etikleşime girebileceğiniz bir alana aktarılacaktır ve bu alanda dosya üzerinde değişiklik yapabileceksiniz.


## Dosya Düzeni Nasıl Olmalı

Programın asıl işleyişi yazdığınız m4 Kodunu LaTeX koduna dönüştürecek ve ardından seçiminize göre PDF biçimine derleyecektir. Fakat bildiğiniz gibi PDF'e çevirme işlemlerinde işin LaTeX kısmını da düşünmeli ve başarılı derleme işlemi için m4 kodunu yazma kısmına LaTeX kodlarını da entegre etmeliyiz. Bu işlemin alternatifi olarak m4 kodlarını bu program aracılığıyla LaTeX koduna çevirip başka bir LaTeX dosyasına bu kodun kaynağını kullanarak içe aktarabilirsiniz.

### Örnek bir Düzen

Aşağıdaki düzende ilk olarak kullanılacak paketler içe aktarıldı, her ne kadar m4 dosyasında gözükmese bile m4 dosyası derlenerek LaTeX kodu haline geldiğinde bu paketleri içeren bir hal alacak bu sebepten dolayı paketleri içe aktarmak büyük önem taşır.

Sonraki adım olarak LaTeX kodunun PDF'e derlenirken hata vermemesi adına birer adet \begin ve \end blokları eklendi. Aşağıdaki kod bloğu kısa gözükse bile .PS ve .PE dışındaki her alana LaTeX kod biçimi yazılabilir ve derlenerek daha detaylı sayfalar ortaya çıkarabilirsiniz

```
\documentclass{standalone}
\usepackage{boxdims,tikz,steinmetz}
\usepackage{eqnarray,amsmath}
\usepackage{amsthm}
\usepackage{amssymb}
\usepackage{amsmath}
\begin{document}
.PS

cct_init
gen_init



resistor; line down 0.5
dot
{CAP: capacitor}
line down 0.5; corner
diode
line right 0.5
source

line to (Here.x, CAP.y)
dot
line to (CAP.x, CAP.y)
.PE

\end{document}
```

## M4 Kod Biçimi İçin Örnek Web Sayfaları


## Nasıl derlenir

Kodunuzu istediğiniz biçimde yazdıktan sonra ortadaki panelde aşağıda bulunan kutucuk ile çalıştığınız sayfayı "Derlenecek" olarak işaretlemeniz gerekli, bu kutucuk sayesinde tek seferde birden çok dosyayı aynı zamanda derleyebilirsiniz. Ne kadar çok dosyayı "Derlenecek" olarak işaretlerseniz iş yükü artacağı için büyük çaplı dosyalarda yalnızca derlemeniz gereken dosyayı "Derlenecek" olarak işaretlemeniz gerekir. Açılır menülerden ise dosyanın LaTeX veya PDF biçiminden birine ve hangi derleme yöntemi kullanılarak derleyeceğinizi (şu anlık yalnızca pgf mevcut) seçebilirsiniz. Derle butonuna basıldığında derleme işlemi başlayacaktır

## Derleme Sırasında Karşılaşılabilecek hatalar

Sık karşılaşılan hatalarda yapılan yazım yanlışları ve eksik kullanılan ()[]{} işaretler örnek verilebilir. Herhangi bir hata meydana geldiğinde bu hata bir bilfirim yoluyla ekranda gözükecektir ve dosyanız ilgili biçime dönüştürülmeyecektir. Daha detaylı hata incelemesi için sol alt tarafta bulunan ayarlar butonuna tıklanarak hata günlükleri kısmına ulaşılabilir ve hatanın analizi yapılabilir.

## Derlendikten Sonrası

Dosyanızı derledikten sonra eğer PDF biçimine derlediyseniz ilgili dosyaya tıkladığınızda programın sağ tarafında kalan kısmında bir önizleme sekmesi açıldığını görebilirsiniz. Bu sekmede yalnızca 1 adet PDF önizleyebilirsiniz ve önizleme işlemi canlı gerçekleştiğinden sonucu direkt derleme işleminden sonra herhangi bir işlem yapmadan görebilirsiniz. Sekmenin aşağısındaki bulunan tuşlardan eğer 1'den fazla sayfa bulunuyorsa bunlar arasında geçiş yapabilir, sayfayı büyütüp küçültebilirsiniz.

## Programın Güncelliği

Program her başlatıldığında internet bağlantısı olduğu sürece bir versiyon kontrolü yapmaktadır böylece yeni versiyonlarda program sizi haberdar edecek ve tek bir tık ile programı güncelleyebileceksiniz. Ayarlar kısmından otomatik güncelleme seçeneğini işaretleyerek programın kendisini otomatik güncellemesini sağlayabilirsiniz.


## TeX Dağıtımları

Bilgisayarınızda derleme işlemleri için mutlaka Texlive/MiKTeX gibi tex dağıtımları bulunmalıdır. CircuitMacropy kolaylık sağlamak adına devre çizimi için gerekli olan circuit-macros kütüphanesini kendiliğinden yükler fakat harici kütüphaneler için ilgili dağıtıma kütüphaneyi yüklemeniz gerekmektedir (miktex kendi içerisinde kütüphane yükleme işlemini barındırır). Eğer bilgisayarınızda birden fazla tex dağıtımı var ise CircuitMacropy'ın içindeki ayarlar kısmından hangi tex dağıtımını kullanarak derleyeceğinizi seçebilirsiniz.

## M4 Kod Biçimi İçin Kullanılabilecek Kaynaklar

#### [Kütüphanenin Kendi Web Sitesi](https://ece.uwaterloo.ca/~aplevich/Circuit_macros/html/examples.html)

Bu bağlantı üzerinden circuit-macros kütüphanesini geliştiren kişinin sunduğu detaylı ve çeşitli örnekler bulunan web sayfasını kullanabilirsiniz. içerisinde kütüphaneye ait çeşitli fonksiyonların nasıl kullanıldığı bulunmaktadır.

#### [M4 Dili İçin Örneklendirilmiş Web Sayfası](https://mbreen.com/m4.html)

Buradaki bağlantı genel M4 yapısına aşina olabilmeniz için gereken kaynaklardan biridir. İçeriğinde ilgili dilin nasıl ve hangi kurallar çerçevesinde kullanılması gerektiğini gösterir.

## Dikkat Edilmesi Gereken Sorunlar

- Programın yapısı gereği çalışılacak dosyalar harici bir depolama aygıtında bulunmamalıdır. Mutlaka bilgisayarınızın ana diski içerisinde yer almalıdır.
- İlk kullanım sırasında programın internete bağlı olması gerekmektedir. İlk çalıştırma sırasında gerekli bağımlılıklar yüklenir
