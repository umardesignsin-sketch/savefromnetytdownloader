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
    },
}

PUBLISHED_SLUGS = tuple(LOCALIZED_TOOLS["es"])
assert set(PUBLISHED_SLUGS) == set(LOCALIZED_TOOLS["fr"])
assert set(LOCALIZED_GUIDES["es"]) == set(LOCALIZED_GUIDES["fr"]) <= set(PUBLISHED_SLUGS)


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
