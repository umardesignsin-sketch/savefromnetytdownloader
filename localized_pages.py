"""Curated translations of working downloader pages.

Only a slug with complete page copy is published. Adding a locale to the
registry is deliberately separate from adding a language to the sitemap.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class LocalizedTool:
    heading: str
    intro: str
    how: str
    formats: str
    limits: str
    question: str
    answer: str


@dataclass(frozen=True)
class LocalizedGuide:
    """What the English tool page explains, written for one language.

    Every claim follows the downloader: link shapes come from
    extractors/detect.py, formats and limits from extractors/service.py and
    the per-tool filter in app.py.
    """
    facts: tuple     # (label, value) shown before the steps
    steps: tuple     # how to use the tool, in order
    links: tuple     # (link shape with ID placeholder, what it identifies)
    sections: tuple  # (heading, (paragraph, ...)) for the format guide
    faq: tuple       # (question, answer) after the tool's main question
    see_also: tuple  # (published slug, label) linked in context


LANGUAGE_UI = {
    "es": {
        "name": "Español",
        "home_title": "Descargador y convertidor de vídeos | SaveFromNet",
        "home_heading": "Descarga y convierte medios públicos",
        "home_intro": "Pega el enlace directo de un vídeo, Reel, Short, foto o audio que tengas permiso para guardar. Comprueba los formatos disponibles antes de preparar el archivo.",
        "nav_tools": "Herramientas",
        "nav_how": "Cómo funciona",
        "nav_rights": "Uso responsable",
        "url_label": "Enlace público del contenido",
        "url_placeholder": "Pega aquí un enlace público",
        "paste": "Pegar",
        "download": "Analizar enlace",
        "rights": "Descarga solo contenido propio o para el que tengas permiso. No accedemos a publicaciones privadas ni evitamos restricciones.",
        "formats_title": "Opciones reales para cada enlace",
        "formats_home": "El analizador identifica la plataforma y muestra únicamente los archivos y calidades que puede preparar para ese contenido. Una resolución ausente no se puede crear cambiando la dirección.",
        "how_title": "Cómo usar el descargador",
        "how_home": "Copia el enlace de una publicación individual, pégalo arriba y analiza el resultado. Elige un formato que aparezca en la lista; la preparación se realiza en segundo plano y el archivo temporal se guarda desde tu navegador.",
        "limits_title": "Cuando el contenido no está disponible",
        "limits_home": "Las publicaciones eliminadas, privadas, en directo, limitadas por región o que exigen iniciar sesión pueden fallar. SaveFromNet no evita DRM, muros de pago ni controles de acceso.",
        "platforms_title": "Plataformas y herramientas",
        "related_title": "Herramientas relacionadas",
        "faq_title": "Preguntas frecuentes",
        "faq_home_question": "¿Puedo elegir cualquier calidad?",
        "faq_home_answer": "No. Cada fuente devuelve sus propios formatos. Solo mostramos las opciones que el servicio puede preparar para ese enlace.",
        "faq_availability_question": "¿Por qué no aparece el archivo que busco?",
        "faq_availability_answer": "Puede faltar en la fuente o requerir acceso privado, inicio de sesión o una región concreta. Prueba un enlace directo a una publicación pública.",
        "history_title": "Descargas recientes de este navegador",
        "history_view": "Ver historial",
        "facts_title": "Antes de descargar",
        "on_page": "En esta página",
        "steps_title": "Paso a paso",
        "links_title": "Enlaces compatibles",
        "links_intro": "Formas de enlace que acepta esta página; ID es el identificador que aparece en tu enlace.",
        "guide_title": "Guía de formatos y límites",
        "next_title": "Según lo que necesites",
        "footer": "Descarga únicamente contenido que tengas derecho a usar.",
        "english": "English",
        "french": "Français",
    },
    "fr": {
        "name": "Français",
        "home_title": "Téléchargeur et convertisseur vidéo | SaveFromNet",
        "home_heading": "Téléchargez et convertissez des médias publics",
        "home_intro": "Collez le lien direct d'une vidéo, d'un Reel, d'un Short, d'une photo ou d'un audio que vous avez le droit d'enregistrer. Vérifiez les formats disponibles avant de préparer le fichier.",
        "nav_tools": "Outils",
        "nav_how": "Mode d'emploi",
        "nav_rights": "Utilisation responsable",
        "url_label": "Lien public du contenu",
        "url_placeholder": "Collez un lien public ici",
        "paste": "Coller",
        "download": "Analyser le lien",
        "rights": "Téléchargez uniquement vos contenus ou ceux pour lesquels vous avez une autorisation. Nous n'accédons pas aux publications privées et ne contournons aucune restriction.",
        "formats_title": "Les formats réellement disponibles",
        "formats_home": "L'analyseur reconnaît la plateforme et n'affiche que les fichiers et qualités qu'il peut préparer pour ce contenu. Modifier l'URL ne crée pas une résolution absente.",
        "how_title": "Comment utiliser le téléchargeur",
        "how_home": "Copiez le lien d'une publication précise, collez-le ci-dessus et analysez le résultat. Choisissez un format proposé : la préparation se fait en arrière-plan et le fichier temporaire s'enregistre depuis votre navigateur.",
        "limits_title": "Quand un contenu reste inaccessible",
        "limits_home": "Les publications supprimées, privées, en direct, limitées à une région ou nécessitant une connexion peuvent échouer. SaveFromNet ne contourne ni DRM, ni paywalls, ni contrôle d'accès.",
        "platforms_title": "Plateformes et outils",
        "related_title": "Outils associés",
        "faq_title": "Questions fréquentes",
        "faq_home_question": "Puis-je choisir n'importe quelle qualité ?",
        "faq_home_answer": "Non. Chaque source propose ses propres formats. Seules les options que le service peut préparer pour ce lien sont affichées.",
        "faq_availability_question": "Pourquoi le fichier voulu n'apparaît-il pas ?",
        "faq_availability_answer": "Il peut manquer à la source ou nécessiter un accès privé, une connexion ou une région précise. Essayez le lien direct d'une publication publique.",
        "history_title": "Téléchargements récents de ce navigateur",
        "history_view": "Voir l'historique",
        "facts_title": "Avant de télécharger",
        "on_page": "Sur cette page",
        "steps_title": "Étape par étape",
        "links_title": "Liens acceptés",
        "links_intro": "Formes de lien acceptées par cette page ; ID désigne l'identifiant qui figure dans votre lien.",
        "guide_title": "Guide des formats et des limites",
        "next_title": "Selon votre besoin",
        "footer": "Téléchargez uniquement les contenus que vous avez le droit d'utiliser.",
        "english": "English",
        "spanish": "Español",
    },
}


LOCALIZED_TOOLS = {
    "es": {
        "universal-video-downloader": LocalizedTool(
            "Descargador y convertidor universal",
            "Un solo campo para enlaces públicos de ocho plataformas compatibles.",
            "Pega el enlace de una publicación concreta. El detector comprueba el dominio y la ruta y envía ese contenido al extractor correspondiente; una página de búsqueda no identifica un archivo.",
            "El resultado puede contener vídeo, audio o imágenes según la fuente. Elige una opción que aparezca tras el análisis, nunca una calidad supuesta.",
            "Cada plataforma impone sus propios límites. Un enlace privado, eliminado o que requiera iniciar sesión no se puede procesar.",
            "¿Admite cualquier sitio web?",
            "No. Se aceptan enlaces públicos compatibles de YouTube, Instagram, TikTok, Facebook, Pinterest, Reddit, Threads y Dailymotion.",
        ),
        "youtube-downloader": LocalizedTool(
            "Descargador y convertidor de YouTube",
            "Compara vídeo y audio de un vídeo o Short público de YouTube.",
            "Usa un enlace directo youtube.com/watch, youtube.com/shorts o youtu.be de un solo contenido. Tras analizarlo podrás comparar las opciones de vídeo y sonido disponibles.",
            "Pueden aparecer MP4, WebM, audio original o una conversión MP3 cuando exista una pista sonora accesible. La lista depende de esa publicación.",
            "Las listas de reproducción, los alquileres, los directos y los vídeos privados no forman parte de este flujo público.",
            "¿El convertidor garantiza 4K o MP3?",
            "No. Solo ofrece las combinaciones que el extractor encuentra y puede preparar dentro del límite de tamaño.",
        ),
        "youtube-video-downloader": LocalizedTool(
            "Descargador de vídeos de YouTube",
            "Guarda un vídeo público con una resolución que realmente esté disponible.",
            "Copia el enlace de la página watch?v= o su versión youtu.be. Analiza ese único vídeo y consulta el tipo de archivo, la altura y la estimación de tamaño antes de elegir.",
            "Una opción de alta resolución puede necesitar unir vídeo y audio compatibles. MP4 y WebM no son intercambiables solo por cambiar la extensión.",
            "Si el vídeo está eliminado, restringido o bloqueado para accesos anónimos, no aparecerá ninguna descarga.",
            "¿Todos los vídeos ofrecen 1080p?",
            "No. La resolución depende de las pistas accesibles para el vídeo concreto y del límite de procesamiento.",
        ),
        "youtube-shorts-downloader": LocalizedTool(
            "Descargador de YouTube Shorts",
            "Analiza un Short público y guarda una opción de vídeo disponible.",
            "Abre el Short individual y copia su URL youtube.com/shorts/ con el identificador. Un feed de Shorts o un canal no señala un archivo específico.",
            "Los vídeos verticales pueden exponer diferentes tamaños y contenedores. El resultado muestra únicamente las variantes devueltas para ese Short.",
            "Un Short privado, eliminado, en directo o bloqueado por YouTube no se puede obtener mediante un cambio de URL.",
            "¿Puedo guardar solo el sonido?",
            "Si existe audio accesible, abre el convertidor de YouTube a MP3 de la sección de herramientas relacionadas.",
        ),
        "youtube-to-mp3": LocalizedTool(
            "Convertidor de YouTube a MP3",
            "Convierte a MP3 el audio accesible de un vídeo o Short público.",
            "Pega un enlace directo de YouTube y espera al análisis. Selecciona la opción MP3 que aparezca; el servidor extrae el audio y lo convierte antes de crear un archivo temporal.",
            "MP3 es una conversión del sonido original, no un archivo que YouTube entregue necesariamente. Una tasa de bits mayor no restaura calidad perdida.",
            "Los vídeos sin audio, las listas, las publicaciones privadas y los contenidos que exigen iniciar sesión no producen un MP3 aquí.",
            "¿Siempre está disponible MP3 a 320 kbps?",
            "No. Elige solo las opciones mostradas para ese enlace; no prometemos una tasa de bits fija.",
        ),
        "youtube-to-mp4": LocalizedTool(
            "Convertidor de YouTube a MP4",
            "Encuentra las resoluciones MP4 que se pueden preparar para un vídeo público.",
            "Pega el enlace de un vídeo o Short. El resultado se centra en las opciones MP4 devueltas para ese contenido, en vez de mostrar una lista fija de resoluciones.",
            "Algunos vídeos separan imagen y sonido; el servidor solo ofrece un MP4 terminado cuando puede combinar pistas compatibles.",
            "Si la fuente devuelve únicamente WebM o no ofrece cierta altura, no se puede forzar MP4 cambiando el nombre del archivo.",
            "¿Cambiar WebM a .mp4 convierte el vídeo?",
            "No. Cambiar la extensión no modifica el códec ni crea una opción MP4 que no exista.",
        ),
        "instagram-downloader": LocalizedTool(
            "Descargador de Instagram",
            "Analiza fotos y vídeos de publicaciones o Reels públicos.",
            "Copia la URL directa instagram.com/p/ o instagram.com/reel/ de una publicación. El resultado puede contener una foto, un vídeo o varios elementos de un carrusel.",
            "Las imágenes conservan el formato expuesto por la fuente; los vídeos aparecen solo si la publicación ofrece un archivo accesible.",
            "Instagram puede solicitar una cuenta incluso en ciertas publicaciones visibles como públicas. No accedemos a perfiles privados.",
            "¿Se puede pegar el enlace de un perfil?",
            "Esta página se centra en publicaciones individuales. Un perfil puede requerir inicio de sesión y no equivale a un solo archivo.",
        ),
        "instagram-reels-downloader": LocalizedTool(
            "Descargador de Reels de Instagram",
            "Consulta si un Reel público ofrece un vídeo accesible.",
            "Usa la URL directa instagram.com/reel/ del Reel que puedes guardar. Analízala para ver si el extractor devuelve un archivo de vídeo para esa publicación.",
            "Normalmente se muestra la opción MP4 de origen cuando está disponible; no se inventan alturas adicionales.",
            "Los Reels eliminados, privados o sujetos a inicio de sesión pueden no devolver ningún formato.",
            "¿Sirve un enlace al feed de Reels?",
            "No. Copia el enlace de un Reel individual, no el de una página de exploración o un perfil.",
        ),
        "instagram-photo-downloader": LocalizedTool(
            "Descargador de fotos de Instagram",
            "Encuentra las imágenes originales de una publicación pública.",
            "Pega un enlace instagram.com/p/ que contenga fotografías. Si es un carrusel, revisa cada elemento accesible que devuelve el análisis.",
            "Una imagen puede aparecer como JPEG, PNG o WebP según lo que exponga Instagram. Un vídeo sin foto no ofrece una descarga fotográfica.",
            "Las publicaciones privadas o que exigen una sesión activa no se recuperan aquí.",
            "¿Convierte las fotos a otra resolución?",
            "Esta herramienta muestra los archivos expuestos por la fuente. Para convertir una imagen propia después, usa las herramientas de imagen del sitio.",
        ),
        "tiktok-downloader": LocalizedTool(
            "Descargador de TikTok",
            "Analiza un vídeo o publicación fotográfica pública de TikTok.",
            "Copia el enlace de un vídeo /@usuario/video/ID, una publicación /photo/ID o un enlace corto vm.tiktok.com que apunte a una pieza concreta.",
            "El analizador muestra los vídeos, fotos o pistas de audio que TikTok permita consultar para ese enlace. Las calidades no se fijan por adelantado.",
            "TikTok puede bloquear peticiones de centros de datos o retirar una publicación; no se evita el inicio de sesión.",
            "¿Se puede descargar el sonido de un vídeo?",
            "Si existe audio accesible, abre el convertidor de TikTok a MP3 para ver la opción correspondiente.",
        ),
        "tiktok-to-mp3": LocalizedTool(
            "Convertidor de TikTok a MP3",
            "Prepara un MP3 a partir del sonido accesible de un vídeo público.",
            "Pega la URL directa /@usuario/video/ID o un enlace corto al mismo vídeo. Elige MP3 solo cuando el análisis encuentre una pista sonora.",
            "El servidor convierte la pista disponible; un clip silencioso no puede convertirse en música o voz.",
            "Una historia caducada, un vídeo eliminado o un enlace bloqueado por TikTok no tendrá audio descargable.",
            "¿MP3 mejora el sonido del vídeo?",
            "No. La conversión cambia el formato, pero no recupera detalle que falte en el audio original.",
        ),
        "facebook-video-downloader": LocalizedTool(
            "Descargador de vídeos de Facebook",
            "Busca formatos de un vídeo o Reel público de Facebook.",
            "Pega una URL facebook.com/watch?v=, /videos/, /reel/ o fb.watch que identifique una publicación individual.",
            "La lista refleja los archivos que la fuente devuelve para ese vídeo; una resolución que no aparece no se puede solicitar manualmente.",
            "Los vídeos limitados a amigos, las páginas que exigen inicio de sesión y las publicaciones eliminadas quedan fuera.",
            "¿Puedo usar un enlace a un grupo privado?",
            "No. El servicio solo consulta contenido públicamente accesible sin iniciar sesión.",
        ),
        "pinterest-video-downloader": LocalizedTool(
            "Descargador de vídeos, imágenes y GIF de Pinterest",
            "Comprueba el archivo original de un Pin público.",
            "Copia la URL pinterest.com/pin/ID o su enlace corto pin.it. El contenido puede ser una imagen, un GIF o un vídeo.",
            "Se ofrece el elemento que el Pin expone realmente. Un Pin que remite a un sitio externo puede no alojar ningún archivo descargable en Pinterest.",
            "Los tableros completos y los Pins privados no identifican un único archivo público.",
            "¿Todos los Pins contienen vídeo?",
            "No. Muchos contienen solo una imagen o enlazan a una página externa; el resultado indica el tipo real.",
        ),
        "reddit-video-downloader": LocalizedTool(
            "Descargador de vídeos de Reddit",
            "Guarda un vídeo de una publicación pública, con sonido cuando exista.",
            "Usa el enlace permanente reddit.com/r/comunidad/comments/ID/ o un enlace corto redd.it/ID de una sola publicación.",
            "Reddit puede separar imagen y sonido. Cuando ambas pistas son accesibles y compatibles, el servidor las une en el archivo final.",
            "Los posts eliminados, privados, en cuarentena o marcados para adultos pueden impedir el acceso anónimo.",
            "¿Todos los vídeos de Reddit tienen sonido?",
            "No. Si la fuente no ofrece una pista sonora utilizable, el servicio no puede inventarla.",
        ),
        "threads-video-downloader": LocalizedTool(
            "Descargador de vídeos de Threads",
            "Comprueba si una publicación pública de Threads expone un vídeo.",
            "Pega el enlace directo threads.com/@usuario/post/ID. El analizador revisa los metadatos públicos de esa publicación individual.",
            "Si Threads publica un archivo MP4 accesible, se ofrece esa fuente. Es posible que no haya duración, tamaño o varias resoluciones.",
            "Los posts privados, sin metadatos de vídeo o que requieran iniciar sesión no dan lugar a un archivo.",
            "¿Por qué solo aparece una calidad?",
            "Threads puede exponer un único vídeo público; el servicio no crea variantes que la fuente no facilita.",
        ),
        "dailymotion-video-downloader": LocalizedTool(
            "Descargador de vídeos de Dailymotion",
            "Elige una calidad devuelta para un vídeo público concreto.",
            "Pega un enlace dailymotion.com/video/ID o dai.ly/ID. Analiza la publicación antes de escoger entre las alturas disponibles.",
            "El resultado puede incluir MP4 o WebM según las pistas accesibles. El tamaño estimado solo aparece cuando hay datos suficientes.",
            "Los canales, listas, vídeos privados y contenidos bloqueados por región no son enlaces a un archivo público utilizable.",
            "¿Puedo forzar una calidad superior?",
            "No. Solo se ofrecen las alturas devueltas para ese vídeo y compatibles con el límite de procesamiento.",
        ),
    },
    "fr": {
        "universal-video-downloader": LocalizedTool(
            "Téléchargeur et convertisseur universel",
            "Un seul champ pour les liens publics de huit plateformes compatibles.",
            "Collez le lien d'une publication précise. Le détecteur vérifie le domaine et le chemin avant de transmettre ce contenu à l'extracteur adapté ; une page de recherche ne désigne pas un fichier.",
            "Le résultat peut contenir de la vidéo, de l'audio ou des images selon la source. Choisissez une option affichée après l'analyse, jamais une qualité supposée.",
            "Chaque plateforme a ses propres limites. Un lien privé, supprimé ou nécessitant une connexion ne peut pas être traité.",
            "Tous les sites web sont-ils acceptés ?",
            "Non. L'outil accepte les liens publics compatibles de YouTube, Instagram, TikTok, Facebook, Pinterest, Reddit, Threads et Dailymotion.",
        ),
        "youtube-downloader": LocalizedTool(
            "Téléchargeur et convertisseur YouTube",
            "Comparez la vidéo et l'audio d'une vidéo ou d'un Short YouTube public.",
            "Utilisez le lien direct youtube.com/watch, youtube.com/shorts ou youtu.be d'un seul contenu. L'analyse permet ensuite de comparer les choix de vidéo et de son disponibles.",
            "MP4, WebM, audio d'origine ou conversion MP3 peuvent apparaître lorsqu'une piste sonore accessible existe. La liste dépend de cette publication.",
            "Les playlists, locations, directs et vidéos privées ne font pas partie de ce parcours public.",
            "Le convertisseur garantit-il la 4K ou le MP3 ?",
            "Non. Il propose seulement les combinaisons trouvées par l'extracteur et préparables dans la limite de taille.",
        ),
        "youtube-video-downloader": LocalizedTool(
            "Téléchargeur de vidéos YouTube",
            "Enregistrez une vidéo publique dans une résolution réellement disponible.",
            "Copiez le lien watch?v= ou sa version youtu.be. Analysez cette seule vidéo et vérifiez le type de fichier, la hauteur et l'estimation de taille avant de choisir.",
            "Une haute résolution peut nécessiter la fusion de pistes vidéo et audio compatibles. MP4 et WebM ne deviennent pas interchangeables en renommant le fichier.",
            "Une vidéo supprimée, restreinte ou bloquée pour les visiteurs anonymes ne donnera aucun fichier.",
            "Toutes les vidéos proposent-elles le 1080p ?",
            "Non. La résolution dépend des pistes accessibles pour cette vidéo et de la limite de traitement.",
        ),
        "youtube-shorts-downloader": LocalizedTool(
            "Téléchargeur de YouTube Shorts",
            "Analysez un Short public et enregistrez une vidéo proposée.",
            "Ouvrez le Short précis et copiez son URL youtube.com/shorts/ avec son identifiant. Un fil de Shorts ou une chaîne ne désigne pas un fichier unique.",
            "Les vidéos verticales peuvent avoir plusieurs tailles et conteneurs. Le résultat ne montre que les variantes renvoyées pour ce Short.",
            "Un Short privé, supprimé, en direct ou bloqué par YouTube ne devient pas accessible en modifiant l'URL.",
            "Puis-je enregistrer uniquement le son ?",
            "Si l'audio est accessible, ouvrez le convertisseur YouTube vers MP3 dans les outils associés.",
        ),
        "youtube-to-mp3": LocalizedTool(
            "Convertisseur YouTube en MP3",
            "Convertissez en MP3 l'audio accessible d'une vidéo ou d'un Short public.",
            "Collez un lien YouTube direct et attendez l'analyse. Sélectionnez l'option MP3 proposée : le serveur extrait puis convertit le son avant de créer un fichier temporaire.",
            "Le MP3 est une conversion de la piste d'origine, pas nécessairement un fichier fourni par YouTube. Un débit plus élevé ne restaure pas les détails perdus.",
            "Les vidéos muettes, playlists, publications privées ou nécessitant une connexion ne produisent pas de MP3 ici.",
            "Le MP3 à 320 kb/s est-il toujours proposé ?",
            "Non. Choisissez uniquement les options affichées pour ce lien ; aucun débit fixe n'est promis.",
        ),
        "youtube-to-mp4": LocalizedTool(
            "Convertisseur YouTube en MP4",
            "Trouvez les résolutions MP4 préparables pour une vidéo publique.",
            "Collez le lien d'une vidéo ou d'un Short. Le résultat se concentre sur les options MP4 de ce contenu au lieu d'afficher une liste fixe de résolutions.",
            "Certaines vidéos séparent image et son ; le serveur propose un MP4 final uniquement s'il peut associer des pistes compatibles.",
            "Si la source ne renvoie que du WebM ou omet une hauteur, renommer le fichier ne permet pas de forcer le MP4.",
            "Renommer un WebM en .mp4 suffit-il ?",
            "Non. L'extension ne modifie pas le codec et ne crée pas une option MP4 absente de la source.",
        ),
        "instagram-downloader": LocalizedTool(
            "Téléchargeur Instagram",
            "Analysez les photos et vidéos de publications ou Reels publics.",
            "Copiez l'URL directe instagram.com/p/ ou instagram.com/reel/ d'une publication. Le résultat peut contenir une photo, une vidéo ou plusieurs éléments d'un carrousel.",
            "Les images gardent le format exposé par la source ; une vidéo apparaît seulement si la publication fournit un fichier accessible.",
            "Instagram peut demander une connexion même pour certaines publications visibles publiquement. Les comptes privés sont exclus.",
            "Puis-je coller l'adresse d'un profil ?",
            "Cette page traite surtout les publications individuelles. Un profil peut nécessiter une connexion et ne correspond pas à un seul fichier.",
        ),
        "instagram-reels-downloader": LocalizedTool(
            "Téléchargeur de Reels Instagram",
            "Vérifiez si un Reel public fournit une vidéo accessible.",
            "Utilisez l'URL instagram.com/reel/ du Reel que vous pouvez enregistrer. Analysez-la pour voir si l'extracteur renvoie un fichier vidéo.",
            "Le MP4 d'origine est proposé lorsqu'il est accessible ; aucune résolution supplémentaire n'est inventée.",
            "Un Reel supprimé, privé ou soumis à une connexion peut ne renvoyer aucun format.",
            "Un lien vers le fil des Reels suffit-il ?",
            "Non. Copiez le lien d'un Reel précis, pas celui d'une page de découverte ou d'un profil.",
        ),
        "instagram-photo-downloader": LocalizedTool(
            "Téléchargeur de photos Instagram",
            "Trouvez les images d'origine d'une publication publique.",
            "Collez le lien instagram.com/p/ d'une publication contenant des photos. Pour un carrousel, examinez chaque élément accessible renvoyé par l'analyse.",
            "Une image peut être en JPEG, PNG ou WebP selon la source. Une publication uniquement vidéo ne donne pas de photo téléchargeable.",
            "Les publications privées ou nécessitant une session active ne sont pas récupérées.",
            "L'outil crée-t-il d'autres résolutions ?",
            "Il affiche les fichiers fournis par la source. Pour convertir ensuite votre propre image, utilisez les outils d'image du site.",
        ),
        "tiktok-downloader": LocalizedTool(
            "Téléchargeur TikTok",
            "Analysez une vidéo ou une publication photo TikTok publique.",
            "Copiez le lien d'une vidéo /@utilisateur/video/ID, d'une publication /photo/ID ou un lien court vm.tiktok.com vers un contenu précis.",
            "L'analyseur montre les vidéos, photos ou pistes audio que TikTok laisse consulter pour ce lien. Les qualités ne sont pas prédéfinies.",
            "TikTok peut bloquer les requêtes de centres de données ou supprimer une publication ; aucune connexion n'est contournée.",
            "Puis-je extraire le son d'une vidéo ?",
            "Si l'audio est accessible, ouvrez le convertisseur TikTok en MP3 pour voir l'option correspondante.",
        ),
        "tiktok-to-mp3": LocalizedTool(
            "Convertisseur TikTok en MP3",
            "Préparez un MP3 à partir du son accessible d'une vidéo publique.",
            "Collez l'URL directe /@utilisateur/video/ID ou un lien court vers cette vidéo. Choisissez MP3 uniquement si l'analyse trouve une piste sonore.",
            "Le serveur convertit la piste disponible ; une vidéo muette ne peut pas devenir de la musique ou de la parole.",
            "Une Story expirée, une vidéo supprimée ou un lien bloqué par TikTok n'a pas d'audio récupérable.",
            "Le MP3 améliore-t-il le son ?",
            "Non. La conversion change le format, mais ne restaure pas les détails absents de l'audio d'origine.",
        ),
        "facebook-video-downloader": LocalizedTool(
            "Téléchargeur de vidéos Facebook",
            "Cherchez les formats d'une vidéo ou d'un Reel Facebook public.",
            "Collez une URL facebook.com/watch?v=, /videos/, /reel/ ou fb.watch identifiant une publication précise.",
            "La liste reflète les fichiers renvoyés pour cette vidéo ; une résolution absente ne peut pas être demandée manuellement.",
            "Les vidéos réservées aux amis, les pages imposant une connexion et les publications supprimées sont exclues.",
            "Un lien de groupe privé fonctionne-t-il ?",
            "Non. Le service ne consulte que les contenus publics accessibles sans connexion.",
        ),
        "pinterest-video-downloader": LocalizedTool(
            "Téléchargeur de vidéos, images et GIF Pinterest",
            "Vérifiez le fichier d'origine d'une épingle publique.",
            "Copiez l'URL pinterest.com/pin/ID ou son lien court pin.it. Le contenu peut être une image, un GIF ou une vidéo.",
            "L'outil propose l'élément réellement exposé par l'épingle. Un lien vers un site externe peut ne contenir aucun fichier hébergé par Pinterest.",
            "Les tableaux entiers et les épingles privées ne désignent pas un fichier public unique.",
            "Toutes les épingles contiennent-elles une vidéo ?",
            "Non. Beaucoup ne comportent qu'une image ou mènent à un autre site ; le résultat indique le type réel.",
        ),
        "reddit-video-downloader": LocalizedTool(
            "Téléchargeur de vidéos Reddit",
            "Enregistrez une vidéo de publication publique, avec le son s'il existe.",
            "Utilisez le permalien reddit.com/r/communauté/comments/ID/ ou un lien court redd.it/ID d'une seule publication.",
            "Reddit peut séparer image et son. Lorsque les deux pistes sont accessibles et compatibles, le serveur les réunit dans le fichier final.",
            "Les posts supprimés, privés, en quarantaine ou réservés aux adultes peuvent bloquer l'accès anonyme.",
            "Toutes les vidéos Reddit ont-elles du son ?",
            "Non. Si la source ne fournit aucune piste sonore utilisable, le service ne peut pas en inventer.",
        ),
        "threads-video-downloader": LocalizedTool(
            "Téléchargeur de vidéos Threads",
            "Vérifiez si une publication Threads publique expose une vidéo.",
            "Collez le lien direct threads.com/@utilisateur/post/ID. L'analyseur consulte les métadonnées publiques de cette publication précise.",
            "Si Threads publie un MP4 accessible, ce fichier est proposé. La durée, la taille ou plusieurs résolutions peuvent manquer.",
            "Les posts privés, sans métadonnées vidéo ou nécessitant une connexion ne fournissent aucun fichier.",
            "Pourquoi n'y a-t-il qu'une seule qualité ?",
            "Threads peut n'exposer qu'une vidéo publique ; le service ne crée pas de variantes absentes de la source.",
        ),
        "dailymotion-video-downloader": LocalizedTool(
            "Téléchargeur de vidéos Dailymotion",
            "Choisissez une qualité renvoyée pour une vidéo publique précise.",
            "Collez un lien dailymotion.com/video/ID ou dai.ly/ID. Analysez la publication avant de choisir une hauteur disponible.",
            "Le résultat peut inclure du MP4 ou du WebM selon les pistes accessibles. Une estimation de taille n'apparaît que si les données suffisent.",
            "Les chaînes, playlists, vidéos privées et contenus bloqués par région ne fournissent pas de fichier public utilisable.",
            "Puis-je forcer une meilleure qualité ?",
            "Non. Seules les hauteurs renvoyées pour cette vidéo et compatibles avec la limite de traitement sont proposées.",
        ),
    },
}

LOCALIZED_GUIDES = {
    "es": {
        "youtube-downloader": LocalizedGuide(
            facts=(
                ("Enlaces", "Un vídeo o Short público: youtube.com/watch, youtu.be o youtube.com/shorts"),
                ("Opciones", "Vídeo MP4 o WebM con sonido, audio original y MP3 convertido, según la fuente"),
                ("Límite", "Un contenido cada vez; archivos preparados de hasta 512 MB"),
            ),
            steps=(
                "Abre en YouTube el vídeo o Short que tienes derecho a guardar y copia su dirección desde la barra del navegador o con Compartir > Copiar enlace.",
                "Pégala en el campo de arriba y pulsa «Analizar enlace». El servidor consulta ese único contenido; con YouTube el análisis puede tardar unos segundos.",
                "Compara las filas de la tarjeta: vídeos con su altura y tamaño, audio original y MP3. Elige una y pulsa «Preparar descarga».",
                "Cuando la barra llegue a «Completado», pulsa «Guardar archivo». Tu navegador decide en qué carpeta se guarda.",
            ),
            links=(
                ("youtube.com/watch?v=ID", "La página normal de un vídeo. Si el enlace incluye &list= o &t=, solo se analiza el vídeo indicado por v=, completo."),
                ("youtu.be/ID", "El enlace corto del botón Compartir. El parámetro ?si= que añade la aplicación no cambia nada."),
                ("youtube.com/shorts/ID", "Un Short concreto, no el feed de Shorts ni la pestaña Shorts de un canal."),
                ("m.youtube.com/watch?v=ID", "La versión móvil del sitio, copiada desde el navegador del teléfono."),
                ("music.youtube.com/watch?v=ID", "Una pista pública de YouTube Music; las que exigen suscripción no están disponibles."),
            ),
            sections=(
                ("Vídeo o audio: qué ofrece el convertidor", (
                    "Esta página no filtra el resultado: muestra a la vez los archivos de vídeo, la pista de audio original y la conversión a MP3 que el servidor puede preparar para ese enlace. Es la opción adecuada cuando aún no sabes si necesitas la imagen o solo el sonido. Si ya lo sabes, el descargador de vídeos o el convertidor a MP3 muestran una lista más corta.",
                    "Cada fila de vídeo indica el contenedor (MP4 o WebM), la altura en píxeles y, cuando la fuente da datos suficientes, el tamaño. El signo ≈ marca una estimación; «Tamaño desconocido» significa que no hay datos fiables, no que el archivo esté vacío.",
                )),
                ("Por qué cambian las opciones entre vídeos", (
                    "YouTube guarda la imagen y el sonido de casi todos los vídeos en pistas separadas. El servidor solo muestra una fila de vídeo cuando encuentra una pista de audio compatible para unirla: los MP4 se combinan con audio M4A y los WebM con audio WebM. En YouTube nunca se ofrece un vídeo mudo como si fuera completo.",
                    "Las opciones que superarían 512 MB no aparecen, y la lista llega como máximo a 2160 píxeles de altura. Por eso un vídeo largo puede quedarse sin 4K o sin 1080p aquí aunque el reproductor de YouTube los muestre.",
                )),
                ("Audio original y MP3", (
                    "La fila «Original audio» es la pista de sonido tal como la entrega YouTube, normalmente en M4A o WebM, sin volver a codificarla. «Converted MP3» se crea con ffmpeg a partir de esa misma pista: es más compatible con reproductores antiguos, pero no mejora la calidad. La fila de MP3 no indica tamaño porque el archivo no existe hasta que se convierte.",
                )),
                ("Qué queda fuera", (
                    "Las listas de reproducción completas, las películas de alquiler o compra, el contenido con DRM, los vídeos privados y los directos que siguen en emisión no se procesan. Un vídeo con restricción de edad o de región, o que YouTube bloquea para accesos sin cuenta, puede fallar aunque se vea en tu navegador con la sesión iniciada.",
                )),
            ),
            faq=(
                ("¿Qué diferencia hay con el descargador de vídeos de YouTube?", "Las dos páginas usan el mismo análisis. Esta muestra juntos el vídeo, el audio original y el MP3; el descargador de vídeos solo deja las filas de vídeo y no acepta enlaces /shorts/, que tienen su propia página."),
                ("¿Funciona en el móvil?", "Sí. El formulario funciona en los navegadores actuales de Android e iPhone. Copia el enlace en la aplicación de YouTube con Compartir > Copiar enlace, pégalo aquí y guarda el archivo cuando esté listo; la carpeta depende de tu navegador."),
                ("¿Cuánto tiempo se guarda el archivo preparado?", "Alrededor de una hora, y puede borrarse antes si el servidor se reinicia. Mientras tanto aparece en «Descargas recientes de este navegador», desde donde puedes volver a guardarlo."),
                ("¿Por qué falla un enlace que se ve bien en YouTube?", "El servidor consulta YouTube sin cuenta. Un vídeo privado, eliminado, en directo, con restricción de edad o de región, o bloqueado para accesos automáticos puede no devolver ninguna opción. No usamos tu sesión ni evitamos esos controles."),
            ),
            see_also=(
                ("youtube-video-downloader", "Solo vídeo: descargador de vídeos de YouTube"),
                ("youtube-to-mp3", "Solo sonido: convertidor de YouTube a MP3"),
                ("youtube-to-mp4", "Solo archivos MP4: convertidor de YouTube a MP4"),
                ("youtube-shorts-downloader", "Enlaces /shorts/: descargador de YouTube Shorts"),
            ),
        ),
        "youtube-video-downloader": LocalizedGuide(
            facts=(
                ("Enlaces", "Un vídeo público: youtube.com/watch?v= o youtu.be"),
                ("Opciones", "Archivos de vídeo MP4 o WebM con sonido, según el vídeo"),
                ("Límite", "Un vídeo terminado cada vez, de hasta 512 MB"),
            ),
            steps=(
                "Copia el enlace de un único vídeo público que te pertenezca o que tengas permiso para guardar: la dirección watch?v= del navegador o el enlace youtu.be de Compartir.",
                "Pégalo arriba y pulsa «Analizar enlace». La tarjeta muestra el título, el canal, la duración y las filas de vídeo que el servidor puede preparar.",
                "Elige una fila. Por defecto queda marcada la mejor opción de hasta 1080 píxeles de altura, para que un clic rápido no inicie un archivo 4K enorme; puedes escoger cualquier otra.",
                "Pulsa «Preparar descarga». Durante «Combinando vídeo y audio» el servidor une las pistas; cuando aparezca «Guardar archivo», descárgalo desde tu navegador.",
            ),
            links=(
                ("youtube.com/watch?v=ID", "La página de un vídeo. Los parámetros &list= y &t= se ignoran: se prepara el vídeo completo indicado por v=."),
                ("youtu.be/ID", "El enlace corto de Compartir, también con ?si= al final."),
                ("m.youtube.com/watch?v=ID", "La dirección que copia el navegador del móvil."),
                ("youtube.com/embed/ID", "La dirección de un vídeo incrustado en otra web."),
            ),
            sections=(
                ("Cómo leer la tarjeta de resultados", (
                    "Cada fila muestra el contenedor y la altura (por ejemplo 720p o 1080p) y, cuando YouTube los facilita, las dimensiones en píxeles, la tasa de bits aproximada y el tamaño. El signo ≈ indica un tamaño estimado; «Tamaño desconocido» aparece cuando YouTube no da datos suficientes para el vídeo completo con su audio.",
                    "La cifra más alta no siempre es la mejor elección. Escoge el archivo que tu dispositivo puede reproducir y guardar: un 1080p de un vídeo largo puede ocupar varios cientos de MB.",
                )),
                ("MP4 o WebM", (
                    "YouTube puede ofrecer la misma altura en MP4 y en WebM. Cada MP4 se combina con audio M4A y cada WebM con audio WebM, así que el archivo final conserva el contenedor que elijas. MP4 suele ser el más compatible con móviles, televisores y editores; WebM se abre en los navegadores actuales y en reproductores como VLC.",
                    "Cambiar la extensión de .webm a .mp4 no convierte el vídeo: el códec sigue siendo el mismo y algunos programas no lo abrirán.",
                )),
                ("1080p, 4K y el límite de 512 MB", (
                    "Las resoluciones altas llegan sin sonido y el servidor solo las ofrece si puede unirles una pista de audio compatible. Además, se descartan las opciones que superarían 512 MB o 2160 píxeles de altura: no hay 8K, y un vídeo largo puede quedarse sin 4K o sin 1080p.",
                    "Si no aparece la resolución que esperabas, elige la más alta que sí muestra la tarjeta. Que el reproductor de YouTube ofrezca 4K no significa que haya un archivo 4K descargable aquí.",
                )),
                ("Shorts, listas y directos", (
                    "Esta página solo acepta vídeos normales. Un enlace youtube.com/shorts/ se rechaza con un aviso: usa el descargador de YouTube Shorts. Las listas de reproducción, los vídeos privados, los alquileres y los directos en curso no se procesan, y un vídeo con restricción de edad o de región puede fallar para un servidor sin cuenta.",
                )),
            ),
            faq=(
                ("¿Cómo descargo un vídeo de YouTube?", "Pega el enlace watch?v= o youtu.be de un vídeo público, pulsa «Analizar enlace», elige una fila de vídeo y pulsa «Preparar descarga». Cuando termine, guarda el archivo temporal. Descarga solo vídeos propios o con permiso."),
                ("¿El vídeo descargado tendrá sonido?", "Sí. En YouTube solo se ofrecen las filas que el servidor puede combinar con una pista de audio compatible. Un vídeo sin audio accesible no aparece como descarga completa."),
                ("¿Puedo pegar un enlace de Shorts?", "En esta página no. Los enlaces /shorts/ tienen su propio descargador, y el descargador y convertidor de YouTube general acepta los dos tipos."),
                ("¿Por qué falla un vídeo público?", "Puede estar eliminado, ser privado, tener restricción de edad o de región, estar en directo o estar bloqueado para accesos automáticos sin cuenta. La herramienta no usa tu cuenta ni evita esos controles."),
            ),
            see_also=(
                ("youtube-shorts-downloader", "Enlaces /shorts/: descargador de YouTube Shorts"),
                ("youtube-to-mp4", "Solo filas MP4: convertidor de YouTube a MP4"),
                ("youtube-to-mp3", "Solo el sonido: convertidor de YouTube a MP3"),
                ("youtube-downloader", "Vídeo y audio juntos: descargador y convertidor de YouTube"),
            ),
        ),
        "youtube-shorts-downloader": LocalizedGuide(
            facts=(
                ("Enlaces", "Un Short público con la forma youtube.com/shorts/ID"),
                ("Opciones", "Archivos de vídeo MP4 o WebM con sonido devueltos para ese Short"),
                ("Límite", "Un Short cada vez; archivos de hasta 512 MB"),
            ),
            steps=(
                "En la aplicación de YouTube, abre el Short, toca Compartir y elige Copiar enlace. En el ordenador, copia la dirección youtube.com/shorts/ de la barra del navegador.",
                "Pega el enlace arriba y pulsa «Analizar enlace». El servidor comprueba que la ruta contiene /shorts/ seguido del identificador de 11 caracteres.",
                "Revisa las filas de vídeo: contenedor, altura, dimensiones y tamaño. Elige una y pulsa «Preparar descarga».",
                "Cuando la barra llegue a «Completado», pulsa «Guardar archivo». Tu navegador decide dónde se guarda, normalmente en la carpeta de descargas.",
            ),
            links=(
                ("youtube.com/shorts/ID", "El enlace de un Short concreto, con o sin el parámetro ?si= que añade Compartir."),
                ("m.youtube.com/shorts/ID", "La misma dirección copiada desde el navegador del móvil."),
            ),
            sections=(
                ("Por qué esta página pide un enlace /shorts/", (
                    "El detector solo clasifica un enlace como Short cuando su ruta es /shorts/ seguida del identificador. Si pegas aquí la versión youtu.be o watch?v= del mismo clip, se trata como vídeo normal y la página te avisa de que necesitas otra herramienta: usa el descargador de vídeos de YouTube o el descargador general, que acepta los dos tipos.",
                    "Un feed de Shorts, la pestaña Shorts de un canal, una búsqueda o una lista no identifican un único archivo y no se aceptan.",
                )),
                ("Formatos de un Short vertical", (
                    "La mayoría de los Shorts son verticales, así que la altura suele ser la cifra mayor. La etiqueta de cada fila es la altura en píxeles que declara YouTube, y la tarjeta muestra también ancho × alto para que compruebes la orientación. Puede haber versiones MP4 y WebM de la misma altura; MP4 suele ser la más compatible con teléfonos y editores.",
                    "Igual que con los vídeos normales, el servidor une imagen y sonido antes de entregarte el archivo y solo muestra las filas que puede combinar con audio. Las opciones de más de 512 MB o de más de 2160 píxeles de altura no aparecen.",
                )),
                ("Solo el sonido de un Short", (
                    "Esta página muestra únicamente archivos de vídeo. Si quieres el audio, pega el mismo enlace /shorts/ en el convertidor de YouTube a MP3: allí verás la opción MP3 cuando el Short tenga una pista de sonido accesible. Un clip sin audio no puede convertirse en música o voz.",
                )),
                ("Si un Short no ofrece ningún archivo", (
                    "Un Short eliminado, privado, con restricción de edad, en directo o bloqueado para accesos sin cuenta puede no devolver nada al servidor. Cambiar la URL no crea un formato que falta. Si el análisis caduca porque dejaste la tarjeta abierta más de diez minutos, vuelve a pegar el enlace.",
                )),
            ),
            faq=(
                ("¿Cómo descargo un Short de YouTube?", "Copia el enlace youtube.com/shorts/ de un Short público, pégalo arriba y pulsa «Analizar enlace». Elige una fila de vídeo, pulsa «Preparar descarga» y guarda el archivo cuando esté listo."),
                ("¿Puedo pegar un feed de Shorts o un canal?", "No. Usa el enlace de un Short individual. Un feed o un canal contiene muchos vídeos y no indica qué archivo preparar."),
                ("¿Por qué mi enlace youtu.be no funciona aquí?", "Porque un enlace youtu.be o watch?v= se clasifica como vídeo normal. Pégalo en el descargador de vídeos de YouTube o copia la dirección /shorts/ del Short."),
                ("¿Funciona en el móvil?", "Sí, desde el navegador del teléfono. Copia el enlace en la aplicación de YouTube, pégalo en esta página y guarda el archivo; tu navegador decide la carpeta de destino."),
            ),
            see_also=(
                ("youtube-to-mp3", "El sonido del Short en MP3"),
                ("youtube-video-downloader", "Vídeos normales con enlace watch o youtu.be"),
                ("youtube-downloader", "Vídeo y audio en una sola página"),
            ),
        ),
        "instagram-reels-downloader": LocalizedGuide(
            facts=(
                ("Enlaces", "Un Reel público: instagram.com/reel/ID/"),
                ("Opciones", "El vídeo que Instagram entrega a un visitante sin cuenta"),
                ("Límite", "Un Reel cada vez; sin perfiles privados ni inicio de sesión"),
            ),
            steps=(
                "En la aplicación de Instagram, abre el Reel, toca el icono de compartir y elige Copiar enlace. En el ordenador, copia la dirección del Reel abierto.",
                "Pégalo arriba y pulsa «Analizar enlace». El servidor consulta ese Reel tal como lo vería alguien sin cuenta.",
                "Si aparece una fila de vídeo, revisa la extensión, la altura y el tamaño cuando estén disponibles, y pulsa «Preparar descarga».",
                "Guarda el archivo cuando aparezca «Guardar archivo». Si no aparece ninguna fila, el Reel no está disponible para accesos públicos.",
            ),
            links=(
                ("instagram.com/reel/ID/", "El enlace de un Reel concreto. El parámetro ?igsh= que añade Compartir no afecta."),
                ("instagram.com/reels/ID/", "La variante en plural que a veces aparece al copiar desde el navegador; se trata igual."),
            ),
            sections=(
                ("Usa el enlace del Reel, no el de la publicación", (
                    "Esta página solo acepta enlaces /reel/ (o /reels/). Una dirección instagram.com/p/ corresponde a una publicación que puede tener fotos, vídeo o un carrusel, y se analiza en el descargador de Instagram general. Un perfil, una historia o la página Explorar tampoco identifican un único Reel.",
                )),
                ("Por qué un Reel visible puede fallar", (
                    "Instagram puede mostrar un clip a tu navegador con la sesión iniciada y ocultárselo a un servidor sin cuenta. Prueba a abrir el enlace en una ventana privada sin iniciar sesión: si Instagram pide entrar, la herramienta tampoco podrá acceder. SaveFromNet no acepta contraseñas ni cookies de tu cuenta y no accede a perfiles privados ni a Reels eliminados.",
                )),
                ("Qué significa el resultado", (
                    "La tarjeta describe el archivo que ha devuelto la fuente; no promete todas las calidades que ves en la aplicación. A veces Instagram no declara la altura y la fila aparece como «Source video», y el tamaño puede quedar como desconocido en lugar de deducirse de la vista previa.",
                    "Si Instagram entrega la imagen y el sonido por separado, el servidor los une en un solo archivo. Si el Reel no tiene ninguna pista de sonido, la fila lo indica con «no audio». La herramienta no elimina marcas de agua ni recupera contenido caducado.",
                )),
            ),
            faq=(
                ("¿Qué enlace de Reel debo pegar?", "El enlace directo instagram.com/reel/ de un Reel público. Los enlaces de perfil, de historia o de publicación /p/ corresponden a otras herramientas."),
                ("¿Por qué un Reel se reproduce en mi móvil pero falla aquí?", "Tu sesión de Instagram puede tener un acceso que un servidor anónimo no tiene. Los Reels privados, eliminados o que exigen iniciar sesión no se pueden obtener con esta herramienta pública."),
                ("¿Puedo elegir la resolución del Reel?", "Solo entre las filas que devuelve el análisis, y puede haber una sola. No se inventan resoluciones ni tamaños."),
                ("¿El vídeo tendrá sonido?", "Sí, cuando el Reel tiene audio accesible: si llega por separado, el servidor lo combina con la imagen. Un Reel sin pista de sonido se marca con «no audio»."),
            ),
            see_also=(
                ("instagram-downloader", "Publicaciones /p/ y carruseles: descargador de Instagram"),
                ("instagram-photo-downloader", "Fotos de una publicación de Instagram"),
                ("facebook-video-downloader", "Vídeos y Reels de Facebook"),
            ),
        ),
        "facebook-video-downloader": LocalizedGuide(
            facts=(
                ("Enlaces", "Un vídeo o Reel público: watch?v=, /videos/, /reel/, fb.watch o /share/v/"),
                ("Opciones", "Los archivos de vídeo que Facebook entrega sin iniciar sesión"),
                ("Límite", "Una publicación cada vez; archivos de hasta 512 MB"),
            ),
            steps=(
                "Abre el vídeo o Reel en Facebook y copia su enlace: en la aplicación, con Compartir y después Copiar enlace; en el ordenador, desde la barra de direcciones o con la opción Copiar enlace del menú de la publicación.",
                "Antes de pegarlo, comprueba que el vídeo se ve en una ventana privada sin iniciar sesión. Si Facebook pide entrar, el servidor tampoco lo verá.",
                "Pégalo arriba y pulsa «Analizar enlace». Compara las filas de vídeo que aparezcan y elige una.",
                "Pulsa «Preparar descarga» y guarda el archivo cuando aparezca «Guardar archivo».",
            ),
            links=(
                ("facebook.com/watch?v=ID", "La página de vídeo de Facebook Watch, con identificador numérico."),
                ("facebook.com/NOMBRE/videos/ID", "Un vídeo publicado en una página o un perfil."),
                ("facebook.com/reel/ID", "Un Reel individual de Facebook."),
                ("fb.watch/ID", "El enlace corto que genera Facebook al compartir un vídeo."),
                ("facebook.com/share/v/ID", "El enlace que copia la aplicación con Compartir; /share/r/ID es la versión para Reels."),
            ),
            sections=(
                ("Copia la publicación del vídeo, no el muro", (
                    "Una página de vídeo, un Reel o un enlace fb.watch identifican un solo vídeo. Un perfil, la portada de una página o un grupo no lo hacen, y el detector los rechaza antes de consultar a Facebook. También se aceptan las direcciones m.facebook.com y web.facebook.com, que se tratan igual que facebook.com.",
                )),
                ("Público para ti no siempre es público", (
                    "Un vídeo compartido solo con amigos o dentro de un grupo puede reproducirse en tu cuenta y no estar al alcance de este servicio anónimo. SaveFromNet no pide credenciales de Facebook ni evita la configuración de privacidad del autor. Si la publicación se ve sin iniciar sesión, el análisis tiene las mismas posibilidades que cualquier visitante.",
                )),
                ("Qué calidades puede devolver Facebook", (
                    "Facebook no siempre declara la altura de sus archivos. Cuando falta, la fila aparece como HD o SD según la etiqueta de la fuente, o como «Source video». Si la altura existe, verás cifras como 720p o 1080p y las dimensiones en píxeles. Que el reproductor muestre HD no garantiza una descarga HD aquí.",
                    "Si la imagen y el sonido llegan por separado, el servidor los une dentro del límite de 512 MB. Si la publicación no tiene ninguna pista de sonido, la fila lo indica con «no audio». Un tamaño desconocido se muestra como tal en vez de inventar una cifra.",
                )),
            ),
            faq=(
                ("¿Funcionan los Reels y los enlaces fb.watch?", "Sí. Se aceptan los Reels públicos /reel/, los enlaces fb.watch y los enlaces /share/v/ o /share/r/ de la aplicación, además de las páginas watch?v= y /videos/."),
                ("¿Puedo descargar un vídeo solo para amigos?", "No. El servidor no usa tu cuenta de Facebook ni evita la configuración de público del autor. Comprueba la publicación sin iniciar sesión."),
                ("¿Todos los vídeos de Facebook tienen HD y sonido?", "No. La altura y el audio dependen de los archivos accesibles. El análisis solo muestra lo que puede preparar para esa publicación."),
                ("¿Cómo copio el enlace desde la aplicación?", "Toca Compartir en el vídeo y elige Copiar enlace. Suele dar una dirección facebook.com/share/ o fb.watch, que puedes pegar directamente aquí."),
            ),
            see_also=(
                ("instagram-reels-downloader", "Reels de Instagram"),
                ("universal-video-downloader", "Enlaces de otras plataformas en un solo campo"),
            ),
        ),
        "pinterest-video-downloader": LocalizedGuide(
            facts=(
                ("Enlaces", "Un Pin público: pinterest.com/pin/ID o pin.it"),
                ("Opciones", "La imagen, el GIF o el vídeo original que expone el Pin"),
                ("Límite", "Un Pin cada vez; ni tableros ni búsquedas"),
            ),
            steps=(
                "Abre el Pin y copia su enlace: en la aplicación, toca Compartir y elige Copiar enlace (normalmente obtendrás un pin.it); en el ordenador, copia la dirección pinterest.com/pin/ de la barra.",
                "Pégalo arriba y pulsa «Analizar enlace». El servidor consulta los archivos de ese Pin.",
                "Mira el tipo de cada elemento: imagen (JPG, PNG o WebP), GIF o vídeo (MP4 o WebM). Elige el que necesitas.",
                "Pulsa «Preparar descarga» y guarda el archivo cuando esté listo.",
            ),
            links=(
                ("pinterest.com/pin/ID/", "La página de un Pin con su identificador numérico."),
                ("es.pinterest.com/pin/ID/", "La versión de Pinterest de tu país; también sirven otros subdominios como fr.pinterest.com o in.pinterest.com."),
                ("pin.it/ID", "El enlace corto que copia la aplicación con Compartir."),
            ),
            sections=(
                ("Un Pin puede ser imagen, GIF o vídeo", (
                    "El resultado refleja el archivo que Pinterest expone para ese Pin. Cada elemento aparece con su extensión real y una etiqueta como «Item 1 · original»: JPG, PNG o WebP para las imágenes, GIF para las animaciones y MP4 o WebM para los vídeos. Estos elementos originales se muestran sin tamaño estimado. Un Pin de imagen fija no producirá una fila de vídeo.",
                    "En algunos Pins de vídeo el resultado muestra, en cambio, filas por altura con el sonido ya unido, además del audio original y una conversión a MP3. Depende de cómo entregue Pinterest ese vídeo.",
                )),
                ("Una animación no siempre es un GIF", (
                    "La vista previa animada de un Pin puede ser un vídeo y no un GIF descargable. Después del análisis, comprueba si el elemento es imagen, GIF o vídeo y usa el tipo que realmente aparece. La herramienta no renombra un MP4 como GIF ni promete una animación cuando Pinterest solo expone una imagen.",
                )),
                ("Enlaces externos y tableros", (
                    "Muchos Pins remiten a otra web. Esta herramienta no sigue ese destino ni descarga archivos de otros sitios: solo examina el contenido alojado en Pinterest. Un tablero, una búsqueda o un perfil contienen muchos Pins y no se aceptan; analiza los Pins de uno en uno.",
                )),
            ),
            faq=(
                ("¿Puedo pegar un tablero de Pinterest?", "No. Pega el enlace de un Pin público o su enlace corto pin.it. Un tablero contiene varios Pins y no es un único archivo."),
                ("¿Por qué un Pin de vídeo devuelve una imagen?", "El Pin puede exponer solo una imagen fija o una vista previa mientras el vídeo está alojado en otro lugar. La herramienta muestra el elemento real al que puede acceder; no fabrica un vídeo."),
                ("¿Puedo descargar la web a la que enlaza un Pin?", "No. Solo se examina el contenido de Pinterest de ese Pin; la herramienta no visita el sitio de destino."),
                ("¿Sirven los enlaces es.pinterest.com?", "Sí. Los subdominios de país de pinterest.com se aceptan igual que pinterest.com, siempre que la dirección sea /pin/ seguida del número del Pin."),
            ),
            see_also=(
                ("instagram-photo-downloader", "Fotos de publicaciones de Instagram"),
                ("universal-video-downloader", "Enlaces de otras plataformas en un solo campo"),
            ),
        ),
        "universal-video-downloader": LocalizedGuide(
            facts=(
                ("Plataformas", "YouTube, Instagram, TikTok, Facebook, Pinterest, Reddit, Threads y Dailymotion"),
                ("Opciones", "Vídeo, audio o imágenes, según lo que devuelva la fuente"),
                ("Límite", "Un enlace cada vez; archivos preparados de hasta 512 MB"),
            ),
            steps=(
                "Copia el enlace de la publicación concreta que quieres guardar, en cualquiera de las ocho plataformas compatibles. Puedes pegarlo con o sin https:// al principio.",
                "Pulsa «Analizar enlace». El detector reconoce la plataforma por el dominio y la ruta y envía el enlace al extractor adecuado; un dominio no compatible se rechaza antes de hacer ninguna consulta.",
                "Revisa la tarjeta: puede mostrar filas de vídeo, de audio o de imagen. Elige una de las que aparecen y pulsa «Preparar descarga».",
                "Cuando aparezca «Guardar archivo», descárgalo desde tu navegador. El archivo temporal se borra al cabo de una hora, aproximadamente.",
            ),
            links=(
                ("youtube.com/watch?v=ID", "Un vídeo de YouTube; también sirven youtu.be/ID y youtube.com/shorts/ID."),
                ("instagram.com/p/ID/", "Una publicación de Instagram; los Reels usan instagram.com/reel/ID/."),
                ("tiktok.com/@USUARIO/video/ID", "Un vídeo de TikTok; las publicaciones de fotos usan /photo/ID, y también sirven los enlaces cortos vm.tiktok.com."),
                ("facebook.com/reel/ID", "Un Reel de Facebook; también fb.watch/ID y las páginas watch?v= o /videos/."),
                ("pinterest.com/pin/ID/", "Un Pin; también el enlace corto pin.it/ID."),
                ("reddit.com/r/COMUNIDAD/comments/ID/", "Una publicación de Reddit; también redd.it/ID."),
                ("threads.com/@USUARIO/post/ID", "Una publicación de Threads; los enlaces threads.net se convierten a threads.com."),
                ("dailymotion.com/video/ID", "Un vídeo de Dailymotion; también dai.ly/ID."),
            ),
            sections=(
                ("Qué tiene de distinto el descargador universal", (
                    "Las páginas específicas filtran el resultado: el convertidor a MP3 solo muestra el MP3 y el descargador de Reels solo muestra vídeo. Esta página no filtra nada. Enseña todo lo que el servidor puede preparar para el enlace: vídeo, audio original, conversión a MP3 o imágenes. Es útil cuando no sabes qué herramienta usar o quieres comparar todas las opciones.",
                    "También acepta enlaces que las páginas en español no cubren, como un perfil público de Instagram, una historia de Instagram o las historias de una cuenta de TikTok. Muchos de esos contenidos exigen iniciar sesión y, en ese caso, no devuelven nada.",
                )),
                ("Cómo se decide qué aparece en la tarjeta", (
                    "YouTube, Facebook, Reddit, Dailymotion y los vídeos de TikTok e Instagram pasan por un extractor que devuelve filas de vídeo por altura, en MP4 o WebM, además del audio original y un MP3 cuando hay sonido. Las publicaciones de Instagram, los Pins y las fotos de TikTok devuelven elementos originales, hasta 12 por enlace, cada uno con su extensión real. Threads ofrece como máximo un vídeo MP4.",
                    "Ningún archivo puede superar 512 MB, y las filas de vídeo que lo superarían ni siquiera aparecen. El tamaño solo se muestra cuando la fuente da datos suficientes; el signo ≈ marca una estimación.",
                )),
                ("Enlaces que no funcionan", (
                    "Un feed, una búsqueda, un tablero de Pinterest, una lista de reproducción o la portada de una red social no identifican un archivo concreto. Tampoco se procesan publicaciones privadas, eliminadas, en directo o que exigen iniciar sesión. Si el dominio no pertenece a una de las ocho plataformas, la página lo indica sin consultar ninguna web: SaveFromNet no descarga de sitios arbitrarios.",
                )),
            ),
            faq=(
                ("¿Hay que pegar el enlace con https://?", "No. Si falta, se añade automáticamente. Los enlaces con puerto, usuario o contraseña se rechazan."),
                ("¿Es mejor usar esta página o la de cada plataforma?", "El análisis es el mismo. Esta página muestra todas las opciones juntas; las páginas específicas filtran la lista y explican con más detalle los enlaces de su plataforma."),
                ("¿Puedo pegar varios enlaces a la vez?", "No. Analiza un enlace cada vez y prepara una descarga por cada fila que elijas. Si analizas muchos enlaces seguidos y aparece «Demasiadas solicitudes», espera un minuto."),
                ("¿Dónde se guarda el archivo?", "Donde tu navegador guarda las descargas. El archivo temporal se conserva alrededor de una hora en el servidor y, mientras tanto, aparece en «Descargas recientes de este navegador»."),
            ),
            see_also=(
                ("youtube-downloader", "YouTube: vídeo y audio"),
                ("instagram-downloader", "Publicaciones y Reels de Instagram"),
                ("tiktok-downloader", "Vídeos y fotos de TikTok"),
                ("facebook-video-downloader", "Vídeos y Reels de Facebook"),
                ("reddit-video-downloader", "Vídeos de Reddit con sonido"),
            ),
        ),
        "youtube-to-mp3": LocalizedGuide(
            facts=(
                ("Enlaces", "Un vídeo o Short público: youtube.com/watch, youtu.be o youtube.com/shorts"),
                ("Resultado", "Una sola opción: MP3 convertido a partir del audio accesible"),
                ("Límite", "Un contenido cada vez; archivos de hasta 512 MB"),
            ),
            steps=(
                "Abre el vídeo o Short que tienes derecho a guardar y copia su enlace con Compartir > Copiar enlace o desde la barra del navegador.",
                "Pégalo arriba y pulsa «Analizar enlace». El servidor comprueba si ese contenido tiene una pista de sonido accesible.",
                "Si la tiene, la tarjeta muestra la fila «Converted MP3». Pulsa «Preparar descarga»: durante «Extrayendo audio», el servidor convierte el sonido con ffmpeg.",
                "Cuando aparezca «Guardar archivo», descarga el MP3. En vídeos largos la conversión tarda más; mantén la página abierta.",
            ),
            links=(
                ("youtube.com/watch?v=ID", "La página de un vídeo. Si el enlace lleva &list=, solo se convierte el vídeo indicado por v=, nunca la lista."),
                ("youtu.be/ID", "El enlace corto de Compartir, con o sin ?si=."),
                ("youtube.com/shorts/ID", "Un Short concreto."),
                ("music.youtube.com/watch?v=ID", "Una pista pública de YouTube Music."),
            ),
            sections=(
                ("Qué contiene el MP3", (
                    "YouTube no entrega archivos MP3. El servidor descarga la mejor pista de audio accesible (normalmente M4A u Opus en WebM) y la convierte a MP3 con ffmpeg. Por eso la tarjeta muestra una sola fila, «Converted MP3», sin tamaño: el archivo no existe hasta que termina la conversión.",
                    "El MP3 es más compatible con reproductores, coches y programas antiguos, pero es una conversión con pérdida: no recupera detalle que falte en el original y no hay una tasa de bits fija garantizada.",
                )),
                ("Si prefieres el audio sin convertir", (
                    "Si quieres la pista original sin volver a codificarla, usa el descargador y convertidor de YouTube: allí aparece también la fila «Original audio» con su formato real, junto al MP3 y a los archivos de vídeo.",
                )),
                ("Problemas frecuentes", (
                    "Si el enlace se rechaza, comprueba que apunta a un solo vídeo o Short: las listas, los canales y las búsquedas no se aceptan. Si el análisis falla, el vídeo puede ser privado, estar eliminado, tener restricción de edad o de región, ser un directo en curso o estar bloqueado para accesos automáticos.",
                    "Si no aparece la fila MP3, el contenido no tiene una pista de sonido accesible. Si la tarjeta lleva abierta más de diez minutos, vuelve a analizar el enlace antes de preparar la descarga.",
                )),
            ),
            faq=(
                ("¿Cómo convierto un vídeo de YouTube a MP3?", "Pega el enlace de un vídeo o Short público, pulsa «Analizar enlace», elige «Converted MP3» y pulsa «Preparar descarga». Cuando termine la conversión, guarda el archivo."),
                ("¿Puedo convertir una lista de reproducción entera?", "No. Cada análisis corresponde a un solo vídeo; si el enlace incluye &list=, la lista se ignora."),
                ("¿Por qué el MP3 no indica tamaño?", "Porque se crea al convertir. El tamaño final depende de la duración y de la conversión, y no se conoce hasta que termina."),
                ("¿Funciona en el móvil?", "Sí. Usa el navegador del teléfono; el MP3 terminado se guarda donde tu navegador guarda las descargas."),
            ),
            see_also=(
                ("youtube-downloader", "Audio original y vídeo: descargador y convertidor de YouTube"),
                ("youtube-video-downloader", "El vídeo completo: descargador de vídeos de YouTube"),
                ("tiktok-to-mp3", "El sonido de un vídeo de TikTok en MP3"),
            ),
        ),
        "youtube-to-mp4": LocalizedGuide(
            facts=(
                ("Enlaces", "Un vídeo o Short público: youtube.com/watch, youtu.be o youtube.com/shorts"),
                ("Resultado", "Solo filas MP4 con sonido, por altura"),
                ("Límite", "Un contenido cada vez; hasta 512 MB y 2160 píxeles de altura"),
            ),
            steps=(
                "Copia el enlace de un único vídeo o Short público que tengas derecho a guardar.",
                "Pégalo arriba y pulsa «Analizar enlace». La tarjeta muestra solo las filas MP4 que el servidor puede preparar para ese contenido.",
                "Elige una altura. Por defecto queda marcada la mejor opción de hasta 1080 píxeles; puedes escoger otra.",
                "Pulsa «Preparar descarga». Si el MP4 necesita unir imagen y sonido, verás la etapa «Combinando vídeo y audio» antes de «Guardar archivo».",
            ),
            links=(
                ("youtube.com/watch?v=ID", "La página de un vídeo; &list= y &t= se ignoran."),
                ("youtu.be/ID", "El enlace corto de Compartir."),
                ("youtube.com/shorts/ID", "Un Short concreto."),
                ("m.youtube.com/watch?v=ID", "La versión móvil del sitio."),
            ),
            sections=(
                ("Qué significa una fila MP4", (
                    "Cada fila es un archivo MP4 terminado: imagen en MP4 combinada con audio M4A, o un MP4 que ya trae el sonido. La etiqueta indica la altura en píxeles, y la tarjeta añade las dimensiones, la tasa de bits y el tamaño cuando YouTube los facilita.",
                    "Las resoluciones altas de YouTube llegan sin sonido, así que el servidor solo ofrece una altura si puede unirle una pista de audio compatible. Nunca se entrega un MP4 mudo como si estuviera completo.",
                )),
                ("Por qué falta una resolución", (
                    "Algunas alturas solo existen en WebM; esta página no las muestra y no las renombra como MP4. Si necesitas esa resolución en WebM, el descargador de vídeos de YouTube muestra los dos contenedores. También se descartan las opciones de más de 512 MB o de más de 2160 píxeles de altura, así que un vídeo largo puede quedarse sin 4K o sin 1080p.",
                )),
                ("MP4 y compatibilidad", (
                    "MP4 es el contenedor que aceptan casi todos los móviles, televisores y editores, y por eso esta página se centra en él. Aun así, el códec de vídeo dentro del MP4 depende de lo que publique YouTube; si un dispositivo antiguo no reproduce el archivo, puede servir una altura menor o un reproductor como VLC.",
                )),
            ),
            faq=(
                ("¿Cómo descargo un vídeo de YouTube en MP4?", "Pega el enlace, pulsa «Analizar enlace», elige una fila MP4 y pulsa «Preparar descarga». Cuando termine, guarda el archivo."),
                ("¿El MP4 tendrá sonido?", "Sí. Solo se ofrecen las alturas que el servidor puede combinar con audio M4A o que ya incluyen sonido."),
                ("¿Por qué no aparece ninguna fila?", "Puede que el vídeo solo tenga WebM dentro del límite de tamaño, o que sea privado, esté eliminado, en directo o restringido. Prueba el descargador de vídeos de YouTube para ver todos los contenedores."),
            ),
            see_also=(
                ("youtube-video-downloader", "MP4 y WebM: descargador de vídeos de YouTube"),
                ("youtube-to-mp3", "Solo el sonido: convertidor de YouTube a MP3"),
                ("youtube-shorts-downloader", "Enlaces /shorts/: descargador de YouTube Shorts"),
            ),
        ),
        "instagram-downloader": LocalizedGuide(
            facts=(
                ("Enlaces", "Una publicación /p/ o un Reel /reel/ públicos"),
                ("Opciones", "Fotos, vídeos o elementos de carrusel originales, hasta 12"),
                ("Acceso", "Solo lo que Instagram muestra sin iniciar sesión"),
            ),
            steps=(
                "En Instagram, abre la publicación o el Reel, toca el icono de compartir y elige Copiar enlace.",
                "Pégalo arriba y pulsa «Analizar enlace». El servidor consulta esa publicación como un visitante sin cuenta.",
                "Revisa los elementos: en una publicación aparecen numerados («Item 1 · original», «Item 2 · original»…) con su extensión real; en un Reel aparecen filas de vídeo y, si hay sonido, de audio.",
                "Elige uno, pulsa «Preparar descarga» y guárdalo. Repite con cada elemento del carrusel que necesites: cada uno se prepara por separado.",
            ),
            links=(
                ("instagram.com/p/ID/", "Una publicación con foto, vídeo o carrusel. El parámetro ?igsh= de Compartir no afecta."),
                ("instagram.com/reel/ID/", "Un Reel; también la variante instagram.com/reels/ID/."),
                ("instagram.com/tv/ID/", "Un vídeo antiguo de IGTV; se trata como una publicación."),
            ),
            sections=(
                ("Publicaciones: cada elemento por separado", (
                    "Para una dirección /p/, el servidor lista los elementos originales de la publicación, hasta 12, cada uno con su extensión: JPG, PNG o WebP para las fotos y MP4 o WebM para los vídeos. No se crea un ZIP ni se une el carrusel en un solo archivo. Estos elementos aparecen sin tamaño estimado.",
                    "Si Instagram no deja leer los elementos, el servidor prueba con el extractor de vídeo, que puede encontrar el vídeo de una publicación pública. Las publicaciones solo de fotos no tienen ese segundo intento y fallan si Instagram pide iniciar sesión.",
                )),
                ("Reels: vídeo y audio", (
                    "Un enlace /reel/ se analiza con el extractor de vídeo. La tarjeta puede mostrar filas de vídeo por altura, la pista de audio original y un MP3 convertido cuando el Reel tiene sonido. Si solo te interesa el vídeo, el descargador de Reels muestra una lista más corta.",
                )),
                ("El acceso anónimo decide", (
                    "Una publicación que ves en la aplicación con tu cuenta puede estar oculta para un servidor sin cuenta. Si al abrir el enlace en una ventana privada Instagram pide iniciar sesión, SaveFromNet tampoco podrá leerla. No se usan contraseñas ni cookies, y los perfiles privados quedan fuera.",
                )),
            ),
            faq=(
                ("¿Puedo descargar todas las fotos de un carrusel?", "Sí, una a una. El análisis lista hasta 12 elementos accesibles, y cada uno se prepara y se guarda por separado."),
                ("¿Por qué falla una publicación de fotos y un Reel no?", "Instagram suele pedir inicio de sesión a los accesos automáticos a las fotos. Los vídeos tienen un segundo extractor y las fotos no, así que a veces no hay resultado."),
                ("¿Se pueden descargar historias aquí?", "No. Esta página acepta publicaciones /p/ y Reels. El descargador universal acepta enlaces de historias públicas, pero la mayoría exigen iniciar sesión o caducan pronto."),
            ),
            see_also=(
                ("instagram-reels-downloader", "Solo el vídeo de un Reel"),
                ("instagram-photo-downloader", "Solo las fotos de una publicación"),
                ("universal-video-downloader", "Perfiles e historias: descargador universal"),
            ),
        ),
        "instagram-photo-downloader": LocalizedGuide(
            facts=(
                ("Enlaces", "Una publicación pública con fotos: instagram.com/p/ID/"),
                ("Opciones", "Solo las imágenes originales, hasta 12 por publicación"),
                ("Acceso", "Sin iniciar sesión; perfiles privados excluidos"),
            ),
            steps=(
                "Abre la publicación con fotos y copia su enlace con el icono de compartir > Copiar enlace, o desde la barra del navegador.",
                "Pégalo arriba y pulsa «Analizar enlace». El servidor lee los elementos de la publicación y deja solo las imágenes.",
                "Cada foto aparece numerada con su extensión real (JPG, PNG o WebP). Elige la que necesitas y pulsa «Preparar descarga».",
                "Guarda el archivo y repite con las demás fotos del carrusel: cada una es una descarga independiente.",
            ),
            links=(
                ("instagram.com/p/ID/", "Una publicación con una foto o un carrusel. El parámetro ?igsh= de Compartir no afecta."),
            ),
            sections=(
                ("La imagen tal como la publica Instagram", (
                    "La herramienta descarga el archivo de imagen que Instagram expone para cada elemento, sin recortarlo, ampliarlo ni recomprimirlo. No crea una resolución mayor que la publicada ni extrae fotogramas de un vídeo. Si una publicación solo tiene vídeos, no aparece ninguna foto.",
                    "Los elementos se muestran sin tamaño estimado. Para convertir después tu propia imagen a otro formato o tamaño, usa las herramientas de imagen del sitio.",
                )),
                ("Carruseles y publicaciones mixtas", (
                    "En un carrusel, cada foto accesible aparece como una fila propia, hasta un máximo de 12. Si el carrusel mezcla fotos y vídeos, esta página solo muestra las fotos; para ver también los vídeos, usa el descargador de Instagram general. Instagram puede mostrar menos elementos a un visitante sin cuenta que en la aplicación.",
                )),
                ("Por qué una foto pública puede fallar", (
                    "Instagram suele redirigir los accesos automáticos a sus fotos hacia la página de inicio de sesión. Cuando eso ocurre no hay resultado, aunque la publicación se vea en tu aplicación. SaveFromNet no usa tu cuenta ni accede a perfiles privados; prueba más tarde o comprueba el enlace en una ventana privada.",
                )),
            ),
            faq=(
                ("¿Puedo pegar un enlace de Reel?", "No. Los Reels son vídeos y tienen su propio descargador. Esta página acepta enlaces /p/ y muestra solo imágenes."),
                ("¿Por qué no aparece el tamaño de la foto?", "El servidor no lo conoce antes de descargarla; por eso la fila indica «Tamaño desconocido»."),
                ("¿Puedo descargar la foto de perfil o una historia?", "No en esta página. Solo se aceptan publicaciones /p/."),
                ("¿Puedo descargar todas las fotos de una vez?", "No. Cada foto se prepara y se guarda por separado; no se crea un ZIP. Pulsa «Preparar descarga» para cada una que necesites."),
                ("¿En qué formato se guarda la foto?", "En el que expone Instagram, habitualmente JPG. La extensión aparece en cada fila antes de descargar, y el archivo no se convierte."),
            ),
            see_also=(
                ("instagram-downloader", "Fotos y vídeos juntos: descargador de Instagram"),
                ("instagram-reels-downloader", "Reels de Instagram"),
                ("pinterest-video-downloader", "Imágenes de un Pin de Pinterest"),
            ),
        ),
        "tiktok-downloader": LocalizedGuide(
            facts=(
                ("Enlaces", "Un vídeo /video/, una publicación de fotos /photo/ o un enlace corto vm.tiktok.com"),
                ("Opciones", "Vídeo y sonido para los vídeos; imágenes, hasta 12, para las fotos"),
                ("Límite", "Un enlace cada vez; archivos de hasta 512 MB"),
            ),
            steps=(
                "En TikTok, toca Compartir en el vídeo o en la publicación de fotos y elige Copiar enlace. Normalmente obtendrás un enlace corto vm.tiktok.com o la dirección completa.",
                "Pégalo arriba y pulsa «Analizar enlace». Un vídeo pasa por el extractor de vídeo; una publicación /photo/ se lee como una galería de imágenes.",
                "Revisa la tarjeta: filas de vídeo y de audio para un vídeo, o imágenes numeradas para una publicación de fotos. Elige una y pulsa «Preparar descarga».",
                "Guarda el archivo cuando esté listo. Si TikTok bloquea la consulta, vuelve a intentarlo más tarde.",
            ),
            links=(
                ("tiktok.com/@USUARIO/video/ID", "Un vídeo concreto; el identificador es numérico."),
                ("tiktok.com/@USUARIO/photo/ID", "Una publicación de fotos (carrusel)."),
                ("vm.tiktok.com/ID", "El enlace corto de Compartir; también vt.tiktok.com/ID y tiktok.com/t/ID."),
            ),
            sections=(
                ("Vídeos y publicaciones de fotos", (
                    "Para un vídeo, la tarjeta muestra los archivos de vídeo que devuelve TikTok, con su altura y, cuando hay datos, su tamaño. Si el vídeo tiene sonido, aparece también un MP3 convertido, y la pista de audio original cuando TikTok la entrega por separado.",
                    "Para una publicación /photo/, la tarjeta muestra las imágenes originales numeradas, hasta 12, con su extensión real y sin tamaño estimado. La música de una publicación de fotos no se ofrece aquí.",
                )),
                ("Enlaces cortos", (
                    "Los enlaces vm.tiktok.com, vt.tiktok.com y tiktok.com/t/ se tratan siempre como vídeo. Si un enlace corto lleva a una publicación de fotos y el análisis falla, ábrelo en el navegador y copia la dirección completa con /photo/.",
                )),
                ("Cuando TikTok bloquea la consulta", (
                    "TikTok limita a veces las peticiones desde centros de datos aunque la publicación se vea en tu móvil. Las publicaciones eliminadas, privadas, con restricción de región o reservadas a usuarios con sesión también fallan. SaveFromNet no inicia sesión ni evita esas restricciones; si aparece «No se pudo acceder a esta publicación pública.», prueba más tarde.",
                )),
            ),
            faq=(
                ("¿Qué enlace de TikTok debo pegar?", "El de un vídeo o una publicación de fotos concreta, o su enlace corto. Un perfil, la página Para ti o una búsqueda no identifican un archivo."),
                ("¿Puedo descargar las fotos de un carrusel de TikTok?", "Sí, con la dirección /photo/. Se listan hasta 12 imágenes, y cada una se prepara por separado."),
                ("¿Puedo descargar historias de TikTok aquí?", "No. Esta página acepta vídeos y publicaciones de fotos. El descargador universal acepta enlaces de historias públicas, aunque muchas exigen iniciar sesión o ya han caducado."),
                ("¿Por qué las fotos no indican tamaño?", "Las imágenes de una publicación de fotos se listan antes de descargarlas, así que el servidor aún no conoce su tamaño y la fila muestra «Tamaño desconocido»."),
            ),
            see_also=(
                ("tiktok-to-mp3", "Solo el sonido: convertidor de TikTok a MP3"),
                ("universal-video-downloader", "Historias y otras plataformas: descargador universal"),
                ("instagram-reels-downloader", "Reels de Instagram"),
            ),
        ),
        "tiktok-to-mp3": LocalizedGuide(
            facts=(
                ("Enlaces", "Un vídeo público: tiktok.com/@usuario/video/ID o un enlace corto"),
                ("Resultado", "Una sola opción: MP3 convertido a partir del sonido del vídeo"),
                ("Límite", "Un vídeo cada vez; las publicaciones de fotos no se aceptan"),
            ),
            steps=(
                "En TikTok, toca Compartir en el vídeo y elige Copiar enlace.",
                "Pégalo arriba y pulsa «Analizar enlace». El servidor comprueba si el vídeo tiene una pista de sonido accesible.",
                "Si la tiene, aparece la fila «Converted MP3». Pulsa «Preparar descarga»; durante «Extrayendo audio», el servidor convierte el sonido con ffmpeg.",
                "Guarda el MP3 cuando aparezca «Guardar archivo».",
            ),
            links=(
                ("tiktok.com/@USUARIO/video/ID", "Un vídeo concreto."),
                ("vm.tiktok.com/ID", "El enlace corto de Compartir; también vt.tiktok.com/ID y tiktok.com/t/ID."),
            ),
            sections=(
                ("De dónde sale el MP3", (
                    "El servidor toma el sonido que TikTok entrega con el vídeo y lo convierte a MP3 con ffmpeg. Es el audio de ese clip tal como se publicó, con la música o la voz que se oiga en él; no se busca la canción original en otro servicio.",
                    "La fila MP3 no indica tamaño porque el archivo se crea al convertir. Tampoco se promete una tasa de bits fija: convertir no recupera calidad que falte en el original.",
                )),
                ("Qué no se puede convertir", (
                    "Las publicaciones de fotos (/photo/) no se aceptan en esta página, y un clip sin pista de sonido no produce un MP3. Tampoco los vídeos eliminados, privados, con restricción de región o reservados a usuarios con sesión.",
                    "Un enlace corto se trata como vídeo. Si lleva a una publicación de fotos, el análisis fallará: para las imágenes, usa el descargador de TikTok con la dirección /photo/.",
                )),
                ("Uso responsable del audio", (
                    "La música de muchos vídeos de TikTok pertenece a terceros. Descarga solo audio propio o que tengas permiso para usar como piensas hacerlo.",
                )),
            ),
            faq=(
                ("¿Cómo convierto un TikTok a MP3?", "Pega el enlace del vídeo, pulsa «Analizar enlace», elige «Converted MP3» y pulsa «Preparar descarga». Cuando termine, guarda el archivo."),
                ("¿Por qué no aparece la opción MP3?", "El vídeo no tiene una pista de sonido accesible o TikTok ha bloqueado la consulta. Si el enlace es de una publicación de fotos, la página lo rechaza."),
                ("¿Puedo convertir el sonido de una publicación de fotos?", "No. Esta página solo acepta vídeos."),
                ("¿Puedo obtener el audio original sin convertir?", "Aquí no: esta página solo ofrece el MP3. El descargador de TikTok muestra la pista original cuando TikTok la entrega por separado."),
                ("¿Funciona en el móvil?", "Sí. Copia el enlace en la aplicación de TikTok, pégalo en esta página desde el navegador del teléfono y guarda el MP3; la carpeta de destino depende de tu navegador."),
            ),
            see_also=(
                ("tiktok-downloader", "Vídeo y fotos: descargador de TikTok"),
                ("youtube-to-mp3", "Convertidor de YouTube a MP3"),
            ),
        ),
        "reddit-video-downloader": LocalizedGuide(
            facts=(
                ("Enlaces", "El enlace permanente de una publicación: reddit.com/r/comunidad/comments/ID/ o redd.it/ID"),
                ("Opciones", "Archivos de vídeo por altura, con sonido cuando Reddit lo ofrece"),
                ("Límite", "Una publicación cada vez; archivos de hasta 512 MB"),
            ),
            steps=(
                "Abre la publicación con el vídeo y copia su dirección desde la barra del navegador. Debe contener /comments/ seguido del identificador.",
                "Pégala arriba y pulsa «Analizar enlace». El detector valida el dominio y la ruta y quita los parámetros de seguimiento antes de consultar Reddit.",
                "Elige una de las filas de vídeo. Por defecto queda marcada la mejor opción de hasta 1080 píxeles de altura.",
                "Pulsa «Preparar descarga». Si Reddit separa imagen y sonido, verás «Combinando vídeo y audio» antes de «Guardar archivo».",
            ),
            links=(
                ("reddit.com/r/COMUNIDAD/comments/ID/", "El enlace permanente de una publicación; puede llevar el título detrás."),
                ("reddit.com/user/USUARIO/comments/ID/", "Una publicación hecha en un perfil de usuario."),
                ("redd.it/ID", "El enlace corto de una publicación."),
                ("old.reddit.com/r/COMUNIDAD/comments/ID/", "La interfaz antigua de Reddit; se trata igual."),
            ),
            sections=(
                ("Enlaces de Compartir con /s/", (
                    "La aplicación de Reddit suele copiar enlaces del tipo reddit.com/r/comunidad/s/código. Esa forma no identifica la publicación y el detector la rechaza. Abre el enlace en el navegador, espera a que cargue la publicación y copia la dirección que contiene /comments/.",
                )),
                ("Vídeo con sonido", (
                    "Reddit suele guardar la imagen y el sonido de sus vídeos por separado. Cuando las dos pistas son públicas y compatibles, el servidor las descarga y las une en un solo MP4. Si la publicación no tiene ninguna pista de sonido, las filas se marcan con «no audio»: la conversión no puede inventar voz ni música.",
                )),
                ("Qué publicaciones no funcionan", (
                    "Las publicaciones eliminadas, privadas, en cuarentena o marcadas para adultos pueden no estar disponibles sin cuenta. Una publicación de texto o de imagen no contiene vídeo, y una que enlaza a YouTube u otro sitio no aloja el vídeo en Reddit: usa la herramienta de esa plataforma.",
                )),
            ),
            faq=(
                ("¿Cómo descargo un vídeo de Reddit?", "Copia el enlace permanente de la publicación, pégalo arriba, pulsa «Analizar enlace», elige una fila de vídeo y pulsa «Preparar descarga». Guarda el archivo cuando esté listo."),
                ("¿Por qué se rechaza mi enlace de la aplicación?", "Probablemente es un enlace /s/ de Compartir. Ábrelo en el navegador y copia la dirección con /comments/."),
                ("¿Sirve el enlace de una comunidad o de un perfil?", "No. Una comunidad r/… o un perfil contienen muchas publicaciones; pega el enlace de una sola."),
                ("¿Puedo guardar solo el sonido de un vídeo de Reddit?", "En esta página no: solo muestra vídeo. El descargador universal enseña también el audio original y un MP3 cuando la publicación tiene sonido."),
            ),
            see_also=(
                ("universal-video-downloader", "Otras plataformas en un solo campo"),
                ("youtube-video-downloader", "Vídeos de YouTube enlazados desde Reddit"),
            ),
        ),
        "threads-video-downloader": LocalizedGuide(
            facts=(
                ("Enlaces", "Una publicación pública: threads.com/@usuario/post/ID"),
                ("Resultado", "Como máximo un vídeo MP4 de origen"),
                ("Límite", "Una publicación cada vez; archivos de hasta 512 MB"),
            ),
            steps=(
                "En Threads, abre la publicación, toca Compartir y elige Copiar enlace, o copia la dirección desde el navegador.",
                "Pégala arriba y pulsa «Analizar enlace». El servidor lee los metadatos públicos de esa publicación, los mismos que usan las vistas previas de enlaces.",
                "Si encuentra un vídeo alojado en los servidores de Meta, la tarjeta muestra una fila «Source video» en MP4.",
                "Pulsa «Preparar descarga» y guarda el archivo, que se llama threads-video.mp4. Hazlo pronto: el acceso al archivo de origen puede cambiar.",
            ),
            links=(
                ("threads.com/@USUARIO/post/ID", "Una publicación concreta. El parámetro ?xmt= que añade Compartir no afecta."),
                ("threads.net/@USUARIO/post/ID", "La dirección antigua; se convierte a threads.com antes del análisis."),
            ),
            sections=(
                ("Por qué hay una sola opción", (
                    "Threads no tiene un extractor estable como YouTube. SaveFromNet lee la etiqueta de vídeo de los metadatos públicos de la página y solo la acepta si el archivo está en los servidores de medios de Meta. Esa etiqueta apunta a un único MP4, así que no hay lista de resoluciones, ni duración, ni tamaño previo.",
                    "Si la publicación tiene varios vídeos o mezcla fotos y vídeo, solo puede ofrecerse el que aparezca en esos metadatos. Las fotos de Threads no se descargan con esta herramienta.",
                )),
                ("Por qué el resultado puede estar vacío", (
                    "Muchas publicaciones con vídeo no incluyen esa etiqueta para visitantes sin cuenta, y Threads puede redirigir al inicio de sesión. En ese caso la página indica que no hay un vídeo público. Los perfiles y los feeds no son enlaces a una publicación.",
                )),
                ("Si la preparación falla", (
                    "La dirección del archivo que publica Meta es temporal. Si la preparación termina con un error porque el vídeo de origen ya no está disponible, vuelve a analizar el enlace para obtener una dirección nueva y prepara la descarga enseguida. El vídeo se transfiere tal cual, sin convertirlo, y la descarga se detiene si supera 512 MB.",
                )),
            ),
            faq=(
                ("¿Qué enlace de Threads debo pegar?", "El de una publicación concreta, con la forma threads.com/@usuario/post/ID. Los enlaces threads.net también sirven."),
                ("¿Puedo descargar fotos de Threads?", "No. Esta herramienta solo busca un vídeo en los metadatos públicos de la publicación."),
                ("¿Por qué el archivo se llama threads-video.mp4?", "El servidor guarda siempre los vídeos de Threads con ese nombre; puedes cambiarlo después en tu dispositivo."),
                ("¿El vídeo tendrá sonido?", "Se descarga el MP4 tal como lo publica Meta, sin combinar ni convertir nada: si el archivo de origen tiene sonido, lo conserva."),
                ("¿Funciona en el móvil?", "Sí. Copia el enlace con Compartir en la aplicación de Threads, pégalo aquí desde el navegador del teléfono y guarda el archivo cuando esté listo."),
            ),
            see_also=(
                ("instagram-reels-downloader", "Reels de Instagram"),
                ("facebook-video-downloader", "Vídeos de Facebook"),
                ("universal-video-downloader", "Otras plataformas en un solo campo"),
            ),
        ),
        "dailymotion-video-downloader": LocalizedGuide(
            facts=(
                ("Enlaces", "Un vídeo público: dailymotion.com/video/ID o dai.ly/ID"),
                ("Opciones", "Alturas en MP4 o WebM devueltas para ese vídeo"),
                ("Límite", "Un vídeo cada vez; archivos de hasta 512 MB"),
            ),
            steps=(
                "Abre el vídeo en Dailymotion y copia su dirección o el enlace corto dai.ly del botón Compartir.",
                "Pégalo arriba y pulsa «Analizar enlace». Un enlace dai.ly se convierte primero en la dirección dailymotion.com/video/ del mismo vídeo.",
                "Compara las alturas disponibles. Por defecto queda marcada la mejor opción de hasta 1080 píxeles; puedes elegir otra.",
                "Pulsa «Preparar descarga» y guarda el archivo cuando aparezca «Guardar archivo».",
            ),
            links=(
                ("dailymotion.com/video/ID", "La página de un vídeo; el identificador suele empezar por x."),
                ("dai.ly/ID", "El enlace corto que genera Compartir."),
            ),
            sections=(
                ("Cómo leer las calidades", (
                    "Dailymotion puede ofrecer varias alturas del mismo vídeo. Cada fila indica el contenedor, la altura y, cuando la fuente informa de la tasa de bits y la duración, un tamaño aproximado marcado con ≈. Que el reproductor muestre una calidad no garantiza que un descargador sin cuenta reciba el mismo archivo.",
                    "Una altura mayor suele ocupar más, pero el códec y la tasa de bits también cuentan. Las opciones que superarían 512 MB no aparecen, lo que puede dejar fuera las calidades altas de un vídeo largo.",
                )),
                ("Enlaces que no identifican un vídeo", (
                    "Los canales, las listas de reproducción y las búsquedas no son enlaces a un vídeo concreto, y el detector los rechaza. Los vídeos privados, eliminados o bloqueados por región tampoco se procesan; en ese último caso, la página indica que el contenido no está disponible en la región del servidor.",
                )),
                ("Sonido y archivo final", (
                    "Las calidades de Dailymotion suelen llegar con la imagen y el sonido juntos, así que normalmente no hace falta combinar pistas. Si la fuente no ofrece ninguna pista de sonido, la fila se marca con «no audio» en lugar de presentarse como un vídeo completo. El archivo se guarda en el contenedor que indica la fila.",
                )),
            ),
            faq=(
                ("¿Funciona un enlace dai.ly?", "Sí. Se convierte a la dirección del vídeo en dailymotion.com antes del análisis."),
                ("¿Por qué el tamaño aparece como desconocido?", "Dailymotion no siempre da la tasa de bits o la duración necesarias. Mostrar «Tamaño desconocido» es más fiel que inventar una cifra."),
                ("¿Puedo descargar una lista de reproducción?", "No. Analiza cada vídeo con su propio enlace."),
                ("¿Puedo descargar un vídeo privado o protegido con contraseña?", "No. Solo se procesan vídeos públicos que se pueden ver sin iniciar sesión ni introducir una contraseña."),
                ("¿Funciona en el móvil?", "Sí. Copia el enlace con Compartir en la aplicación de Dailymotion, pégalo en esta página desde el navegador y guarda el archivo; la carpeta depende de tu navegador."),
            ),
            see_also=(
                ("universal-video-downloader", "Otras plataformas en un solo campo"),
                ("youtube-video-downloader", "Vídeos de YouTube"),
            ),
        ),
    },
    "fr": {
        "youtube-downloader": LocalizedGuide(
            facts=(
                ("Liens", "Une vidéo ou un Short public : youtube.com/watch, youtu.be ou youtube.com/shorts"),
                ("Choix", "Vidéo MP4 ou WebM avec le son, audio d'origine et MP3 converti, selon la source"),
                ("Limite", "Un contenu à la fois ; fichiers préparés jusqu'à 512 Mo"),
            ),
            steps=(
                "Ouvrez sur YouTube la vidéo ou le Short que vous avez le droit d'enregistrer, puis copiez son adresse depuis la barre du navigateur ou via Partager > Copier le lien.",
                "Collez-la dans le champ ci-dessus et cliquez sur « Analyser le lien ». Le serveur interroge ce seul contenu ; avec YouTube, l'analyse peut prendre quelques secondes.",
                "Comparez les lignes de la fiche : vidéos avec leur hauteur et leur taille, audio d'origine et MP3. Choisissez-en une, puis cliquez sur « Préparer le téléchargement ».",
                "Quand la barre atteint « Terminé », cliquez sur « Enregistrer le fichier ». Votre navigateur choisit le dossier de destination.",
            ),
            links=(
                ("youtube.com/watch?v=ID", "La page classique d'une vidéo. Si le lien contient &list= ou &t=, seule la vidéo désignée par v= est analysée, en entier."),
                ("youtu.be/ID", "Le lien court du bouton Partager. Le paramètre ?si= ajouté par l'application ne change rien."),
                ("youtube.com/shorts/ID", "Un Short précis, pas le fil des Shorts ni l'onglet Shorts d'une chaîne."),
                ("m.youtube.com/watch?v=ID", "La version mobile du site, copiée depuis le navigateur du téléphone."),
                ("music.youtube.com/watch?v=ID", "Un titre public de YouTube Music ; ceux réservés aux abonnés ne sont pas accessibles."),
            ),
            sections=(
                ("Vidéo ou audio : ce que propose le convertisseur", (
                    "Cette page ne filtre pas le résultat : elle affiche ensemble les fichiers vidéo, la piste audio d'origine et la conversion MP3 que le serveur peut préparer pour ce lien. C'est le bon choix lorsque vous ne savez pas encore s'il vous faut l'image ou seulement le son. Sinon, le téléchargeur de vidéos ou le convertisseur MP3 affichent une liste plus courte.",
                    "Chaque ligne vidéo indique le conteneur (MP4 ou WebM), la hauteur en pixels et, quand la source fournit assez de données, la taille. Le signe ≈ signale une estimation ; « Taille inconnue » signifie qu'aucune donnée fiable n'est disponible, pas que le fichier est vide.",
                )),
                ("Pourquoi les choix varient d'une vidéo à l'autre", (
                    "YouTube stocke l'image et le son de la plupart des vidéos dans des pistes séparées. Le serveur n'affiche une ligne vidéo que s'il trouve une piste audio compatible à y associer : les MP4 sont réunis avec un audio M4A, les WebM avec un audio WebM. Sur YouTube, une vidéo muette n'est jamais proposée comme fichier complet.",
                    "Les options qui dépasseraient 512 Mo n'apparaissent pas, et la liste s'arrête à 2160 pixels de hauteur. Une longue vidéo peut donc être privée de 4K ou de 1080p ici, même si le lecteur YouTube les propose.",
                )),
                ("Audio d'origine et MP3", (
                    "La ligne « Original audio » est la piste sonore telle que YouTube la fournit, généralement en M4A ou en WebM, sans réencodage. « Converted MP3 » est créé avec ffmpeg à partir de cette même piste : il est plus compatible avec les anciens lecteurs, mais n'améliore pas la qualité. La ligne MP3 n'indique pas de taille, car le fichier n'existe qu'après la conversion.",
                )),
                ("Ce qui n'est pas pris en charge", (
                    "Les playlists entières, les films loués ou achetés, les contenus protégés par DRM, les vidéos privées et les directs en cours ne sont pas traités. Une vidéo soumise à une limite d'âge ou de région, ou bloquée par YouTube pour les accès sans compte, peut échouer même si elle s'affiche dans votre navigateur connecté.",
                )),
            ),
            faq=(
                ("Quelle différence avec le téléchargeur de vidéos YouTube ?", "Les deux pages utilisent la même analyse. Celle-ci affiche ensemble la vidéo, l'audio d'origine et le MP3 ; le téléchargeur de vidéos ne garde que les lignes vidéo et n'accepte pas les liens /shorts/, qui ont leur propre page."),
                ("Est-ce que ça fonctionne sur mobile ?", "Oui. Le formulaire fonctionne dans les navigateurs récents sur Android et iPhone. Copiez le lien dans l'application YouTube via Partager > Copier le lien, collez-le ici, puis enregistrez le fichier une fois prêt ; le dossier dépend de votre navigateur."),
                ("Combien de temps le fichier préparé reste-t-il disponible ?", "Environ une heure, et il peut disparaître plus tôt si le serveur redémarre. En attendant, il figure dans « Téléchargements récents de ce navigateur », d'où vous pouvez l'enregistrer de nouveau."),
                ("Pourquoi un lien qui s'affiche sur YouTube échoue-t-il ici ?", "Le serveur interroge YouTube sans compte. Une vidéo privée, supprimée, en direct, soumise à une limite d'âge ou de région, ou bloquée pour les accès automatisés peut ne renvoyer aucune option. Nous n'utilisons pas votre session et ne contournons pas ces contrôles."),
            ),
            see_also=(
                ("youtube-video-downloader", "Vidéo seule : téléchargeur de vidéos YouTube"),
                ("youtube-to-mp3", "Son seul : convertisseur YouTube en MP3"),
                ("youtube-to-mp4", "Fichiers MP4 seulement : convertisseur YouTube en MP4"),
                ("youtube-shorts-downloader", "Liens /shorts/ : téléchargeur de YouTube Shorts"),
            ),
        ),
        "youtube-video-downloader": LocalizedGuide(
            facts=(
                ("Liens", "Une vidéo publique : youtube.com/watch?v= ou youtu.be"),
                ("Choix", "Fichiers vidéo MP4 ou WebM avec le son, selon la vidéo"),
                ("Limite", "Une vidéo terminée à la fois, jusqu'à 512 Mo"),
            ),
            steps=(
                "Copiez le lien d'une seule vidéo publique qui vous appartient ou que vous avez le droit d'enregistrer : l'adresse watch?v= du navigateur ou le lien youtu.be du bouton Partager.",
                "Collez-le ci-dessus et cliquez sur « Analyser le lien ». La fiche affiche le titre, la chaîne, la durée et les lignes vidéo que le serveur peut préparer.",
                "Choisissez une ligne. Par défaut, la meilleure option jusqu'à 1080 pixels de hauteur est cochée, pour qu'un clic rapide ne lance pas un énorme fichier 4K ; vous pouvez en choisir une autre.",
                "Cliquez sur « Préparer le téléchargement ». Pendant l'étape « Fusion vidéo et audio », le serveur assemble les pistes ; dès que « Enregistrer le fichier » apparaît, téléchargez-le depuis votre navigateur.",
            ),
            links=(
                ("youtube.com/watch?v=ID", "La page d'une vidéo. Les paramètres &list= et &t= sont ignorés : la vidéo complète désignée par v= est préparée."),
                ("youtu.be/ID", "Le lien court du bouton Partager, y compris avec ?si= à la fin."),
                ("m.youtube.com/watch?v=ID", "L'adresse copiée depuis le navigateur du téléphone."),
                ("youtube.com/embed/ID", "L'adresse d'une vidéo intégrée dans un autre site."),
            ),
            sections=(
                ("Lire la fiche de résultats", (
                    "Chaque ligne indique le conteneur et la hauteur (par exemple 720p ou 1080p) et, quand YouTube les fournit, les dimensions en pixels, le débit approximatif et la taille. Le signe ≈ indique une taille estimée ; « Taille inconnue » apparaît quand YouTube ne fournit pas assez de données pour la vidéo complète avec son audio.",
                    "Le chiffre le plus élevé n'est pas toujours le meilleur choix. Prenez le fichier que votre appareil peut lire et stocker : un 1080p d'une longue vidéo peut peser plusieurs centaines de Mo.",
                )),
                ("MP4 ou WebM", (
                    "YouTube peut proposer la même hauteur en MP4 et en WebM. Chaque MP4 est associé à un audio M4A et chaque WebM à un audio WebM : le fichier final garde le conteneur choisi. Le MP4 est généralement le plus compatible avec les téléphones, téléviseurs et logiciels de montage ; le WebM s'ouvre dans les navigateurs récents et dans des lecteurs comme VLC.",
                    "Renommer un .webm en .mp4 ne convertit pas la vidéo : le codec reste le même et certains logiciels refuseront de l'ouvrir.",
                )),
                ("1080p, 4K et la limite de 512 Mo", (
                    "Les hautes résolutions arrivent sans son, et le serveur ne les propose que s'il peut y associer une piste audio compatible. Les options qui dépasseraient 512 Mo ou 2160 pixels de hauteur sont aussi écartées : pas de 8K, et une longue vidéo peut perdre la 4K ou le 1080p.",
                    "Si la résolution attendue n'apparaît pas, choisissez la plus haute que la fiche affiche réellement. Qu'un lecteur YouTube propose la 4K ne signifie pas qu'un fichier 4K est téléchargeable ici.",
                )),
                ("Shorts, playlists et directs", (
                    "Cette page accepte uniquement les vidéos classiques. Un lien youtube.com/shorts/ est refusé avec un message : utilisez le téléchargeur de YouTube Shorts. Les playlists, vidéos privées, locations et directs en cours ne sont pas traités, et une vidéo limitée par âge ou par région peut échouer pour un serveur sans compte.",
                )),
            ),
            faq=(
                ("Comment télécharger une vidéo YouTube ?", "Collez le lien watch?v= ou youtu.be d'une vidéo publique, cliquez sur « Analyser le lien », choisissez une ligne vidéo puis « Préparer le téléchargement ». Une fois terminé, enregistrez le fichier temporaire. Ne téléchargez que vos vidéos ou celles que vous êtes autorisé à enregistrer."),
                ("La vidéo téléchargée aura-t-elle du son ?", "Oui. Sur YouTube, seules les lignes que le serveur peut associer à une piste audio compatible sont proposées. Une vidéo sans audio accessible n'apparaît pas comme fichier complet."),
                ("Puis-je coller un lien de Short ?", "Pas sur cette page. Les liens /shorts/ ont leur propre téléchargeur, et le téléchargeur et convertisseur YouTube général accepte les deux."),
                ("Pourquoi une vidéo publique échoue-t-elle ?", "Elle peut être supprimée, privée, limitée par âge ou par région, en direct ou bloquée pour les accès automatisés sans compte. L'outil n'utilise pas votre compte et ne contourne pas ces contrôles."),
            ),
            see_also=(
                ("youtube-shorts-downloader", "Liens /shorts/ : téléchargeur de YouTube Shorts"),
                ("youtube-to-mp4", "Lignes MP4 seulement : convertisseur YouTube en MP4"),
                ("youtube-to-mp3", "Le son seul : convertisseur YouTube en MP3"),
                ("youtube-downloader", "Vidéo et audio ensemble : téléchargeur et convertisseur YouTube"),
            ),
        ),
        "youtube-shorts-downloader": LocalizedGuide(
            facts=(
                ("Liens", "Un Short public au format youtube.com/shorts/ID"),
                ("Choix", "Fichiers vidéo MP4 ou WebM avec le son renvoyés pour ce Short"),
                ("Limite", "Un Short à la fois ; fichiers jusqu'à 512 Mo"),
            ),
            steps=(
                "Dans l'application YouTube, ouvrez le Short, touchez Partager puis Copier le lien. Sur ordinateur, copiez l'adresse youtube.com/shorts/ dans la barre du navigateur.",
                "Collez le lien ci-dessus et cliquez sur « Analyser le lien ». Le serveur vérifie que le chemin contient /shorts/ suivi de l'identifiant de 11 caractères.",
                "Examinez les lignes vidéo : conteneur, hauteur, dimensions et taille. Choisissez-en une et cliquez sur « Préparer le téléchargement ».",
                "Quand la barre atteint « Terminé », cliquez sur « Enregistrer le fichier ». Votre navigateur décide de l'emplacement, en général le dossier Téléchargements.",
            ),
            links=(
                ("youtube.com/shorts/ID", "Le lien d'un Short précis, avec ou sans le paramètre ?si= ajouté par Partager."),
                ("m.youtube.com/shorts/ID", "La même adresse copiée depuis le navigateur du téléphone."),
            ),
            sections=(
                ("Pourquoi cette page demande un lien /shorts/", (
                    "Le détecteur ne classe un lien comme Short que si son chemin est /shorts/ suivi de l'identifiant. Si vous collez ici la version youtu.be ou watch?v= du même clip, elle est traitée comme une vidéo classique et la page vous indique qu'il faut un autre outil : utilisez le téléchargeur de vidéos YouTube ou le téléchargeur général, qui accepte les deux.",
                    "Un fil de Shorts, l'onglet Shorts d'une chaîne, une recherche ou une playlist ne désignent pas un fichier unique et sont refusés.",
                )),
                ("Les formats d'un Short vertical", (
                    "La plupart des Shorts sont verticaux : la hauteur est alors généralement le plus grand des deux chiffres. L'étiquette de chaque ligne correspond à la hauteur en pixels déclarée par YouTube, et la fiche affiche aussi largeur × hauteur pour vérifier l'orientation. Une même hauteur peut exister en MP4 et en WebM ; le MP4 est généralement le plus compatible avec les téléphones et les logiciels de montage.",
                    "Comme pour les vidéos classiques, le serveur assemble l'image et le son avant de vous remettre le fichier et n'affiche que les lignes qu'il peut associer à un audio. Les options de plus de 512 Mo ou de plus de 2160 pixels de hauteur n'apparaissent pas.",
                )),
                ("Seulement le son d'un Short", (
                    "Cette page n'affiche que des fichiers vidéo. Pour l'audio, collez le même lien /shorts/ dans le convertisseur YouTube en MP3 : l'option MP3 y apparaît si le Short possède une piste sonore accessible. Un clip muet ne peut pas devenir de la musique ou de la parole.",
                )),
                ("Quand un Short ne propose aucun fichier", (
                    "Un Short supprimé, privé, limité par âge, en direct ou bloqué pour les accès sans compte peut ne rien renvoyer au serveur. Modifier l'URL ne crée pas un format absent. Si l'analyse expire parce que la fiche est restée ouverte plus de dix minutes, collez de nouveau le lien.",
                )),
            ),
            faq=(
                ("Comment télécharger un Short YouTube ?", "Copiez le lien youtube.com/shorts/ d'un Short public, collez-le ci-dessus et cliquez sur « Analyser le lien ». Choisissez une ligne vidéo, cliquez sur « Préparer le téléchargement » puis enregistrez le fichier une fois prêt."),
                ("Puis-je coller un fil de Shorts ou une chaîne ?", "Non. Utilisez le lien d'un Short individuel. Un fil ou une chaîne contient de nombreuses vidéos et ne désigne pas le fichier à préparer."),
                ("Pourquoi mon lien youtu.be ne fonctionne-t-il pas ici ?", "Parce qu'un lien youtu.be ou watch?v= est classé comme vidéo classique. Collez-le dans le téléchargeur de vidéos YouTube, ou copiez l'adresse /shorts/ du Short."),
                ("Est-ce que ça fonctionne sur téléphone ?", "Oui, depuis le navigateur du téléphone. Copiez le lien dans l'application YouTube, collez-le sur cette page et enregistrez le fichier ; votre navigateur choisit le dossier de destination."),
            ),
            see_also=(
                ("youtube-to-mp3", "Le son du Short en MP3"),
                ("youtube-video-downloader", "Vidéos classiques avec un lien watch ou youtu.be"),
                ("youtube-downloader", "Vidéo et audio sur une seule page"),
            ),
        ),
        "instagram-reels-downloader": LocalizedGuide(
            facts=(
                ("Liens", "Un Reel public : instagram.com/reel/ID/"),
                ("Choix", "La vidéo qu'Instagram fournit à un visiteur sans compte"),
                ("Limite", "Un Reel à la fois ; ni profils privés ni connexion"),
            ),
            steps=(
                "Dans l'application Instagram, ouvrez le Reel, touchez l'icône de partage puis Copier le lien. Sur ordinateur, copiez l'adresse du Reel ouvert.",
                "Collez-le ci-dessus et cliquez sur « Analyser le lien ». Le serveur consulte ce Reel comme le verrait une personne non connectée.",
                "Si une ligne vidéo apparaît, vérifiez l'extension, la hauteur et la taille lorsqu'elles sont indiquées, puis cliquez sur « Préparer le téléchargement ».",
                "Enregistrez le fichier dès que « Enregistrer le fichier » apparaît. Si aucune ligne ne s'affiche, le Reel n'est pas accessible publiquement.",
            ),
            links=(
                ("instagram.com/reel/ID/", "Le lien d'un Reel précis. Le paramètre ?igsh= ajouté par Partager n'a aucun effet."),
                ("instagram.com/reels/ID/", "La variante au pluriel qui apparaît parfois dans le navigateur ; elle est traitée de la même façon."),
            ),
            sections=(
                ("Le lien du Reel, pas celui de la publication", (
                    "Cette page accepte uniquement les liens /reel/ (ou /reels/). Une adresse instagram.com/p/ correspond à une publication qui peut contenir des photos, une vidéo ou un carrousel : elle s'analyse dans le téléchargeur Instagram général. Un profil, une Story ou la page Explorer ne désignent pas non plus un Reel unique.",
                )),
                ("Pourquoi un Reel visible peut échouer", (
                    "Instagram peut montrer un clip à votre navigateur connecté tout en le cachant à un serveur sans compte. Essayez d'ouvrir le lien dans une fenêtre de navigation privée sans vous connecter : si Instagram demande de se connecter, l'outil n'y aura pas accès non plus. SaveFromNet n'accepte ni mot de passe ni cookies de votre compte, et n'accède ni aux profils privés ni aux Reels supprimés.",
                )),
                ("Ce que signifie le résultat", (
                    "La fiche décrit le fichier renvoyé par la source ; elle ne promet pas toutes les qualités visibles dans l'application. Il arrive qu'Instagram ne déclare pas la hauteur : la ligne s'affiche alors comme « Source video », et la taille peut rester inconnue plutôt que d'être déduite de l'aperçu.",
                    "Si Instagram fournit l'image et le son séparément, le serveur les réunit dans un seul fichier. Si le Reel n'a aucune piste sonore, la ligne l'indique par « no audio ». L'outil ne retire pas de filigrane et ne récupère pas un contenu expiré.",
                )),
            ),
            faq=(
                ("Quel lien de Reel faut-il coller ?", "Le lien direct instagram.com/reel/ d'un Reel public. Les liens de profil, de Story ou de publication /p/ relèvent d'autres outils."),
                ("Pourquoi un Reel se lit-il sur mon téléphone mais échoue ici ?", "Votre session Instagram peut avoir un accès dont un serveur anonyme ne dispose pas. Les Reels privés, supprimés ou réservés aux comptes connectés ne peuvent pas être récupérés avec cet outil public."),
                ("Puis-je choisir la résolution du Reel ?", "Seulement parmi les lignes renvoyées par l'analyse, et il peut n'y en avoir qu'une. Aucune résolution ni taille n'est inventée."),
                ("La vidéo aura-t-elle du son ?", "Oui, si le Reel possède un audio accessible : s'il arrive séparément, le serveur l'associe à l'image. Un Reel sans piste sonore est signalé par « no audio »."),
            ),
            see_also=(
                ("instagram-downloader", "Publications /p/ et carrousels : téléchargeur Instagram"),
                ("instagram-photo-downloader", "Photos d'une publication Instagram"),
                ("facebook-video-downloader", "Vidéos et Reels Facebook"),
            ),
        ),
        "facebook-video-downloader": LocalizedGuide(
            facts=(
                ("Liens", "Une vidéo ou un Reel public : watch?v=, /videos/, /reel/, fb.watch ou /share/v/"),
                ("Choix", "Les fichiers vidéo que Facebook fournit sans connexion"),
                ("Limite", "Une publication à la fois ; fichiers jusqu'à 512 Mo"),
            ),
            steps=(
                "Ouvrez la vidéo ou le Reel sur Facebook et copiez son lien : dans l'application, via Partager puis Copier le lien ; sur ordinateur, depuis la barre d'adresse ou l'option Copier le lien du menu de la publication.",
                "Avant de le coller, vérifiez que la vidéo s'affiche dans une fenêtre de navigation privée sans connexion. Si Facebook demande de se connecter, le serveur ne la verra pas non plus.",
                "Collez le lien ci-dessus et cliquez sur « Analyser le lien ». Comparez les lignes vidéo proposées et choisissez-en une.",
                "Cliquez sur « Préparer le téléchargement » puis enregistrez le fichier quand « Enregistrer le fichier » apparaît.",
            ),
            links=(
                ("facebook.com/watch?v=ID", "La page vidéo de Facebook Watch, avec un identifiant numérique."),
                ("facebook.com/NOM/videos/ID", "Une vidéo publiée sur une Page ou un profil."),
                ("facebook.com/reel/ID", "Un Reel Facebook individuel."),
                ("fb.watch/ID", "Le lien court généré par Facebook lors du partage d'une vidéo."),
                ("facebook.com/share/v/ID", "Le lien copié par l'application via Partager ; /share/r/ID est la version pour les Reels."),
            ),
            sections=(
                ("Copiez la publication vidéo, pas le fil", (
                    "Une page vidéo, un Reel ou un lien fb.watch désignent une seule vidéo. Un profil, la page d'accueil d'une Page ou un groupe ne le font pas, et le détecteur les refuse avant même d'interroger Facebook. Les adresses m.facebook.com et web.facebook.com sont acceptées et traitées comme facebook.com.",
                )),
                ("Public pour vous ne veut pas dire public pour tous", (
                    "Une vidéo réservée aux amis ou à un groupe peut se lire dans votre compte sans être accessible à ce service anonyme. SaveFromNet ne demande pas d'identifiants Facebook et ne contourne pas les paramètres de confidentialité de l'auteur. Si la publication s'affiche sans connexion, l'analyse a les mêmes chances que n'importe quel visiteur.",
                )),
                ("Les qualités que Facebook peut renvoyer", (
                    "Facebook ne déclare pas toujours la hauteur de ses fichiers. Dans ce cas, la ligne s'affiche comme HD ou SD selon l'étiquette de la source, ou comme « Source video ». Si la hauteur est connue, vous verrez 720p ou 1080p et les dimensions en pixels. Qu'un lecteur affiche HD ne garantit pas un téléchargement HD ici.",
                    "Si l'image et le son arrivent séparément, le serveur les assemble dans la limite de 512 Mo. Si la publication n'a aucune piste sonore, la ligne l'indique par « no audio ». Une taille inconnue reste affichée comme telle au lieu d'un chiffre inventé.",
                )),
            ),
            faq=(
                ("Les Reels et les liens fb.watch fonctionnent-ils ?", "Oui. Les Reels publics /reel/, les liens fb.watch et les liens /share/v/ ou /share/r/ de l'application sont acceptés, tout comme les pages watch?v= et /videos/."),
                ("Puis-je télécharger une vidéo réservée aux amis ?", "Non. Le serveur n'utilise pas votre compte Facebook et ne contourne pas l'audience choisie par l'auteur. Vérifiez la publication sans être connecté."),
                ("Toutes les vidéos Facebook ont-elles la HD et le son ?", "Non. La hauteur et l'audio dépendent des fichiers accessibles. L'analyse n'affiche que ce qu'elle peut préparer pour cette publication."),
                ("Comment copier le lien depuis l'application ?", "Touchez Partager sous la vidéo puis Copier le lien. Vous obtenez en général une adresse facebook.com/share/ ou fb.watch, à coller directement ici."),
            ),
            see_also=(
                ("instagram-reels-downloader", "Reels Instagram"),
                ("universal-video-downloader", "Liens d'autres plateformes dans un seul champ"),
            ),
        ),
        "pinterest-video-downloader": LocalizedGuide(
            facts=(
                ("Liens", "Une épingle publique : pinterest.com/pin/ID ou pin.it"),
                ("Choix", "L'image, le GIF ou la vidéo d'origine exposés par l'épingle"),
                ("Limite", "Une épingle à la fois ; ni tableaux ni recherches"),
            ),
            steps=(
                "Ouvrez l'épingle et copiez son lien : dans l'application, touchez Partager puis Copier le lien (vous obtenez généralement un pin.it) ; sur ordinateur, copiez l'adresse pinterest.com/pin/ de la barre.",
                "Collez-le ci-dessus et cliquez sur « Analyser le lien ». Le serveur consulte les fichiers de cette épingle.",
                "Regardez le type de chaque élément : image (JPG, PNG ou WebP), GIF ou vidéo (MP4 ou WebM). Choisissez celui dont vous avez besoin.",
                "Cliquez sur « Préparer le téléchargement » et enregistrez le fichier quand il est prêt.",
            ),
            links=(
                ("pinterest.com/pin/ID/", "La page d'une épingle avec son identifiant numérique."),
                ("fr.pinterest.com/pin/ID/", "La version de Pinterest pour votre pays ; les autres sous-domaines comme es.pinterest.com ou in.pinterest.com fonctionnent aussi."),
                ("pin.it/ID", "Le lien court copié par l'application via Partager."),
            ),
            sections=(
                ("Une épingle peut être une image, un GIF ou une vidéo", (
                    "Le résultat reflète le fichier que Pinterest expose pour cette épingle. Chaque élément apparaît avec sa véritable extension et une étiquette comme « Item 1 · original » : JPG, PNG ou WebP pour les images, GIF pour les animations, MP4 ou WebM pour les vidéos. Ces éléments d'origine s'affichent sans taille estimée. Une épingle avec une image fixe ne produira pas de ligne vidéo.",
                    "Pour certaines épingles vidéo, le résultat affiche plutôt des lignes par hauteur avec le son déjà associé, ainsi que l'audio d'origine et une conversion MP3. Cela dépend de la manière dont Pinterest fournit cette vidéo.",
                )),
                ("Une animation n'est pas forcément un GIF", (
                    "L'aperçu animé d'une épingle peut être une vidéo plutôt qu'un GIF téléchargeable. Après l'analyse, vérifiez si l'élément est une image, un GIF ou une vidéo, et utilisez le type qui apparaît réellement. L'outil ne renomme pas un MP4 en GIF et ne promet pas d'animation lorsque Pinterest n'expose qu'une image.",
                )),
                ("Liens externes et tableaux", (
                    "Beaucoup d'épingles renvoient vers un autre site. Cet outil ne suit pas cette destination et ne télécharge pas les fichiers d'autres sites : il examine uniquement le contenu hébergé par Pinterest. Un tableau, une recherche ou un profil regroupent de nombreuses épingles et sont refusés ; analysez les épingles une par une.",
                )),
            ),
            faq=(
                ("Puis-je coller un tableau Pinterest ?", "Non. Collez le lien d'une épingle publique ou son lien court pin.it. Un tableau contient plusieurs épingles et ne correspond pas à un fichier unique."),
                ("Pourquoi une épingle vidéo renvoie-t-elle une image ?", "L'épingle peut n'exposer qu'une image fixe ou un aperçu, la vidéo étant hébergée ailleurs. L'outil affiche l'élément réel auquel il a accès ; il ne fabrique pas de vidéo."),
                ("Puis-je télécharger le site vers lequel renvoie une épingle ?", "Non. Seul le contenu Pinterest de cette épingle est examiné ; l'outil ne visite pas le site de destination."),
                ("Les liens fr.pinterest.com fonctionnent-ils ?", "Oui. Les sous-domaines nationaux de pinterest.com sont acceptés comme pinterest.com, à condition que l'adresse soit /pin/ suivi du numéro de l'épingle."),
            ),
            see_also=(
                ("instagram-photo-downloader", "Photos de publications Instagram"),
                ("universal-video-downloader", "Liens d'autres plateformes dans un seul champ"),
            ),
        ),
        "universal-video-downloader": LocalizedGuide(
            facts=(
                ("Plateformes", "YouTube, Instagram, TikTok, Facebook, Pinterest, Reddit, Threads et Dailymotion"),
                ("Choix", "Vidéo, audio ou images, selon ce que renvoie la source"),
                ("Limite", "Un lien à la fois ; fichiers préparés jusqu'à 512 Mo"),
            ),
            steps=(
                "Copiez le lien de la publication précise que vous voulez enregistrer, sur l'une des huit plateformes prises en charge. Vous pouvez le coller avec ou sans https:// au début.",
                "Cliquez sur « Analyser le lien ». Le détecteur reconnaît la plateforme d'après le domaine et le chemin, puis transmet le lien à l'extracteur adapté ; un domaine non pris en charge est refusé avant toute requête.",
                "Examinez la fiche : elle peut contenir des lignes vidéo, audio ou image. Choisissez l'une de celles qui s'affichent, puis cliquez sur « Préparer le téléchargement ».",
                "Quand « Enregistrer le fichier » apparaît, téléchargez-le depuis votre navigateur. Le fichier temporaire est supprimé au bout d'une heure environ.",
            ),
            links=(
                ("youtube.com/watch?v=ID", "Une vidéo YouTube ; youtu.be/ID et youtube.com/shorts/ID fonctionnent aussi."),
                ("instagram.com/p/ID/", "Une publication Instagram ; les Reels utilisent instagram.com/reel/ID/."),
                ("tiktok.com/@UTILISATEUR/video/ID", "Une vidéo TikTok ; les publications photo utilisent /photo/ID, et les liens courts vm.tiktok.com sont acceptés."),
                ("facebook.com/reel/ID", "Un Reel Facebook ; fb.watch/ID et les pages watch?v= ou /videos/ fonctionnent aussi."),
                ("pinterest.com/pin/ID/", "Une épingle ; le lien court pin.it/ID fonctionne aussi."),
                ("reddit.com/r/NOM/comments/ID/", "Une publication Reddit ; redd.it/ID fonctionne aussi."),
                ("threads.com/@UTILISATEUR/post/ID", "Une publication Threads ; les liens threads.net sont convertis en threads.com."),
                ("dailymotion.com/video/ID", "Une vidéo Dailymotion ; dai.ly/ID fonctionne aussi."),
            ),
            sections=(
                ("Ce qui distingue le téléchargeur universel", (
                    "Les pages spécialisées filtrent le résultat : le convertisseur MP3 n'affiche que le MP3, le téléchargeur de Reels que la vidéo. Cette page ne filtre rien. Elle montre tout ce que le serveur peut préparer pour le lien : vidéo, audio d'origine, conversion MP3 ou images. Elle est utile quand vous ne savez pas quel outil choisir ou que vous voulez comparer toutes les options.",
                    "Elle accepte aussi des liens que les pages en français ne couvrent pas, comme un profil Instagram public, une Story Instagram ou les Stories d'un compte TikTok. Beaucoup de ces contenus exigent une connexion et ne renvoient alors rien.",
                )),
                ("Comment le contenu de la fiche est déterminé", (
                    "YouTube, Facebook, Reddit, Dailymotion ainsi que les vidéos TikTok et Instagram passent par un extracteur qui renvoie des lignes vidéo par hauteur, en MP4 ou en WebM, plus l'audio d'origine et un MP3 quand il y a du son. Les publications Instagram, les épingles et les photos TikTok renvoient des éléments d'origine, jusqu'à 12 par lien, chacun avec sa véritable extension. Threads propose au plus une vidéo MP4.",
                    "Aucun fichier ne peut dépasser 512 Mo, et les lignes vidéo qui dépasseraient cette limite n'apparaissent même pas. La taille ne s'affiche que si la source fournit assez de données ; le signe ≈ indique une estimation.",
                )),
                ("Les liens qui ne fonctionnent pas", (
                    "Un fil, une recherche, un tableau Pinterest, une playlist ou la page d'accueil d'un réseau social ne désignent pas un fichier précis. Les publications privées, supprimées, en direct ou réservées aux comptes connectés ne sont pas traitées non plus. Si le domaine n'appartient pas à l'une des huit plateformes, la page le signale sans interroger aucun site : SaveFromNet ne télécharge pas depuis des sites arbitraires.",
                )),
            ),
            faq=(
                ("Faut-il coller le lien avec https:// ?", "Non. S'il manque, il est ajouté automatiquement. Les liens contenant un port, un nom d'utilisateur ou un mot de passe sont refusés."),
                ("Vaut-il mieux utiliser cette page ou celle de la plateforme ?", "L'analyse est la même. Cette page affiche toutes les options ensemble ; les pages spécialisées filtrent la liste et détaillent les liens de leur plateforme."),
                ("Puis-je coller plusieurs liens à la fois ?", "Non. Analysez un lien à la fois et préparez un téléchargement par ligne choisie. Si vous analysez beaucoup de liens d'affilée et que « Trop de demandes » s'affiche, attendez une minute."),
                ("Où le fichier est-il enregistré ?", "Là où votre navigateur enregistre les téléchargements. Le fichier temporaire reste environ une heure sur le serveur et figure entre-temps dans « Téléchargements récents de ce navigateur »."),
            ),
            see_also=(
                ("youtube-downloader", "YouTube : vidéo et audio"),
                ("instagram-downloader", "Publications et Reels Instagram"),
                ("tiktok-downloader", "Vidéos et photos TikTok"),
                ("facebook-video-downloader", "Vidéos et Reels Facebook"),
                ("reddit-video-downloader", "Vidéos Reddit avec le son"),
            ),
        ),
        "youtube-to-mp3": LocalizedGuide(
            facts=(
                ("Liens", "Une vidéo ou un Short public : youtube.com/watch, youtu.be ou youtube.com/shorts"),
                ("Résultat", "Une seule option : un MP3 converti depuis l'audio accessible"),
                ("Limite", "Un contenu à la fois ; fichiers jusqu'à 512 Mo"),
            ),
            steps=(
                "Ouvrez la vidéo ou le Short que vous avez le droit d'enregistrer et copiez son lien via Partager > Copier le lien ou depuis la barre du navigateur.",
                "Collez-le ci-dessus et cliquez sur « Analyser le lien ». Le serveur vérifie que ce contenu possède une piste sonore accessible.",
                "Si c'est le cas, la fiche affiche la ligne « Converted MP3 ». Cliquez sur « Préparer le téléchargement » : pendant l'étape « Extraction de l'audio », le serveur convertit le son avec ffmpeg.",
                "Quand « Enregistrer le fichier » apparaît, téléchargez le MP3. Pour une longue vidéo, la conversion prend plus de temps ; gardez la page ouverte.",
            ),
            links=(
                ("youtube.com/watch?v=ID", "La page d'une vidéo. Si le lien contient &list=, seule la vidéo désignée par v= est convertie, jamais la playlist."),
                ("youtu.be/ID", "Le lien court du bouton Partager, avec ou sans ?si=."),
                ("youtube.com/shorts/ID", "Un Short précis."),
                ("music.youtube.com/watch?v=ID", "Un titre public de YouTube Music."),
            ),
            sections=(
                ("Ce que contient le MP3", (
                    "YouTube ne fournit pas de fichiers MP3. Le serveur télécharge la meilleure piste audio accessible (généralement en M4A ou en Opus dans un WebM) et la convertit en MP3 avec ffmpeg. C'est pourquoi la fiche n'affiche qu'une ligne, « Converted MP3 », sans taille : le fichier n'existe qu'à la fin de la conversion.",
                    "Le MP3 est plus compatible avec les lecteurs, les autoradios et les anciens logiciels, mais c'est une conversion avec perte : elle ne restaure pas les détails absents de l'original, et aucun débit fixe n'est garanti.",
                )),
                ("Pour garder l'audio sans conversion", (
                    "Si vous voulez la piste d'origine sans réencodage, utilisez le téléchargeur et convertisseur YouTube : la ligne « Original audio » y apparaît avec son format réel, à côté du MP3 et des fichiers vidéo.",
                )),
                ("Problèmes fréquents", (
                    "Si le lien est refusé, vérifiez qu'il désigne une seule vidéo ou un seul Short : les playlists, chaînes et recherches ne sont pas acceptées. Si l'analyse échoue, la vidéo peut être privée, supprimée, limitée par âge ou par région, en direct ou bloquée pour les accès automatisés.",
                    "Si la ligne MP3 n'apparaît pas, le contenu n'a pas de piste sonore accessible. Si la fiche est ouverte depuis plus de dix minutes, analysez de nouveau le lien avant de préparer le téléchargement.",
                )),
            ),
            faq=(
                ("Comment convertir une vidéo YouTube en MP3 ?", "Collez le lien d'une vidéo ou d'un Short public, cliquez sur « Analyser le lien », choisissez « Converted MP3 » puis « Préparer le téléchargement ». Une fois la conversion terminée, enregistrez le fichier."),
                ("Puis-je convertir une playlist entière ?", "Non. Chaque analyse correspond à une seule vidéo ; si le lien contient &list=, la playlist est ignorée."),
                ("Pourquoi le MP3 n'indique-t-il pas de taille ?", "Parce qu'il est créé pendant la conversion. Sa taille finale dépend de la durée et de la conversion, et n'est connue qu'à la fin."),
                ("Est-ce que ça fonctionne sur téléphone ?", "Oui. Utilisez le navigateur du téléphone ; le MP3 terminé est enregistré là où votre navigateur range les téléchargements."),
            ),
            see_also=(
                ("youtube-downloader", "Audio d'origine et vidéo : téléchargeur et convertisseur YouTube"),
                ("youtube-video-downloader", "La vidéo complète : téléchargeur de vidéos YouTube"),
                ("tiktok-to-mp3", "Le son d'une vidéo TikTok en MP3"),
            ),
        ),
        "youtube-to-mp4": LocalizedGuide(
            facts=(
                ("Liens", "Une vidéo ou un Short public : youtube.com/watch, youtu.be ou youtube.com/shorts"),
                ("Résultat", "Uniquement des lignes MP4 avec le son, par hauteur"),
                ("Limite", "Un contenu à la fois ; jusqu'à 512 Mo et 2160 pixels de hauteur"),
            ),
            steps=(
                "Copiez le lien d'une seule vidéo ou d'un seul Short public que vous avez le droit d'enregistrer.",
                "Collez-le ci-dessus et cliquez sur « Analyser le lien ». La fiche n'affiche que les lignes MP4 que le serveur peut préparer pour ce contenu.",
                "Choisissez une hauteur. Par défaut, la meilleure option jusqu'à 1080 pixels est cochée ; vous pouvez en choisir une autre.",
                "Cliquez sur « Préparer le téléchargement ». Si le MP4 doit réunir l'image et le son, l'étape « Fusion vidéo et audio » s'affiche avant « Enregistrer le fichier ».",
            ),
            links=(
                ("youtube.com/watch?v=ID", "La page d'une vidéo ; &list= et &t= sont ignorés."),
                ("youtu.be/ID", "Le lien court du bouton Partager."),
                ("youtube.com/shorts/ID", "Un Short précis."),
                ("m.youtube.com/watch?v=ID", "La version mobile du site."),
            ),
            sections=(
                ("Ce que signifie une ligne MP4", (
                    "Chaque ligne est un fichier MP4 complet : une image MP4 associée à un audio M4A, ou un MP4 qui contient déjà le son. L'étiquette indique la hauteur en pixels, et la fiche ajoute les dimensions, le débit et la taille quand YouTube les fournit.",
                    "Les hautes résolutions de YouTube arrivent sans son ; le serveur ne propose donc une hauteur que s'il peut y associer une piste audio compatible. Un MP4 muet n'est jamais présenté comme complet.",
                )),
                ("Pourquoi une résolution manque", (
                    "Certaines hauteurs n'existent qu'en WebM ; cette page ne les affiche pas et ne les renomme pas en MP4. Si vous avez besoin de cette résolution en WebM, le téléchargeur de vidéos YouTube montre les deux conteneurs. Les options de plus de 512 Mo ou de plus de 2160 pixels de hauteur sont aussi écartées : une longue vidéo peut donc perdre la 4K ou le 1080p.",
                )),
                ("MP4 et compatibilité", (
                    "Le MP4 est le conteneur accepté par presque tous les téléphones, téléviseurs et logiciels de montage, d'où cette page dédiée. Le codec vidéo qu'il contient dépend toutefois de ce que publie YouTube ; si un ancien appareil ne lit pas le fichier, une hauteur plus faible ou un lecteur comme VLC peut aider.",
                )),
            ),
            faq=(
                ("Comment télécharger une vidéo YouTube en MP4 ?", "Collez le lien, cliquez sur « Analyser le lien », choisissez une ligne MP4 puis « Préparer le téléchargement ». Une fois terminé, enregistrez le fichier."),
                ("Le MP4 aura-t-il du son ?", "Oui. Seules les hauteurs que le serveur peut associer à un audio M4A, ou qui contiennent déjà le son, sont proposées."),
                ("Pourquoi aucune ligne n'apparaît-elle ?", "La vidéo n'a peut-être que du WebM dans la limite de taille, ou elle est privée, supprimée, en direct ou restreinte. Essayez le téléchargeur de vidéos YouTube pour voir tous les conteneurs."),
            ),
            see_also=(
                ("youtube-video-downloader", "MP4 et WebM : téléchargeur de vidéos YouTube"),
                ("youtube-to-mp3", "Le son seul : convertisseur YouTube en MP3"),
                ("youtube-shorts-downloader", "Liens /shorts/ : téléchargeur de YouTube Shorts"),
            ),
        ),
        "instagram-downloader": LocalizedGuide(
            facts=(
                ("Liens", "Une publication /p/ ou un Reel /reel/ publics"),
                ("Choix", "Photos, vidéos ou éléments de carrousel d'origine, jusqu'à 12"),
                ("Accès", "Uniquement ce qu'Instagram montre sans connexion"),
            ),
            steps=(
                "Dans Instagram, ouvrez la publication ou le Reel, touchez l'icône de partage puis Copier le lien.",
                "Collez-le ci-dessus et cliquez sur « Analyser le lien ». Le serveur consulte cette publication comme un visiteur non connecté.",
                "Examinez les éléments : pour une publication, ils sont numérotés (« Item 1 · original », « Item 2 · original »…) avec leur véritable extension ; pour un Reel, des lignes vidéo et, s'il y a du son, audio s'affichent.",
                "Choisissez-en un, cliquez sur « Préparer le téléchargement » et enregistrez-le. Recommencez pour chaque élément du carrousel dont vous avez besoin : chacun est préparé séparément.",
            ),
            links=(
                ("instagram.com/p/ID/", "Une publication avec photo, vidéo ou carrousel. Le paramètre ?igsh= ajouté par Partager n'a aucun effet."),
                ("instagram.com/reel/ID/", "Un Reel ; la variante instagram.com/reels/ID/ fonctionne aussi."),
                ("instagram.com/tv/ID/", "Une ancienne vidéo IGTV ; elle est traitée comme une publication."),
            ),
            sections=(
                ("Publications : chaque élément séparément", (
                    "Pour une adresse /p/, le serveur liste les éléments d'origine de la publication, jusqu'à 12, chacun avec son extension : JPG, PNG ou WebP pour les photos, MP4 ou WebM pour les vidéos. Aucun ZIP n'est créé et le carrousel n'est pas fusionné en un seul fichier. Ces éléments s'affichent sans taille estimée.",
                    "Si Instagram ne laisse pas lire les éléments, le serveur essaie l'extracteur vidéo, qui peut trouver la vidéo d'une publication publique. Les publications composées uniquement de photos n'ont pas cette seconde chance et échouent si Instagram exige une connexion.",
                )),
                ("Reels : vidéo et audio", (
                    "Un lien /reel/ est analysé par l'extracteur vidéo. La fiche peut afficher des lignes vidéo par hauteur, la piste audio d'origine et un MP3 converti lorsque le Reel a du son. Si seule la vidéo vous intéresse, le téléchargeur de Reels affiche une liste plus courte.",
                )),
                ("L'accès anonyme est décisif", (
                    "Une publication visible dans l'application avec votre compte peut être cachée à un serveur sans compte. Si Instagram demande de se connecter quand vous ouvrez le lien dans une fenêtre de navigation privée, SaveFromNet ne pourra pas la lire non plus. Aucun mot de passe ni cookie n'est utilisé, et les profils privés sont exclus.",
                )),
            ),
            faq=(
                ("Puis-je télécharger toutes les photos d'un carrousel ?", "Oui, une par une. L'analyse liste jusqu'à 12 éléments accessibles, et chacun est préparé et enregistré séparément."),
                ("Pourquoi une publication photo échoue-t-elle alors qu'un Reel fonctionne ?", "Instagram demande souvent une connexion aux accès automatisés à ses photos. Les vidéos ont un second extracteur, pas les photos ; il arrive donc qu'aucun résultat ne s'affiche."),
                ("Puis-je télécharger des Stories ici ?", "Non. Cette page accepte les publications /p/ et les Reels. Le téléchargeur universel accepte les liens de Stories publiques, mais la plupart exigent une connexion ou expirent rapidement."),
            ),
            see_also=(
                ("instagram-reels-downloader", "La vidéo d'un Reel seulement"),
                ("instagram-photo-downloader", "Les photos d'une publication seulement"),
                ("universal-video-downloader", "Profils et Stories : téléchargeur universel"),
            ),
        ),
        "instagram-photo-downloader": LocalizedGuide(
            facts=(
                ("Liens", "Une publication publique avec photos : instagram.com/p/ID/"),
                ("Choix", "Uniquement les images d'origine, jusqu'à 12 par publication"),
                ("Accès", "Sans connexion ; profils privés exclus"),
            ),
            steps=(
                "Ouvrez la publication avec photos et copiez son lien via l'icône de partage > Copier le lien, ou depuis la barre du navigateur.",
                "Collez-le ci-dessus et cliquez sur « Analyser le lien ». Le serveur lit les éléments de la publication et ne garde que les images.",
                "Chaque photo apparaît numérotée avec sa véritable extension (JPG, PNG ou WebP). Choisissez celle qu'il vous faut et cliquez sur « Préparer le téléchargement ».",
                "Enregistrez le fichier, puis recommencez pour les autres photos du carrousel : chacune est un téléchargement distinct.",
            ),
            links=(
                ("instagram.com/p/ID/", "Une publication avec une photo ou un carrousel. Le paramètre ?igsh= ajouté par Partager n'a aucun effet."),
            ),
            sections=(
                ("L'image telle qu'Instagram la publie", (
                    "L'outil télécharge le fichier image qu'Instagram expose pour chaque élément, sans le recadrer, l'agrandir ni le recompresser. Il ne crée pas de résolution supérieure à celle publiée et n'extrait pas d'image d'une vidéo. Si une publication ne contient que des vidéos, aucune photo n'apparaît.",
                    "Les éléments s'affichent sans taille estimée. Pour convertir ensuite votre propre image dans un autre format ou une autre taille, utilisez les outils d'image du site.",
                )),
                ("Carrousels et publications mixtes", (
                    "Dans un carrousel, chaque photo accessible apparaît sur sa propre ligne, dans la limite de 12. Si le carrousel mélange photos et vidéos, cette page n'affiche que les photos ; pour voir aussi les vidéos, utilisez le téléchargeur Instagram général. Instagram peut montrer moins d'éléments à un visiteur non connecté que dans l'application.",
                )),
                ("Pourquoi une photo publique peut échouer", (
                    "Instagram redirige souvent les accès automatisés à ses photos vers la page de connexion. Dans ce cas, aucun résultat ne s'affiche, même si la publication est visible dans votre application. SaveFromNet n'utilise pas votre compte et n'accède pas aux profils privés ; réessayez plus tard ou vérifiez le lien dans une fenêtre de navigation privée.",
                )),
            ),
            faq=(
                ("Puis-je coller un lien de Reel ?", "Non. Les Reels sont des vidéos et ont leur propre téléchargeur. Cette page accepte les liens /p/ et n'affiche que des images."),
                ("Pourquoi la taille de la photo n'est-elle pas indiquée ?", "Le serveur ne la connaît pas avant le téléchargement ; la ligne affiche donc « Taille inconnue »."),
                ("Puis-je télécharger une photo de profil ou une Story ?", "Pas sur cette page. Seules les publications /p/ sont acceptées."),
                ("Puis-je télécharger toutes les photos d'un coup ?", "Non. Chaque photo est préparée et enregistrée séparément ; aucun ZIP n'est créé. Cliquez sur « Préparer le téléchargement » pour chacune."),
                ("Dans quel format la photo est-elle enregistrée ?", "Dans celui qu'expose Instagram, généralement JPG. L'extension figure sur chaque ligne avant le téléchargement, et le fichier n'est pas converti."),
            ),
            see_also=(
                ("instagram-downloader", "Photos et vidéos ensemble : téléchargeur Instagram"),
                ("instagram-reels-downloader", "Reels Instagram"),
                ("pinterest-video-downloader", "Images d'une épingle Pinterest"),
            ),
        ),
        "tiktok-downloader": LocalizedGuide(
            facts=(
                ("Liens", "Une vidéo /video/, une publication photo /photo/ ou un lien court vm.tiktok.com"),
                ("Choix", "Vidéo et son pour les vidéos ; images, jusqu'à 12, pour les photos"),
                ("Limite", "Un lien à la fois ; fichiers jusqu'à 512 Mo"),
            ),
            steps=(
                "Dans TikTok, touchez Partager sur la vidéo ou la publication photo, puis Copier le lien. Vous obtenez généralement un lien court vm.tiktok.com ou l'adresse complète.",
                "Collez-le ci-dessus et cliquez sur « Analyser le lien ». Une vidéo passe par l'extracteur vidéo ; une publication /photo/ est lue comme une galerie d'images.",
                "Examinez la fiche : lignes vidéo et audio pour une vidéo, images numérotées pour une publication photo. Choisissez-en une et cliquez sur « Préparer le téléchargement ».",
                "Enregistrez le fichier quand il est prêt. Si TikTok bloque la requête, réessayez plus tard.",
            ),
            links=(
                ("tiktok.com/@UTILISATEUR/video/ID", "Une vidéo précise ; l'identifiant est numérique."),
                ("tiktok.com/@UTILISATEUR/photo/ID", "Une publication photo (carrousel)."),
                ("vm.tiktok.com/ID", "Le lien court du bouton Partager ; vt.tiktok.com/ID et tiktok.com/t/ID fonctionnent aussi."),
            ),
            sections=(
                ("Vidéos et publications photo", (
                    "Pour une vidéo, la fiche affiche les fichiers vidéo renvoyés par TikTok, avec leur hauteur et, quand les données existent, leur taille. Si la vidéo a du son, un MP3 converti apparaît aussi, ainsi que la piste audio d'origine lorsque TikTok la fournit séparément.",
                    "Pour une publication /photo/, la fiche affiche les images d'origine numérotées, jusqu'à 12, avec leur véritable extension et sans taille estimée. La musique d'une publication photo n'est pas proposée ici.",
                )),
                ("Liens courts", (
                    "Les liens vm.tiktok.com, vt.tiktok.com et tiktok.com/t/ sont toujours traités comme des vidéos. Si un lien court mène à une publication photo et que l'analyse échoue, ouvrez-le dans le navigateur et copiez l'adresse complète contenant /photo/.",
                )),
                ("Quand TikTok bloque la requête", (
                    "TikTok limite parfois les requêtes provenant de centres de données, même si la publication s'affiche sur votre téléphone. Les publications supprimées, privées, limitées par région ou réservées aux comptes connectés échouent aussi. SaveFromNet ne se connecte pas et ne contourne pas ces restrictions ; si le message « Cette publication publique est inaccessible. » apparaît, réessayez plus tard.",
                )),
            ),
            faq=(
                ("Quel lien TikTok faut-il coller ?", "Le lien d'une vidéo ou d'une publication photo précise, ou son lien court. Un profil, la page Pour toi ou une recherche ne désignent pas un fichier."),
                ("Puis-je télécharger les photos d'un carrousel TikTok ?", "Oui, avec l'adresse /photo/. Jusqu'à 12 images sont listées, et chacune est préparée séparément."),
                ("Puis-je télécharger des Stories TikTok ici ?", "Non. Cette page accepte les vidéos et les publications photo. Le téléchargeur universel accepte les liens de Stories publiques, mais beaucoup exigent une connexion ou ont déjà expiré."),
                ("Pourquoi les photos n'indiquent-elles pas de taille ?", "Les images d'une publication photo sont listées avant d'être téléchargées : le serveur ne connaît donc pas encore leur taille, et la ligne affiche « Taille inconnue »."),
            ),
            see_also=(
                ("tiktok-to-mp3", "Le son seul : convertisseur TikTok en MP3"),
                ("universal-video-downloader", "Stories et autres plateformes : téléchargeur universel"),
                ("instagram-reels-downloader", "Reels Instagram"),
            ),
        ),
        "tiktok-to-mp3": LocalizedGuide(
            facts=(
                ("Liens", "Une vidéo publique : tiktok.com/@utilisateur/video/ID ou un lien court"),
                ("Résultat", "Une seule option : un MP3 converti depuis le son de la vidéo"),
                ("Limite", "Une vidéo à la fois ; les publications photo ne sont pas acceptées"),
            ),
            steps=(
                "Dans TikTok, touchez Partager sur la vidéo puis Copier le lien.",
                "Collez-le ci-dessus et cliquez sur « Analyser le lien ». Le serveur vérifie que la vidéo possède une piste sonore accessible.",
                "Si c'est le cas, la ligne « Converted MP3 » apparaît. Cliquez sur « Préparer le téléchargement » ; pendant l'étape « Extraction de l'audio », le serveur convertit le son avec ffmpeg.",
                "Enregistrez le MP3 quand « Enregistrer le fichier » apparaît.",
            ),
            links=(
                ("tiktok.com/@UTILISATEUR/video/ID", "Une vidéo précise."),
                ("vm.tiktok.com/ID", "Le lien court du bouton Partager ; vt.tiktok.com/ID et tiktok.com/t/ID fonctionnent aussi."),
            ),
            sections=(
                ("D'où vient le MP3", (
                    "Le serveur prend le son que TikTok fournit avec la vidéo et le convertit en MP3 avec ffmpeg. C'est l'audio de ce clip tel qu'il a été publié, avec la musique ou la voix qu'on y entend ; la chanson d'origine n'est pas recherchée sur un autre service.",
                    "La ligne MP3 n'indique pas de taille, car le fichier est créé pendant la conversion. Aucun débit fixe n'est promis non plus : convertir ne restaure pas une qualité absente de l'original.",
                )),
                ("Ce qui ne peut pas être converti", (
                    "Les publications photo (/photo/) ne sont pas acceptées sur cette page, et un clip sans piste sonore ne produit pas de MP3. Les vidéos supprimées, privées, limitées par région ou réservées aux comptes connectés non plus.",
                    "Un lien court est traité comme une vidéo. S'il mène à une publication photo, l'analyse échouera : pour les images, utilisez le téléchargeur TikTok avec l'adresse /photo/.",
                )),
                ("Utiliser l'audio de façon responsable", (
                    "La musique de nombreuses vidéos TikTok appartient à des tiers. Ne téléchargez que l'audio qui vous appartient ou que vous êtes autorisé à utiliser pour l'usage prévu.",
                )),
            ),
            faq=(
                ("Comment convertir un TikTok en MP3 ?", "Collez le lien de la vidéo, cliquez sur « Analyser le lien », choisissez « Converted MP3 » puis « Préparer le téléchargement ». Une fois terminé, enregistrez le fichier."),
                ("Pourquoi l'option MP3 n'apparaît-elle pas ?", "La vidéo n'a pas de piste sonore accessible, ou TikTok a bloqué la requête. Un lien de publication photo est refusé par la page."),
                ("Puis-je convertir le son d'une publication photo ?", "Non. Cette page n'accepte que les vidéos."),
                ("Puis-je obtenir l'audio d'origine sans conversion ?", "Pas ici : cette page ne propose que le MP3. Le téléchargeur TikTok affiche la piste d'origine lorsque TikTok la fournit séparément."),
                ("Est-ce que ça fonctionne sur téléphone ?", "Oui. Copiez le lien dans l'application TikTok, collez-le sur cette page depuis le navigateur du téléphone et enregistrez le MP3 ; le dossier de destination dépend de votre navigateur."),
            ),
            see_also=(
                ("tiktok-downloader", "Vidéo et photos : téléchargeur TikTok"),
                ("youtube-to-mp3", "Convertisseur YouTube en MP3"),
            ),
        ),
        "reddit-video-downloader": LocalizedGuide(
            facts=(
                ("Liens", "Le permalien d'une publication : reddit.com/r/communauté/comments/ID/ ou redd.it/ID"),
                ("Choix", "Fichiers vidéo par hauteur, avec le son quand Reddit le fournit"),
                ("Limite", "Une publication à la fois ; fichiers jusqu'à 512 Mo"),
            ),
            steps=(
                "Ouvrez la publication contenant la vidéo et copiez son adresse depuis la barre du navigateur. Elle doit contenir /comments/ suivi de l'identifiant.",
                "Collez-la ci-dessus et cliquez sur « Analyser le lien ». Le détecteur vérifie le domaine et le chemin, puis retire les paramètres de suivi avant d'interroger Reddit.",
                "Choisissez une ligne vidéo. Par défaut, la meilleure option jusqu'à 1080 pixels de hauteur est cochée.",
                "Cliquez sur « Préparer le téléchargement ». Si Reddit sépare l'image et le son, l'étape « Fusion vidéo et audio » s'affiche avant « Enregistrer le fichier ».",
            ),
            links=(
                ("reddit.com/r/NOM/comments/ID/", "Le permalien d'une publication ; il peut être suivi du titre."),
                ("reddit.com/user/NOM/comments/ID/", "Une publication faite sur un profil utilisateur."),
                ("redd.it/ID", "Le lien court d'une publication."),
                ("old.reddit.com/r/NOM/comments/ID/", "L'ancienne interface de Reddit ; elle est traitée de la même façon."),
            ),
            sections=(
                ("Les liens de partage en /s/", (
                    "L'application Reddit copie souvent des liens de la forme reddit.com/r/communauté/s/code. Cette forme ne désigne pas la publication et le détecteur la refuse. Ouvrez le lien dans le navigateur, attendez que la publication se charge et copiez l'adresse qui contient /comments/.",
                )),
                ("Une vidéo avec le son", (
                    "Reddit stocke souvent l'image et le son de ses vidéos séparément. Lorsque les deux pistes sont publiques et compatibles, le serveur les télécharge et les réunit dans un seul MP4. Si la publication n'a aucune piste sonore, les lignes sont marquées « no audio » : la conversion ne peut pas inventer de voix ni de musique.",
                )),
                ("Les publications qui ne fonctionnent pas", (
                    "Les publications supprimées, privées, en quarantaine ou réservées aux adultes peuvent être inaccessibles sans compte. Une publication de texte ou d'image ne contient pas de vidéo, et une publication qui renvoie vers YouTube ou un autre site n'héberge pas la vidéo sur Reddit : utilisez l'outil de cette plateforme.",
                )),
            ),
            faq=(
                ("Comment télécharger une vidéo Reddit ?", "Copiez le permalien de la publication, collez-le ci-dessus, cliquez sur « Analyser le lien », choisissez une ligne vidéo puis « Préparer le téléchargement ». Enregistrez le fichier quand il est prêt."),
                ("Pourquoi mon lien de l'application est-il refusé ?", "Il s'agit sans doute d'un lien de partage en /s/. Ouvrez-le dans le navigateur et copiez l'adresse contenant /comments/."),
                ("Le lien d'une communauté ou d'un profil fonctionne-t-il ?", "Non. Une communauté r/… ou un profil contient de nombreuses publications ; collez le lien d'une seule."),
                ("Puis-je garder uniquement le son d'une vidéo Reddit ?", "Pas sur cette page, qui n'affiche que la vidéo. Le téléchargeur universel montre aussi l'audio d'origine et un MP3 lorsque la publication a du son."),
            ),
            see_also=(
                ("universal-video-downloader", "Autres plateformes dans un seul champ"),
                ("youtube-video-downloader", "Vidéos YouTube partagées sur Reddit"),
            ),
        ),
        "threads-video-downloader": LocalizedGuide(
            facts=(
                ("Liens", "Une publication publique : threads.com/@utilisateur/post/ID"),
                ("Résultat", "Au plus une vidéo MP4 d'origine"),
                ("Limite", "Une publication à la fois ; fichiers jusqu'à 512 Mo"),
            ),
            steps=(
                "Dans Threads, ouvrez la publication, touchez Partager puis Copier le lien, ou copiez l'adresse depuis le navigateur.",
                "Collez-la ci-dessus et cliquez sur « Analyser le lien ». Le serveur lit les métadonnées publiques de cette publication, celles qu'utilisent les aperçus de liens.",
                "S'il trouve une vidéo hébergée sur les serveurs de Meta, la fiche affiche une ligne « Source video » en MP4.",
                "Cliquez sur « Préparer le téléchargement » et enregistrez le fichier, nommé threads-video.mp4. Faites-le rapidement : l'accès au fichier source peut changer.",
            ),
            links=(
                ("threads.com/@UTILISATEUR/post/ID", "Une publication précise. Le paramètre ?xmt= ajouté par Partager n'a aucun effet."),
                ("threads.net/@UTILISATEUR/post/ID", "L'ancienne adresse ; elle est convertie en threads.com avant l'analyse."),
            ),
            sections=(
                ("Pourquoi une seule option", (
                    "Threads n'a pas d'extracteur stable comme YouTube. SaveFromNet lit la balise vidéo des métadonnées publiques de la page et ne l'accepte que si le fichier est hébergé sur les serveurs de médias de Meta. Cette balise désigne un seul MP4 : il n'y a donc ni liste de résolutions, ni durée, ni taille à l'avance.",
                    "Si la publication contient plusieurs vidéos ou mélange photos et vidéo, seule celle qui figure dans ces métadonnées peut être proposée. Les photos Threads ne se téléchargent pas avec cet outil.",
                )),
                ("Pourquoi le résultat peut être vide", (
                    "Beaucoup de publications vidéo n'incluent pas cette balise pour les visiteurs non connectés, et Threads peut rediriger vers la connexion. La page indique alors qu'aucune vidéo publique n'est disponible. Les profils et les fils ne sont pas des liens vers une publication.",
                )),
                ("Si la préparation échoue", (
                    "L'adresse du fichier publiée par Meta est temporaire. Si la préparation se termine par une erreur parce que la vidéo source n'est plus disponible, analysez de nouveau le lien pour obtenir une adresse fraîche et lancez aussitôt le téléchargement. La vidéo est transférée telle quelle, sans conversion, et le téléchargement s'arrête si elle dépasse 512 Mo.",
                )),
            ),
            faq=(
                ("Quel lien Threads faut-il coller ?", "Celui d'une publication précise, de la forme threads.com/@utilisateur/post/ID. Les liens threads.net fonctionnent aussi."),
                ("Puis-je télécharger des photos Threads ?", "Non. Cet outil cherche uniquement une vidéo dans les métadonnées publiques de la publication."),
                ("Pourquoi le fichier s'appelle-t-il threads-video.mp4 ?", "Le serveur enregistre toujours les vidéos Threads sous ce nom ; vous pouvez le renommer ensuite sur votre appareil."),
                ("La vidéo aura-t-elle du son ?", "Le MP4 est téléchargé tel que Meta le publie, sans fusion ni conversion : si le fichier source a du son, il le conserve."),
                ("Est-ce que ça fonctionne sur téléphone ?", "Oui. Copiez le lien via Partager dans l'application Threads, collez-le ici depuis le navigateur du téléphone et enregistrez le fichier une fois prêt."),
            ),
            see_also=(
                ("instagram-reels-downloader", "Reels Instagram"),
                ("facebook-video-downloader", "Vidéos Facebook"),
                ("universal-video-downloader", "Autres plateformes dans un seul champ"),
            ),
        ),
        "dailymotion-video-downloader": LocalizedGuide(
            facts=(
                ("Liens", "Une vidéo publique : dailymotion.com/video/ID ou dai.ly/ID"),
                ("Choix", "Hauteurs en MP4 ou WebM renvoyées pour cette vidéo"),
                ("Limite", "Une vidéo à la fois ; fichiers jusqu'à 512 Mo"),
            ),
            steps=(
                "Ouvrez la vidéo sur Dailymotion et copiez son adresse, ou le lien court dai.ly du bouton Partager.",
                "Collez-le ci-dessus et cliquez sur « Analyser le lien ». Un lien dai.ly est d'abord converti en adresse dailymotion.com/video/ de la même vidéo.",
                "Comparez les hauteurs disponibles. Par défaut, la meilleure option jusqu'à 1080 pixels est cochée ; vous pouvez en choisir une autre.",
                "Cliquez sur « Préparer le téléchargement » et enregistrez le fichier quand « Enregistrer le fichier » apparaît.",
            ),
            links=(
                ("dailymotion.com/video/ID", "La page d'une vidéo ; l'identifiant commence généralement par x."),
                ("dai.ly/ID", "Le lien court généré par Partager."),
            ),
            sections=(
                ("Lire les qualités", (
                    "Dailymotion peut proposer plusieurs hauteurs d'une même vidéo. Chaque ligne indique le conteneur, la hauteur et, quand la source donne le débit et la durée, une taille approximative précédée de ≈. Qu'un lecteur affiche une qualité ne garantit pas qu'un téléchargeur sans compte reçoive le même fichier.",
                    "Une hauteur plus élevée prend généralement plus de place, mais le codec et le débit comptent aussi. Les options qui dépasseraient 512 Mo n'apparaissent pas, ce qui peut écarter les hautes qualités d'une longue vidéo.",
                )),
                ("Les liens qui ne désignent pas une vidéo", (
                    "Les chaînes, playlists et recherches ne sont pas des liens vers une vidéo précise, et le détecteur les refuse. Les vidéos privées, supprimées ou bloquées par région ne sont pas traitées non plus ; dans ce dernier cas, la page indique que le contenu est indisponible dans la région du serveur.",
                )),
                ("Le son et le fichier final", (
                    "Les qualités Dailymotion arrivent généralement avec l'image et le son ensemble, si bien qu'il n'y a d'ordinaire aucune piste à assembler. Si la source ne fournit aucune piste sonore, la ligne est marquée « no audio » au lieu d'être présentée comme une vidéo complète. Le fichier est enregistré dans le conteneur indiqué par la ligne.",
                )),
            ),
            faq=(
                ("Un lien dai.ly fonctionne-t-il ?", "Oui. Il est converti en adresse de la vidéo sur dailymotion.com avant l'analyse."),
                ("Pourquoi la taille est-elle inconnue ?", "Dailymotion ne fournit pas toujours le débit ou la durée nécessaires. Afficher « Taille inconnue » est plus fidèle qu'inventer un chiffre."),
                ("Puis-je télécharger une playlist ?", "Non. Analysez chaque vidéo avec son propre lien."),
                ("Puis-je télécharger une vidéo privée ou protégée par mot de passe ?", "Non. Seules les vidéos publiques visibles sans connexion ni mot de passe sont traitées."),
                ("Est-ce que ça fonctionne sur téléphone ?", "Oui. Copiez le lien via Partager dans l'application Dailymotion, collez-le sur cette page depuis le navigateur et enregistrez le fichier ; le dossier dépend de votre navigateur."),
            ),
            see_also=(
                ("universal-video-downloader", "Autres plateformes dans un seul champ"),
                ("youtube-video-downloader", "Vidéos YouTube"),
            ),
        ),
    },
}

PUBLISHED_SLUGS = tuple(LOCALIZED_TOOLS["es"])
assert set(PUBLISHED_SLUGS) == set(LOCALIZED_TOOLS["fr"])
assert set(LOCALIZED_GUIDES["es"]) == set(LOCALIZED_GUIDES["fr"]) == set(PUBLISHED_SLUGS)


def alternates(base_url, slug=None):
    """Return reciprocal absolute URLs only for published translations."""
    if slug is not None and slug not in PUBLISHED_SLUGS:
        return ()
    suffix = f"/{slug}" if slug else ""
    english = base_url + (suffix or "/")
    return (
        ("en", english),
        ("es", base_url + "/es" + suffix),
        ("fr", base_url + "/fr" + suffix),
        ("x-default", english),
    )
