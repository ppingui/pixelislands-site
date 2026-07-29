#!/usr/bin/env python3
"""Generate the /guides/ hub page for every locale.

Usage: python3 build_guides_hub.py

Articles list which locales they exist in via their i18n dict; a locale hub only
links the articles actually translated for it, so no hub can link a 404.
"""
import pathlib

import build_locales as BL

SITE = "https://pixelislands.app"
APP_URL = "https://apps.apple.com/app/pixel-islands-step-track-game/id6760819710"
LOCALE_DIRS = ["", "de", "fr", "es", "ja", "pt-br", "ru", "uk"]
HREFLANG_OF = {"": "en", "de": "de", "fr": "fr", "es": "es", "ja": "ja",
               "pt-br": "pt-BR", "ru": "ru", "uk": "uk"}

# ---------------------------------------------------------------- articles
# i18n: locale-dir -> (card title, card blurb). "" is English.
ARTICLES = [
    dict(slug="best-walking-games-iphone", i18n={
        "": ("7 best walking games for iPhone",
             "Cozy builders, creature collectors, zombie escapes — honestly compared."),
    }),
    dict(slug="how-to-make-walking-fun", i18n={
        "": ("How to make walking fun",
             "12 ideas that survive past week two."),
    }),
    dict(slug="how-many-steps-a-day", i18n={
        "": ("How many steps a day do you need?",
             "Spoiler: 10,000 was a 1960s ad campaign."),
    }),
    dict(slug="apple-watch-steps-not-syncing", i18n={
        "": ("Apple Watch steps not syncing?",
             "Eight fixes, starting with the one that usually works."),
        "de": ("Apple Watch synct keine Schritte?",
               "8 Lösungen der Reihe nach — deine Schritte sind fast nie weg."),
        "fr": ("Pas Apple Watch non synchronisés",
               "8 solutions pour récupérer les pas bloqués entre montre et iPhone."),
        "es": ("El Apple Watch no sincroniza los pasos",
               "8 soluciones en orden, de la más fácil a la más drástica."),
        "ja": ("Apple Watchの歩数が同期されない",
               "歩数は消えていません。効く対処法を順番に8つ。"),
        "pt-br": ("Passos do Apple Watch não sincronizam",
                  "Oito soluções, da mais simples à mais drástica."),
        "ru": ("Apple Watch не синхронизирует шаги",
               "Восемь решений по порядку — шаги почти никогда не теряются."),
        "uk": ("Apple Watch не синхронізує кроки",
               "8 рішень по порядку — від швидкого поштовху до розпарювання."),
    }),
    dict(slug="step-counter-battery-gps", i18n={
        "": ("Do step counters drain your battery?",
             "GPS is the culprit — step counting itself is nearly free."),
        "de": ("Kosten Schrittzähler Akku?",
               "Schritte zählen ist gratis. GPS ist der eigentliche Preis."),
        "fr": ("Compteurs de pas et batterie",
               "Compter les pas ne coûte presque rien. Le GPS, si."),
        "es": ("¿Las apps de pasos gastan batería?",
               "Contar pasos es casi gratis; el GPS es el gasto real."),
        "ja": ("歩数計アプリはバッテリーを食う？",
               "歩数カウントは実質タダ。本当の犯人はGPSです。"),
        "pt-br": ("Apps de passos gastam bateria?",
                  "Contar passos é de graça. O GPS é que consome."),
        "ru": ("Шагомеры сажают батарею?",
               "Считать шаги почти бесплатно. Батарею сажает GPS."),
        "uk": ("Чи садять крокоміри акумулятор?",
               "Кроки майже безкоштовні. Заряд садить GPS — ось як це перевірити."),
    }),
    dict(slug="average-steps-per-day-by-age", i18n={
        "": ("Average steps per day by age",
             "What people actually walk, by age, sex and country."),
        "de": ("Schritte pro Tag im Durchschnitt",
               "Werte nach Alter, Geschlecht und Land — mit ehrlichen Grenzen."),
        "fr": ("Nombre moyen de pas par jour",
               "Moyennes par âge, sexe et pays — et pourquoi la vôtre diffère."),
        "es": ("Media de pasos al día por edad",
               "Rangos aproximados por edad, sexo y país, con matices honestos."),
        "ja": ("1日の平均歩数：年代別・国別データ",
               "成人はおよそ4,000〜5,000歩。年齢とともに減少。"),
        "pt-br": ("Média de passos por dia por idade",
                  "Faixas aproximadas por idade, sexo e país."),
        "ru": ("Средние шаги в день по возрасту",
               "Сколько ходят на самом деле: по возрасту, полу и странам."),
        "uk": ("Середня кількість кроків за віком",
               "Скільки ходять інші: діапазони за віком, статтю та країнами."),
    }),
]

# Pull the localized card copy already maintained for the homepage sections.
_HOME_KEYS = [("best-walking-games-iphone", "g1t", "g1d"),
              ("how-to-make-walking-fun", "g2t", "g2d"),
              ("how-many-steps-a-day", "g3t", "g3d")]
_BY_SLUG = {a["slug"]: a for a in ARTICLES}
for loc, strings in BL.L.items():
    for slug, tkey, dkey in _HOME_KEYS:
        if tkey in strings:
            _BY_SLUG[slug]["i18n"][loc] = (strings[tkey], strings[dkey])

# ---------------------------------------------------------------- hub copy
HUB = {
"": dict(
    lang="en", og_locale="en_US",
    title="Walking Guides — Steps, Habits & App Comparisons | Pixel Islands",
    meta="Research-backed guides on daily step counts, building a walking habit, "
         "step-tracker battery life, and the best walking games for iPhone.",
    h1="Walking guides",
    intro="Everything we've learned about steps, habits, and making a daily walk something "
          "you look forward to — written by the team behind Pixel Islands.",
    nav_features="Features", nav_guides="Guides", nav_dl="Download",
    foot_home="Home", foot_support="Support", foot_privacy="Privacy",
    footer_made="© 2026 Pixel Islands",
    cta_h2="Make your next walk count",
    cta_p="Pixel Islands grows a cozy pixel island from your daily steps. Free on iPhone.",
    cta_btn="Get Pixel Islands",
),
"de": dict(
    lang="de", og_locale="de_DE",
    title="Ratgeber rund ums Gehen — Schritte, Gewohnheiten & Apps | Pixel Islands",
    meta="Fundierte Ratgeber zu täglichen Schrittzahlen, Geh-Gewohnheiten, Akkuverbrauch von "
         "Schrittzählern und den besten Walking-Games fürs iPhone.",
    h1="Ratgeber rund ums Gehen",
    intro="Alles, was wir über Schritte, Gewohnheiten und schöne Spaziergänge gelernt haben — "
          "vom Team hinter Pixel Islands.",
    cta_h2="Mach deinen nächsten Spaziergang wertvoll",
    cta_p="Pixel Islands lässt aus deinen Schritten eine gemütliche Pixel-Insel wachsen. Kostenlos fürs iPhone.",
    cta_btn="Pixel Islands laden",
    foot_home="Start",
),
"fr": dict(
    lang="fr", og_locale="fr_FR",
    title="Guides de la marche — pas, habitudes et applis | Pixel Islands",
    meta="Des guides documentés sur le nombre de pas quotidien, l'habitude de marcher, "
         "la batterie des podomètres et les meilleurs jeux de marche sur iPhone.",
    h1="Guides de la marche",
    intro="Tout ce que nous avons appris sur les pas, les habitudes et l'art de rendre "
          "la marche quotidienne agréable — par l'équipe derrière Pixel Islands.",
    cta_h2="Donnez du sens à votre prochaine marche",
    cta_p="Pixel Islands fait pousser une île en pixel art au fil de vos pas. Gratuit sur iPhone.",
    cta_btn="Obtenir Pixel Islands",
    foot_home="Accueil",
),
"es": dict(
    lang="es", og_locale="es_ES",
    title="Guías para caminar — pasos, hábitos y apps | Pixel Islands",
    meta="Guías con base científica sobre pasos diarios, el hábito de caminar, la batería "
         "de los podómetros y los mejores juegos de caminar para iPhone.",
    h1="Guías para caminar",
    intro="Todo lo que hemos aprendido sobre pasos, hábitos y cómo hacer que el paseo diario "
          "apetezca — del equipo detrás de Pixel Islands.",
    cta_h2="Haz que tu próximo paseo cuente",
    cta_p="Pixel Islands hace crecer una isla de pixel art con tus pasos diarios. Gratis en iPhone.",
    cta_btn="Descargar Pixel Islands",
    foot_home="Inicio",
),
"ja": dict(
    lang="ja", og_locale="ja_JP",
    title="ウォーキングガイド — 歩数・習慣・アプリ比較 | Pixel Islands",
    meta="1日の歩数、歩く習慣の作り方、歩数計アプリのバッテリー、iPhoneのウォーキングゲームまで。"
         "根拠にもとづくガイド集です。",
    h1="ウォーキングガイド",
    intro="歩数と習慣、そして毎日の散歩を楽しみに変える方法について学んできたことをまとめました。"
          "Pixel Islandsチームより。",
    cta_h2="次の一歩を、意味のあるものに",
    cta_p="Pixel Islandsは毎日の歩数でピクセルアートの島を育てます。iPhoneで無料。",
    cta_btn="Pixel Islandsを入手",
    foot_home="ホーム",
),
"pt-br": dict(
    lang="pt-BR", og_locale="pt_BR",
    title="Guias de caminhada — passos, hábitos e apps | Pixel Islands",
    meta="Guias baseados em pesquisa sobre passos diários, hábito de caminhar, bateria de "
         "contadores de passos e os melhores jogos de caminhada para iPhone.",
    h1="Guias de caminhada",
    intro="Tudo o que aprendemos sobre passos, hábitos e como tornar a caminhada diária algo "
          "gostoso — pela equipe por trás do Pixel Islands.",
    cta_h2="Faça a próxima caminhada valer",
    cta_p="O Pixel Islands faz crescer uma ilha em pixel art com seus passos diários. Grátis no iPhone.",
    cta_btn="Baixar Pixel Islands",
    foot_home="Início",
),
"ru": dict(
    lang="ru", og_locale="ru_RU",
    title="Гайды о ходьбе — шаги, привычки и приложения | Pixel Islands",
    meta="Гайды с опорой на исследования: сколько шагов в день нужно, как выработать привычку "
         "ходить, расход батареи шагомерами и лучшие игры-шагомеры для iPhone.",
    h1="Гайды о ходьбе",
    intro="Всё, что мы узнали о шагах, привычках и о том, как сделать ежедневную прогулку "
          "желанной — от команды Pixel Islands.",
    cta_h2="Пусть следующая прогулка не пропадёт зря",
    cta_p="Pixel Islands выращивает уютный пиксельный остров из твоих шагов. Бесплатно на iPhone.",
    cta_btn="Установить Pixel Islands",
    foot_home="Главная",
),
"uk": dict(
    lang="uk", og_locale="uk_UA",
    title="Гайди про ходьбу — кроки, звички та застосунки | Pixel Islands",
    meta="Гайди з опорою на дослідження: скільки кроків на день потрібно, як виробити звичку "
         "ходити, витрата батареї крокомірами та найкращі ігри-крокоміри для iPhone.",
    h1="Гайди про ходьбу",
    intro="Усе, що ми дізналися про кроки, звички й те, як зробити щоденну прогулянку "
          "бажаною — від команди Pixel Islands.",
    cta_h2="Хай наступна прогулянка не мине даремно",
    cta_p="Pixel Islands вирощує затишний піксельний острів з твоїх кроків. Безкоштовно на iPhone.",
    cta_btn="Встановити Pixel Islands",
    foot_home="Головна",
),
}

# Fill nav/footer labels for locales from the homepage string table.
for loc in LOCALE_DIRS:
    if not loc:
        continue
    src = BL.L[loc]
    HUB[loc].setdefault("nav_features", src["nav_features"])
    HUB[loc].setdefault("nav_guides", src["nav_guides"])
    HUB[loc].setdefault("nav_dl", src["nav_dl"])
    HUB[loc].setdefault("foot_support", src["foot_support"])
    HUB[loc].setdefault("foot_privacy", src["foot_privacy"])
    HUB[loc].setdefault("footer_made", src["footer_made"])


def hub_url(loc):
    return f"{SITE}/guides/" if not loc else f"{SITE}/{loc}/guides/"


def render(loc):
    t = HUB[loc]
    up = "../" if not loc else "../../"      # to site root
    home = "../"                              # to this locale's homepage
    arts = [a for a in ARTICLES if loc in a["i18n"]]

    hreflang = "\n".join(
        f'<link rel="alternate" hreflang="{HREFLANG_OF[l]}" href="{hub_url(l)}">'
        for l in LOCALE_DIRS
    ) + f'\n<link rel="alternate" hreflang="x-default" href="{hub_url("")}">'

    cards = "\n".join(
        f'        <a href="{a["slug"]}/">{a["i18n"][loc][0]}<small>{a["i18n"][loc][1]}</small></a>'
        for a in arts
    )

    items = ",\n".join(
        f'      {{"@type": "ListItem", "position": {i}, '
        f'"url": "{hub_url(loc)}{a["slug"]}/", "name": {_json_str(a["i18n"][loc][0])}}}'
        for i, a in enumerate(arts, 1)
    )

    return f"""<!DOCTYPE html>
<html lang="{t['lang']}">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{t['title']}</title>
<meta name="description" content="{t['meta']}">
<link rel="canonical" href="{hub_url(loc)}">
{hreflang}
<meta property="og:type" content="website">
<meta property="og:locale" content="{t['og_locale']}">
<meta property="og:title" content="{t['h1']} | Pixel Islands">
<meta property="og:description" content="{t['meta']}">
<meta property="og:url" content="{hub_url(loc)}">
<meta property="og:image" content="{SITE}/assets/hero.jpg">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" type="image/png" href="{up}assets/appicon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Nunito:wght@600;700;800;900&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{up}styles.css">
<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "CollectionPage",
  "name": {_json_str(t['h1'])},
  "description": {_json_str(t['meta'])},
  "url": "{hub_url(loc)}",
  "inLanguage": "{t['lang']}",
  "isPartOf": {{ "@type": "WebSite", "name": "Pixel Islands", "url": "{SITE}/" }},
  "mainEntity": {{
    "@type": "ItemList",
    "itemListElement": [
{items}
    ]
  }}
}}
</script>
</head>
<body>

<header class="site">
  <div class="wrap nav">
    <a class="brand" href="{home}">
      <img src="{up}assets/appicon.png" alt="Pixel Islands" width="36" height="36">
      Pixel Islands
    </a>
    <nav>
      <a href="{home}#features">{t['nav_features']}</a>
      <a href="{up}{'guides/' if not loc else loc + '/guides/'}">{t['nav_guides']}</a>
      <a href="{up}support/">{t['foot_support']}</a>
      <a class="cta-mini" href="{APP_URL}">{t['nav_dl']}</a>
    </nav>
  </div>
</header>

<main>
  <section>
    <div class="wrap">
      <div class="section-head">
        <h1>{t['h1']}</h1>
        <p>{t['intro']}</p>
      </div>
      <div class="guide-cards">
{cards}
      </div>
    </div>
  </section>

  <div class="cta-band">
    <h2>{t['cta_h2']}</h2>
    <p>{t['cta_p']}</p>
    <a class="appstore-badge" href="{APP_URL}" aria-label="{t['cta_btn']}">
      <svg viewBox="0 0 200 60" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="App Store">
        <rect width="200" height="60" rx="12" fill="#111"/>
        <g fill="#fff">
          <path d="M36.4 30.6c0-3.6 2.9-5.3 3-5.4-1.6-2.4-4.2-2.7-5.1-2.8-2.2-.2-4.2 1.3-5.3 1.3-1.1 0-2.8-1.2-4.6-1.2-2.4 0-4.6 1.4-5.8 3.5-2.5 4.3-.6 10.6 1.8 14.1 1.2 1.7 2.6 3.6 4.4 3.5 1.8-.1 2.4-1.1 4.6-1.1 2.1 0 2.7 1.1 4.6 1.1 1.9 0 3.1-1.7 4.3-3.4 1.3-2 1.9-3.9 1.9-4-.1-.1-3.8-1.5-3.8-5.6zM33 20.1c1-1.2 1.6-2.8 1.5-4.5-1.4.1-3.1 1-4.1 2.1-.9 1-1.7 2.7-1.5 4.3 1.6.1 3.1-.7 4.1-1.9z"/>
          <text x="52" y="38" font-family="-apple-system, Helvetica, Arial, sans-serif" font-size="17" font-weight="700" fill="#fff">App Store</text>
        </g>
      </svg>
    </a>
  </div>
</main>

<footer class="site">
  <div class="wrap cols">
    <div>{t['footer_made']}</div>
    <div>
      <a href="{home}">{t['foot_home']}</a>
      <a href="{up}support/">{t['foot_support']}</a>
      <a href="{up}privacy/">{t['foot_privacy']}</a>
    </div>
  </div>
</footer>

</body>
</html>
"""


def _json_str(s):
    import json
    return json.dumps(s, ensure_ascii=False)


if __name__ == "__main__":
    root = pathlib.Path(__file__).parent
    for loc in LOCALE_DIRS:
        out = root / ("guides" if not loc else f"{loc}/guides") / "index.html"
        # never link an article that does not exist on disk
        for a in ARTICLES:
            if loc in a["i18n"] and not (out.parent / a["slug"] / "index.html").exists():
                raise SystemExit(f"{out}: would link missing article {a['slug']}")
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(render(loc), encoding="utf-8")
        n = len([a for a in ARTICLES if loc in a["i18n"]])
        print(f"{out}: OK ({n} articles)")
