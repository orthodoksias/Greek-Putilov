# -*- coding: utf-8 -*-
"""Генератор трёхъязычного сайта «Греческий клуб Путиловского храма»."""
import os, html

OUT = "/home/claude/Greek-Putilov"

GR_CONS = "https://www.mfa.gr/russia/ru/consulate-general-st-petersburg/"
CY_CONS = "http://www.mfa.gov.cy/mfa/consulate/consulate_spb.nsf/index_ru/index_ru?OpenDocument"
VK = "https://vk.ru/putilovsky1906"
TG = "https://t.me/s/greeks_of_SaintPetersburg"
GREEKSPB = "https://greekspb.com/"
GLOBUS = "https://globus.aquaviva.ru/khram-svt-nikolaya-chudotvortsa-i-mts-tsaritsy-aleksandry-putilovskiy/photo"
TEMPLE = "https://putilovskij-hram.ru"
GALLERY = [
 ("steps1",  {"ru":"Участники встречи у входа в храм","el":"Οι συμμετέχοντες στην είσοδο του ναού","en":"Participants at the church entrance"}),
 ("steps2",  {"ru":"Встреча греческого сообщества у храма","el":"Συνάντηση της ελληνικής κοινότητας έξω από τον ναό","en":"Greek community gathering outside the church"}),
 ("church1", {"ru":"После богослужения в храме","el":"Μετά την ακολουθία στον ναό","en":"After the service in the church"}),
 ("yard1",   {"ru":"Во дворе у трапезной храма","el":"Στην αυλή δίπλα στην τράπεζα του ναού","en":"In the courtyard by the church refectory"}),
 ("yard2",   {"ru":"Гости и члены общины во дворе храма","el":"Προσκεκλημένοι και μέλη της κοινότητας στην αυλή του ναού","en":"Guests and community members in the church courtyard"}),
 ("asterix", {"ru":"Семейный праздник в трапезной, 1 июня 2026","el":"Οικογενειακή γιορτή στην τράπεζα, 1 Ιουνίου 2026","en":"Family gathering in the refectory, 1 June 2026"}),
 ("may25-1", {"ru":"Панихида по жертвам геноцида, май 2025","el":"Μνημόσυνο για τα θύματα της Γενοκτονίας, Μάιος 2025","en":"Memorial service for the genocide victims, May 2025"}),
 ("may25-2", {"ru":"Настоятель на панихиде, май 2025","el":"Ο προϊστάμενος στο μνημόσυνο, Μάιος 2025","en":"The rector at the memorial service, May 2025"}),
 ("may25-3", {"ru":"Участники памятной встречи, май 2025","el":"Οι συμμετέχοντες στην εκδήλωση μνήμης, Μάιος 2025","en":"Participants of the commemoration, May 2025"}),
 ("may25-4", {"ru":"Приветствие за чаепитием в трапезной, май 2025","el":"Χαιρετισμός κατά το τσάι στην τράπεζα, Μάιος 2025","en":"A greeting at the tea in the refectory, May 2025"}),
 ("athos1",  {"ru":"Афон: иллюстрации к циклу лекций «Благость Афона»","el":"Άγιον Όρος: εικόνες για τον κύκλο διαλέξεων «Η Χάρις του Άθω»","en":"Athos: illustrations for the lecture cycle “The Grace of Athos”"}),
 ("athos2",  {"ru":"Афон: иллюстрации к циклу лекций «Благость Афона»","el":"Άγιον Όρος: εικόνες για τον κύκλο διαλέξεων «Η Χάρις του Άθω»","en":"Athos: illustrations for the lecture cycle “The Grace of Athos”"}),
]
CARD_IMG = {"kids":"asterix","pontos25":"may25-1"}
RECTOR_IMG = "rector"

# ---------- события (общая часть: даты, ссылки) ----------
# ключ: (sort, iso, tg-link)
EVENTS = [
    ("2026-10-25", "https://t.me/greeks_of_SaintPetersburg/986", "oxi26"),
    ("2026-07-24", "https://t.me/c/1945782712/5873", "film2"),
    ("2026-06-07", "https://t.me/greeks_of_SaintPetersburg/887", "athos2"),
    ("2026-06-01", "https://t.me/greeks_of_SaintPetersburg/890", "kids"),
    ("2026-05-23", "https://t.me/c/1945782712/5691", "film1"),
    ("2026-05-17", "https://t.me/c/1945782712/5576", "pontos26"),
    ("2026-03-22", "https://t.me/c/1945782712/5342", "indep26"),
    ("2026-02-15", "https://t.me/greeks_of_SaintPetersburg/779", "athos1"),
    ("2025-05-18", "https://greekspb.com/", "pontos25"),
    ("2019-10-27", "https://www.orthodoxianewsagency.gr/pdf.php?id=157075", "oxi19"),
    ("2018-03-25", "https://www.mfa.gr/russia/ru/consulate-general-st-petersburg/news/obiavlieniie.html", "nat18"),
]

MONTHS = {
    "ru": ["января","февраля","марта","апреля","мая","июня","июля","августа","сентября","октября","ноября","декабря"],
    "el": ["Ιανουαρίου","Φεβρουαρίου","Μαρτίου","Απριλίου","Μαΐου","Ιουνίου","Ιουλίου","Αυγούστου","Σεπτεμβρίου","Οκτωβρίου","Νοεμβρίου","Δεκεμβρίου"],
    "en": ["January","February","March","April","May","June","July","August","September","October","November","December"],
}

def fmt_date(lang, iso):
    y, m, d = iso.split("-")
    mo = MONTHS[lang][int(m) - 1]
    d = int(d)
    return f"{d} {mo} {y}" if lang != "en" else f"{mo} {d}, {y}"

def a(href, text):
    return f'<a href="{html.escape(href)}" target="_blank" rel="noopener">{text}</a>'

# ---------- тексты ----------
def T(lang):
    gr, cy = GR_CONS, CY_CONS
    if lang == "ru":
        return dict(
            lang="ru", title="Греческий клуб Путиловского храма",
            desc="Встречи греческого сообщества Санкт-Петербурга в храме святителя Николая Чудотворца и мученицы царицы Александры (Путиловском).",
            nav=[("about","О храме"),("meetings","Встречи"),("media","Фото и видео"),("contacts","Контакты")],
            hero_kicker="Санкт-Петербург · пр. Стачек, 48",
            hero_h="Греческий клуб Путиловского храма",
            hero_p="Богослужения на греческом языке, памятные даты, лекции об Афоне, киноклуб и семейные встречи греков Петербурга в храме святителя Николая Чудотворца и мученицы царицы Александры.",
            hero_btn="Ближайшие и прошедшие встречи",
            about_h="О храме",
            hist_h="История Путиловского храма",
            hist=[
              "Храм святителя Николая Чудотворца и мученицы царицы Александры построен при Путиловском заводе. Строительство началось в 1901 году; деньги собирали сами рабочие, добровольно отчисляя часть заработка. Храм возвели в память об основателе завода Николае Ивановиче Путилове.",
              "Освящение состоялось в 1906–1907 годах: верхний храм посвящён святителю Николаю, нижний (в крипте) — великомученику Георгию Победоносцу. Позднее в склеп при храме перенесли останки самого Н. И. Путилова и его супруги.",
              "Проект выполнил архитектор Василий Косяков в русско-византийском стиле; интерьер был оформлен в древнерусском духе, утварь и паникадила изготовила фирма братьев Оловянишниковых.",
              "В 1925 году храм закрыли, а в конце 1920-х перестроили в заводской клуб «Красный путиловец»: были снесены купола и колокольня, в фасад врезали стеклянную призму. Здание вернули церкви в 2000-х годах; сегодня это объект культурного наследия регионального значения. В храме идут службы, работают воскресная школа, молодёжный и другие клубы.",
            ],
            rector_h="Настоятель храма",
            rector_name="Протоиерей Владимир Гончаренко",
            rector=[
              "Родился 29 ноября 1976 года. Окончил физический факультет Санкт-Петербургского государственного университета (1997), Санкт-Петербургскую духовную семинарию (2001) и Санкт-Петербургскую духовную академию (2005); в 2004–2005 годах учился в Афинском национальном университете имени Каподистрии. Кандидат богословия, преподаёт в Санкт-Петербургской духовной академии.",
              "Диаконская хиротония — 4 декабря 2005 года, иерейская — 15 января 2006 года; в сан протоиерея возведён в 2016 году. Настоятелем Путиловского храма назначен 4 марта 2006 года — вскоре после возвращения здания Церкви; первая после долгого перерыва Божественная литургия в нижнем храме состоялась в марте 2006 года.",
              "Отец Владимир много лет поддерживает греческое сообщество Петербурга: совершает богослужения с греческими песнопениями и проповедью на греческом языке, служит панихиды и литии в памятные для греков дни, радушно принимает встречи общины в трапезной храма.",
            ],
            meet_h="Встречи греческого сообщества в храме",
            meet_p=f"Храм стал одной из постоянных площадок для греков Санкт-Петербурга. Службы к национальным датам проходят совместно с Генеральным консульством Греции ({a(gr,'сайт консульства')}) и при участии Генерального консульства Республики Кипр ({a(cy,'сайт консульства')}); лекции и киноклуб организует Культурно-просветительское общество греков Санкт-Петербурга ({a(GREEKSPB,'greekspb.com')}).",
            more="Источник анонса", tr_place="Трапезная храма (пр. Стачек, 48Б)", ch_place="Храм, пр. Стачек, 48",
            upcoming="Недавно", past="Архив",
            media_h="Фото и видео",
            media_p="Фоторепортажи, анонсы и видео встреч публикуются на страницах прихода и общества греков. Ниже — ссылки и фотографии встреч.",
            media_links=[(VK,"ВКонтакте: страница Путиловского храма","Анонсы, фотоотчёты и новости прихода"),
                         (TG,"Telegram: «Греки Санкт-Петербурга»","Анонсы и отчёты, более 500 фото и 80 видео (канал общества, не только храм)"),
                         (GREEKSPB,"Сайт общества «Греки Санкт-Петербурга»","Новости, отчёты и речи на памятных встречах"),
                         (GLOBUS,"«Глобус» Санкт-Петербургской митрополии","Фоторепортажи из храма")],
            photo_cap="Фотографии встреч — из материалов общества греков Санкт-Петербурга (Telegram-канал, greekspb.com) и прихода.",
            contacts_h="Контактная информация",
            c_addr_l="Адрес", c_addr="Санкт-Петербург, проспект Стачек, 48 (трапезная — 48Б)",
            c_hours_l="Часы работы", c_hours="ежедневно с 09:00 до 19:00",
            c_vk_l="ВКонтакте", c_vk="Страница Путиловского храма",
            c_site_l="Сайт храма",
            c_cons_l="Консульства", c_gr="Генеральное консульство Греции в Санкт-Петербурге", c_cy="Генеральное консульство Республики Кипр в Санкт-Петербурге",
            c_tg_l="Telegram", c_tg="Канал «Греки Санкт-Петербурга»",
            footer="Неофициальный информационный сайт. Материалы — из открытых источников: страница храма во ВКонтакте, канал «Греки Санкт-Петербурга», сайты консульств и общества греков.",
            evt=self_events_ru(gr, cy),
        )
    if lang == "el":
        return dict(
            lang="el", title="Ελληνική Λέσχη του Ναού Πουτίλοφ",
            desc="Συναντήσεις της ελληνικής κοινότητας της Αγίας Πετρούπολης στον Ιερό Ναό του Αγίου Νικολάου και της Αγίας Μάρτυρος Βασιλίσσης Αλεξάνδρας (Πουτίλοφ).",
            nav=[("about","Ο Ναός"),("meetings","Συναντήσεις"),("media","Φωτογραφίες & βίντεο"),("contacts","Επικοινωνία")],
            hero_kicker="Αγία Πετρούπολη · Λεωφ. Στάτσεκ 48",
            hero_h="Ελληνική Λέσχη του Ναού Πουτίλοφ",
            hero_p="Ακολουθίες στα ελληνικά, εθνικές επέτειοι, διαλέξεις για το Άγιον Όρος, κινηματογραφική λέσχη και οικογενειακές συναντήσεις των Ελλήνων της Αγίας Πετρούπολης στον Ιερό Ναό του Αγίου Νικολάου και της Μάρτυρος Βασιλίσσης Αλεξάνδρας.",
            hero_btn="Οι συναντήσεις μας",
            about_h="Ο Ναός",
            hist_h="Ιστορία του Ναού Πουτίλοφ",
            hist=[
              "Ο Ναός του Αγίου Νικολάου του Θαυματουργού και της Αγίας Μάρτυρος Βασιλίσσης Αλεξάνδρας χτίστηκε στο πλαίσιο του εργοστασίου Πουτίλοφ. Οι εργασίες ξεκίνησαν το 1901· τα χρήματα συγκέντρωσαν οι ίδιοι οι εργάτες, προσφέροντας εθελοντικά μέρος του μισθού τους. Ο ναός ανεγέρθηκε στη μνήμη του ιδρυτή του εργοστασίου, Νικολάι Ιβάνοβιτς Πουτίλοφ.",
              "Τα εγκαίνια έγιναν το 1906–1907: ο άνω ναός αφιερώθηκε στον Άγιο Νικόλαο και ο κάτω (στην κρύπτη) στον Άγιο Γεώργιο τον Τροπαιοφόρο. Αργότερα, στην κρύπτη μεταφέρθηκαν τα λείψανα του ίδιου του Πουτίλοφ και της συζύγου του.",
              "Το σχέδιο ανήκει στον αρχιτέκτονα Βασίλι Κοσιάκοφ, σε ρωσοβυζαντινό ρυθμό· το εσωτερικό διακοσμήθηκε στο πνεύμα της παλαιάς Ρωσίας και τα σκεύη και οι πολυέλαιοι κατασκευάστηκαν από την εταιρεία των αδελφών Ολοβιανισνικόφ.",
              "Το 1925 ο ναός έκλεισε και στα τέλη της δεκαετίας του 1920 μετατράπηκε σε εργατική λέσχη («Κόκκινος Πουτίλοβετς»): κατεδαφίστηκαν οι τρούλοι και το κωδωνοστάσιο. Το κτίριο επιστράφηκε στην Εκκλησία τη δεκαετία του 2000 και σήμερα αποτελεί μνημείο πολιτιστικής κληρονομιάς περιφερειακής σημασίας. Στον ναό τελούνται ακολουθίες και λειτουργούν κατηχητικό σχολείο, νεανική λέσχη και άλλες δραστηριότητες.",
            ],
            rector_h="Ο προϊστάμενος του Ναού",
            rector_name="Πρωτοπρεσβύτερος Βλαδίμηρος Γκοντσαρένκο",
            rector=[
              "Γεννήθηκε στις 29 Νοεμβρίου 1976. Αποφοίτησε από τη Φυσική του Κρατικού Πανεπιστημίου της Αγίας Πετρούπολης (1997), την Ιερατική Σχολή (2001) και την Πνευματική Ακαδημία της Αγίας Πετρούπολης (2005)· το 2004–2005 σπούδασε στο Εθνικό και Καποδιστριακό Πανεπιστήμιο Αθηνών. Είναι υποψήφιος διδάκτωρ θεολογίας και διδάσκει στην Πνευματική Ακαδημία.",
              "Χειροτονήθηκε διάκονος στις 4 Δεκεμβρίου 2005 και πρεσβύτερος στις 15 Ιανουαρίου 2006· το 2016 ανυψώθηκε σε πρωτοπρεσβύτερο. Διορίστηκε προϊστάμενος του Ναού Πουτίλοφ στις 4 Μαρτίου 2006, λίγο μετά την επιστροφή του κτιρίου στην Εκκλησία· η πρώτη Θεία Λειτουργία στον κάτω ναό μετά από μακρά διακοπή τελέστηκε τον Μάρτιο του 2006.",
              "Ο π. Βλαδίμηρος στηρίζει εδώ και χρόνια την ελληνική κοινότητα της πόλης: τελεί ακολουθίες με ελληνικούς ύμνους και κηρύγματα στα ελληνικά, μνημόσυνα και δοξολογίες για τις εθνικές επετείους, και φιλοξενεί θερμά τις συναντήσεις της κοινότητας στην τράπεζα του ναού.",
            ],
            meet_h="Συναντήσεις της ελληνικής κοινότητας στον Ναό",
            meet_p=f"Ο ναός αποτελεί σταθερό χώρο συνάντησης των Ελλήνων της Αγίας Πετρούπολης. Οι ακολουθίες για τις εθνικές επετείους τελούνται σε συνεργασία με το Γενικό Προξενείο της Ελλάδος ({a(gr,'ιστότοπος προξενείου')}) και με τη συμμετοχή του Γενικού Προξενείου της Κυπριακής Δημοκρατίας ({a(cy,'ιστότοπος προξενείου')})· διαλέξεις και κινηματογραφική λέσχη οργανώνει η Πολιτιστική και Εκπαιδευτική Εταιρεία των Ελλήνων της Αγίας Πετρούπολης ({a(GREEKSPB,'greekspb.com')}).",
            more="Πηγή ανακοίνωσης", tr_place="Τράπεζα του ναού (Λεωφ. Στάτσεκ 48Β)", ch_place="Ναός, Λεωφ. Στάτσεκ 48",
            upcoming="Πρόσφατα", past="Αρχείο",
            media_h="Φωτογραφίες και βίντεο",
            media_p="Φωτογραφικό υλικό, ανακοινώσεις και βίντεο των συναντήσεων δημοσιεύονται στις σελίδες της ενορίας και της ελληνικής κοινότητας. Παρακάτω θα βρείτε συνδέσμους και φωτογραφίες των συναντήσεων.",
            media_links=[(VK,"VK: σελίδα του Ναού Πουτίλοφ","Ανακοινώσεις, φωτογραφίες και νέα της ενορίας"),
                         (TG,"Telegram: «Έλληνες της Αγίας Πετρούπολης»","Ανακοινώσεις και αναφορές, πάνω από 500 φωτογραφίες και 80 βίντεο (κανάλι της κοινότητας, όχι μόνο για τον ναό)"),
                         (GREEKSPB,"Ιστότοπος των Ελλήνων της Αγίας Πετρούπολης","Νέα, αναφορές και ομιλίες σε εκδηλώσεις μνήμης"),
                         (GLOBUS,"«Globus» της Μητρόπολης Αγίας Πετρούπολης","Φωτορεπορτάζ από τον ναό")],
            photo_cap="Φωτογραφίες των συναντήσεων — από υλικό της κοινότητας των Ελλήνων (κανάλι Telegram, greekspb.com) και της ενορίας.",
            contacts_h="Στοιχεία επικοινωνίας",
            c_addr_l="Διεύθυνση", c_addr="Αγία Πετρούπολη, Λεωφόρος Στάτσεκ 48 (τράπεζα — 48Β)",
            c_hours_l="Ώρες λειτουργίας", c_hours="καθημερινά 09:00–19:00",
            c_vk_l="VK", c_vk="Σελίδα του Ναού Πουτίλοφ",
            c_site_l="Ιστότοπος του ναού",
            c_cons_l="Προξενεία", c_gr="Γενικό Προξενείο της Ελλάδος στην Αγία Πετρούπολη", c_cy="Γενικό Προξενείο της Κυπριακής Δημοκρατίας στην Αγία Πετρούπολη",
            c_tg_l="Telegram", c_tg="Κανάλι «Έλληνες της Αγίας Πετρούπολης»",
            footer="Ανεπίσημος ενημερωτικός ιστότοπος. Το υλικό προέρχεται από δημόσιες πηγές: τη σελίδα του ναού στο VK, το κανάλι «Έλληνες της Αγίας Πετρούπολης», τους ιστοτόπους των προξενείων και της κοινότητας.",
            evt=self_events_el(gr, cy),
        )
    return dict(
        lang="en", title="Greek Club of the Putilov Church",
        desc="Meetings of the Greek community of St Petersburg at the Church of St Nicholas the Wonderworker and Martyr Empress Alexandra (the Putilov Church).",
        nav=[("about","The Church"),("meetings","Meetings"),("media","Photos & video"),("contacts","Contacts")],
        hero_kicker="Saint Petersburg · 48 Stachek Avenue",
        hero_h="Greek Club of the Putilov Church",
        hero_p="Services in Greek, national anniversaries, lectures on Mount Athos, a film club and family gatherings of the St Petersburg Greeks at the Church of St Nicholas the Wonderworker and Martyr Empress Alexandra.",
        hero_btn="Our meetings",
        about_h="The Church",
        hist_h="History of the Putilov Church",
        hist=[
          "The Church of St Nicholas the Wonderworker and Martyr Empress Alexandra was built for the Putilov Works. Construction began in 1901; the money was raised by the workers themselves, who voluntarily gave part of their wages. The church was raised in memory of the plant's founder, Nikolai Ivanovich Putilov.",
          "It was consecrated in 1906–1907: the upper church is dedicated to St Nicholas, the lower one (in the crypt) to the Great Martyr St George. Later the remains of Putilov and his wife were moved to the crypt.",
          "The design is by architect Vasily Kosyakov in the Russo-Byzantine style; the interior was decorated in the spirit of Old Russia, with vessels and chandeliers made by the Olovyanishnikov Brothers.",
          "The church was closed in 1925 and in the late 1920s rebuilt as the factory club “Krasny Putilovets”: the domes and bell tower were demolished. The building was returned to the Church in the 2000s and is now a regional cultural heritage site. Services are held here, and the parish runs a Sunday school, a youth club and other groups.",
        ],
        rector_h="The Rector",
        rector_name="Archpriest Vladimir Goncharenko",
        rector=[
          "Born 29 November 1976. He graduated in physics from St Petersburg State University (1997), the St Petersburg Theological Seminary (2001) and the St Petersburg Theological Academy (2005), and studied at the National and Kapodistrian University of Athens in 2004–2005. A Candidate of Theology, he teaches at the St Petersburg Theological Academy.",
          "Ordained deacon on 4 December 2005 and priest on 15 January 2006; raised to archpriest in 2016. He became rector of the Putilov Church on 4 March 2006, soon after the building was returned to the Church; the first Divine Liturgy in the lower church after a long interval was served in March 2006.",
          "For many years Fr Vladimir has supported the Greek community of the city: he serves with Greek chant and preaches in Greek, celebrates memorial services and doxologies on Greek national dates, and warmly hosts the community's gatherings in the church refectory.",
        ],
        meet_h="Greek community meetings at the church",
        meet_p=f"The church is a regular home for the Greeks of St Petersburg. Services for national anniversaries are held together with the Consulate General of Greece ({a(gr,'consulate website')}) and with the participation of the Consulate General of the Republic of Cyprus ({a(cy,'consulate website')}); lectures and the film club are organised by the Cultural and Educational Society of the Greeks of St Petersburg ({a(GREEKSPB,'greekspb.com')}).",
        more="Announcement source", tr_place="Church refectory (48B Stachek Ave.)", ch_place="Church, 48 Stachek Ave.",
        upcoming="Recent", past="Archive",
        media_h="Photos and video",
        media_p="Photo reports, announcements and videos of the meetings are published on the parish and community pages. Below are links and photographs of the meetings.",
        media_links=[(VK,"VK: Putilov Church page","Announcements, photo reports and parish news"),
                     (TG,"Telegram: “Greeks of St Petersburg”","Announcements and reports, 500+ photos and 80+ videos (the community's channel, not only the church)"),
                     (GREEKSPB,"Website of the Greeks of St Petersburg","News, reports and speeches from memorial events"),
                     (GLOBUS,"“Globus” of the St Petersburg Metropolis","Photo reports from the church")],
        photo_cap="Photographs of the meetings — from materials of the Greek community (Telegram channel, greekspb.com) and the parish.",
        contacts_h="Contact information",
        c_addr_l="Address", c_addr="St Petersburg, Stachek Avenue 48 (refectory — 48B)",
        c_hours_l="Opening hours", c_hours="daily 09:00–19:00",
        c_vk_l="VK", c_vk="Putilov Church page",
        c_site_l="Church website",
        c_cons_l="Consulates", c_gr="Consulate General of Greece in St Petersburg", c_cy="Consulate General of the Republic of Cyprus in St Petersburg",
        c_tg_l="Telegram", c_tg="“Greeks of St Petersburg” channel",
        footer="Unofficial information website. Materials come from public sources: the church's VK page, the “Greeks of St Petersburg” channel, the consulates' and the community's websites.",
        evt=self_events_en(gr, cy),
    )

# ---------- тексты событий ----------
def self_events_ru(gr, cy):
    return {
     "oxi26": ("Молебен ко Дню «Охи»", "Торжественный молебен по случаю национального праздника Греции. Приглашало Генеральное консульство Греции; богослужение провёл настоятель, отец Владимир, после службы — чаепитие.", "12:00", "church"),
     "film2": ("Киноклуб: «Счастье в Афинах» (1955)", "Первый фильм Михалиса Какоянниса на языке оригинала с русскими субтитрами. Перед показом Александр Данилов рассказал о режиссёре — создателе «Грека Зорбы», «Стеллы», «Электры». Организатор — Общество греков Санкт-Петербурга.", "19:30", "tr"),
     "athos2": ("Лекция «Свято-Пантелеймонов монастырь — ключевой центр русского православия на Афоне»", "Вторая лекция цикла «Благость Афона». Лектор — Сергей Леонидович Бровко.", "12:00", "tr"),
     "kids": ("Праздник ко Дню защиты детей", "Семейная встреча: просмотр мультфильма «Двенадцать подвигов Астерикса», угощение, игры и беседы. Благодарность — отцу Владимиру за гостеприимство и Эммануилу Папуцоглу за угощение.", "", "tr"),
     "film1": ("Киноклуб: «Мандолина капитана Корелли»", "Фильм о событиях 1943 года на острове Кефалония, в русском дубляже с греческими субтитрами; обсуждение после просмотра. Вход свободный.", "19:30", "tr"),
     "pontos26": ("День памяти жертв геноцида понтийских греков", f"Заупокойная лития по жертвам трагедии, организованная {a(gr,'Генеральным консульством Греции')} совместно с протоиереем Владимиром Гончаренко; после богослужения — краткая памятная встреча.", "12:00", "church"),
     "indep26": ("Доксология ко Дню независимости Греции", "Торжественное богослужение в день национального праздника провёл отец Владимир; затем — традиционное чаепитие.", "12:00", "church"),
     "athos1": ("Лекция «Свято-Андреевский скит на Афоне — зеркало русского православия»", "Первая лекция цикла «Благость Афона» после праздничного богослужения. Язык — русский, вход свободный.", "12:00", "tr"),
     "pontos25": ("Панихида в канун Дня памяти жертв геноцида греков Понта и Малой Азии", f"Богослужение на греческом и церковнославянском языках провёл отец Владимир. Присутствовали представители {a(gr,'Генерального консульства Греции')}, члены общины и прихожане. За чаепитием прозвучали приветствия Генерального консула Греции Димитриоса Спароса и председателя Общества греков Ефстратиоса Сиурдакиса; участники делились семейными историями.", "", "church"),
     "oxi19": ("Литургия на древнегреческом языке накануне Дня «Охи»", f"Литургию возглавил отец Владимир; присутствовали Генеральные консулы Греции Спиридон Вулгарис ({a(gr,'консульство Греции')}) и Кипра Димитрий Асос ({a(cy,'консульство Кипра')}). Пели хор храма и студенты Духовной академии с Кипра и из Сирии.", "", "church"),
     "nat18": ("Литургия на греческом языке ко Дню независимости (25 марта)", f"Божественная литургия на греческом языке, организованная {a(gr,'Генеральным консульством Греции')} совместно со священником храма.", "10:00", "church"),
    }

def self_events_el(gr, cy):
    return {
     "oxi26": ("Δοξολογία για την Εθνική Εορτή της 28ης Οκτωβρίου", "Πανηγυρική δοξολογία για την εθνική εορτή. Πρόσκληση από το Γενικό Προξενείο της Ελλάδος· τέλεσε ο προϊστάμενος π. Βλαδίμηρος και ακολούθησε τσάι.", "12:00", "church"),
     "film2": ("Κινηματογραφική λέσχη: «Ευτυχία στην Αθήνα» (1955)", "Η πρώτη ταινία του Μιχάλη Κακογιάννη στο πρωτότυπο με ρωσικούς υπότιτλους. Πριν την προβολή ο Αλεξάντρ Ντανίλοφ μίλησε για τον σκηνοθέτη του «Ζορμπά», της «Στέλλας» και της «Ηλέκτρας». Διοργάνωση: Ελληνική Κοινότητα Αγίας Πετρούπολης.", "19:30", "tr"),
     "athos2": ("Διάλεξη «Η Ιερά Μονή Αγίου Παντελεήμονος — κέντρο της ρωσικής ορθοδοξίας στο Άγιον Όρος»", "Δεύτερη διάλεξη του κύκλου «Η Χάρις του Άθω». Ομιλητής: Σεργκέι Λεονίντοβιτς Μπρόβκο.", "12:00", "tr"),
     "kids": ("Γιορτή για την Παγκόσμια Ημέρα του Παιδιού", "Οικογενειακή συνάντηση με προβολή του κινούμενου σχεδίου «Οι 12 άθλοι του Αστερίξ», φαγητό, παιχνίδια και κουβέντα. Ευχαριστίες στον π. Βλαδίμηρο για τη φιλοξενία και στον Εμμανουήλ Παπουτσόγλου για το κέρασμα.", "", "tr"),
     "film1": ("Κινηματογραφική λέσχη: «Ο Λοχαγός Κορέλι»", "Ταινία για τα γεγονότα του 1943 στην Κεφαλονιά, με ρωσική μεταγλώττιση και ελληνικούς υπότιτλους· συζήτηση μετά την προβολή. Ελεύθερη είσοδος.", "19:30", "tr"),
     "pontos26": ("Ημέρα Εθνικής Μνήμης της Γενοκτονίας των Ελλήνων του Πόντου", f"Μνημόσυνο υπέρ αναπαύσεως των θυμάτων, που διοργάνωσε το {a(gr,'Γενικό Προξενείο της Ελλάδος')} σε συνεργασία με τον πρωτοϊερέα Βλαδίμηρο Γκοντσαρένκο· ακολούθησε σύντομη εκδήλωση μνήμης.", "12:00", "church"),
     "indep26": ("Δοξολογία για την Εθνική Παλιγγενεσία", "Πανηγυρική δοξολογία για την επέτειο της Ελληνικής Ανεξαρτησίας, χοροστατούντος του π. Βλαδίμηρου, και παραδοσιακό τσάι μετά την ακολουθία.", "12:00", "church"),
     "athos1": ("Διάλεξη «Το Ρωσικό Σκητάριο του Αγίου Ανδρέα στο Άγιον Όρος»", "Πρώτη διάλεξη του κύκλου «Η Χάρις του Άθω» μετά την πανηγυρική ακολουθία. Γλώσσα: ρωσικά, ελεύθερη είσοδος.", "12:00", "tr"),
     "pontos25": ("Μνημόσυνο την παραμονή της Ημέρας Μνήμης της Γενοκτονίας των Ελλήνων του Πόντου και της Μικράς Ασίας", f"Η ακολουθία τελέστηκε στα ελληνικά και στα εκκλησιαστικά σλαβικά από τον π. Βλαδίμηρο. Παρέστησαν εκπρόσωποι του {a(gr,'Γενικού Προξενείου της Ελλάδος')}, μέλη της κοινότητας και ενορίτες. Στο τσάι ακούστηκαν χαιρετισμοί του Γενικού Προξένου Δημήτριου Σπάρου και του προέδρου της κοινότητας Ευστράτιου Σιουρδάκη· οι παρευρισκόμενοι μοιράστηκαν οικογενειακές ιστορίες.", "", "church"),
     "oxi19": ("Θεία Λειτουργία στα αρχαία ελληνικά την παραμονή της 28ης Οκτωβρίου", f"Τη Λειτουργία τέλεσε ο π. Βλαδίμηρος· παρέστησαν οι Γενικοί Πρόξενοι της Ελλάδος Σπυρίδων Βούλγαρης ({a(gr,'προξενείο Ελλάδος')}) και της Κύπρου Δημήτριος Άσσος ({a(cy,'προξενείο Κύπρου')}). Έψαλαν η χορωδία του ναού και φοιτητές της Θεολογικής Ακαδημίας από την Κύπρο και τη Συρία.", "", "church"),
     "nat18": ("Θεία Λειτουργία στα ελληνικά για την Εθνική Εορτή της 25ης Μαρτίου", f"Θεία Λειτουργία στα ελληνικά, σε διοργάνωση του {a(gr,'Γενικού Προξενείου της Ελλάδος')} σε συνεργασία με ιερέα του ναού.", "10:00", "church"),
    }

def self_events_en(gr, cy):
    return {
     "oxi26": ("Doxology for “Ohi” Day", "A festive service for the Greek national holiday, at the invitation of the Consulate General of Greece. Fr Vladimir led the service, followed by tea.", "12:00", "church"),
     "film2": ("Film club: “Happiness in Athens” (1955)", "Michael Cacoyannis's first feature, in the original Greek with Russian subtitles. Before the screening Alexander Danilov spoke about the director of “Zorba the Greek”, “Stella” and “Electra”. Organised by the Society of the Greeks of St Petersburg.", "19:30", "tr"),
     "athos2": ("Lecture: “The St Panteleimon Monastery — the key centre of Russian Orthodoxy on Athos”", "The second lecture in the cycle “The Grace of Athos”, given by Sergei L. Brovko.", "12:00", "tr"),
     "kids": ("Children's Day gathering", "A family evening: the cartoon “The Twelve Tasks of Asterix”, food, games and conversation. Thanks to Fr Vladimir for his hospitality and to Emmanuel Papoutsoglou for the treats.", "", "tr"),
     "film1": ("Film club: “Captain Corelli's Mandolin”", "A film about the 1943 events on Cephalonia, shown dubbed in Russian with Greek subtitles; discussion afterwards. Free admission.", "19:30", "tr"),
     "pontos26": ("Remembrance Day of the Pontic Greek Genocide", f"A memorial litia for the victims, organised by the {a(gr,'Consulate General of Greece')} together with Archpriest Vladimir Goncharenko, followed by a short commemorative gathering.", "12:00", "church"),
     "indep26": ("Doxology for Greek Independence Day", "A festive service led by Fr Vladimir for the anniversary of Greek independence, followed by the traditional tea.", "12:00", "church"),
     "athos1": ("Lecture: “The Russian St Andrew's Skete on Athos”", "The first lecture in the cycle “The Grace of Athos”, after the festive service. In Russian; free admission.", "12:00", "tr"),
     "pontos25": ("Memorial service on the eve of Remembrance Day for the Genocide of the Pontic and Asia Minor Greeks", f"Fr Vladimir led the service in Greek and Church Slavonic. Representatives of the {a(gr,'Consulate General of Greece')}, community members and parishioners attended. At the tea, greetings were read from Consul General Dimitrios Sparos and from community chairman Efstratios Siourdakis; participants shared family stories.", "", "church"),
     "oxi19": ("Liturgy in Ancient Greek on the eve of “Ohi” Day", f"Fr Vladimir led the Liturgy, attended by the Consuls General of Greece, Spyridon Vulgaris ({a(gr,'Greek consulate')}), and of Cyprus, Dimitrios Asos ({a(cy,'Cypriot consulate')}). The church choir sang together with Theological Academy students from Cyprus and Syria.", "", "church"),
     "nat18": ("Liturgy in Greek for the National Day (25 March)", f"A Divine Liturgy in Greek organised by the {a(gr,'Consulate General of Greece')} together with a priest of the church.", "10:00", "church"),
    }

# ---------- вёрстка ----------
def render(lang):
    t = T(lang)
    langs = [("ru", "RU"), ("el", "ΕΛ"), ("en", "EN")]
    sw = "".join(
        f'<a href="../{c}/" class="lang{" on" if c == lang else ""}" hreflang="{c}" lang="{c}">{n}</a>' for c, n in langs)
    nav = "".join(f'<a href="#{i}">{html.escape(n)}</a>' for i, n in t["nav"])
    hist = "".join(f"<p>{html.escape(p)}</p>" for p in t["hist"])
    rect = "".join(f"<p>{html.escape(p)}</p>" for p in t["rector"])
    cards = []
    for iso, link, key in EVENTS:
        title, body, tm, place = t["evt"][key]
        pl = t["ch_place"] if place == "church" else t["tr_place"]
        when = fmt_date(lang, iso) + (f" · {tm}" if tm else "")
        old = iso < "2026-01-01"
        im = f'<img class="cimg" src="../assets/img/{CARD_IMG[key]}.jpg" loading="lazy" alt="{html.escape(title)}">' if key in CARD_IMG else ""
        cards.append(
            f'<article class="card{" old" if old else ""}">{im}<div class="when">{when}</div>'
            f'<h3>{html.escape(title)}</h3><p>{body}</p>'
            f'<div class="meta"><span>{html.escape(pl)}</span> · {a(link, html.escape(t["more"]))}</div></article>')
    media = "".join(
        f'<a class="link" href="{html.escape(h)}" target="_blank" rel="noopener"><strong>{html.escape(n)}</strong><span>{html.escape(d)}</span></a>'
        for h, n, d in t["media_links"])
    photos = "".join(
        f'<figure><a href="../assets/img/{k}.jpg" target="_blank"><img src="../assets/img/{k}.jpg" loading="lazy" alt="{html.escape(c[lang])}"></a><figcaption>{html.escape(c[lang])}</figcaption></figure>'
        for k, c in GALLERY)
    return f"""<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(t['title'])}</title>
<meta name="description" content="{html.escape(t['desc'])}">
<link rel="alternate" hreflang="ru" href="../ru/"><link rel="alternate" hreflang="el" href="../el/"><link rel="alternate" hreflang="en" href="../en/">
<link rel="stylesheet" href="../assets/style.css">
</head>
<body>
<header class="top"><div class="wrap bar">
  <a class="brand" href="#top"><span class="cross">✝</span><span>{html.escape(t['title'])}</span></a>
  <nav>{nav}</nav><div class="langs">{sw}</div>
</div></header>
<main id="top">
<section class="hero"><div class="wrap">
  <p class="kicker">{html.escape(t['hero_kicker'])}</p>
  <h1>{html.escape(t['hero_h'])}</h1>
  <p class="lead">{html.escape(t['hero_p'])}</p>
  <a class="btn" href="#meetings">{html.escape(t['hero_btn'])}</a>
</div></section>

<section id="about"><div class="wrap">
  <h2>{html.escape(t['about_h'])}</h2>
  <div class="two">
    <div><h3>{html.escape(t['hist_h'])}</h3>{hist}</div>
    <div class="panel"><h3>{html.escape(t['rector_h'])}</h3><img class="portrait" src="../assets/img/{RECTOR_IMG}.jpg" alt="{html.escape(t['rector_name'])}"><p class="name">{html.escape(t['rector_name'])}</p>{rect}</div>
  </div>
</div></section>

<section id="meetings" class="alt"><div class="wrap">
  <h2>{html.escape(t['meet_h'])}</h2>
  <p class="intro">{t['meet_p']}</p>
  <div class="grid">{''.join(cards)}</div>
</div></section>

<section id="media"><div class="wrap">
  <h2>{html.escape(t['media_h'])}</h2>
  <p class="intro">{html.escape(t['media_p'])}</p>
  <div class="links">{media}</div>
  <div class="photos">{photos}</div>
  <p class="cap">{html.escape(t['photo_cap'])}</p>
</div></section>

<section id="contacts" class="alt"><div class="wrap">
  <h2>{html.escape(t['contacts_h'])}</h2>
  <dl class="contacts">
    <dt>{html.escape(t['c_addr_l'])}</dt><dd>{html.escape(t['c_addr'])}</dd>
    <dt>{html.escape(t['c_hours_l'])}</dt><dd>{html.escape(t['c_hours'])}</dd>
    <dt>{html.escape(t['c_vk_l'])}</dt><dd>{a(VK, html.escape(t['c_vk']))}</dd>
    <dt>{html.escape(t['c_site_l'])}</dt><dd>{a(TEMPLE, 'putilovskij-hram.ru')}</dd>
    <dt>{html.escape(t['c_tg_l'])}</dt><dd>{a(TG, html.escape(t['c_tg']))}</dd>
    <dt>{html.escape(t['c_cons_l'])}</dt><dd>{a(GR_CONS, html.escape(t['c_gr']))}<br>{a(CY_CONS, html.escape(t['c_cy']))}</dd>
  </dl>
</div></section>
</main>
<footer><div class="wrap"><p>{html.escape(t['footer'])}</p></div></footer>
</body></html>
"""

CSS = """/* Палитра — в переменных ниже; при необходимости подставьте точные цвета сайта putilovskij-hram.ru */
:root{
  --navy:#1d2f55; --navy-d:#14213c; --gold:#b8923a; --gold-l:#e4cf9a;
  --cream:#f8f4ea; --paper:#fffdf8; --ink:#222a3a; --muted:#5d667a; --line:#e3dac3;
}
*{box-sizing:border-box}
html{scroll-behavior:smooth;scroll-padding-top:70px}
body{margin:0;font:17px/1.65 Georgia,"Times New Roman",serif;color:var(--ink);background:var(--paper)}
.wrap{max-width:1080px;margin:0 auto;padding:0 20px}
a{color:var(--navy);text-decoration-color:var(--gold)}a:hover{color:var(--gold)}
.top{position:sticky;top:0;z-index:10;background:var(--navy);color:#fff;border-bottom:3px solid var(--gold)}
.bar{display:flex;align-items:center;gap:18px;flex-wrap:wrap;padding-top:10px;padding-bottom:10px}
.brand{display:flex;gap:10px;align-items:center;color:#fff;text-decoration:none;font-weight:bold}
.cross{color:var(--gold-l);font-size:22px}
nav{display:flex;gap:16px;flex-wrap:wrap;margin-left:auto;font:15px system-ui,sans-serif}
nav a{color:#e9edf7;text-decoration:none}nav a:hover{color:var(--gold-l)}
.langs{display:flex;gap:4px;font:13px system-ui,sans-serif}
.lang{color:#fff;text-decoration:none;border:1px solid #ffffff55;padding:2px 8px;border-radius:4px}
.lang.on{background:var(--gold);border-color:var(--gold);color:var(--navy-d);font-weight:bold}
.hero{background:linear-gradient(160deg,var(--navy-d),var(--navy));color:#fff;padding:72px 0 80px;border-bottom:6px solid var(--gold)}
.kicker{color:var(--gold-l);letter-spacing:.08em;text-transform:uppercase;font:14px system-ui,sans-serif;margin:0 0 10px}
h1{font-size:clamp(30px,5vw,50px);line-height:1.15;margin:0 0 16px}
.lead{max-width:720px;font-size:19px;color:#e5eaf5}
.btn{display:inline-block;margin-top:14px;background:var(--gold);color:var(--navy-d);padding:11px 22px;border-radius:4px;text-decoration:none;font:600 15px system-ui,sans-serif}
.btn:hover{background:var(--gold-l);color:var(--navy-d)}
section{padding:56px 0}section.alt{background:var(--cream)}
h2{font-size:30px;color:var(--navy);margin:0 0 22px;padding-bottom:10px;border-bottom:2px solid var(--gold);display:inline-block}
h3{color:var(--navy);margin:0 0 10px;font-size:20px}
.two{display:grid;grid-template-columns:3fr 2fr;gap:36px}
.panel{background:var(--cream);border-left:4px solid var(--gold);padding:20px 22px;border-radius:4px;align-self:start}
.panel .name{font-weight:bold;font-size:19px;color:var(--navy);margin-top:0}
.intro{max-width:860px}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(310px,1fr));gap:20px;margin-top:24px}
.card{background:#fff;border:1px solid var(--line);border-top:4px solid var(--gold);border-radius:4px;padding:18px 20px}
.card.old{border-top-color:var(--navy)}
.card h3{font-size:18px;margin:4px 0 8px}.card p{margin:0 0 10px;font-size:16px}
.when{font:600 13px system-ui,sans-serif;color:var(--gold);text-transform:uppercase;letter-spacing:.04em}
.meta{font:13px system-ui,sans-serif;color:var(--muted)}
.links{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:14px;margin:20px 0}
.link{display:block;background:var(--cream);border:1px solid var(--line);padding:14px 16px;border-radius:4px;text-decoration:none;color:var(--ink)}
.link strong{display:block;color:var(--navy)}.link span{font-size:14px;color:var(--muted)}
.link:hover{border-color:var(--gold)}
.photos{display:grid;grid-template-columns:repeat(auto-fill,minmax(240px,1fr));gap:16px}
.photos img{width:100%;height:200px;object-fit:cover;border-radius:4px;border:1px solid var(--line);display:block}
figure{margin:0}figcaption{font:13px system-ui,sans-serif;color:var(--muted);margin-top:4px}
.cimg{width:100%;height:190px;object-fit:cover;border-radius:3px;margin-bottom:10px}
.portrait{width:100%;border-radius:4px;margin-bottom:12px}
.cap{font:13px system-ui,sans-serif;color:var(--muted)}
.contacts{display:grid;grid-template-columns:170px 1fr;gap:10px 20px;max-width:760px}
.contacts dt{font-weight:bold;color:var(--navy)}.contacts dd{margin:0}
footer{background:var(--navy-d);color:#c5cde0;padding:26px 0;font:14px system-ui,sans-serif}
@media(max-width:760px){.two{grid-template-columns:1fr}.contacts{grid-template-columns:1fr}nav{margin-left:0}}
"""

ROOT = """<!doctype html><html lang="ru"><head><meta charset="utf-8"><title>Greek Club of the Putilov Church</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<script>
var l=(navigator.language||"ru").slice(0,2);var t={ru:"ru",el:"el"}[l]||(l==="en"?"en":"ru");
location.replace(t+"/");
</script>
<noscript><meta http-equiv="refresh" content="0; url=ru/"></noscript></head>
<body style="font-family:Georgia,serif;text-align:center;padding:60px">
<h1>Греческий клуб Путиловского храма</h1>
<p><a href="ru/">Русский</a> · <a href="el/">Ελληνικά</a> · <a href="en/">English</a></p></body></html>
"""

README = """# Greek-Putilov — «Греческий клуб Путиловского храма»

Статический трёхъязычный сайт (русский / ελληνικά / English) о встречах греческого сообщества Санкт-Петербурга в Путиловском храме.

- `index.html` — выбор языка по языку браузера
- `ru/`, `el/`, `en/` — страницы сайта
- `assets/style.css` — оформление (палитра — в переменных `:root`)
- `build/build.py` — генератор страниц (`python3 build/build.py`); все тексты — в нём

Публикация: GitHub → Settings → Pages → Deploy from a branch → `main` / root.
"""

def main():
    for d in ("ru", "el", "en", "assets", "build"):
        os.makedirs(os.path.join(OUT, d), exist_ok=True)
    for l in ("ru", "el", "en"):
        open(os.path.join(OUT, l, "index.html"), "w", encoding="utf-8").write(render(l))
    open(os.path.join(OUT, "assets", "style.css"), "w", encoding="utf-8").write(CSS)
    open(os.path.join(OUT, "index.html"), "w", encoding="utf-8").write(ROOT)
    open(os.path.join(OUT, "README.md"), "w", encoding="utf-8").write(README)
    open(os.path.join(OUT, ".nojekyll"), "w").write("")
    import shutil
    shutil.copy(__file__, os.path.join(OUT, "build", "build.py"))
    print("ok")

if __name__ == "__main__":
    main()
