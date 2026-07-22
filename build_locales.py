#!/usr/bin/env python3
"""Generate localized homepages from a shared template.

Usage: python3 build_locales.py
Regenerates <locale>/index.html for every locale in L below.
English homepage (index.html) is maintained by hand; keep structure in sync.
"""
import json
import pathlib

SITE = "https://pixelislands.app"
APP_URL = "https://apps.apple.com/app/pixel-islands-step-track-game/id6760819710"

HREFLANGS = [
    ("en", "/"), ("de", "/de/"), ("fr", "/fr/"), ("es", "/es/"), ("ja", "/ja/"),
    ("pt-BR", "/pt-br/"), ("ru", "/ru/"), ("uk", "/uk/"),
]

LANG_NAMES = [
    ("/", "English"), ("/de/", "Deutsch"), ("/fr/", "Français"), ("/es/", "Español"),
    ("/ja/", "日本語"), ("/pt-br/", "Português"), ("/ru/", "Русский"), ("/uk/", "Українська"),
]

L = {
"de": dict(
    lang="de", og_locale="de_DE",
    title="Pixel Islands – Schrittzähler-Spiel für iPhone | Geh spazieren, lass deine Insel wachsen",
    meta="Pixel Islands verwandelt deine täglichen Schritte in eine gemütliche Pixel-Insel, die in 8 Stufen wächst. Schrittzähler-Spiel für iPhone mit Widget, Apple-Health-Anbindung und sammelbaren Inseln. Kostenlos laden.",
    og_title="Pixel Islands – Geh spazieren, lass deine Insel wachsen",
    og_desc="Ein gemütliches Schrittzähler-Spiel für iPhone. Deine echten Schritte lassen eine Pixel-Insel in 8 Stufen wachsen.",
    nav_how="So funktioniert's", nav_features="Funktionen", nav_islands="Inseln", nav_faq="FAQ", nav_dl="Laden",
    h1="Deine Schritte lassen<br>eine Pixel-Insel wachsen",
    sub="Pixel Islands ist ein gemütliches Schrittzähler-Spiel für iPhone. Geh in der echten Welt spazieren und sieh zu, wie deine Insel in 8 Stufen wächst — ohne Druck, ohne Coaching, einfach Wachstum.",
    rating="4,8 im App Store",
    hero_alt="Fünf schwebende Pixel-Inseln aus dem Spiel Pixel Islands: Cyberpunk, Sakura, Wiese, Olymp und Steampunk",
    badge1="Laden im", badge2="App Store",
    how_h2="Gehen, das sich lohnt",
    how_p="Kein Coaching, kein schlechtes Gewissen, keine komplizierten Statistiken. Nur ein einfacher Kreislauf, der Lust auf den längeren Heimweg macht.",
    s1t="1. Geh deinen Tag", s1p="Pixel Islands liest deine Schritte aus Apple Health — Handy in der Tasche, Apple Watch am Arm, alles zählt. Kein GPS, kein Akku-Fresser.",
    s2t="2. Sieh sie wachsen", s2p="Jeder Schritt nährt deine Insel. Aus nacktem Fels werden Gras, Bäche, Häuser, ganze kleine Welten — über 8 Stufen.",
    s3t="3. Sammle sie alle", s3p="Vollende eine Insel und wähle dein nächstes Thema. Baue eine schwebende Sammlung kleiner Welten — angetrieben allein durch dein Gehen.",
    evo_h2="Vom nackten Fels zur lebendigen Welt",
    evo_p="Das ist die Sakura-Insel auf ihrem Weg durch 8 Stufen — angetrieben von echten Schritten.",
    evo_meta="Jede Stufe schaltest du mit deinen Schritten frei. Schau kurz rein, sieh, was sich verändert hat, und geh weiter Richtung nächster Stufe.",
    stage_tpl="Stufe {n} von 8", keep_walking="Weitergehen …",
    labels=["Ein nackter Fels im Himmel","Erste Grasflecken","Ein Bach findet seinen Weg","Blüten schlagen Wurzeln","Ein Pfad und eine Laterne","Der Schrein erscheint","Kirschbäume in voller Blüte","Eine Welt für sich"],
    feat_h2="Kleine App, viel zu lieben",
    f1t="8 wachsende Stufen", f1p="Jede Insel wächst vom nackten Fels zum lebendigen Diorama — Spaziergang für Spaziergang.",
    f2t="Sammelbare Themen", f2p="Sakura-Schreine, nordisches Asgard, Steampunk-Häfen, Neon-Cyberpunk und mehr.",
    f3t="Homescreen-Widget", f3p="Deine Insel lebt auf deinem Homescreen — Fortschritt auf einen Blick, den ganzen Tag.",
    f4t="Apple Health als Basis", f4p="Liest nur deine Schrittzahl aus HealthKit. Kein GPS, kein Tracking, akkuschonend.",
    f5t="iCloud-Sync", f5p="Deine Inseln sind sicher gesichert. Neues iPhone? Deine Sammlung zieht mit um.",
    f6t="Privat by Design", f6p="Deine Gesundheitsdaten werden nie verkauft, nie für Werbung genutzt, nie geteilt.",
    themes_h2="Welche Insel züchtest du als Nächstes?", themes_p="Jede vollendete Insel schaltet die Wahl einer neuen Welt frei.",
    theme_names=["Sakura","Asgard","Steampunk","Cyberpunk"],
    faq_h2="Fragen, beantwortet",
    faq=[
        ("Wie zählt Pixel Islands meine Schritte?","Pixel Islands liest deine Schrittzahl aus Apple Health (HealthKit). Es nutzt kein GPS und läuft nicht im Hintergrund — also akkuschonend. Alle in Apple Health erfassten Schritte zählen, auch die von deiner Apple Watch."),
        ("Ist Pixel Islands kostenlos?","Ja — kostenlos laden und spielen. Ein optionales Premium schaltet zusätzliche Insel-Themen und leichte Beschleunigung frei."),
        ("Sind meine Gesundheitsdaten privat?","Pixel Islands liest nur deine Schrittzahl — sonst nichts — und nutzt sie ausschließlich für deine Insel. Deine Daten werden nie verkauft, nie für Werbung genutzt, nie geteilt."),
        ("Was passiert, wenn ich eine Insel vollende?","Erreicht deine Insel die letzte Stufe, wandert sie in deine Sammlung und du wählst ein neues Thema — von Kirschblüten-Schreinen bis Steampunk-Häfen."),
        ("Funktioniert Pixel Islands mit der Apple Watch?","Schritte deiner Apple Watch landen in Apple Health, und genau dort liest Pixel Islands sie aus — deine Watch-Spaziergänge zählen also alle."),
        ("Welches iPhone brauche ich?","Pixel Islands läuft auf iPhones mit iOS 17 oder neuer und ist in 20 Sprachen verfügbar."),
    ],
    cta_h2="Bereit für deine erste Insel?", cta_p="Kostenlos im App Store. Dein nächster Spaziergang zählt schon.",
    footer_made="© 2026 Pixel Islands · Gemacht mit 🏝️ und vielen Spaziergängen",
    foot_support="Support", foot_privacy="Datenschutz", foot_store="App Store",
    nav_guides="Guides",
    guides_h2="Gehen, gut recherchiert",
    guides_p="Guides vom Pixel-Islands-Team, damit deine Schritte zählen.",
    g1t="Die 7 besten Walking-Games fürs iPhone", g1d="Gemütliche Aufbau-Spiele, Sammel-Kreaturen, Zombie-Fluchten — ehrlich verglichen.",
    g2t="So macht Gehen Spaß", g2d="12 Ideen, die auch Woche zwei überleben.",
    g3t="Wie viele Schritte pro Tag brauchst du?", g3d="Spoiler: 10.000 waren eine Werbekampagne aus den 60ern.",
),
"fr": dict(
    lang="fr", og_locale="fr_FR",
    title="Pixel Islands – Jeu podomètre pour iPhone | Marchez pour faire grandir votre île",
    meta="Pixel Islands transforme vos pas quotidiens en une île pixel art qui grandit en 8 étapes. Jeu de marche pour iPhone avec widget, Apple Santé et îles à collectionner. Téléchargement gratuit.",
    og_title="Pixel Islands – Marchez pour faire grandir votre île",
    og_desc="Un jeu podomètre tout en douceur pour iPhone. Vos vrais pas font grandir une île en pixels, en 8 étapes.",
    nav_how="Comment ça marche", nav_features="Fonctionnalités", nav_islands="Îles", nav_faq="FAQ", nav_dl="Télécharger",
    h1="Vos pas font grandir<br>une petite île en pixels",
    sub="Pixel Islands est un jeu podomètre tout en douceur pour iPhone. Marchez dans le monde réel et regardez votre île évoluer en 8 étapes — sans pression, sans coaching, juste de la croissance.",
    rating="4,8 sur l'App Store",
    hero_alt="Cinq îles pixel art flottantes du jeu Pixel Islands : cyberpunk, sakura, prairie, Olympe et steampunk",
    badge1="Télécharger dans", badge2="l'App Store",
    how_h2="La marche, enfin récompensée",
    how_p="Pas de coaching, pas de culpabilité, pas de statistiques compliquées. Juste une boucle simple qui donne envie de prendre le chemin le plus long.",
    s1t="1. Marchez comme d'habitude", s1p="Pixel Islands lit vos pas dans Apple Santé — téléphone en poche, Apple Watch au poignet, tout compte. Pas de GPS, pas de batterie vidée.",
    s2t="2. Regardez-la grandir", s2p="Chaque pas nourrit votre île. La roche nue devient herbe, ruisseaux, maisons, petits mondes entiers — en 8 étapes.",
    s3t="3. Collectionnez-les toutes", s3p="Terminez une île, choisissez le thème suivant. Construisez une collection flottante de petits mondes, propulsée par vos pas.",
    evo_h2="De la roche nue au monde vivant",
    evo_p="Voici l'île Sakura qui grandit à travers ses 8 étapes — grâce à de vrais pas.",
    evo_meta="Chaque étape se débloque avec vos pas. Ouvrez l'app quelques secondes, voyez ce qui a changé, et repartez marcher vers la suivante.",
    stage_tpl="Étape {n} sur 8", keep_walking="Continuez à marcher…",
    labels=["Un rocher nu dans le ciel","Premières touffes d'herbe","Un ruisseau trouve son chemin","Les fleurs prennent racine","Un sentier et une lanterne","Le sanctuaire apparaît","Cerisiers en fleurs","Un monde à part entière"],
    feat_h2="Petite app, grand plaisir",
    f1t="8 étapes d'évolution", f1p="Chaque île passe de la roche nue à un diorama vivant, promenade après promenade.",
    f2t="Thèmes à collectionner", f2p="Sanctuaires sakura, Asgard nordique, ports steampunk, cyberpunk néon et plus.",
    f3t="Widget d'écran d'accueil", f3p="Votre île vit sur votre écran d'accueil — progrès visible en un coup d'œil.",
    f4t="Propulsé par Apple Santé", f4p="Ne lit que votre nombre de pas via HealthKit. Pas de GPS, pas de pistage, batterie préservée.",
    f5t="Synchronisation iCloud", f5p="Vos îles sont sauvegardées. Nouvel iPhone ? Votre collection vous suit.",
    f6t="Privé par conception", f6p="Vos données de santé ne sont jamais vendues, jamais utilisées pour la pub, jamais partagées.",
    themes_h2="Quelle île ferez-vous grandir ensuite ?", themes_p="Chaque île terminée débloque le choix d'un nouveau monde.",
    theme_names=["Sakura","Asgard","Steampunk","Cyberpunk"],
    faq_h2="Vos questions, nos réponses",
    faq=[
        ("Comment Pixel Islands compte-t-il mes pas ?","Pixel Islands lit votre nombre de pas dans Apple Santé (HealthKit). Pas de GPS ni d'activité en arrière-plan : la batterie est préservée. Tous les pas enregistrés dans Apple Santé comptent, y compris ceux de votre Apple Watch."),
        ("Pixel Islands est-il gratuit ?","Oui — gratuit à télécharger et à jouer. Un Premium optionnel débloque des thèmes d'îles supplémentaires et une légère accélération."),
        ("Mes données de santé restent-elles privées ?","Pixel Islands ne lit que votre nombre de pas — rien d'autre — et l'utilise uniquement pour faire grandir votre île. Jamais vendues, jamais utilisées pour la publicité, jamais partagées."),
        ("Que se passe-t-il quand je termine une île ?","Quand votre île atteint sa dernière étape, elle rejoint votre collection et vous choisissez un nouveau thème — des sanctuaires en fleurs aux ports steampunk."),
        ("Compatible avec l'Apple Watch ?","Les pas comptés par votre Apple Watch sont enregistrés dans Apple Santé, où Pixel Islands les lit — vos marches avec la Watch comptent toutes."),
        ("Quel iPhone me faut-il ?","Pixel Islands fonctionne sur iPhone avec iOS 17 ou plus récent, en 20 langues."),
    ],
    cta_h2="Prêt à faire grandir votre première île ?", cta_p="Gratuit sur l'App Store. Votre prochaine promenade compte déjà.",
    footer_made="© 2026 Pixel Islands · Fait avec 🏝️ et beaucoup de marche",
    foot_support="Assistance", foot_privacy="Confidentialité", foot_store="App Store",
    nav_guides="Guides",
    guides_h2="La marche, étudiée",
    guides_p="Les guides de l'équipe Pixel Islands pour des pas qui comptent.",
    g1t="Les 7 meilleurs jeux de marche sur iPhone", g1d="Builders cosy, collection de créatures, évasions zombies — comparés honnêtement.",
    g2t="Comment rendre la marche amusante", g2d="12 idées qui tiennent au-delà de la deuxième semaine.",
    g3t="Combien de pas par jour vous faut-il ?", g3d="Spoiler : 10 000, c'était une pub des années 60.",
),
"es": dict(
    lang="es", og_locale="es_ES",
    title="Pixel Islands – Juego podómetro para iPhone | Camina y haz crecer tu isla",
    meta="Pixel Islands convierte tus pasos diarios en una isla pixel art que crece en 8 etapas. Juego de caminar para iPhone con widget, Apple Salud e islas coleccionables. Descarga gratis.",
    og_title="Pixel Islands – Camina y haz crecer tu isla",
    og_desc="Un acogedor juego podómetro para iPhone. Tus pasos reales hacen crecer una isla píxel en 8 etapas.",
    nav_how="Cómo funciona", nav_features="Funciones", nav_islands="Islas", nav_faq="FAQ", nav_dl="Descargar",
    h1="Tus pasos hacen crecer<br>una pequeña isla píxel",
    sub="Pixel Islands es un acogedor juego podómetro para iPhone. Camina en el mundo real y mira cómo tu isla evoluciona en 8 etapas: sin presión, sin sermones, solo crecimiento.",
    rating="4,8 en el App Store",
    hero_alt="Cinco islas pixel art flotantes del juego Pixel Islands: cyberpunk, sakura, pradera, Olimpo y steampunk",
    badge1="Descargar en el", badge2="App Store",
    how_h2="Caminar, por fin recompensado",
    how_p="Sin coaching, sin culpa, sin estadísticas complicadas. Solo un ciclo simple que te hace querer volver a casa por el camino largo.",
    s1t="1. Camina tu día", s1p="Pixel Islands lee tus pasos de Apple Salud: móvil en el bolsillo, Apple Watch en la muñeca, todo cuenta. Sin GPS y sin gastar batería.",
    s2t="2. Mírala crecer", s2p="Cada paso alimenta tu isla. La roca desnuda se convierte en hierba, arroyos, casas, pequeños mundos enteros — en 8 etapas.",
    s3t="3. Colecciónalas todas", s3p="Termina una isla y elige el siguiente tema. Construye una colección flotante de pequeños mundos impulsada solo por tus pasos.",
    evo_h2="De roca desnuda a mundo vivo",
    evo_p="Esta es la isla Sakura creciendo por sus 8 etapas — con pasos reales.",
    evo_meta="Cada etapa se desbloquea con tus pasos. Entra unos segundos, mira qué ha cambiado y sigue caminando hacia la siguiente.",
    stage_tpl="Etapa {n} de 8", keep_walking="Sigue caminando…",
    labels=["Una roca desnuda en el cielo","Primeros brotes de hierba","Un arroyo se abre camino","Los cerezos echan raíces","Un sendero y un farol","Aparece el santuario","Cerezos en plena flor","Un mundo propio"],
    feat_h2="App pequeña, mucho que querer",
    f1t="8 etapas de evolución", f1p="Cada isla crece de roca desnuda a un diorama vivo, paseo a paseo.",
    f2t="Temas coleccionables", f2p="Santuarios sakura, Asgard nórdico, puertos steampunk, cyberpunk neón y más.",
    f3t="Widget en pantalla de inicio", f3p="Tu isla vive en tu pantalla de inicio: progreso de un vistazo, todo el día.",
    f4t="Impulsado por Apple Salud", f4p="Solo lee tu número de pasos de HealthKit. Sin GPS, sin rastreo, sin gastar batería.",
    f5t="Sincronización iCloud", f5p="Tus islas están respaldadas. ¿iPhone nuevo? Tu colección te acompaña.",
    f6t="Privado por diseño", f6p="Tus datos de salud nunca se venden, nunca se usan para publicidad, nunca se comparten.",
    themes_h2="¿Qué isla harás crecer ahora?", themes_p="Cada isla completada desbloquea la elección de un nuevo mundo.",
    theme_names=["Sakura","Asgard","Steampunk","Cyberpunk"],
    faq_h2="Preguntas, respondidas",
    faq=[
        ("¿Cómo cuenta mis pasos Pixel Islands?","Pixel Islands lee tu número de pasos de Apple Salud (HealthKit). No usa GPS ni se ejecuta en segundo plano, así que cuida la batería. Cuentan todos los pasos registrados en Apple Salud, incluidos los de tu Apple Watch."),
        ("¿Es gratis Pixel Islands?","Sí: gratis para descargar y jugar. Un Premium opcional desbloquea temas de isla adicionales y una ligera aceleración."),
        ("¿Mis datos de salud son privados?","Pixel Islands solo lee tu número de pasos —nada más— y lo usa únicamente para hacer crecer tu isla. Nunca se venden, nunca se usan para publicidad, nunca se comparten."),
        ("¿Qué pasa cuando completo una isla?","Cuando tu isla alcanza su etapa final, pasa a tu colección y eliges un nuevo tema: de santuarios en flor a puertos steampunk."),
        ("¿Funciona con Apple Watch?","Los pasos de tu Apple Watch se guardan en Apple Salud, y de ahí los lee Pixel Islands: tus paseos con el Watch cuentan todos."),
        ("¿Qué iPhone necesito?","Pixel Islands funciona en iPhone con iOS 17 o posterior y está disponible en 20 idiomas."),
    ],
    cta_h2="¿Listo para hacer crecer tu primera isla?", cta_p="Gratis en el App Store. Tu próximo paseo ya cuenta.",
    footer_made="© 2026 Pixel Islands · Hecho con 🏝️ y muchos paseos",
    foot_support="Soporte", foot_privacy="Privacidad", foot_store="App Store",
    nav_guides="Guías",
    guides_h2="Caminar, investigado",
    guides_p="Guías del equipo de Pixel Islands para que tus pasos cuenten.",
    g1t="Los 7 mejores juegos de caminar para iPhone", g1d="Builders acogedores, colección de criaturas, huidas zombis — comparados con honestidad.",
    g2t="Cómo hacer que caminar sea divertido", g2d="12 ideas que sobreviven a la segunda semana.",
    g3t="¿Cuántos pasos al día necesitas?", g3d="Spoiler: 10.000 fue una campaña publicitaria de los 60.",
),
"ja": dict(
    lang="ja", og_locale="ja_JP",
    title="Pixel Islands – iPhone向け歩数計ゲーム | 歩いて島を育てよう",
    meta="Pixel Islandsは毎日の歩数がピクセルアートの島になる歩数計ゲーム。8段階で成長する島、ウィジェット、ヘルスケア連携。無料でダウンロード。",
    og_title="Pixel Islands – 歩いて島を育てよう",
    og_desc="iPhone向けのゆったり歩数計ゲーム。現実の歩数でピクセルの島が8段階で育ちます。",
    nav_how="仕組み", nav_features="機能", nav_islands="島", nav_faq="FAQ", nav_dl="ダウンロード",
    h1="歩くたびに育つ、<br>小さなピクセルの島",
    sub="Pixel IslandsはiPhone向けのゆったり歩数計ゲーム。現実世界で歩くと、島が8段階で成長していきます。プレッシャーもコーチングもなし。ただ、育っていくだけ。",
    rating="App Storeで4.8",
    hero_alt="Pixel Islandsの5つの浮かぶピクセルアートの島:サイバーパンク、桜、草原、オリンポス、スチームパンク",
    badge1="ダウンロードは", badge2="App Store",
    how_h2="歩くことが、ごほうびになる",
    how_p="コーチングも罪悪感も複雑な統計もなし。遠回りして帰りたくなる、シンプルなループだけ。",
    s1t="1. いつも通り歩く", s1p="Pixel Islandsはヘルスケア(Apple Health)から歩数を読み取ります。ポケットのiPhoneも、手首のApple Watchもすべてカウント。GPS不使用でバッテリーにやさしい。",
    s2t="2. 島が育つのを眺める", s2p="一歩ごとに島が育ちます。むき出しの岩が草原になり、小川が流れ、家が建ち、小さな世界が完成していく — 全8段階。",
    s3t="3. 全部集める", s3p="島を完成させたら、次のテーマを選択。歩くだけで、浮かぶ小さな世界のコレクションが増えていきます。",
    evo_h2="むき出しの岩から、生きた世界へ",
    evo_p="これは桜の島が8段階で育っていく様子。本物の歩数で成長します。",
    evo_meta="各ステージは歩数で解放されます。数秒アプリを開いて変化を確かめたら、次のステージへ向けてまた歩こう。",
    stage_tpl="ステージ {n} / 8", keep_walking="歩き続けよう…",
    labels=["空に浮かぶむき出しの岩","最初の草が芽生える","小川が流れはじめる","桜が根を下ろす","小道と灯籠","神社が現れる","満開の桜","ひとつの世界が完成"],
    feat_h2="小さなアプリに、たくさんの魅力",
    f1t="8段階で成長", f1p="どの島も、むき出しの岩から生きたジオラマへ。散歩のたびに育ちます。",
    f2t="集められるテーマ", f2p="桜の神社、北欧のアスガルド、スチームパンクの空中港、ネオンのサイバーパンクなど。",
    f3t="ホーム画面ウィジェット", f3p="島はホーム画面に。進み具合がいつでもひと目でわかります。",
    f4t="ヘルスケア連携", f4p="HealthKitから歩数だけを読み取ります。GPSなし、追跡なし、バッテリーにやさしい。",
    f5t="iCloud同期", f5p="島は安全にバックアップ。iPhoneを替えてもコレクションは一緒です。",
    f6t="プライバシー第一", f6p="健康データを売ることも、広告に使うことも、共有することもありません。",
    themes_h2="次はどの島を育てる?", themes_p="島を完成させるたびに、新しい世界を選べます。",
    theme_names=["桜","アスガルド","スチームパンク","サイバーパンク"],
    faq_h2="よくある質問",
    faq=[
        ("歩数はどうやってカウントされますか?","Pixel Islandsはヘルスケア(HealthKit)から歩数を読み取ります。GPSもバックグラウンド動作も不要なので、バッテリーにやさしい設計です。Apple Watchで記録された歩数もすべてカウントされます。"),
        ("Pixel Islandsは無料ですか?","はい、ダウンロードもプレイも無料です。オプションのプレミアムで追加の島テーマとゆるやかな成長ブーストが解放されます。"),
        ("健康データのプライバシーは?","Pixel Islandsが読み取るのは歩数だけ。島を育てる目的にのみ使います。販売も、広告利用も、第三者共有も一切ありません。"),
        ("島を完成させるとどうなりますか?","最終ステージに達した島はコレクションに加わり、次に育てる島のテーマを選べます。桜の神社からスチームパンクの空中港まで。"),
        ("Apple Watchでも使えますか?","Apple Watchの歩数はヘルスケアに保存され、Pixel Islandsはそこから読み取ります。Watchでの散歩もすべてカウントされます。"),
        ("対応するiPhoneは?","iOS 17以降のiPhoneに対応し、20言語で利用できます。"),
    ],
    cta_h2="最初の島を育てはじめよう", cta_p="App Storeで無料。次の散歩からもう始まっています。",
    footer_made="© 2026 Pixel Islands · 🏝️とたくさんの散歩から生まれました",
    foot_support="サポート", foot_privacy="プライバシー", foot_store="App Store",
    nav_guides="ガイド",
    guides_h2="歩くことを、調べてみた",
    guides_p="歩数を意味あるものにする、Pixel Islandsチームのガイド。",
    g1t="iPhone向けウォーキングゲーム ベスト7", g1d="ゆったり系からクリーチャー収集、ゾンビ脱出まで。正直に比較。",
    g2t="ウォーキングを楽しくする方法", g2d="2週目も続く、12のアイデア。",
    g3t="1日に必要な歩数は?", g3d="ネタバレ:1万歩は60年代の広告でした。",
),
"pt-br": dict(
    lang="pt-BR", og_locale="pt_BR",
    title="Pixel Islands – Jogo pedômetro para iPhone | Caminhe e faça sua ilha crescer",
    meta="O Pixel Islands transforma seus passos diários em uma ilha pixel art que cresce em 8 estágios. Jogo de caminhada para iPhone com widget, Apple Saúde e ilhas colecionáveis. Baixe grátis.",
    og_title="Pixel Islands – Caminhe e faça sua ilha crescer",
    og_desc="Um jogo pedômetro aconchegante para iPhone. Seus passos reais fazem crescer uma ilha de pixels em 8 estágios.",
    nav_how="Como funciona", nav_features="Recursos", nav_islands="Ilhas", nav_faq="FAQ", nav_dl="Baixar",
    h1="Seus passos fazem crescer<br>uma ilhinha de pixels",
    sub="Pixel Islands é um jogo pedômetro aconchegante para iPhone. Caminhe no mundo real e veja sua ilha evoluir em 8 estágios — sem pressão, sem cobrança, só crescimento.",
    rating="4,8 na App Store",
    hero_alt="Cinco ilhas pixel art flutuantes do jogo Pixel Islands: cyberpunk, sakura, campina, Olimpo e steampunk",
    badge1="Baixar na", badge2="App Store",
    how_h2="Caminhar, enfim recompensado",
    how_p="Sem coaching, sem culpa, sem estatísticas complicadas. Só um ciclo simples que dá vontade de voltar pra casa pelo caminho mais longo.",
    s1t="1. Caminhe seu dia", s1p="O Pixel Islands lê seus passos do Apple Saúde — celular no bolso, Apple Watch no pulso, tudo conta. Sem GPS, sem drenar bateria.",
    s2t="2. Veja a ilha crescer", s2p="Cada passo alimenta sua ilha. A rocha nua vira grama, riachos, casas, pequenos mundos inteiros — em 8 estágios.",
    s3t="3. Colecione todas", s3p="Termine uma ilha e escolha o próximo tema. Monte uma coleção flutuante de mundinhos movida só pelos seus passos.",
    evo_h2="Da rocha nua a um mundo vivo",
    evo_p="Esta é a ilha Sakura crescendo pelos 8 estágios — com passos de verdade.",
    evo_meta="Cada estágio é desbloqueado com seus passos. Abra por alguns segundos, veja o que mudou e continue caminhando até o próximo.",
    stage_tpl="Estágio {n} de 8", keep_walking="Continue caminhando…",
    labels=["Uma rocha nua no céu","Primeiros tufos de grama","Um riacho abre caminho","As cerejeiras criam raízes","Uma trilha e uma lanterna","O santuário aparece","Cerejeiras em plena flor","Um mundo próprio"],
    feat_h2="App pequeno, muito pra amar",
    f1t="8 estágios de evolução", f1p="Cada ilha cresce de rocha nua a um diorama vivo, caminhada após caminhada.",
    f2t="Temas colecionáveis", f2p="Santuários sakura, Asgard nórdica, portos steampunk, cyberpunk neon e mais.",
    f3t="Widget na tela de início", f3p="Sua ilha mora na tela de início — progresso à vista o dia todo.",
    f4t="Movido pelo Apple Saúde", f4p="Lê apenas sua contagem de passos do HealthKit. Sem GPS, sem rastreamento, sem gastar bateria.",
    f5t="Sincronização iCloud", f5p="Suas ilhas ficam salvas. iPhone novo? Sua coleção vai junto.",
    f6t="Privado por padrão", f6p="Seus dados de saúde nunca são vendidos, nunca usados em anúncios, nunca compartilhados.",
    themes_h2="Qual ilha você vai criar agora?", themes_p="Cada ilha concluída desbloqueia a escolha de um novo mundo.",
    theme_names=["Sakura","Asgard","Steampunk","Cyberpunk"],
    faq_h2="Perguntas, respondidas",
    faq=[
        ("Como o Pixel Islands conta meus passos?","O Pixel Islands lê sua contagem de passos do Apple Saúde (HealthKit). Não usa GPS nem roda em segundo plano, então poupa bateria. Todos os passos registrados no Apple Saúde contam, inclusive os do seu Apple Watch."),
        ("O Pixel Islands é grátis?","Sim — grátis para baixar e jogar. Um Premium opcional desbloqueia temas de ilha extras e uma leve aceleração."),
        ("Meus dados de saúde são privados?","O Pixel Islands lê apenas sua contagem de passos — nada mais — e usa só para fazer sua ilha crescer. Nunca vendidos, nunca usados em publicidade, nunca compartilhados."),
        ("O que acontece quando completo uma ilha?","Quando a ilha atinge o estágio final, ela entra na sua coleção e você escolhe um novo tema — de santuários floridos a portos steampunk."),
        ("Funciona com Apple Watch?","Os passos do seu Apple Watch vão para o Apple Saúde, de onde o Pixel Islands os lê — suas caminhadas com o Watch contam todas."),
        ("Qual iPhone eu preciso?","O Pixel Islands roda em iPhone com iOS 17 ou mais recente e está disponível em 20 idiomas."),
    ],
    cta_h2="Pronto para criar sua primeira ilha?", cta_p="Grátis na App Store. Sua próxima caminhada já conta.",
    footer_made="© 2026 Pixel Islands · Feito com 🏝️ e muitas caminhadas",
    foot_support="Suporte", foot_privacy="Privacidade", foot_store="App Store",
    nav_guides="Guias",
    guides_h2="Caminhar, pesquisado",
    guides_p="Guias do time do Pixel Islands para fazer seus passos valerem.",
    g1t="Os 7 melhores jogos de caminhada para iPhone", g1d="Builders aconchegantes, coleção de criaturas, fugas de zumbis — comparados com honestidade.",
    g2t="Como tornar a caminhada divertida", g2d="12 ideias que sobrevivem à segunda semana.",
    g3t="Quantos passos por dia você precisa?", g3d="Spoiler: 10.000 foi uma campanha publicitária dos anos 60.",
),
"ru": dict(
    lang="ru", og_locale="ru_RU",
    title="Pixel Islands – игра-шагомер для iPhone | Ходи пешком и выращивай остров",
    meta="Pixel Islands превращает ежедневные шаги в уютный пиксельный остров, который растёт в 8 этапов. Игра-шагомер для iPhone с виджетом, Apple Health и коллекцией островов. Скачайте бесплатно.",
    og_title="Pixel Islands – Ходи пешком и выращивай остров",
    og_desc="Уютная игра-шагомер для iPhone. Настоящие шаги растят пиксельный остров в 8 стадий.",
    nav_how="Как это работает", nav_features="Возможности", nav_islands="Острова", nav_faq="FAQ", nav_dl="Скачать",
    h1="Твои шаги растят<br>маленький пиксельный остров",
    sub="Pixel Islands — уютная игра-шагомер для iPhone. Гуляй в реальном мире и смотри, как остров проходит 8 стадий роста — без давления, без тренерских нотаций, просто рост.",
    rating="4,8 в App Store",
    hero_alt="Пять парящих пиксельных островов из игры Pixel Islands: киберпанк, сакура, луг, Олимп и стимпанк",
    badge1="Загрузите в", badge2="App Store",
    how_h2="Ходьба, которая радует",
    how_p="Никакого коучинга, чувства вины и сложной статистики. Только простой цикл, из-за которого хочется пойти домой длинной дорогой.",
    s1t="1. Просто гуляй", s1p="Pixel Islands читает шаги из Apple Health — телефон в кармане, Apple Watch на запястье, всё считается. Без GPS и расхода батареи.",
    s2t="2. Смотри, как остров растёт", s2p="Каждый шаг питает остров. Голая скала превращается в траву, ручьи, дома — целые маленькие миры за 8 стадий.",
    s3t="3. Собери их все", s3p="Заверши остров и выбери следующую тему. Собери парящую коллекцию маленьких миров — исключительно ходьбой.",
    evo_h2="От голой скалы до живого мира",
    evo_p="Это остров Сакура растёт через 8 стадий — на настоящих шагах.",
    evo_meta="Каждая стадия открывается шагами. Загляни на пару секунд, посмотри, что изменилось, и шагай к следующей.",
    stage_tpl="Стадия {n} из 8", keep_walking="Продолжай идти…",
    labels=["Голая скала в небе","Первые ростки травы","Ручей находит дорогу","Сакура пускает корни","Тропинка и фонарь","Появляется храм","Сакура в полном цвету","Целый собственный мир"],
    feat_h2="Маленькое приложение, много любви",
    f1t="8 стадий роста", f1p="Каждый остров вырастает из голой скалы в живую диораму — прогулка за прогулкой.",
    f2t="Коллекция тем", f2p="Храмы сакуры, скандинавский Асгард, стимпанк-порты, неоновый киберпанк и не только.",
    f3t="Виджет на главном экране", f3p="Остров живёт на главном экране — прогресс виден весь день.",
    f4t="Работает на Apple Health", f4p="Читает только количество шагов из HealthKit. Без GPS, без слежки, бережёт батарею.",
    f5t="Синхронизация iCloud", f5p="Острова надёжно сохранены. Новый iPhone? Коллекция переедет с тобой.",
    f6t="Приватность по умолчанию", f6p="Данные о здоровье никогда не продаются, не используются для рекламы и не передаются.",
    themes_h2="Какой остров вырастишь следующим?", themes_p="Каждый завершённый остров открывает выбор нового мира.",
    theme_names=["Сакура","Асгард","Стимпанк","Киберпанк"],
    faq_h2="Вопросы и ответы",
    faq=[
        ("Как Pixel Islands считает шаги?","Pixel Islands читает количество шагов из Apple Health (HealthKit). Без GPS и работы в фоне — батарея не страдает. Считаются все шаги из Apple Health, включая шаги с Apple Watch."),
        ("Pixel Islands бесплатный?","Да — скачать и играть можно бесплатно. Необязательный Premium открывает дополнительные темы островов и лёгкое ускорение роста."),
        ("Мои данные о здоровье в безопасности?","Pixel Islands читает только количество шагов — больше ничего — и использует его только для роста острова. Данные никогда не продаются, не идут на рекламу и не передаются третьим лицам."),
        ("Что происходит, когда остров завершён?","Когда остров достигает финальной стадии, он попадает в коллекцию, а ты выбираешь новую тему — от цветущих храмов до стимпанк-портов."),
        ("Работает ли с Apple Watch?","Шаги с Apple Watch сохраняются в Apple Health, откуда их и читает Pixel Islands — все прогулки с часами засчитываются."),
        ("Какой iPhone нужен?","Pixel Islands работает на iPhone с iOS 17 и новее, доступен на 20 языках."),
    ],
    cta_h2="Готов вырастить первый остров?", cta_p="Бесплатно в App Store. Следующая прогулка уже идёт в счёт.",
    footer_made="© 2026 Pixel Islands · Сделано с 🏝️ и множеством прогулок",
    foot_support="Поддержка", foot_privacy="Конфиденциальность", foot_store="App Store",
    nav_guides="Гайды",
    guides_h2="Ходьба: разбор по фактам",
    guides_p="Гайды команды Pixel Islands о том, как заставить шаги работать.",
    g1t="7 лучших игр-шагомеров для iPhone", g1d="Уютные строилки, коллекции существ, побеги от зомби — честное сравнение.",
    g2t="Как сделать ходьбу интересной", g2d="12 идей, которые переживут вторую неделю.",
    g3t="Сколько шагов в день нужно?", g3d="Спойлер: 10 000 — рекламная кампания 60-х.",
),
"uk": dict(
    lang="uk", og_locale="uk_UA",
    title="Pixel Islands – гра-крокомір для iPhone | Ходи пішки та вирощуй острів",
    meta="Pixel Islands перетворює щоденні кроки на затишний піксельний острів, що росте у 8 етапів. Гра-крокомір для iPhone з віджетом, Apple Health і колекцією островів. Завантажуйте безкоштовно.",
    og_title="Pixel Islands – Ходи пішки та вирощуй острів",
    og_desc="Затишна гра-крокомір для iPhone. Справжні кроки вирощують піксельний острів у 8 стадій.",
    nav_how="Як це працює", nav_features="Можливості", nav_islands="Острови", nav_faq="FAQ", nav_dl="Завантажити",
    h1="Твої кроки вирощують<br>маленький піксельний острів",
    sub="Pixel Islands — затишна гра-крокомір для iPhone. Гуляй у реальному світі й дивись, як острів проходить 8 стадій росту — без тиску, без тренерських повчань, просто ріст.",
    rating="4,8 в App Store",
    hero_alt="П'ять летючих піксельних островів із гри Pixel Islands: кіберпанк, сакура, лука, Олімп і стімпанк",
    badge1="Завантажте в", badge2="App Store",
    how_h2="Ходьба, що тішить",
    how_p="Жодного коучингу, почуття провини чи складної статистики. Лише простий цикл, через який хочеться повертатися додому довшою дорогою.",
    s1t="1. Просто гуляй", s1p="Pixel Islands зчитує кроки з Apple Health — телефон у кишені, Apple Watch на зап'ясті, все рахується. Без GPS і витрат батареї.",
    s2t="2. Дивись, як острів росте", s2p="Кожен крок живить острів. Гола скеля перетворюється на траву, струмки, будинки — цілі маленькі світи за 8 стадій.",
    s3t="3. Зібери їх усі", s3p="Заверши острів і обери наступну тему. Збери летючу колекцію маленьких світів — самою лише ходьбою.",
    evo_h2="Від голої скелі до живого світу",
    evo_p="Це острів Сакура росте крізь 8 стадій — на справжніх кроках.",
    evo_meta="Кожна стадія відкривається кроками. Зазирни на кілька секунд, подивися, що змінилось, і крокуй до наступної.",
    stage_tpl="Стадія {n} з 8", keep_walking="Продовжуй іти…",
    labels=["Гола скеля в небі","Перші паростки трави","Струмок знаходить шлях","Сакура пускає коріння","Стежка й ліхтар","З'являється храм","Сакура в повному цвіту","Цілий власний світ"],
    feat_h2="Маленький застосунок, багато любові",
    f1t="8 стадій росту", f1p="Кожен острів виростає з голої скелі в живу діораму — прогулянка за прогулянкою.",
    f2t="Колекція тем", f2p="Храми сакури, скандинавський Асґард, стімпанк-порти, неоновий кіберпанк і не тільки.",
    f3t="Віджет на головному екрані", f3p="Острів живе на головному екрані — прогрес видно цілий день.",
    f4t="Працює на Apple Health", f4p="Зчитує лише кількість кроків із HealthKit. Без GPS, без стеження, береже батарею.",
    f5t="Синхронізація iCloud", f5p="Острови надійно збережені. Новий iPhone? Колекція переїде з тобою.",
    f6t="Приватність за замовчуванням", f6p="Дані про здоров'я ніколи не продаються, не використовуються для реклами й не передаються.",
    themes_h2="Який острів виростиш наступним?", themes_p="Кожен завершений острів відкриває вибір нового світу.",
    theme_names=["Сакура","Асґард","Стімпанк","Кіберпанк"],
    faq_h2="Питання й відповіді",
    faq=[
        ("Як Pixel Islands рахує кроки?","Pixel Islands зчитує кількість кроків з Apple Health (HealthKit). Без GPS і роботи у фоні — батарея не страждає. Рахуються всі кроки з Apple Health, зокрема з Apple Watch."),
        ("Pixel Islands безкоштовний?","Так — завантажити й грати можна безкоштовно. Необов'язковий Premium відкриває додаткові теми островів і легке прискорення росту."),
        ("Чи приватні мої дані про здоров'я?","Pixel Islands зчитує лише кількість кроків — більше нічого — і використовує її тільки для росту острова. Дані ніколи не продаються, не йдуть на рекламу й не передаються третім особам."),
        ("Що станеться, коли острів завершено?","Коли острів досягає фінальної стадії, він потрапляє до колекції, а ти обираєш нову тему — від квітучих храмів до стімпанк-портів."),
        ("Чи працює з Apple Watch?","Кроки з Apple Watch зберігаються в Apple Health, звідки їх і зчитує Pixel Islands — усі прогулянки з годинником зараховуються."),
        ("Який iPhone потрібен?","Pixel Islands працює на iPhone з iOS 17 і новіших, доступний 20 мовами."),
    ],
    cta_h2="Готовий виростити перший острів?", cta_p="Безкоштовно в App Store. Наступна прогулянка вже йде в залік.",
    footer_made="© 2026 Pixel Islands · Зроблено з 🏝️ та безліччю прогулянок",
    foot_support="Підтримка", foot_privacy="Конфіденційність", foot_store="App Store",
    nav_guides="Гайди",
    guides_h2="Ходьба: розбір по фактах",
    guides_p="Гайди команди Pixel Islands про те, як змусити кроки працювати.",
    g1t="7 найкращих ігор-крокомірів для iPhone", g1d="Затишні будувалки, колекції істот, втечі від зомбі — чесне порівняння.",
    g2t="Як зробити ходьбу цікавою", g2d="12 ідей, що переживуть другий тиждень.",
    g3t="Скільки кроків на день потрібно?", g3d="Спойлер: 10 000 — рекламна кампанія 60-х.",
),
}

BADGE_SVG = '''<svg viewBox="0 0 200 60" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="%%BADGE1%% %%BADGE2%%">
          <rect width="200" height="60" rx="12" fill="#111"/>
          <g fill="#fff">
            <path d="M36.4 30.6c0-3.6 2.9-5.3 3-5.4-1.6-2.4-4.2-2.7-5.1-2.8-2.2-.2-4.2 1.3-5.3 1.3-1.1 0-2.8-1.2-4.6-1.2-2.4 0-4.6 1.4-5.8 3.5-2.5 4.3-.6 10.6 1.8 14.1 1.2 1.7 2.6 3.6 4.4 3.5 1.8-.1 2.4-1.1 4.6-1.1 2.1 0 2.7 1.1 4.6 1.1 1.9 0 3.1-1.7 4.3-3.4 1.3-2 1.9-3.9 1.9-4-.1-.1-3.8-1.5-3.8-5.6zM33 20.1c1-1.2 1.6-2.8 1.5-4.5-1.4.1-3.1 1-4.1 2.1-.9 1-1.7 2.7-1.5 4.3 1.6.1 3.1-.7 4.1-1.9z"/>
            <text x="52" y="24" font-family="-apple-system, Helvetica, Arial, sans-serif" font-size="11" fill="#fff">%%BADGE1%%</text>
            <text x="52" y="43" font-family="-apple-system, Helvetica, Arial, sans-serif" font-size="17" font-weight="700" fill="#fff">%%BADGE2%%</text>
          </g>
        </svg>'''

TEMPLATE = '''<!DOCTYPE html>
<html lang="%%LANG%%">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>%%TITLE%%</title>
<meta name="description" content="%%META%%">
<link rel="canonical" href="%%CANONICAL%%">
<meta name="apple-itunes-app" content="app-id=6760819710">
%%HREFLANG%%
<meta property="og:type" content="website">
<meta property="og:site_name" content="Pixel Islands">
<meta property="og:locale" content="%%OG_LOCALE%%">
<meta property="og:title" content="%%OG_TITLE%%">
<meta property="og:description" content="%%OG_DESC%%">
<meta property="og:url" content="%%CANONICAL%%">
<meta property="og:image" content="https://pixelislands.app/assets/hero.jpg">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="%%OG_TITLE%%">
<meta name="twitter:description" content="%%OG_DESC%%">
<meta name="twitter:image" content="https://pixelislands.app/assets/hero.jpg">
<link rel="icon" type="image/png" href="../assets/appicon.png">
<link rel="apple-touch-icon" href="../assets/appicon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Nunito:wght@600;700;800;900&display=swap" rel="stylesheet">
<link rel="stylesheet" href="../styles.css">
<script type="application/ld+json">%%APP_JSONLD%%</script>
<script type="application/ld+json">%%FAQ_JSONLD%%</script>
</head>
<body>

<header class="site">
  <div class="wrap nav">
    <a class="brand" href="./">
      <img src="../assets/appicon.png" alt="Pixel Islands" width="36" height="36">
      Pixel Islands
    </a>
    <nav>
      <a href="#how">%%NAV_HOW%%</a>
      <a href="#features">%%NAV_FEATURES%%</a>
      <a href="#themes">%%NAV_ISLANDS%%</a>
      <a href="#faq">FAQ</a>
      <a href="#guides">%%NAV_GUIDES%%</a>
      <a class="cta-mini" href="%%APP_URL%%">%%NAV_DL%%</a>
    </nav>
  </div>
</header>

<main>
  <div class="wrap hero">
    <h1>%%H1%%</h1>
    <p class="sub">%%SUB%%</p>
    <div class="store-row">
      <a class="appstore-badge" href="%%APP_URL%%" aria-label="%%BADGE1%% %%BADGE2%%">
        %%BADGE_SVG%%
      </a>
      <div class="rating"><span class="stars">★★★★★</span> %%RATING%%</div>
    </div>
    <div class="hero-img">
      <img src="../assets/hero.jpg" alt="%%HERO_ALT%%" width="1600" height="900" fetchpriority="high">
    </div>
  </div>

  <section id="how">
    <div class="wrap">
      <div class="section-head">
        <h2>%%HOW_H2%%</h2>
        <p>%%HOW_P%%</p>
      </div>
      <div class="steps">
        <div class="step-card"><div class="emoji">🚶</div><h3>%%S1T%%</h3><p>%%S1P%%</p></div>
        <div class="step-card"><div class="emoji">🏝️</div><h3>%%S2T%%</h3><p>%%S2P%%</p></div>
        <div class="step-card"><div class="emoji">✨</div><h3>%%S3T%%</h3><p>%%S3P%%</p></div>
      </div>
    </div>
  </section>

  <section id="evolution">
    <div class="wrap">
      <div class="section-head">
        <h2>%%EVO_H2%%</h2>
        <p>%%EVO_P%%</p>
      </div>
      <div class="evolution">
        <div class="island-frame" id="islandFrame">
          <img src="../assets/stage1.png" alt="1/8" class="active" width="480" height="480">
          <img src="../assets/stage2.png" alt="2/8" width="480" height="480" loading="lazy">
          <img src="../assets/stage3.png" alt="3/8" width="480" height="480" loading="lazy">
          <img src="../assets/stage4.png" alt="4/8" width="480" height="480" loading="lazy">
          <img src="../assets/stage5.png" alt="5/8" width="480" height="480" loading="lazy">
          <img src="../assets/stage6.png" alt="6/8" width="480" height="480" loading="lazy">
          <img src="../assets/stage7.png" alt="7/8" width="480" height="480" loading="lazy">
          <img src="../assets/stage8.png" alt="8/8" width="480" height="480" loading="lazy">
        </div>
        <div class="meta">
          <h3 id="stageTitle">%%STAGE1_TITLE%%</h3>
          <p>%%EVO_META%%</p>
          <div class="progress-track"><div class="progress-fill" id="progressFill" style="width:12.5%"></div></div>
          <div class="stage-label" id="stageSteps">%%KEEP_WALKING%%</div>
        </div>
      </div>
    </div>
  </section>

  <section id="features">
    <div class="wrap">
      <div class="section-head"><h2>%%FEAT_H2%%</h2></div>
      <div class="features">
        <div class="feature"><div class="emoji">🌱</div><h3>%%F1T%%</h3><p>%%F1P%%</p></div>
        <div class="feature"><div class="emoji">🗺️</div><h3>%%F2T%%</h3><p>%%F2P%%</p></div>
        <div class="feature"><div class="emoji">📱</div><h3>%%F3T%%</h3><p>%%F3P%%</p></div>
        <div class="feature"><div class="emoji">❤️</div><h3>%%F4T%%</h3><p>%%F4P%%</p></div>
        <div class="feature"><div class="emoji">☁️</div><h3>%%F5T%%</h3><p>%%F5P%%</p></div>
        <div class="feature"><div class="emoji">🔒</div><h3>%%F6T%%</h3><p>%%F6P%%</p></div>
      </div>
    </div>
  </section>

  <section id="themes">
    <div class="wrap">
      <div class="section-head">
        <h2>%%THEMES_H2%%</h2>
        <p>%%THEMES_P%%</p>
      </div>
      <div class="themes">
        <div class="theme-card"><img src="../assets/theme-sakura.png" alt="%%TN1%%" loading="lazy" width="480" height="480"><span>%%TN1%%</span></div>
        <div class="theme-card"><img src="../assets/theme-asgard.png" alt="%%TN2%%" loading="lazy" width="480" height="480"><span>%%TN2%%</span></div>
        <div class="theme-card"><img src="../assets/theme-steampunk.png" alt="%%TN3%%" loading="lazy" width="480" height="480"><span>%%TN3%%</span></div>
        <div class="theme-card"><img src="../assets/theme-cyberpunk.png" alt="%%TN4%%" loading="lazy" width="480" height="480"><span>%%TN4%%</span></div>
      </div>
    </div>
  </section>

  <section id="faq">
    <div class="wrap">
      <div class="section-head"><h2>%%FAQ_H2%%</h2></div>
      <div class="faq">
%%FAQ_HTML%%
      </div>
    </div>
  </section>

  <section id="guides">
    <div class="wrap">
      <div class="section-head">
        <h2>%%GUIDES_H2%%</h2>
        <p>%%GUIDES_P%%</p>
      </div>
      <div class="guide-cards">
        <a href="guides/best-walking-games-iphone/">%%G1T%%<small>%%G1D%%</small></a>
        <a href="guides/how-to-make-walking-fun/">%%G2T%%<small>%%G2D%%</small></a>
        <a href="guides/how-many-steps-a-day/">%%G3T%%<small>%%G3D%%</small></a>
      </div>
    </div>
  </section>

  <div class="cta-band">
    <h2>%%CTA_H2%%</h2>
    <p>%%CTA_P%%</p>
    <a class="appstore-badge" href="%%APP_URL%%" aria-label="%%BADGE1%% %%BADGE2%%">
      %%BADGE_SVG%%
    </a>
  </div>
</main>

<footer class="site">
  <div class="wrap cols">
    <div>%%FOOTER_MADE%%</div>
    <div>
      <a href="%%APP_URL%%">%%FOOT_STORE%%</a>
      <a href="../support/">%%FOOT_SUPPORT%%</a>
      <a href="../privacy/">%%FOOT_PRIVACY%%</a>
    </div>
  </div>
  <div class="wrap" style="margin-top:16px; font-size:0.88rem">🌐 %%LANGROW%%</div>
</footer>

<script>
(function () {
  var frame = document.getElementById('islandFrame');
  var imgs = frame.querySelectorAll('img');
  var title = document.getElementById('stageTitle');
  var fill = document.getElementById('progressFill');
  var label = document.getElementById('stageSteps');
  var tpl = %%STAGE_TPL_JS%%;
  var labels = %%LABELS_JS%%;
  var i = 0;
  setInterval(function () {
    imgs[i].classList.remove('active');
    i = (i + 1) % imgs.length;
    imgs[i].classList.add('active');
    title.textContent = tpl.replace('{n}', i + 1);
    fill.style.width = ((i + 1) / 8 * 100) + '%';
    label.textContent = labels[i];
  }, 2200);
})();
</script>

</body>
</html>
'''


def hreflang_block():
    lines = [f'<link rel="alternate" hreflang="{code}" href="{SITE}{path}">' for code, path in HREFLANGS]
    lines.append(f'<link rel="alternate" hreflang="x-default" href="{SITE}/">')
    return "\n".join(lines)


def langrow(current_path):
    parts = []
    for path, name in LANG_NAMES:
        rel = ".." + path if path != "/" else "../"
        if path == current_path:
            parts.append(f'<strong style="color:#fff">{name}</strong>')
        else:
            parts.append(f'<a href="{rel}">{name}</a>')
    return " · ".join(parts)


def build(locale_dir, t):
    path = f"/{locale_dir}/"
    canonical = SITE + path
    app_jsonld = json.dumps({
        "@context": "https://schema.org",
        "@type": "SoftwareApplication",
        "name": "Pixel Islands: Step Track Game",
        "operatingSystem": "iOS",
        "applicationCategory": "HealthApplication",
        "inLanguage": t["lang"],
        "description": t["meta"],
        "image": "https://pixelislands.app/assets/appicon.png",
        "url": canonical,
        "installUrl": APP_URL,
        "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"},
        "aggregateRating": {"@type": "AggregateRating", "ratingValue": "4.8", "ratingCount": "21"},
        "author": {"@type": "Person", "name": "Kyrylo Lozovyi"},
    }, ensure_ascii=False)
    faq_jsonld = json.dumps({
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "inLanguage": t["lang"],
        "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}
            for q, a in t["faq"]
        ],
    }, ensure_ascii=False)
    faq_html = "\n".join(
        f'        <details>\n          <summary>{q}</summary>\n          <p>{a}</p>\n        </details>'
        for q, a in t["faq"]
    )
    badge = BADGE_SVG.replace("%%BADGE1%%", t["badge1"]).replace("%%BADGE2%%", t["badge2"])
    html = TEMPLATE
    repl = {
        "%%LANG%%": t["lang"], "%%TITLE%%": t["title"], "%%META%%": t["meta"],
        "%%CANONICAL%%": canonical, "%%HREFLANG%%": hreflang_block(),
        "%%OG_LOCALE%%": t["og_locale"], "%%OG_TITLE%%": t["og_title"], "%%OG_DESC%%": t["og_desc"],
        "%%APP_JSONLD%%": app_jsonld, "%%FAQ_JSONLD%%": faq_jsonld,
        "%%NAV_HOW%%": t["nav_how"], "%%NAV_FEATURES%%": t["nav_features"],
        "%%NAV_ISLANDS%%": t["nav_islands"], "%%NAV_DL%%": t["nav_dl"],
        "%%APP_URL%%": APP_URL, "%%H1%%": t["h1"], "%%SUB%%": t["sub"], "%%RATING%%": t["rating"],
        "%%HERO_ALT%%": t["hero_alt"], "%%BADGE_SVG%%": badge,
        "%%BADGE1%%": t["badge1"], "%%BADGE2%%": t["badge2"],
        "%%HOW_H2%%": t["how_h2"], "%%HOW_P%%": t["how_p"],
        "%%S1T%%": t["s1t"], "%%S1P%%": t["s1p"], "%%S2T%%": t["s2t"], "%%S2P%%": t["s2p"],
        "%%S3T%%": t["s3t"], "%%S3P%%": t["s3p"],
        "%%EVO_H2%%": t["evo_h2"], "%%EVO_P%%": t["evo_p"], "%%EVO_META%%": t["evo_meta"],
        "%%STAGE1_TITLE%%": t["stage_tpl"].replace("{n}", "1"),
        "%%KEEP_WALKING%%": t["keep_walking"],
        "%%FEAT_H2%%": t["feat_h2"],
        "%%F1T%%": t["f1t"], "%%F1P%%": t["f1p"], "%%F2T%%": t["f2t"], "%%F2P%%": t["f2p"],
        "%%F3T%%": t["f3t"], "%%F3P%%": t["f3p"], "%%F4T%%": t["f4t"], "%%F4P%%": t["f4p"],
        "%%F5T%%": t["f5t"], "%%F5P%%": t["f5p"], "%%F6T%%": t["f6t"], "%%F6P%%": t["f6p"],
        "%%NAV_GUIDES%%": t["nav_guides"],
        "%%GUIDES_H2%%": t["guides_h2"], "%%GUIDES_P%%": t["guides_p"],
        "%%G1T%%": t["g1t"], "%%G1D%%": t["g1d"], "%%G2T%%": t["g2t"], "%%G2D%%": t["g2d"],
        "%%G3T%%": t["g3t"], "%%G3D%%": t["g3d"],
        "%%THEMES_H2%%": t["themes_h2"], "%%THEMES_P%%": t["themes_p"],
        "%%TN1%%": t["theme_names"][0], "%%TN2%%": t["theme_names"][1],
        "%%TN3%%": t["theme_names"][2], "%%TN4%%": t["theme_names"][3],
        "%%FAQ_H2%%": t["faq_h2"], "%%FAQ_HTML%%": faq_html,
        "%%CTA_H2%%": t["cta_h2"], "%%CTA_P%%": t["cta_p"],
        "%%FOOTER_MADE%%": t["footer_made"], "%%FOOT_STORE%%": t["foot_store"],
        "%%FOOT_SUPPORT%%": t["foot_support"], "%%FOOT_PRIVACY%%": t["foot_privacy"],
        "%%LANGROW%%": langrow(path),
        "%%STAGE_TPL_JS%%": json.dumps(t["stage_tpl"], ensure_ascii=False),
        "%%LABELS_JS%%": json.dumps(t["labels"], ensure_ascii=False),
    }
    for k, v in repl.items():
        html = html.replace(k, v)
    out = pathlib.Path(__file__).parent / locale_dir / "index.html"
    out.parent.mkdir(exist_ok=True)
    out.write_text(html, encoding="utf-8")
    leftover = [tok for tok in ("%%",) if tok in html]
    return out, leftover


if __name__ == "__main__":
    for locale_dir, strings in L.items():
        out, leftover = build(locale_dir, strings)
        status = "OK" if not leftover else "UNRESOLVED TOKENS!"
        print(f"{out}: {status}")
