// Anno 117 Mod Manager — pywebview frontend bootstrap.
// Defines the Alpine root component used by index.html.

// UI strings keyed by stable id; English is the canonical source so any key
// missing in another language falls back to en. Add more languages by
// dropping a {key: 'localized text'} entry into the TRANSLATIONS map below.
const TRANSLATIONS = {
  english: {
    'hud.settings':                 'Settings',
    'hud.refreshMods':              'Refresh mod list',
    'hud.searchMod':                'Search a mod…',
    'hud.language':                 'Language',
    'alert.loadPresetFail':         'Failed to load preset: {error}',
    'alert.savePresetFail':         'Failed to save preset: {error}',
    'alert.deletePresetFail':       'Failed to delete preset: {error}',
    'alert.uninstallFail':          'Uninstall failed: {error}',
    'profile.label':           'Profile',
    'profile.new':             '＋ New',
    'profile.delete':          '🗑 Delete',
    'profile.deleteConfirm':   'Delete preset "{name}"?',
    'profile.cantDeleteReserved': 'The "Default" and "Vanilla" profiles cannot be deleted.',
    'profile.promptName':      'Name of the new preset:',
    'mode.manage':             'Manage',
    'mode.order':              'Load order',
    'mode.manage.title':       'Sort and toggle mods on/off',
    'mode.order.title':        'Reorder load order via drag-and-drop',
    'list.head.toggleAll':     'Activate / deactivate all',
    'list.head.category':      'Category',
    'list.head.name':          'Mod name',
    'list.head.size':          'Size',
    'list.head.status':        'Status',
    'list.empty':              'No mods detected in the configured folders.',
    'count.active':            '{n} / {total} active',
    'pill.active':             'ON',
    'pill.off':                'OFF',
    'detail.empty':            'Select a mod from the list to view its sheet.',
    'detail.banner.empty':     'No banner provided for this mod.',
    'detail.description':      'Description',
    'detail.details':          'Details',
    'detail.meta.category':    'Category',
    'detail.meta.difficulty':  'Difficulty',
    'detail.meta.size':        'Size',
    'detail.meta.folder':      'Folder',
    'detail.creator':          'by {name} · v{version}',
    'detail.openFolder':       'Open folder',
    'detail.uninstall':        'Uninstall',
    'detail.uninstallConfirm': 'Uninstall mod "{name}"?\n\nThe folder will be deleted from disk.',
    'tab.placeholder':         'This tab will be ported in phase 2 of the migration.',
    'tab.placeholderHint':     'pywebview POC in progress — only the {tab} tab works for now.',
    'launch.title':            'Launch Anno 117',
    'launch.error':            'Could not launch the game: {err}',
    'mods.openFolder.title':   'Open the mods folder',
    'mods.notFromManager':     'Not installed via the manager',
    'deps.conflict':           'Conflict with: {names}\n\nThis mod is incompatible with one or more active mods.',
    'deps.missingInstalled':   'Missing dependency (not installed): {names}\n\nRequired mods are not present in the mods folder.',
    'deps.missingActive':      'Missing dependency (disabled): {names}\n\nRequired mods are installed but not active.',
    'deps.deprecated':         'Deprecated by: {names}\n\nThis mod is replaced by an active mod. Consider disabling it.',
    'deps.dialog.conflict':    '"{mod}" conflicts with the following active mods:',
    'deps.dialog.missingInstalled': '"{mod}" requires the following mods which are not installed:',
    'deps.dialog.missingActive': '"{mod}" requires the following mods which are installed but disabled:',
    'deps.dialog.deprecated':  '"{mod}" is deprecated by the following active mods:',
    'deps.dialog.enable':      'Enable',
    'deps.dialog.disable':     'Disable',
    'deps.dialog.disableThis': 'Disable this mod',
    'deps.dialog.install':     'Install',
    'deps.dialog.installing':  'Installing…',
    'deps.dialog.close':       'Close',
    'mods.versionMismatch':        'Installed: v{lv} → Available: v{rv}\n\nThere is a mismatch in version numbers between the currently installed local version of the mod and the newest version available on mod.io! Click to directly update the mod with the newest version from mod.io.',
    'mods.versionMismatchInfo':    'Installed: v{lv} · mod.io: v{rv}\n\nThe local version appears newer than what is published on mod.io.',
    'mods.versionMismatchSameFile': 'Installed: v{lv} · mod.io: v{rv}\n\nThe version labels differ but the installed file is up to date. This is likely an authoring inconsistency (modinfo.json not updated by the mod author).',
    'mods.link.cta':           '🔗 Link to mod.io',
    'mods.link.title':         'Link « {name} » to a mod.io record',
    'mods.link.searchPlaceholder': 'Search mod.io…',
    'mods.link.confirm':       'Link',
    'mods.link.empty':         'No matches — try another name.',
    'mods.link.cancel':        'Cancel',
    'tab.news':                'News',
    'tab.activation':          'Activation',
    'tab.browser':             'Mod Browser',
    'tab.collections':         'Collections',
    'tab.install':             'Manual Install',
    'tab.log':                 'Modloader Log',
    'tab.tweak':               'Tweaking',
    'tab.settings':            'Settings',
    'settings.section.paths':       'Paths',
    'settings.section.behaviour':   'Behaviour',
    'settings.section.advanced':    'Advanced',
    'settings.gamePath':            'Anno 117 executable',
    'settings.gamePath.empty':      'Not configured — set the path to Anno117.exe',
    'settings.docsPath':            'Documents folder override',
    'settings.docsPath.empty':      'Auto-detected (uses ~/Documents or the Proton prefix)',
    'settings.browseFile':          'Browse file…',
    'settings.browseFolder':        'Browse folder…',
    'settings.autoDetect':          'Auto-detect',
    'settings.clear':               'Clear',
    'settings.open':                'Open',
    'settings.modLocation':         'Mod storage location',
    'settings.modLocation.documents': 'Documents folder (recommended)',
    'settings.modLocation.game':      'Game install folder',
    'settings.enableNewMods':       'Newly installed mods',
    'settings.enableNewMods.on':    'Always activate them',
    'settings.enableNewMods.off':   'Never activate them',
    'settings.enableNewMods.keep':  'Keep their previous state',
    'settings.textScale':           'Reading text size',
    'settings.textScale.small':     'Small',
    'settings.textScale.medium':    'Medium',
    'settings.textScale.large':     'Large',
    'settings.derived.docsMods':    'Documents mods folder',
    'settings.derived.gameMods':    'Game install mods folder',
    'settings.derived.profile':     'active-profile.txt',
    'settings.derived.appdata':     'AppData',
    'settings.derived.presets':     'Presets',
    'settings.pathError':           'Path could not be saved: {err}',
    'settings.detectError':         'Could not auto-detect: {err}',
    'settings.section.modio':       'mod.io integration',
    'settings.modio.hint':          'Enter your personal mod.io API key to enable the Mod Browser and Collections tabs. Generate one at',
    'settings.modio.apiKey':        'API key',
    'settings.modio.apiKeyPlaceholder': 'Paste your mod.io API key here',
    'settings.modio.save':          'Save',
    'settings.modio.disconnectConfirm': 'Remove the saved mod.io API key?',
    'settings.modio.emptyKey':      'API key is empty.',
    'log.refresh':                  '↻ Refresh',
    'log.copy':                     '⧉ Copy',
    'log.openFile':                 'Open file',
    'log.loading':                  'Loading…',
    'log.empty':                    'mod-loader.log is empty.',
    'log.notFound':                 'mod-loader.log not found at:\n{path}',
    'log.truncated':                'Log truncated to last 2 MB',
    'install.title':                'Manual install',
    'install.hint':                 'Drop a mod ZIP here, or click to browse. The archive must contain a modinfo.json (or .jsonc) file.',
    'install.drop':                 'Drop a .zip mod here',
    'install.or':                   '— or —',
    'install.browse':               'Browse a ZIP file…',
    'install.targetLabel':          'Install destination:',
    'install.installing':           'Installing {name}…',
    'install.success':              '{name} installed.',
    'install.cancelled':            'Cancelled.',
    'install.overwriteConfirm':     'A mod folder named "{name}" already exists. Replace it?',
    'tweak.listHeader':             'Tweakable mods',
    'tweak.optionWord':             'options',
    'tweak.noTweakable':            'None of your installed mods exposes options.',
    'tweak.pickHint':                'Select a mod on the left to tweak its options.',
    'tweak.noOptions':              'This mod has no configurable options.',
    'tweak.resetMod':               'Reset this mod',
    'tweak.resetAll':               'Reset all',
    'tweak.resetModConfirm':        'Reset all options for this mod to their defaults?',
    'tweak.resetAllConfirm':        'Reset every mod’s options? The active-options.jsonc file will be deleted.',
    'tweak.defaultsSection':        '— Default values —',
    'tweak.colorPicker.open':       'Open colour picker',
    'tweak.colorPicker.title':      'Colour picker',
    'tweak.colorPicker.before':     'Before',
    'tweak.colorPicker.after':      'After',
    'tweak.colorPicker.cancel':     'Cancel',
    'tweak.colorPicker.apply':      'Apply',
    'news.refresh':                 '↻ Refresh',
    'news.loading':                 'Fetching latest posts…',
    'news.empty':                   'No news to display.',
    'news.error':                   'Could not fetch news: {err}',
    'news.cached':                  'cached (10 min)',
    'news.includeReddit':           'Include r/anno posts',
    'news.visitUnion':              'Open Anno Union ↗',
    'news.back':                    'Back to news',
    'news.openOnUnion':             'Open on Anno Union ↗',
    'settings.modio.clearKey':      'Clear key',
    'modio.badge.connected':        '● Connected',
    'modio.badge.keyOnly':          '◐ API key only',
    'modio.badge.notSet':           '○ Not set',
    'modio.session':                'Session',
    'modio.expires':                'expires {date}',
    'modio.disconnect':             'Disconnect',
    'modio.disconnectConfirm':      'Disconnect from mod.io? Your API key stays saved; you can reconnect later.',
    'modio.needKeyFirst':           'Save your API key above first, then you can connect.',
    'modio.startConnect':           'Connect to mod.io',
    'modio.email':                  'Email address',
    'modio.emailPlaceholder':       'you@example.com',
    'modio.emailRequired':          'Please enter your email.',
    'modio.termsAgree':             'I agree to the mod.io',
    'modio.termsLink':              'Terms of Use',
    'modio.cancel':                 'Cancel',
    'common.cancel':                'Cancel',
    'common.confirm':               'Confirm',
    'modio.sendCode':               'Send code',
    'modio.sending':                'Sending…',
    'modio.code':                   'Security code',
    'modio.codeRequired':           'Enter the 5-character code from your email.',
    'modio.codeSent':               'A 5-character code was sent to {email}. Check your inbox (and spam).',
    'modio.connect':                'Connect',
    'modio.connecting':             'Connecting…',
    // Mod Browser
    'browser.title':                'Mod Browser',
    'browser.searchPlaceholder':    'Search mods…',
    'browser.search':               'Search',
    'browser.refresh':              'Refresh',
    'browser.sortNewest':           'Newest',
    'browser.sortPopular':          'Most popular',
    'browser.sortDownloads':        'Most downloaded',
    'browser.sortRating':           'Top rated',
    'browser.sortAlpha':            'A → Z',
    'browser.sortBy':               'Sort by:',
    'browser.mySubscriptions':      'My Subscriptions',
    'browser.myFollows':            'My Follows',
    'browser.follow':               'Follow this collection',
    'browser.unfollow':             'Unfollow this collection',
    'browser.tag':                  'Tag:',
    'browser.tagAll':               'All tags',
    'browser.clearSearch':          'Clear search',
    'browser.byAuthor':             'by {name}',
    'browser.clearAuthor':          'Show all authors',
    'browser.filterByAuthor':       'Show only this author\'s mods',
    'browser.bundledMods':          'Bundled mods',
    'browser.bundledEmpty':         'This collection lists no bundled mods.',
    'browser.backToCollection':     'Back to collection',
    'browser.installCollection':    'Install collection',
    'browser.updateCollection':     'Update collection',
    'browser.uninstallMod':         '🗑 Uninstall',
    'browser.uninstallModConfirm':  'Remove « {name} » from disk?',
    'browser.uninstallModOk':       '« {name} » uninstalled.',
    'browser.uninstallCollection':  '🗑 Uninstall collection',
    'browser.uninstallConfirm':     'Delete the « {profile} » profile created from « {name} »?',
    'browser.uninstallAlsoMods':    'Also wipe the {count} mod(s) bundled in this collection from disk?',
    'browser.uninstallOk':          'Profile « {profile} » removed.',
    'browser.uninstallOkWithMods':  'Profile « {profile} » removed; {count} bundled mod(s) wiped from disk.',
    'browser.uninstallFail':        'Uninstall failed: {error}',
    'browser.collectionInstallOk':  '« {name} »: {count}/{total} mods installed. Profile « {profile} » is now active.',
    'browser.collectionInstallFailures': '({count} failed — see log)',
    'browser.back':                 'Back',
    'browser.empty':                'No mods match your search.',
    'browser.loading':              'Loading mods…',
    'browser.error':                'Could not load mods: {error}',
    'browser.notAuth':              'Not connected to mod.io. Connect in the Settings tab.',
    'browser.openSettings':         'Open Settings',
    'browser.prev':                 '‹ Previous',
    'browser.next':                 'Next ›',
    'browser.pageOf':               'Page {page} / {total}',
    'browser.resultsCount':         '{shown} of {total} mods',
    'browser.detailPick':           'Select a mod from the list to see its details.',
    'browser.install':              'Install',
    'browser.installing':           'Installing…',
    'browser.installed':            '✓ Installed',
    'browser.update':               'Update',
    'browser.installOk':            '« {name} » installed.',
    'browser.installFail':          'Install failed: {error}',
    'browser.subscribe':            '+ Subscribe',
    'browser.subscribed':           '✓ Subscribed',
    'browser.unsubscribe':          'Unsubscribe',
    'browser.endorse':              '♥ Endorse',
    'browser.endorsed':             '♥ Endorsed',
    'browser.endorseFail':          'Could not endorse: {error}',
    'browser.subFail':              'Could not subscribe: {error}',
    'browser.openOnModio':          'Open on mod.io ↗',
    'browser.author':               'by {name}',
    'browser.downloads':            '{n} downloads',
    'browser.subscribers':          '{n} subscribers',
    'browser.modsTotal':            '{n} mods',
    'browser.updated':              'Updated {date}',
    'browser.size':                 'Size: {size}',
    'browser.version':              'Version: {v}',
    'browser.changelog':            'Changelog',
    'browser.description':          'Description',
  },
  french: {
    'hud.settings':                 'Paramètres',
    'hud.refreshMods':              'Rafraîchir la liste des mods',
    'hud.searchMod':                'Rechercher un mod…',
    'hud.language':                 'Langue',
    'alert.loadPresetFail':         'Échec du chargement du preset : {error}',
    'alert.savePresetFail':         'Échec de la sauvegarde : {error}',
    'alert.deletePresetFail':       'Échec de la suppression : {error}',
    'alert.uninstallFail':          'Échec de la désinstallation : {error}',
    'profile.label':           'Profil',
    'profile.new':             '＋ Nouveau',
    'profile.delete':          '🗑 Supprimer',
    'profile.deleteConfirm':   'Supprimer le preset « {name} » ?',
    'profile.cantDeleteReserved': 'Les profils « Default » et « Vanilla » ne peuvent pas être supprimés.',
    'profile.promptName':      'Nom du nouveau preset :',
    'mode.manage':             'Gestion',
    'mode.order':              'Ordre de chargement',
    'mode.manage.title':       'Trier et activer/désactiver les mods',
    'mode.order.title':        'Réorganiser l’ordre de chargement par drag-and-drop',
    'list.head.toggleAll':     'Tout activer / désactiver',
    'list.head.category':      'Catégorie',
    'list.head.name':          'Nom du mod',
    'list.head.size':          'Taille',
    'list.head.status':        'Statut',
    'list.empty':              'Aucun mod détecté dans les dossiers configurés.',
    'count.active':            '{n} / {total} actifs',
    'pill.active':             'ACTIF',
    'pill.off':                'OFF',
    'detail.empty':            'Choisissez un mod dans la liste pour consulter sa fiche.',
    'detail.banner.empty':     'Aucune bannière fournie pour ce mod.',
    'detail.description':      'Description',
    'detail.details':          'Détails',
    'detail.meta.category':    'Catégorie',
    'detail.meta.difficulty':  'Difficulté',
    'detail.meta.size':        'Taille',
    'detail.meta.folder':      'Dossier',
    'detail.creator':          'par {name} · v{version}',
    'detail.openFolder':       'Ouvrir le dossier',
    'detail.uninstall':        'Désinstaller',
    'detail.uninstallConfirm': 'Désinstaller le mod « {name} » ?\n\nLe dossier sera supprimé du disque.',
    'tab.placeholder':         'Cet onglet sera porté en phase 2 de la migration.',
    'tab.placeholderHint':     'POC pywebview en cours — seul l’onglet {tab} est fonctionnel pour l’instant.',
    'launch.title':            'Lancer Anno 117',
    'launch.error':            'Impossible de lancer le jeu : {err}',
    'mods.openFolder.title':   'Ouvrir le dossier des mods',
    'mods.notFromManager':     'Non installé via le gestionnaire',
    'deps.conflict':           'Conflit avec : {names}\n\nCe mod est incompatible avec un ou plusieurs mods actifs.',
    'deps.missingInstalled':   'Dépendance manquante (non installée) : {names}\n\nDes mods requis ne sont pas présents dans le dossier.',
    'deps.missingActive':      'Dépendance manquante (désactivée) : {names}\n\nDes mods requis sont installés mais non actifs.',
    'deps.deprecated':         'Remplacé par : {names}\n\nCe mod est déprécié par un mod actif. Pensez à le désactiver.',
    'deps.dialog.conflict':    '« {mod} » est incompatible avec les mods actifs suivants :',
    'deps.dialog.missingInstalled': '« {mod} » requiert les mods suivants qui ne sont pas installés :',
    'deps.dialog.missingActive': '« {mod} » requiert les mods suivants qui sont installés mais désactivés :',
    'deps.dialog.deprecated':  '« {mod} » est remplacé par les mods actifs suivants :',
    'deps.dialog.enable':      'Activer',
    'deps.dialog.disable':     'Désactiver',
    'deps.dialog.disableThis': 'Désactiver ce mod',
    'deps.dialog.install':     'Installer',
    'deps.dialog.installing':  'Installation…',
    'deps.dialog.close':       'Fermer',
    'mods.versionMismatch':        'Installé : v{lv} → Disponible : v{rv}\n\nLes numéros de version ne correspondent pas entre la version locale installée et la dernière version disponible sur mod.io ! Cliquez pour mettre à jour le mod directement depuis mod.io.',
    'mods.versionMismatchInfo':    'Installé : v{lv} · mod.io : v{rv}\n\nLa version locale semble plus récente que celle publiée sur mod.io.',
    'mods.versionMismatchSameFile': 'Installé : v{lv} · mod.io : v{rv}\n\nLes libellés de version diffèrent mais le fichier installé est à jour. Probable incohérence du créateur : modinfo.json non mis à jour.',
    'mods.link.cta':           '🔗 Associer à mod.io',
    'mods.link.title':         'Associer « {name} » à une fiche mod.io',
    'mods.link.searchPlaceholder': 'Rechercher sur mod.io…',
    'mods.link.confirm':       'Associer',
    'mods.link.empty':         'Aucun résultat — essayez un autre nom.',
    'mods.link.cancel':        'Annuler',
    'tab.news':                'Actualités',
    'tab.activation':          'Activation',
    'tab.browser':             'Mod Browser',
    'tab.collections':         'Collections',
    'tab.install':             'Installation manuelle',
    'tab.log':                 'Journal du Modloader',
    'tab.tweak':               'Ajustement',
    'tab.settings':            'Paramètres',
    'settings.section.paths':       'Chemins',
    'settings.section.behaviour':   'Comportement',
    'settings.section.advanced':    'Avancé',
    'settings.gamePath':            'Exécutable Anno 117',
    'settings.gamePath.empty':      'Non configuré — indiquez le chemin de Anno117.exe',
    'settings.docsPath':            'Dossier Documents personnalisé',
    'settings.docsPath.empty':      'Auto-détecté (utilise ~/Documents ou le préfixe Proton)',
    'settings.browseFile':          'Parcourir un fichier…',
    'settings.browseFolder':        'Parcourir un dossier…',
    'settings.autoDetect':          'Auto-détecter',
    'settings.clear':               'Effacer',
    'settings.open':                'Ouvrir',
    'settings.modLocation':         'Emplacement de stockage des mods',
    'settings.modLocation.documents': 'Dossier Documents (recommandé)',
    'settings.modLocation.game':      'Dossier d’installation du jeu',
    'settings.enableNewMods':       'Mods nouvellement installés',
    'settings.enableNewMods.on':    'Toujours les activer',
    'settings.enableNewMods.off':   'Ne jamais les activer',
    'settings.enableNewMods.keep':  'Conserver leur état précédent',
    'settings.textScale':           'Taille du texte (lecture)',
    'settings.textScale.small':     'Petit',
    'settings.textScale.medium':    'Moyen',
    'settings.textScale.large':     'Grand',
    'settings.derived.docsMods':    'Dossier mods (Documents)',
    'settings.derived.gameMods':    'Dossier mods (jeu)',
    'settings.derived.profile':     'active-profile.txt',
    'settings.derived.appdata':     'AppData',
    'settings.derived.presets':     'Presets',
    'settings.pathError':           'Le chemin n’a pas pu être sauvegardé : {err}',
    'settings.detectError':         'Auto-détection échouée : {err}',
    'settings.section.modio':       'Intégration mod.io',
    'settings.modio.hint':          'Saisissez votre clé API mod.io personnelle pour activer les onglets Mod Browser et Collections. Générez-en une sur',
    'settings.modio.apiKey':        'Clé API',
    'settings.modio.apiKeyPlaceholder': 'Collez ici votre clé API mod.io',
    'settings.modio.save':          'Sauvegarder',
    'settings.modio.disconnectConfirm': 'Supprimer la clé API mod.io enregistrée ?',
    'settings.modio.emptyKey':      'La clé API est vide.',
    'log.refresh':                  '↻ Rafraîchir',
    'log.copy':                     '⧉ Copier',
    'log.openFile':                 'Ouvrir le fichier',
    'log.loading':                  'Chargement…',
    'log.empty':                    'mod-loader.log est vide.',
    'log.notFound':                 'mod-loader.log introuvable à :\n{path}',
    'log.truncated':                'Log tronqué aux 2 derniers Mo',
    'install.title':                'Installation manuelle',
    'install.hint':                 'Déposez un ZIP de mod ici, ou cliquez pour parcourir. L’archive doit contenir un fichier modinfo.json (ou .jsonc).',
    'install.drop':                 'Déposez un mod .zip ici',
    'install.or':                   '— ou —',
    'install.browse':               'Parcourir un fichier ZIP…',
    'install.targetLabel':          'Destination d’installation :',
    'install.installing':           'Installation de {name}…',
    'install.success':              '{name} installé.',
    'install.cancelled':            'Annulé.',
    'install.overwriteConfirm':     'Un dossier de mod nommé « {name} » existe déjà. Le remplacer ?',
    'tweak.listHeader':             'Mods configurables',
    'tweak.optionWord':             'options',
    'tweak.noTweakable':            'Aucun de vos mods installés n’expose d’options.',
    'tweak.pickHint':                'Sélectionnez un mod à gauche pour ajuster ses options.',
    'tweak.noOptions':              'Ce mod n’a pas d’options configurables.',
    'tweak.resetMod':               'Réinitialiser ce mod',
    'tweak.resetAll':               'Tout réinitialiser',
    'tweak.resetModConfirm':        'Réinitialiser toutes les options de ce mod aux valeurs par défaut ?',
    'tweak.resetAllConfirm':        'Réinitialiser les options de tous les mods ? Le fichier active-options.jsonc sera supprimé.',
    'tweak.defaultsSection':        '— Valeurs par défaut —',
    'tweak.colorPicker.open':       'Ouvrir le sélecteur de couleur',
    'tweak.colorPicker.title':      'Sélecteur de couleur',
    'tweak.colorPicker.before':     'Avant',
    'tweak.colorPicker.after':      'Après',
    'tweak.colorPicker.cancel':     'Annuler',
    'tweak.colorPicker.apply':      'Appliquer',
    'news.refresh':                 '↻ Rafraîchir',
    'news.loading':                 'Récupération des dernières actualités…',
    'news.empty':                   'Aucune actualité à afficher.',
    'news.error':                   'Échec de la récupération : {err}',
    'news.cached':                  'en cache (10 min)',
    'news.includeReddit':           'Inclure les posts r/anno',
    'news.visitUnion':              'Ouvrir Anno Union ↗',
    'news.back':                    'Retour aux actualités',
    'news.openOnUnion':             'Ouvrir sur Anno Union ↗',
    'settings.modio.clearKey':      'Effacer la clé',
    'modio.badge.connected':        '● Connecté',
    'modio.badge.keyOnly':          '◐ Clé API seulement',
    'modio.badge.notSet':           '○ Non configuré',
    'modio.session':                'Session',
    'modio.expires':                'expire le {date}',
    'modio.disconnect':             'Déconnecter',
    'modio.disconnectConfirm':      'Se déconnecter de mod.io ? Votre clé API reste enregistrée ; vous pouvez vous reconnecter plus tard.',
    'modio.needKeyFirst':           'Enregistrez d’abord votre clé API ci-dessus, puis vous pourrez vous connecter.',
    'modio.startConnect':           'Se connecter à mod.io',
    'modio.email':                  'Adresse email',
    'modio.emailPlaceholder':       'vous@exemple.com',
    'modio.emailRequired':          'Saisissez votre adresse email.',
    'modio.termsAgree':             'J’accepte les',
    'modio.termsLink':              'Conditions d’utilisation mod.io',
    'modio.cancel':                 'Annuler',
    'common.cancel':                'Annuler',
    'common.confirm':               'Confirmer',
    'modio.sendCode':               'Envoyer le code',
    'modio.sending':                'Envoi…',
    'modio.code':                   'Code de sécurité',
    'modio.codeRequired':           'Saisissez le code à 5 caractères reçu par email.',
    'modio.codeSent':               'Un code à 5 caractères a été envoyé à {email}. Vérifiez votre boîte (et les spams).',
    'modio.connect':                'Connecter',
    'modio.connecting':             'Connexion…',
    // Mod Browser
    'browser.title':                'Catalogue de mods',
    'browser.searchPlaceholder':    'Rechercher un mod…',
    'browser.search':               'Rechercher',
    'browser.refresh':              'Rafraîchir',
    'browser.sortNewest':           'Récents',
    'browser.sortPopular':          'Plus populaires',
    'browser.sortDownloads':        'Plus téléchargés',
    'browser.sortRating':           'Mieux notés',
    'browser.sortAlpha':            'A → Z',
    'browser.sortBy':               'Trier par :',
    'browser.mySubscriptions':      'Mes abonnements',
    'browser.myFollows':            'Mes follows',
    'browser.follow':               'Suivre cette collection',
    'browser.unfollow':             'Ne plus suivre cette collection',
    'browser.tag':                  'Tag :',
    'browser.tagAll':               'Tous les tags',
    'browser.clearSearch':          'Effacer la recherche',
    'browser.byAuthor':             'par {name}',
    'browser.clearAuthor':          'Voir tous les auteurs',
    'browser.filterByAuthor':       'Voir uniquement les mods de cet auteur',
    'browser.bundledMods':          'Mods inclus',
    'browser.bundledEmpty':         'Cette collection ne liste aucun mod.',
    'browser.backToCollection':     'Retour à la collection',
    'browser.installCollection':    'Installer la collection',
    'browser.updateCollection':     'Mettre à jour la collection',
    'browser.uninstallMod':         '🗑 Désinstaller',
    'browser.uninstallModConfirm':  'Supprimer « {name} » du disque ?',
    'browser.uninstallModOk':       '« {name} » désinstallé.',
    'browser.uninstallCollection':  '🗑 Désinstaller la collection',
    'browser.uninstallConfirm':     'Supprimer le profil « {profile} » créé à partir de « {name} » ?',
    'browser.uninstallAlsoMods':    'Supprimer aussi du disque les {count} mod(s) inclus dans cette collection ?',
    'browser.uninstallOk':          'Profil « {profile} » supprimé.',
    'browser.uninstallOkWithMods':  'Profil « {profile} » supprimé ; {count} mod(s) inclus effacés du disque.',
    'browser.uninstallFail':        'Échec de la désinstallation : {error}',
    'browser.collectionInstallOk':  '« {name} » : {count}/{total} mods installés. Le profil « {profile} » est maintenant actif.',
    'browser.collectionInstallFailures': '({count} échec(s) — voir le journal)',
    'browser.back':                 'Retour',
    'browser.empty':                'Aucun mod ne correspond à votre recherche.',
    'browser.loading':              'Chargement des mods…',
    'browser.error':                'Impossible de charger les mods : {error}',
    'browser.notAuth':              'Non connecté à mod.io. Connectez-vous dans l’onglet Paramètres.',
    'browser.openSettings':         'Ouvrir les paramètres',
    'browser.prev':                 '‹ Précédent',
    'browser.next':                 'Suivant ›',
    'browser.pageOf':               'Page {page} / {total}',
    'browser.resultsCount':         '{shown} sur {total} mods',
    'browser.detailPick':           'Sélectionnez un mod dans la liste pour voir ses détails.',
    'browser.install':              'Installer',
    'browser.installing':           'Installation…',
    'browser.installed':            '✓ Installé',
    'browser.update':               'Mettre à jour',
    'browser.installOk':            '« {name} » installé.',
    'browser.installFail':          'Échec de l’installation : {error}',
    'browser.subscribe':            '+ S’abonner',
    'browser.subscribed':           '✓ Abonné',
    'browser.unsubscribe':          'Se désabonner',
    'browser.endorse':              '♥ Recommander',
    'browser.endorsed':             '♥ Recommandé',
    'browser.endorseFail':          'Impossible de recommander : {error}',
    'browser.subFail':              'Impossible de s’abonner : {error}',
    'browser.openOnModio':          'Voir sur mod.io ↗',
    'browser.author':               'par {name}',
    'browser.downloads':            '{n} téléchargements',
    'browser.subscribers':          '{n} abonnés',
    'browser.modsTotal':            '{n} mods',
    'browser.updated':              'Mis à jour le {date}',
    'browser.size':                 'Taille : {size}',
    'browser.version':              'Version : {v}',
    'browser.changelog':            'Notes de version',
    'browser.description':          'Description',
  },
  german: {
    'hud.settings':                 'Einstellungen',
    'hud.refreshMods':              'Mod-Liste aktualisieren',
    'hud.searchMod':                'Mod suchen…',
    'hud.language':                 'Sprache',
    'alert.loadPresetFail':         'Preset konnte nicht geladen werden: {error}',
    'alert.savePresetFail':         'Preset konnte nicht gespeichert werden: {error}',
    'alert.deletePresetFail':       'Preset konnte nicht gelöscht werden: {error}',
    'alert.uninstallFail':          'Deinstallation fehlgeschlagen: {error}',
    'profile.label':           'Profil',
    'profile.new':             '＋ Neu',
    'profile.delete':          '🗑 Löschen',
    'profile.deleteConfirm':   'Preset „{name}“ löschen?',
    'profile.cantDeleteReserved': 'Die Profile „Default“ und „Vanilla“ können nicht gelöscht werden.',
    'profile.promptName':      'Name des neuen Presets:',
    'mode.manage':             'Verwalten',
    'mode.order':              'Ladereihenfolge',
    'mode.manage.title':       'Mods sortieren und ein-/ausschalten',
    'mode.order.title':        'Ladereihenfolge per Drag & Drop neu anordnen',
    'list.head.toggleAll':     'Alle aktivieren / deaktivieren',
    'list.head.category':      'Kategorie',
    'list.head.name':          'Mod-Name',
    'list.head.size':          'Größe',
    'list.head.status':        'Status',
    'list.empty':              'Keine Mods in den konfigurierten Ordnern gefunden.',
    'count.active':            '{n} / {total} aktiv',
    'pill.active':             'AN',
    'pill.off':                'AUS',
    'detail.empty':            'Wähle einen Mod aus der Liste, um seine Details anzuzeigen.',
    'detail.banner.empty':     'Für diesen Mod wurde kein Banner bereitgestellt.',
    'detail.description':      'Beschreibung',
    'detail.details':          'Details',
    'detail.meta.category':    'Kategorie',
    'detail.meta.difficulty':  'Schwierigkeit',
    'detail.meta.size':        'Größe',
    'detail.meta.folder':      'Ordner',
    'detail.creator':          'von {name} · v{version}',
    'detail.openFolder':       'Ordner öffnen',
    'detail.uninstall':        'Deinstallieren',
    'detail.uninstallConfirm': 'Mod „{name}“ deinstallieren?\n\nDer Ordner wird von der Festplatte gelöscht.',
    'tab.placeholder':         'Dieser Tab wird in Phase 2 der Migration übernommen.',
    'tab.placeholderHint':     'pywebview-POC läuft — momentan funktioniert nur der Tab {tab}.',
    'launch.title':            'Anno 117 starten',
    'launch.error':            'Spiel konnte nicht gestartet werden: {err}',
    'mods.openFolder.title':   'Mods-Ordner öffnen',
    'mods.notFromManager':             'Nicht über den Manager installiert',
    'deps.conflict':           'Konflikt mit: {names}\n\nDieses Mod ist inkompatibel mit einem oder mehreren aktiven Mods.',
    'deps.missingInstalled':   'Fehlende Abhängigkeit (nicht installiert): {names}\n\nErforderliche Mods sind nicht im Mods-Ordner vorhanden.',
    'deps.missingActive':      'Fehlende Abhängigkeit (deaktiviert): {names}\n\nErforderliche Mods sind installiert, aber nicht aktiv.',
    'deps.deprecated':         'Ersetzt durch: {names}\n\nDieses Mod wird durch ein aktives Mod ersetzt. Erwäge, es zu deaktivieren.',
    'deps.dialog.conflict':    '„{mod}" ist inkompatibel mit folgenden aktiven Mods:',
    'deps.dialog.missingInstalled': '„{mod}" benötigt folgende Mods, die nicht installiert sind:',
    'deps.dialog.missingActive': '„{mod}" benötigt folgende Mods, die installiert, aber deaktiviert sind:',
    'deps.dialog.deprecated':  '„{mod}" wird durch folgende aktive Mods ersetzt:',
    'deps.dialog.enable':      'Aktivieren',
    'deps.dialog.disable':     'Deaktivieren',
    'deps.dialog.disableThis': 'Dieses Mod deaktivieren',
    'deps.dialog.install':     'Installieren',
    'deps.dialog.installing':  'Installiere…',
    'deps.dialog.close':       'Schließen',
    'mods.versionMismatch':        'Installiert: v{lv} → Verfügbar: v{rv}\n\nDie Versionsnummern stimmen nicht überein. Klicke, um das Mod direkt auf die neueste Version von mod.io zu aktualisieren.',
    'mods.versionMismatchInfo':    'Installiert: v{lv} · mod.io: v{rv}\n\nDie lokale Version scheint neuer zu sein als die auf mod.io veröffentlichte.',
    'mods.versionMismatchSameFile': 'Installiert: v{lv} · mod.io: v{rv}\n\nDie Versionsbezeichnungen unterscheiden sich, aber die installierte Datei ist aktuell. Dies ist wahrscheinlich eine Inkonsistenz des Erstellers (modinfo.json nicht aktualisiert).',
    'mods.link.cta':                   '🔗 Mit mod.io verknüpfen',
    'mods.link.title':                 '« {name} » mit einem mod.io-Eintrag verknüpfen',
    'mods.link.searchPlaceholder':     'Auf mod.io suchen…',
    'mods.link.confirm':               'Verknüpfen',
    'mods.link.empty':                 'Keine Treffer — versuche es mit einem anderen Namen.',
    'mods.link.cancel':                'Abbrechen',
    'tab.news':                'Neuigkeiten',
    'tab.activation':          'Aktivierung',
    'tab.browser':             'Mod-Browser',
    'tab.collections':         'Sammlungen',
    'tab.install':             'Manuelle Installation',
    'tab.log':                 'Modloader-Log',
    'tab.tweak':               'Anpassung',
    'tab.settings':            'Einstellungen',
    'settings.section.paths':       'Pfade',
    'settings.section.behaviour':   'Verhalten',
    'settings.section.advanced':    'Erweitert',
    'settings.gamePath':            'Anno 117 ausführbare Datei',
    'settings.gamePath.empty':      'Nicht konfiguriert — gib den Pfad zu Anno117.exe an',
    'settings.docsPath':            'Dokumente-Ordner überschreiben',
    'settings.docsPath.empty':      'Automatisch erkannt (nutzt ~/Documents oder das Proton-Präfix)',
    'settings.browseFile':          'Datei auswählen…',
    'settings.browseFolder':        'Ordner auswählen…',
    'settings.autoDetect':          'Automatisch erkennen',
    'settings.clear':               'Löschen',
    'settings.open':                'Öffnen',
    'settings.modLocation':         'Speicherort der Mods',
    'settings.modLocation.documents': 'Dokumente-Ordner (empfohlen)',
    'settings.modLocation.game':      'Spielinstallationsordner',
    'settings.enableNewMods':       'Neu installierte Mods',
    'settings.enableNewMods.on':    'Immer aktivieren',
    'settings.enableNewMods.off':   'Niemals aktivieren',
    'settings.enableNewMods.keep':  'Vorherigen Status beibehalten',
    'settings.textScale':              'Lesetextgröße',
    'settings.textScale.small':        'Klein',
    'settings.textScale.medium':       'Mittel',
    'settings.textScale.large':        'Groß',
    'settings.derived.docsMods':    'Mods-Ordner (Dokumente)',
    'settings.derived.gameMods':    'Mods-Ordner (Spiel)',
    'settings.derived.profile':     'active-profile.txt',
    'settings.derived.appdata':     'AppData',
    'settings.derived.presets':     'Presets',
    'settings.pathError':           'Pfad konnte nicht gespeichert werden: {err}',
    'settings.detectError':         'Automatische Erkennung fehlgeschlagen: {err}',
    'settings.section.modio':       'mod.io-Integration',
    'settings.modio.hint':          'Gib deinen persönlichen mod.io-API-Schlüssel ein, um die Tabs Mod-Browser und Sammlungen zu aktivieren. Erzeuge einen unter',
    'settings.modio.apiKey':        'API-Schlüssel',
    'settings.modio.apiKeyPlaceholder': 'Füge hier deinen mod.io-API-Schlüssel ein',
    'settings.modio.save':          'Speichern',
    'settings.modio.disconnectConfirm': 'Gespeicherten mod.io-API-Schlüssel entfernen?',
    'settings.modio.emptyKey':      'API-Schlüssel ist leer.',
    'log.refresh':                  '↻ Aktualisieren',
    'log.copy':                     '⧉ Kopieren',
    'log.openFile':                 'Datei öffnen',
    'log.loading':                  'Lädt…',
    'log.empty':                    'mod-loader.log ist leer.',
    'log.notFound':                 'mod-loader.log nicht gefunden unter:\n{path}',
    'log.truncated':                'Log auf die letzten 2 MB gekürzt',
    'install.title':                'Manuelle Installation',
    'install.hint':                 'Lege ein Mod-ZIP hier ab oder klicke zum Auswählen. Das Archiv muss eine modinfo.json (oder .jsonc) enthalten.',
    'install.drop':                 'Mod-.zip hier ablegen',
    'install.or':                   '— oder —',
    'install.browse':               'ZIP-Datei auswählen…',
    'install.targetLabel':          'Installationsziel:',
    'install.installing':           '{name} wird installiert…',
    'install.success':              '{name} installiert.',
    'install.cancelled':            'Abgebrochen.',
    'install.overwriteConfirm':     'Ein Mod-Ordner namens „{name}“ existiert bereits. Ersetzen?',
    'tweak.listHeader':             'Anpassbare Mods',
    'tweak.optionWord':             'Optionen',
    'tweak.noTweakable':            'Keiner deiner installierten Mods bietet Optionen.',
    'tweak.pickHint':                'Wähle links einen Mod, um seine Optionen anzupassen.',
    'tweak.noOptions':              'Dieser Mod hat keine konfigurierbaren Optionen.',
    'tweak.resetMod':               'Diesen Mod zurücksetzen',
    'tweak.resetAll':               'Alle zurücksetzen',
    'tweak.resetModConfirm':        'Alle Optionen dieses Mods auf die Standardwerte zurücksetzen?',
    'tweak.resetAllConfirm':        'Optionen aller Mods zurücksetzen? Die Datei active-options.jsonc wird gelöscht.',
    'tweak.defaultsSection':           '— Standardwerte —',
    'tweak.colorPicker.open':          'Farbwähler öffnen',
    'tweak.colorPicker.title':         'Farbwähler',
    'tweak.colorPicker.before':        'Vorher',
    'tweak.colorPicker.after':         'Nachher',
    'tweak.colorPicker.cancel':        'Abbrechen',
    'tweak.colorPicker.apply':         'Anwenden',
    'news.refresh':                 '↻ Aktualisieren',
    'news.loading':                 'Neueste Beiträge werden geladen…',
    'news.empty':                   'Keine Neuigkeiten verfügbar.',
    'news.error':                   'Neuigkeiten konnten nicht geladen werden: {err}',
    'news.cached':                  'zwischengespeichert (10 Min.)',
    'news.includeReddit':           'r/anno-Beiträge einbeziehen',
    'news.visitUnion':              'Anno Union öffnen ↗',
    'news.back':                       'Zurück zu den News',
    'news.openOnUnion':                'Auf Anno Union öffnen ↗',
    'settings.modio.clearKey':      'Schlüssel löschen',
    'modio.badge.connected':        '● Verbunden',
    'modio.badge.keyOnly':          '◐ Nur API-Schlüssel',
    'modio.badge.notSet':           '○ Nicht gesetzt',
    'modio.session':                'Sitzung',
    'modio.expires':                'läuft ab am {date}',
    'modio.disconnect':             'Trennen',
    'modio.disconnectConfirm':      'Verbindung zu mod.io trennen? Dein API-Schlüssel bleibt gespeichert; du kannst dich später erneut verbinden.',
    'modio.needKeyFirst':           'Speichere zuerst deinen API-Schlüssel oben, dann kannst du dich verbinden.',
    'modio.startConnect':           'Mit mod.io verbinden',
    'modio.email':                  'E-Mail-Adresse',
    'modio.emailPlaceholder':       'du@beispiel.com',
    'modio.emailRequired':          'Bitte gib deine E-Mail-Adresse ein.',
    'modio.termsAgree':             'Ich akzeptiere die mod.io',
    'modio.termsLink':              'Nutzungsbedingungen',
    'modio.cancel':                 'Abbrechen',
    'common.cancel':                   'Abbrechen',
    'common.confirm':                  'Bestätigen',
    'modio.sendCode':               'Code senden',
    'modio.sending':                'Wird gesendet…',
    'modio.code':                   'Sicherheitscode',
    'modio.codeRequired':           'Gib den 5-stelligen Code aus deiner E-Mail ein.',
    'modio.codeSent':               'Ein 5-stelliger Code wurde an {email} gesendet. Prüfe dein Postfach (auch Spam).',
    'modio.connect':                'Verbinden',
    'modio.connecting':             'Verbinde…',
    // Mod Browser
    'browser.title':                'Mod-Browser',
    'browser.searchPlaceholder':    'Mods suchen…',
    'browser.search':               'Suchen',
    'browser.refresh':              'Aktualisieren',
    'browser.sortNewest':           'Neueste',
    'browser.sortPopular':          'Beliebteste',
    'browser.sortDownloads':        'Meiste Downloads',
    'browser.sortRating':           'Bestbewertet',
    'browser.sortAlpha':            'A → Z',
    'browser.sortBy':               'Sortieren nach:',
    'browser.mySubscriptions':         'Meine Abonnements',
    'browser.myFollows':               'Meine Follows',
    'browser.follow':                  'Diese Sammlung folgen',
    'browser.unfollow':                'Sammlung nicht mehr folgen',
    'browser.tag':                  'Tag:',
    'browser.tagAll':               'Alle Tags',
    'browser.clearSearch':          'Suche löschen',
    'browser.byAuthor':             'von {name}',
    'browser.clearAuthor':          'Alle Autoren anzeigen',
    'browser.filterByAuthor':       'Nur Mods dieses Autors anzeigen',
    'browser.bundledMods':          'Enthaltene Mods',
    'browser.bundledEmpty':         'Diese Sammlung enthält keine Mods.',
    'browser.backToCollection':     'Zurück zur Sammlung',
    'browser.installCollection':    'Sammlung installieren',
    'browser.updateCollection':     'Sammlung aktualisieren',
    'browser.uninstallCollection':  '🗑 Sammlung deinstallieren',
    'browser.uninstallConfirm':     'Profil „{profile}“, erstellt aus „{name}“, löschen?',
    'browser.uninstallAlsoMods':    'Auch die {count} in dieser Sammlung enthaltenen Mod(s) von der Festplatte entfernen?',
    'browser.uninstallOk':          'Profil „{profile}“ entfernt.',
    'browser.uninstallOkWithMods':  'Profil „{profile}“ entfernt; {count} enthaltene Mod(s) von der Festplatte gelöscht.',
    'browser.uninstallFail':        'Deinstallation fehlgeschlagen: {error}',
    'browser.collectionInstallOk':  '„{name}“: {count}/{total} Mods installiert. Profil „{profile}“ ist nun aktiv.',
    'browser.collectionInstallFailures': '({count} fehlgeschlagen — siehe Log)',
    'browser.back':                 'Zurück',
    'browser.empty':                'Keine Mods entsprechen deiner Suche.',
    'browser.loading':              'Mods werden geladen…',
    'browser.error':                'Mods konnten nicht geladen werden: {error}',
    'browser.notAuth':              'Nicht mit mod.io verbunden. Verbinde dich im Tab Einstellungen.',
    'browser.openSettings':         'Einstellungen öffnen',
    'browser.prev':                 '‹ Zurück',
    'browser.next':                 'Weiter ›',
    'browser.pageOf':               'Seite {page} / {total}',
    'browser.resultsCount':         '{shown} von {total} Mods',
    'browser.detailPick':           'Wähle einen Mod aus der Liste, um seine Details anzuzeigen.',
    'browser.install':              'Installieren',
    'browser.installing':           'Installation läuft…',
    'browser.installed':            '✓ Installiert',
    'browser.update':               'Aktualisieren',
    'browser.installOk':            '„{name}“ installiert.',
    'browser.installFail':          'Installation fehlgeschlagen: {error}',
    'browser.subscribe':            '+ Abonnieren',
    'browser.subscribed':           '✓ Abonniert',
    'browser.unsubscribe':          'Abbestellen',
    'browser.uninstallMod':            '🗑 Deinstallieren',
    'browser.uninstallModConfirm':     '« {name} » von der Festplatte entfernen?',
    'browser.uninstallModOk':          '« {name} » deinstalliert.',
    'browser.endorse':              '♥ Empfehlen',
    'browser.endorsed':             '♥ Empfohlen',
    'browser.endorseFail':          'Empfehlung fehlgeschlagen: {error}',
    'browser.subFail':              'Abonnement fehlgeschlagen: {error}',
    'browser.openOnModio':          'Auf mod.io öffnen ↗',
    'browser.author':               'von {name}',
    'browser.downloads':            '{n} Downloads',
    'browser.subscribers':          '{n} Abonnenten',
    'browser.modsTotal':            '{n} Mods',
    'browser.updated':              'Aktualisiert {date}',
    'browser.size':                 'Größe: {size}',
    'browser.version':              'Version: {v}',
    'browser.changelog':            'Änderungsprotokoll',
    'browser.description':          'Beschreibung',
  },
  spanish: {
    'hud.settings':                 'Ajustes',
    'hud.refreshMods':              'Actualizar la lista de mods',
    'hud.searchMod':                'Buscar un mod…',
    'hud.language':                 'Idioma',
    'alert.loadPresetFail':         'No se pudo cargar el preset: {error}',
    'alert.savePresetFail':         'No se pudo guardar el preset: {error}',
    'alert.deletePresetFail':       'No se pudo eliminar el preset: {error}',
    'alert.uninstallFail':          'Desinstalación fallida: {error}',
    'profile.label':           'Perfil',
    'profile.new':             '＋ Nuevo',
    'profile.delete':          '🗑 Eliminar',
    'profile.deleteConfirm':   '¿Eliminar el preset «{name}»?',
    'profile.cantDeleteReserved': 'Los perfiles «Default» y «Vanilla» no se pueden eliminar.',
    'profile.promptName':      'Nombre del nuevo preset:',
    'mode.manage':             'Gestionar',
    'mode.order':              'Orden de carga',
    'mode.manage.title':       'Ordenar y activar/desactivar mods',
    'mode.order.title':        'Reordenar el orden de carga arrastrando',
    'list.head.toggleAll':     'Activar / desactivar todos',
    'list.head.category':      'Categoría',
    'list.head.name':          'Nombre del mod',
    'list.head.size':          'Tamaño',
    'list.head.status':        'Estado',
    'list.empty':              'No se detectaron mods en las carpetas configuradas.',
    'count.active':            '{n} / {total} activos',
    'pill.active':             'ON',
    'pill.off':                'OFF',
    'detail.empty':            'Selecciona un mod de la lista para ver su ficha.',
    'detail.banner.empty':     'Este mod no incluye ningún banner.',
    'detail.description':      'Descripción',
    'detail.details':          'Detalles',
    'detail.meta.category':    'Categoría',
    'detail.meta.difficulty':  'Dificultad',
    'detail.meta.size':        'Tamaño',
    'detail.meta.folder':      'Carpeta',
    'detail.creator':          'por {name} · v{version}',
    'detail.openFolder':       'Abrir carpeta',
    'detail.uninstall':        'Desinstalar',
    'detail.uninstallConfirm': '¿Desinstalar el mod «{name}»?\n\nLa carpeta se eliminará del disco.',
    'tab.placeholder':         'Esta pestaña se migrará en la fase 2.',
    'tab.placeholderHint':     'POC de pywebview en curso — solo la pestaña {tab} funciona por ahora.',
    'launch.title':            'Iniciar Anno 117',
    'launch.error':            'No se pudo iniciar el juego: {err}',
    'mods.openFolder.title':   'Abrir la carpeta de mods',
    'mods.notFromManager':             'No instalado mediante el gestor',
    'deps.conflict':           'Conflicto con: {names}\n\nEste mod es incompatible con uno o más mods activos.',
    'deps.missingInstalled':   'Dependencia faltante (no instalada): {names}\n\nLos mods requeridos no están presentes en la carpeta de mods.',
    'deps.missingActive':      'Dependencia faltante (desactivada): {names}\n\nLos mods requeridos están instalados pero no activos.',
    'deps.deprecated':         'Reemplazado por: {names}\n\nEste mod ha sido reemplazado por un mod activo. Considera desactivarlo.',
    'deps.dialog.conflict':    '"{mod}" es incompatible con los siguientes mods activos:',
    'deps.dialog.missingInstalled': '"{mod}" requiere los siguientes mods que no están instalados:',
    'deps.dialog.missingActive': '"{mod}" requiere los siguientes mods que están instalados pero desactivados:',
    'deps.dialog.deprecated':  '"{mod}" ha sido reemplazado por los siguientes mods activos:',
    'deps.dialog.enable':      'Activar',
    'deps.dialog.disable':     'Desactivar',
    'deps.dialog.disableThis': 'Desactivar este mod',
    'deps.dialog.install':     'Instalar',
    'deps.dialog.installing':  'Instalando…',
    'deps.dialog.close':       'Cerrar',
    'mods.versionMismatch':        'Instalado: v{lv} → Disponible: v{rv}\n\nHay una discrepancia en los números de versión. Haz clic para actualizar el mod directamente desde mod.io.',
    'mods.versionMismatchInfo':    'Instalado: v{lv} · mod.io: v{rv}\n\nLa versión local parece más reciente que la publicada en mod.io.',
    'mods.versionMismatchSameFile': 'Instalado: v{lv} · mod.io: v{rv}\n\nLas etiquetas de versión difieren pero el archivo instalado está actualizado. Es probable una inconsistencia del autor (modinfo.json no actualizado).',
    'mods.link.cta':                   '🔗 Asociar con mod.io',
    'mods.link.title':                 'Asociar « {name} » a una ficha mod.io',
    'mods.link.searchPlaceholder':     'Buscar en mod.io…',
    'mods.link.confirm':               'Asociar',
    'mods.link.empty':                 'Sin resultados — prueba otro nombre.',
    'mods.link.cancel':                'Cancelar',
    'tab.news':                'Noticias',
    'tab.activation':          'Activación',
    'tab.browser':             'Catálogo de mods',
    'tab.collections':         'Colecciones',
    'tab.install':             'Instalación manual',
    'tab.log':                 'Registro del Modloader',
    'tab.tweak':               'Ajustes',
    'tab.settings':            'Ajustes',
    'settings.section.paths':       'Rutas',
    'settings.section.behaviour':   'Comportamiento',
    'settings.section.advanced':    'Avanzado',
    'settings.gamePath':            'Ejecutable de Anno 117',
    'settings.gamePath.empty':      'Sin configurar — indica la ruta de Anno117.exe',
    'settings.docsPath':            'Carpeta Documentos personalizada',
    'settings.docsPath.empty':      'Detección automática (usa ~/Documents o el prefijo Proton)',
    'settings.browseFile':          'Buscar archivo…',
    'settings.browseFolder':        'Buscar carpeta…',
    'settings.autoDetect':          'Detección automática',
    'settings.clear':               'Borrar',
    'settings.open':                'Abrir',
    'settings.modLocation':         'Ubicación de almacenamiento de mods',
    'settings.modLocation.documents': 'Carpeta Documentos (recomendado)',
    'settings.modLocation.game':      'Carpeta de instalación del juego',
    'settings.enableNewMods':       'Mods recién instalados',
    'settings.enableNewMods.on':    'Activarlos siempre',
    'settings.enableNewMods.off':   'No activarlos nunca',
    'settings.enableNewMods.keep':  'Mantener su estado anterior',
    'settings.textScale':              'Tamaño del texto (lectura)',
    'settings.textScale.small':        'Pequeño',
    'settings.textScale.medium':       'Medio',
    'settings.textScale.large':        'Grande',
    'settings.derived.docsMods':    'Carpeta de mods (Documentos)',
    'settings.derived.gameMods':    'Carpeta de mods (juego)',
    'settings.derived.profile':     'active-profile.txt',
    'settings.derived.appdata':     'AppData',
    'settings.derived.presets':     'Presets',
    'settings.pathError':           'No se pudo guardar la ruta: {err}',
    'settings.detectError':         'Detección automática fallida: {err}',
    'settings.section.modio':       'Integración con mod.io',
    'settings.modio.hint':          'Introduce tu clave API personal de mod.io para activar las pestañas Catálogo y Colecciones. Genera una en',
    'settings.modio.apiKey':        'Clave API',
    'settings.modio.apiKeyPlaceholder': 'Pega aquí tu clave API de mod.io',
    'settings.modio.save':          'Guardar',
    'settings.modio.disconnectConfirm': '¿Eliminar la clave API de mod.io guardada?',
    'settings.modio.emptyKey':      'La clave API está vacía.',
    'log.refresh':                  '↻ Actualizar',
    'log.copy':                     '⧉ Copiar',
    'log.openFile':                 'Abrir archivo',
    'log.loading':                  'Cargando…',
    'log.empty':                    'mod-loader.log está vacío.',
    'log.notFound':                 'mod-loader.log no encontrado en:\n{path}',
    'log.truncated':                'Registro truncado a los últimos 2 MB',
    'install.title':                'Instalación manual',
    'install.hint':                 'Suelta un ZIP de mod aquí o haz clic para buscar. El archivo debe contener un modinfo.json (o .jsonc).',
    'install.drop':                 'Suelta un mod .zip aquí',
    'install.or':                   '— o —',
    'install.browse':               'Buscar un archivo ZIP…',
    'install.targetLabel':          'Destino de la instalación:',
    'install.installing':           'Instalando {name}…',
    'install.success':              '{name} instalado.',
    'install.cancelled':            'Cancelado.',
    'install.overwriteConfirm':     'Ya existe una carpeta de mod llamada «{name}». ¿Reemplazarla?',
    'tweak.listHeader':             'Mods configurables',
    'tweak.optionWord':             'opciones',
    'tweak.noTweakable':            'Ninguno de tus mods instalados ofrece opciones.',
    'tweak.pickHint':                'Selecciona un mod a la izquierda para ajustar sus opciones.',
    'tweak.noOptions':              'Este mod no tiene opciones configurables.',
    'tweak.resetMod':               'Restablecer este mod',
    'tweak.resetAll':               'Restablecer todo',
    'tweak.resetModConfirm':        '¿Restablecer todas las opciones de este mod a sus valores por defecto?',
    'tweak.resetAllConfirm':        '¿Restablecer las opciones de todos los mods? Se eliminará el archivo active-options.jsonc.',
    'tweak.defaultsSection':           '— Valores predeterminados —',
    'tweak.colorPicker.open':          'Abrir el selector de color',
    'tweak.colorPicker.title':         'Selector de color',
    'tweak.colorPicker.before':        'Antes',
    'tweak.colorPicker.after':         'Después',
    'tweak.colorPicker.cancel':        'Cancelar',
    'tweak.colorPicker.apply':         'Aplicar',
    'news.refresh':                 '↻ Actualizar',
    'news.loading':                 'Cargando últimas publicaciones…',
    'news.empty':                   'No hay noticias para mostrar.',
    'news.error':                   'No se pudieron obtener las noticias: {err}',
    'news.cached':                  'en caché (10 min)',
    'news.includeReddit':           'Incluir publicaciones de r/anno',
    'news.visitUnion':              'Abrir Anno Union ↗',
    'news.back':                       'Volver a las noticias',
    'news.openOnUnion':                'Abrir en Anno Union ↗',
    'settings.modio.clearKey':      'Borrar clave',
    'modio.badge.connected':        '● Conectado',
    'modio.badge.keyOnly':          '◐ Solo clave API',
    'modio.badge.notSet':           '○ Sin configurar',
    'modio.session':                'Sesión',
    'modio.expires':                'caduca el {date}',
    'modio.disconnect':             'Desconectar',
    'modio.disconnectConfirm':      '¿Desconectar de mod.io? Tu clave API permanecerá guardada; podrás reconectarte más tarde.',
    'modio.needKeyFirst':           'Guarda primero tu clave API arriba y luego podrás conectarte.',
    'modio.startConnect':           'Conectar a mod.io',
    'modio.email':                  'Correo electrónico',
    'modio.emailPlaceholder':       'tu@ejemplo.com',
    'modio.emailRequired':          'Introduce tu correo electrónico.',
    'modio.termsAgree':             'Acepto los',
    'modio.termsLink':              'Términos de uso de mod.io',
    'modio.cancel':                 'Cancelar',
    'common.cancel':                   'Cancelar',
    'common.confirm':                  'Confirmar',
    'modio.sendCode':               'Enviar código',
    'modio.sending':                'Enviando…',
    'modio.code':                   'Código de seguridad',
    'modio.codeRequired':           'Introduce el código de 5 caracteres recibido por correo.',
    'modio.codeSent':               'Se envió un código de 5 caracteres a {email}. Revisa tu bandeja (y spam).',
    'modio.connect':                'Conectar',
    'modio.connecting':             'Conectando…',
    // Mod Browser
    'browser.title':                'Catálogo de mods',
    'browser.searchPlaceholder':    'Buscar mods…',
    'browser.search':               'Buscar',
    'browser.refresh':              'Actualizar',
    'browser.sortNewest':           'Más recientes',
    'browser.sortPopular':          'Más populares',
    'browser.sortDownloads':        'Más descargados',
    'browser.sortRating':           'Mejor valorados',
    'browser.sortAlpha':            'A → Z',
    'browser.sortBy':               'Ordenar por:',
    'browser.mySubscriptions':         'Mis suscripciones',
    'browser.myFollows':               'Mis seguimientos',
    'browser.follow':                  'Seguir esta colección',
    'browser.unfollow':                'Dejar de seguir esta colección',
    'browser.tag':                  'Etiqueta:',
    'browser.tagAll':               'Todas las etiquetas',
    'browser.clearSearch':          'Borrar búsqueda',
    'browser.byAuthor':             'por {name}',
    'browser.clearAuthor':          'Mostrar todos los autores',
    'browser.filterByAuthor':       'Mostrar solo los mods de este autor',
    'browser.bundledMods':          'Mods incluidos',
    'browser.bundledEmpty':         'Esta colección no incluye mods.',
    'browser.backToCollection':     'Volver a la colección',
    'browser.installCollection':    'Instalar la colección',
    'browser.updateCollection':     'Actualizar la colección',
    'browser.uninstallCollection':  '🗑 Desinstalar la colección',
    'browser.uninstallConfirm':     '¿Eliminar el perfil «{profile}» creado a partir de «{name}»?',
    'browser.uninstallAlsoMods':    '¿Borrar también del disco los {count} mod(s) incluidos en esta colección?',
    'browser.uninstallOk':          'Perfil «{profile}» eliminado.',
    'browser.uninstallOkWithMods':  'Perfil «{profile}» eliminado; {count} mod(s) incluidos borrados del disco.',
    'browser.uninstallFail':        'Desinstalación fallida: {error}',
    'browser.collectionInstallOk':  '«{name}»: {count}/{total} mods instalados. El perfil «{profile}» está ahora activo.',
    'browser.collectionInstallFailures': '({count} fallidos — ver registro)',
    'browser.back':                 'Volver',
    'browser.empty':                'Ningún mod coincide con tu búsqueda.',
    'browser.loading':              'Cargando mods…',
    'browser.error':                'No se pudieron cargar los mods: {error}',
    'browser.notAuth':              'No conectado a mod.io. Conéctate desde la pestaña Ajustes.',
    'browser.openSettings':         'Abrir ajustes',
    'browser.prev':                 '‹ Anterior',
    'browser.next':                 'Siguiente ›',
    'browser.pageOf':               'Página {page} / {total}',
    'browser.resultsCount':         '{shown} de {total} mods',
    'browser.detailPick':           'Selecciona un mod de la lista para ver sus detalles.',
    'browser.install':              'Instalar',
    'browser.installing':           'Instalando…',
    'browser.installed':            '✓ Instalado',
    'browser.update':               'Actualizar',
    'browser.installOk':            '«{name}» instalado.',
    'browser.installFail':          'Instalación fallida: {error}',
    'browser.subscribe':            '+ Suscribirse',
    'browser.subscribed':           '✓ Suscrito',
    'browser.unsubscribe':          'Cancelar suscripción',
    'browser.uninstallMod':            '🗑 Desinstalar',
    'browser.uninstallModConfirm':     '¿Eliminar « {name} » del disco?',
    'browser.uninstallModOk':          '« {name} » desinstalado.',
    'browser.endorse':              '♥ Recomendar',
    'browser.endorsed':             '♥ Recomendado',
    'browser.endorseFail':          'No se pudo recomendar: {error}',
    'browser.subFail':              'No se pudo suscribir: {error}',
    'browser.openOnModio':          'Ver en mod.io ↗',
    'browser.author':               'por {name}',
    'browser.downloads':            '{n} descargas',
    'browser.subscribers':          '{n} suscriptores',
    'browser.modsTotal':            '{n} mods',
    'browser.updated':              'Actualizado el {date}',
    'browser.size':                 'Tamaño: {size}',
    'browser.version':              'Versión: {v}',
    'browser.changelog':            'Notas de versión',
    'browser.description':          'Descripción',
  },
  italian: {
    'hud.settings':                 'Impostazioni',
    'hud.refreshMods':              'Aggiorna l’elenco dei mod',
    'hud.searchMod':                'Cerca un mod…',
    'hud.language':                 'Lingua',
    'alert.loadPresetFail':         'Impossibile caricare il preset: {error}',
    'alert.savePresetFail':         'Impossibile salvare il preset: {error}',
    'alert.deletePresetFail':       'Impossibile eliminare il preset: {error}',
    'alert.uninstallFail':          'Disinstallazione fallita: {error}',
    'profile.label':           'Profilo',
    'profile.new':             '＋ Nuovo',
    'profile.delete':          '🗑 Elimina',
    'profile.deleteConfirm':   'Eliminare il preset «{name}»?',
    'profile.cantDeleteReserved': 'I profili «Default» e «Vanilla» non possono essere eliminati.',
    'profile.promptName':      'Nome del nuovo preset:',
    'mode.manage':             'Gestisci',
    'mode.order':              'Ordine di caricamento',
    'mode.manage.title':       'Ordina e attiva/disattiva i mod',
    'mode.order.title':        'Riorganizza l’ordine di caricamento con drag-and-drop',
    'list.head.toggleAll':     'Attiva / disattiva tutto',
    'list.head.category':      'Categoria',
    'list.head.name':          'Nome del mod',
    'list.head.size':          'Dimensione',
    'list.head.status':        'Stato',
    'list.empty':              'Nessun mod rilevato nelle cartelle configurate.',
    'count.active':            '{n} / {total} attivi',
    'pill.active':             'ON',
    'pill.off':                'OFF',
    'detail.empty':            'Seleziona un mod dall’elenco per vederne la scheda.',
    'detail.banner.empty':     'Nessun banner fornito per questo mod.',
    'detail.description':      'Descrizione',
    'detail.details':          'Dettagli',
    'detail.meta.category':    'Categoria',
    'detail.meta.difficulty':  'Difficoltà',
    'detail.meta.size':        'Dimensione',
    'detail.meta.folder':      'Cartella',
    'detail.creator':          'di {name} · v{version}',
    'detail.openFolder':       'Apri cartella',
    'detail.uninstall':        'Disinstalla',
    'detail.uninstallConfirm': 'Disinstallare il mod «{name}»?\n\nLa cartella verrà eliminata dal disco.',
    'tab.placeholder':         'Questa scheda sarà portata nella fase 2 della migrazione.',
    'tab.placeholderHint':     'POC pywebview in corso — al momento funziona solo la scheda {tab}.',
    'launch.title':            'Avvia Anno 117',
    'launch.error':            'Impossibile avviare il gioco: {err}',
    'mods.openFolder.title':   'Apri la cartella dei mod',
    'mods.notFromManager':             'Non installato tramite il gestore',
    'deps.conflict':           'Conflitto con: {names}\n\nQuesto mod è incompatibile con uno o più mod attivi.',
    'deps.missingInstalled':   'Dipendenza mancante (non installata): {names}\n\nI mod richiesti non sono presenti nella cartella dei mod.',
    'deps.missingActive':      'Dipendenza mancante (disattivata): {names}\n\nI mod richiesti sono installati ma non attivi.',
    'deps.deprecated':         'Sostituito da: {names}\n\nQuesto mod è stato sostituito da un mod attivo. Valuta di disattivarlo.',
    'deps.dialog.conflict':    '"{mod}" è incompatibile con i seguenti mod attivi:',
    'deps.dialog.missingInstalled': '"{mod}" richiede i seguenti mod che non sono installati:',
    'deps.dialog.missingActive': '"{mod}" richiede i seguenti mod che sono installati ma disattivati:',
    'deps.dialog.deprecated':  '"{mod}" è sostituito dai seguenti mod attivi:',
    'deps.dialog.enable':      'Attiva',
    'deps.dialog.disable':     'Disattiva',
    'deps.dialog.disableThis': 'Disattiva questo mod',
    'deps.dialog.install':     'Installa',
    'deps.dialog.installing':  'Installazione…',
    'deps.dialog.close':       'Chiudi',
    'mods.versionMismatch':        'Installato: v{lv} → Disponibile: v{rv}\n\nC’è una discrepanza nei numeri di versione. Clicca per aggiornare il mod direttamente da mod.io.',
    'mods.versionMismatchInfo':    'Installato: v{lv} · mod.io: v{rv}\n\nLa versione locale sembra più recente di quella pubblicata su mod.io.',
    'mods.versionMismatchSameFile': 'Installato: v{lv} · mod.io: v{rv}\n\nLe etichette di versione differiscono ma il file installato è aggiornato. Probabilmente un’incongruenza dell’autore (modinfo.json non aggiornato).',
    'mods.link.cta':                   '🔗 Collega a mod.io',
    'mods.link.title':                 'Collega « {name} » a una scheda mod.io',
    'mods.link.searchPlaceholder':     'Cerca su mod.io…',
    'mods.link.confirm':               'Collega',
    'mods.link.empty':                 'Nessun risultato — prova un altro nome.',
    'mods.link.cancel':                'Annulla',
    'tab.news':                'Notizie',
    'tab.activation':          'Attivazione',
    'tab.browser':             'Catalogo mod',
    'tab.collections':         'Collezioni',
    'tab.install':             'Installazione manuale',
    'tab.log':                 'Log del Modloader',
    'tab.tweak':               'Personalizzazione',
    'tab.settings':            'Impostazioni',
    'settings.section.paths':       'Percorsi',
    'settings.section.behaviour':   'Comportamento',
    'settings.section.advanced':    'Avanzate',
    'settings.gamePath':            'Eseguibile di Anno 117',
    'settings.gamePath.empty':      'Non configurato — imposta il percorso di Anno117.exe',
    'settings.docsPath':            'Cartella Documenti personalizzata',
    'settings.docsPath.empty':      'Rilevata automaticamente (usa ~/Documents o il prefisso Proton)',
    'settings.browseFile':          'Sfoglia file…',
    'settings.browseFolder':        'Sfoglia cartella…',
    'settings.autoDetect':          'Rilevamento automatico',
    'settings.clear':               'Cancella',
    'settings.open':                'Apri',
    'settings.modLocation':         'Percorso di archiviazione dei mod',
    'settings.modLocation.documents': 'Cartella Documenti (consigliato)',
    'settings.modLocation.game':      'Cartella di installazione del gioco',
    'settings.enableNewMods':       'Mod appena installati',
    'settings.enableNewMods.on':    'Attivali sempre',
    'settings.enableNewMods.off':   'Non attivarli mai',
    'settings.enableNewMods.keep':  'Mantieni il loro stato precedente',
    'settings.textScale':              'Dimensione del testo (lettura)',
    'settings.textScale.small':        'Piccolo',
    'settings.textScale.medium':       'Medio',
    'settings.textScale.large':        'Grande',
    'settings.derived.docsMods':    'Cartella mod (Documenti)',
    'settings.derived.gameMods':    'Cartella mod (gioco)',
    'settings.derived.profile':     'active-profile.txt',
    'settings.derived.appdata':     'AppData',
    'settings.derived.presets':     'Presets',
    'settings.pathError':           'Impossibile salvare il percorso: {err}',
    'settings.detectError':         'Rilevamento automatico non riuscito: {err}',
    'settings.section.modio':       'Integrazione mod.io',
    'settings.modio.hint':          'Inserisci la tua chiave API personale di mod.io per attivare le schede Catalogo e Collezioni. Generane una su',
    'settings.modio.apiKey':        'Chiave API',
    'settings.modio.apiKeyPlaceholder': 'Incolla qui la tua chiave API mod.io',
    'settings.modio.save':          'Salva',
    'settings.modio.disconnectConfirm': 'Rimuovere la chiave API mod.io salvata?',
    'settings.modio.emptyKey':      'La chiave API è vuota.',
    'log.refresh':                  '↻ Aggiorna',
    'log.copy':                     '⧉ Copia',
    'log.openFile':                 'Apri file',
    'log.loading':                  'Caricamento…',
    'log.empty':                    'mod-loader.log è vuoto.',
    'log.notFound':                 'mod-loader.log non trovato in:\n{path}',
    'log.truncated':                'Log troncato agli ultimi 2 MB',
    'install.title':                'Installazione manuale',
    'install.hint':                 'Trascina qui un ZIP di mod o clicca per sfogliare. L’archivio deve contenere un file modinfo.json (o .jsonc).',
    'install.drop':                 'Trascina qui un mod .zip',
    'install.or':                   '— oppure —',
    'install.browse':               'Sfoglia un file ZIP…',
    'install.targetLabel':          'Destinazione installazione:',
    'install.installing':           'Installazione di {name}…',
    'install.success':              '{name} installato.',
    'install.cancelled':            'Annullato.',
    'install.overwriteConfirm':     'Esiste già una cartella di mod chiamata «{name}». Sostituirla?',
    'tweak.listHeader':             'Mod personalizzabili',
    'tweak.optionWord':             'opzioni',
    'tweak.noTweakable':            'Nessuno dei tuoi mod installati espone opzioni.',
    'tweak.pickHint':                'Seleziona un mod a sinistra per personalizzarne le opzioni.',
    'tweak.noOptions':              'Questo mod non ha opzioni configurabili.',
    'tweak.resetMod':               'Reimposta questo mod',
    'tweak.resetAll':               'Reimposta tutto',
    'tweak.resetModConfirm':        'Reimpostare tutte le opzioni di questo mod ai valori predefiniti?',
    'tweak.resetAllConfirm':        'Reimpostare le opzioni di tutti i mod? Il file active-options.jsonc sarà eliminato.',
    'tweak.defaultsSection':           '— Valori predefiniti —',
    'tweak.colorPicker.open':          'Apri il selettore colore',
    'tweak.colorPicker.title':         'Selettore colore',
    'tweak.colorPicker.before':        'Prima',
    'tweak.colorPicker.after':         'Dopo',
    'tweak.colorPicker.cancel':        'Annulla',
    'tweak.colorPicker.apply':         'Applica',
    'news.refresh':                 '↻ Aggiorna',
    'news.loading':                 'Recupero degli ultimi post…',
    'news.empty':                   'Nessuna notizia da mostrare.',
    'news.error':                   'Impossibile recuperare le notizie: {err}',
    'news.cached':                  'in cache (10 min)',
    'news.includeReddit':           'Includi i post di r/anno',
    'news.visitUnion':              'Apri Anno Union ↗',
    'news.back':                       'Torna alle notizie',
    'news.openOnUnion':                'Apri su Anno Union ↗',
    'settings.modio.clearKey':      'Cancella chiave',
    'modio.badge.connected':        '● Connesso',
    'modio.badge.keyOnly':          '◐ Solo chiave API',
    'modio.badge.notSet':           '○ Non impostato',
    'modio.session':                'Sessione',
    'modio.expires':                'scade il {date}',
    'modio.disconnect':             'Disconnetti',
    'modio.disconnectConfirm':      'Disconnettersi da mod.io? La tua chiave API resta salvata; potrai riconnetterti più tardi.',
    'modio.needKeyFirst':           'Salva prima la tua chiave API qui sopra, poi potrai connetterti.',
    'modio.startConnect':           'Connetti a mod.io',
    'modio.email':                  'Indirizzo email',
    'modio.emailPlaceholder':       'tu@esempio.com',
    'modio.emailRequired':          'Inserisci la tua email.',
    'modio.termsAgree':             'Accetto i',
    'modio.termsLink':              'Termini d’uso di mod.io',
    'modio.cancel':                 'Annulla',
    'common.cancel':                   'Annulla',
    'common.confirm':                  'Conferma',
    'modio.sendCode':               'Invia codice',
    'modio.sending':                'Invio…',
    'modio.code':                   'Codice di sicurezza',
    'modio.codeRequired':           'Inserisci il codice di 5 caratteri ricevuto via email.',
    'modio.codeSent':               'Un codice di 5 caratteri è stato inviato a {email}. Controlla la posta in arrivo (e lo spam).',
    'modio.connect':                'Connetti',
    'modio.connecting':             'Connessione…',
    // Mod Browser
    'browser.title':                'Catalogo mod',
    'browser.searchPlaceholder':    'Cerca mod…',
    'browser.search':               'Cerca',
    'browser.refresh':              'Aggiorna',
    'browser.sortNewest':           'Più recenti',
    'browser.sortPopular':          'Più popolari',
    'browser.sortDownloads':        'Più scaricati',
    'browser.sortRating':           'Più votati',
    'browser.sortAlpha':            'A → Z',
    'browser.sortBy':               'Ordina per:',
    'browser.mySubscriptions':         'I miei abbonamenti',
    'browser.myFollows':               'I miei follow',
    'browser.follow':                  'Segui questa collezione',
    'browser.unfollow':                'Smetti di seguire questa collezione',
    'browser.tag':                  'Tag:',
    'browser.tagAll':               'Tutti i tag',
    'browser.clearSearch':          'Cancella ricerca',
    'browser.byAuthor':             'di {name}',
    'browser.clearAuthor':          'Mostra tutti gli autori',
    'browser.filterByAuthor':       'Mostra solo i mod di questo autore',
    'browser.bundledMods':          'Mod inclusi',
    'browser.bundledEmpty':         'Questa collezione non elenca mod inclusi.',
    'browser.backToCollection':     'Torna alla collezione',
    'browser.installCollection':    'Installa la collezione',
    'browser.updateCollection':     'Aggiorna la collezione',
    'browser.uninstallCollection':  '🗑 Disinstalla la collezione',
    'browser.uninstallConfirm':     'Eliminare il profilo «{profile}» creato da «{name}»?',
    'browser.uninstallAlsoMods':    'Eliminare anche dal disco i {count} mod inclusi in questa collezione?',
    'browser.uninstallOk':          'Profilo «{profile}» rimosso.',
    'browser.uninstallOkWithMods':  'Profilo «{profile}» rimosso; {count} mod inclusi eliminati dal disco.',
    'browser.uninstallFail':        'Disinstallazione fallita: {error}',
    'browser.collectionInstallOk':  '«{name}»: {count}/{total} mod installati. Il profilo «{profile}» è ora attivo.',
    'browser.collectionInstallFailures': '({count} falliti — vedi log)',
    'browser.back':                 'Indietro',
    'browser.empty':                'Nessun mod corrisponde alla ricerca.',
    'browser.loading':              'Caricamento dei mod…',
    'browser.error':                'Impossibile caricare i mod: {error}',
    'browser.notAuth':              'Non connesso a mod.io. Connettiti dalla scheda Impostazioni.',
    'browser.openSettings':         'Apri impostazioni',
    'browser.prev':                 '‹ Precedente',
    'browser.next':                 'Successivo ›',
    'browser.pageOf':               'Pagina {page} / {total}',
    'browser.resultsCount':         '{shown} di {total} mod',
    'browser.detailPick':           'Seleziona un mod dall’elenco per vederne i dettagli.',
    'browser.install':              'Installa',
    'browser.installing':           'Installazione…',
    'browser.installed':            '✓ Installato',
    'browser.update':               'Aggiorna',
    'browser.installOk':            '«{name}» installato.',
    'browser.installFail':          'Installazione fallita: {error}',
    'browser.subscribe':            '+ Iscriviti',
    'browser.subscribed':           '✓ Iscritto',
    'browser.unsubscribe':          'Annulla iscrizione',
    'browser.uninstallMod':            '🗑 Disinstalla',
    'browser.uninstallModConfirm':     'Rimuovere « {name} » dal disco?',
    'browser.uninstallModOk':          '« {name} » disinstallato.',
    'browser.endorse':              '♥ Consiglia',
    'browser.endorsed':             '♥ Consigliato',
    'browser.endorseFail':          'Impossibile consigliare: {error}',
    'browser.subFail':              'Impossibile iscriversi: {error}',
    'browser.openOnModio':          'Apri su mod.io ↗',
    'browser.author':               'di {name}',
    'browser.downloads':            '{n} download',
    'browser.subscribers':          '{n} iscritti',
    'browser.modsTotal':            '{n} mod',
    'browser.updated':              'Aggiornato il {date}',
    'browser.size':                 'Dimensione: {size}',
    'browser.version':              'Versione: {v}',
    'browser.changelog':            'Note di versione',
    'browser.description':          'Descrizione',
  },
  polish: {
    'hud.settings':                 'Ustawienia',
    'hud.refreshMods':              'Odśwież listę modów',
    'hud.searchMod':                'Szukaj moda…',
    'hud.language':                 'Język',
    'alert.loadPresetFail':         'Nie udało się wczytać presetu: {error}',
    'alert.savePresetFail':         'Nie udało się zapisać presetu: {error}',
    'alert.deletePresetFail':       'Nie udało się usunąć presetu: {error}',
    'alert.uninstallFail':          'Odinstalowanie nie powiodło się: {error}',
    'profile.label':           'Profil',
    'profile.new':             '＋ Nowy',
    'profile.delete':          '🗑 Usuń',
    'profile.deleteConfirm':   'Usunąć preset „{name}”?',
    'profile.cantDeleteReserved': 'Profili „Default” i „Vanilla” nie można usunąć.',
    'profile.promptName':      'Nazwa nowego presetu:',
    'mode.manage':             'Zarządzaj',
    'mode.order':              'Kolejność wczytywania',
    'mode.manage.title':       'Sortuj i włączaj/wyłączaj mody',
    'mode.order.title':        'Zmień kolejność wczytywania metodą przeciągnij i upuść',
    'list.head.toggleAll':     'Włącz / wyłącz wszystko',
    'list.head.category':      'Kategoria',
    'list.head.name':          'Nazwa moda',
    'list.head.size':          'Rozmiar',
    'list.head.status':        'Status',
    'list.empty':              'Nie wykryto modów w skonfigurowanych folderach.',
    'count.active':            '{n} / {total} aktywnych',
    'pill.active':             'WŁ',
    'pill.off':                'WYŁ',
    'detail.empty':            'Wybierz moda z listy, aby zobaczyć jego kartę.',
    'detail.banner.empty':     'Brak banera dla tego moda.',
    'detail.description':      'Opis',
    'detail.details':          'Szczegóły',
    'detail.meta.category':    'Kategoria',
    'detail.meta.difficulty':  'Trudność',
    'detail.meta.size':        'Rozmiar',
    'detail.meta.folder':      'Folder',
    'detail.creator':          'autor: {name} · v{version}',
    'detail.openFolder':       'Otwórz folder',
    'detail.uninstall':        'Odinstaluj',
    'detail.uninstallConfirm': 'Odinstalować moda „{name}”?\n\nFolder zostanie usunięty z dysku.',
    'tab.placeholder':         'Ta zakładka zostanie przeniesiona w fazie 2 migracji.',
    'tab.placeholderHint':     'POC pywebview w toku — na razie działa tylko zakładka {tab}.',
    'launch.title':            'Uruchom Anno 117',
    'launch.error':            'Nie udało się uruchomić gry: {err}',
    'mods.openFolder.title':   'Otwórz folder modów',
    'mods.notFromManager':             'Niezainstalowane przez menedżera',
    'deps.conflict':           'Konflikt z: {names}\n\nTen mod jest niezgodny z jednym lub więcej aktywnymi modami.',
    'deps.missingInstalled':   'Brakująca zależność (niezainstalowana): {names}\n\nWymagane mody nie są obecne w folderze modów.',
    'deps.missingActive':      'Brakująca zależność (wyłączona): {names}\n\nWymagane mody są zainstalowane, ale nie aktywne.',
    'deps.deprecated':         'Zastąpiony przez: {names}\n\nTen mod jest zastąpiony przez aktywny mod. Rozważ jego wyłączenie.',
    'deps.dialog.conflict':    '„{mod}" jest niezgodny z następującymi aktywnymi modami:',
    'deps.dialog.missingInstalled': '„{mod}" wymaga następujących modów, które nie są zainstalowane:',
    'deps.dialog.missingActive': '„{mod}" wymaga następujących modów, które są zainstalowane, ale wyłączone:',
    'deps.dialog.deprecated':  '„{mod}" jest zastąpiony przez następujące aktywne mody:',
    'deps.dialog.enable':      'Włącz',
    'deps.dialog.disable':     'Wyłącz',
    'deps.dialog.disableThis': 'Wyłącz ten mod',
    'deps.dialog.install':     'Zainstaluj',
    'deps.dialog.installing':  'Instalowanie…',
    'deps.dialog.close':       'Zamknij',
    'mods.versionMismatch':        'Zainstalowany: v{lv} → Dostępny: v{rv}\n\nNiezgodność numerów wersji. Kliknij, aby zaktualizować mod bezpośrednio z mod.io.',
    'mods.versionMismatchInfo':    'Zainstalowany: v{lv} · mod.io: v{rv}\n\nLokalna wersja wydaje się nowsza niż opublikowana na mod.io.',
    'mods.versionMismatchSameFile': 'Zainstalowany: v{lv} · mod.io: v{rv}\n\nEtykiety wersji różnią się, ale zainstalowany plik jest aktualny. To prawdopodobnie niespójność autora (modinfo.json nie zaktualizowany).',
    'mods.link.cta':                   '🔗 Połącz z mod.io',
    'mods.link.title':                 'Połącz « {name} » z wpisem mod.io',
    'mods.link.searchPlaceholder':     'Szukaj w mod.io…',
    'mods.link.confirm':               'Połącz',
    'mods.link.empty':                 'Brak wyników — spróbuj innej nazwy.',
    'mods.link.cancel':                'Anuluj',
    'tab.news':                'Aktualności',
    'tab.activation':          'Aktywacja',
    'tab.browser':             'Przeglądarka modów',
    'tab.collections':         'Kolekcje',
    'tab.install':             'Instalacja ręczna',
    'tab.log':                 'Log Modloadera',
    'tab.tweak':               'Dostosowanie',
    'tab.settings':            'Ustawienia',
    'settings.section.paths':       'Ścieżki',
    'settings.section.behaviour':   'Zachowanie',
    'settings.section.advanced':    'Zaawansowane',
    'settings.gamePath':            'Plik wykonywalny Anno 117',
    'settings.gamePath.empty':      'Nieskonfigurowane — podaj ścieżkę do Anno117.exe',
    'settings.docsPath':            'Niestandardowy folder Dokumenty',
    'settings.docsPath.empty':      'Wykrywane automatycznie (używa ~/Documents lub prefiksu Proton)',
    'settings.browseFile':          'Wybierz plik…',
    'settings.browseFolder':        'Wybierz folder…',
    'settings.autoDetect':          'Wykryj automatycznie',
    'settings.clear':               'Wyczyść',
    'settings.open':                'Otwórz',
    'settings.modLocation':         'Lokalizacja przechowywania modów',
    'settings.modLocation.documents': 'Folder Dokumenty (zalecane)',
    'settings.modLocation.game':      'Folder instalacji gry',
    'settings.enableNewMods':       'Nowo zainstalowane mody',
    'settings.enableNewMods.on':    'Zawsze aktywuj',
    'settings.enableNewMods.off':   'Nigdy nie aktywuj',
    'settings.enableNewMods.keep':  'Zachowaj poprzedni stan',
    'settings.textScale':              'Rozmiar tekstu (czytanie)',
    'settings.textScale.small':        'Mały',
    'settings.textScale.medium':       'Średni',
    'settings.textScale.large':        'Duży',
    'settings.derived.docsMods':    'Folder modów (Dokumenty)',
    'settings.derived.gameMods':    'Folder modów (gra)',
    'settings.derived.profile':     'active-profile.txt',
    'settings.derived.appdata':     'AppData',
    'settings.derived.presets':     'Presety',
    'settings.pathError':           'Nie udało się zapisać ścieżki: {err}',
    'settings.detectError':         'Automatyczne wykrywanie nie powiodło się: {err}',
    'settings.section.modio':       'Integracja z mod.io',
    'settings.modio.hint':          'Wprowadź swój osobisty klucz API mod.io, aby włączyć zakładki Przeglądarka modów i Kolekcje. Wygeneruj go na',
    'settings.modio.apiKey':        'Klucz API',
    'settings.modio.apiKeyPlaceholder': 'Wklej tutaj swój klucz API mod.io',
    'settings.modio.save':          'Zapisz',
    'settings.modio.disconnectConfirm': 'Usunąć zapisany klucz API mod.io?',
    'settings.modio.emptyKey':      'Klucz API jest pusty.',
    'log.refresh':                  '↻ Odśwież',
    'log.copy':                     '⧉ Kopiuj',
    'log.openFile':                 'Otwórz plik',
    'log.loading':                  'Ładowanie…',
    'log.empty':                    'mod-loader.log jest pusty.',
    'log.notFound':                 'mod-loader.log nie znaleziony pod adresem:\n{path}',
    'log.truncated':                'Log skrócony do ostatnich 2 MB',
    'install.title':                'Instalacja ręczna',
    'install.hint':                 'Upuść tutaj plik ZIP moda lub kliknij, aby przeglądać. Archiwum musi zawierać plik modinfo.json (lub .jsonc).',
    'install.drop':                 'Upuść moda .zip tutaj',
    'install.or':                   '— lub —',
    'install.browse':               'Wybierz plik ZIP…',
    'install.targetLabel':          'Miejsce instalacji:',
    'install.installing':           'Instalowanie {name}…',
    'install.success':              '{name} zainstalowany.',
    'install.cancelled':            'Anulowano.',
    'install.overwriteConfirm':     'Folder moda o nazwie „{name}” już istnieje. Zastąpić?',
    'tweak.listHeader':             'Konfigurowalne mody',
    'tweak.optionWord':             'opcji',
    'tweak.noTweakable':            'Żaden z zainstalowanych modów nie udostępnia opcji.',
    'tweak.pickHint':                'Wybierz moda po lewej, aby dostosować jego opcje.',
    'tweak.noOptions':              'Ten mod nie ma konfigurowalnych opcji.',
    'tweak.resetMod':               'Zresetuj tego moda',
    'tweak.resetAll':               'Zresetuj wszystkie',
    'tweak.resetModConfirm':        'Zresetować wszystkie opcje tego moda do wartości domyślnych?',
    'tweak.resetAllConfirm':        'Zresetować opcje wszystkich modów? Plik active-options.jsonc zostanie usunięty.',
    'tweak.defaultsSection':           '— Wartości domyślne —',
    'tweak.colorPicker.open':          'Otwórz selektor koloru',
    'tweak.colorPicker.title':         'Selektor koloru',
    'tweak.colorPicker.before':        'Przed',
    'tweak.colorPicker.after':         'Po',
    'tweak.colorPicker.cancel':        'Anuluj',
    'tweak.colorPicker.apply':         'Zastosuj',
    'news.refresh':                 '↻ Odśwież',
    'news.loading':                 'Pobieranie najnowszych wpisów…',
    'news.empty':                   'Brak aktualności do wyświetlenia.',
    'news.error':                   'Nie udało się pobrać aktualności: {err}',
    'news.cached':                  'w pamięci podręcznej (10 min)',
    'news.includeReddit':           'Uwzględnij wpisy z r/anno',
    'news.visitUnion':              'Otwórz Anno Union ↗',
    'news.back':                       'Powrót do aktualności',
    'news.openOnUnion':                'Otwórz na Anno Union ↗',
    'settings.modio.clearKey':      'Wyczyść klucz',
    'modio.badge.connected':        '● Połączono',
    'modio.badge.keyOnly':          '◐ Tylko klucz API',
    'modio.badge.notSet':           '○ Nieustawione',
    'modio.session':                'Sesja',
    'modio.expires':                'wygasa {date}',
    'modio.disconnect':             'Rozłącz',
    'modio.disconnectConfirm':      'Rozłączyć się z mod.io? Twój klucz API pozostanie zapisany; możesz połączyć się ponownie później.',
    'modio.needKeyFirst':           'Najpierw zapisz swój klucz API powyżej, potem możesz się połączyć.',
    'modio.startConnect':           'Połącz z mod.io',
    'modio.email':                  'Adres e-mail',
    'modio.emailPlaceholder':       'ty@przyklad.com',
    'modio.emailRequired':          'Wprowadź swój adres e-mail.',
    'modio.termsAgree':             'Akceptuję',
    'modio.termsLink':              'Warunki korzystania mod.io',
    'modio.cancel':                 'Anuluj',
    'common.cancel':                   'Anuluj',
    'common.confirm':                  'Potwierdź',
    'modio.sendCode':               'Wyślij kod',
    'modio.sending':                'Wysyłanie…',
    'modio.code':                   'Kod bezpieczeństwa',
    'modio.codeRequired':           'Wprowadź 5-znakowy kod otrzymany e-mailem.',
    'modio.codeSent':               '5-znakowy kod został wysłany na {email}. Sprawdź skrzynkę odbiorczą (i spam).',
    'modio.connect':                'Połącz',
    'modio.connecting':             'Łączenie…',
    // Mod Browser
    'browser.title':                'Przeglądarka modów',
    'browser.searchPlaceholder':    'Szukaj modów…',
    'browser.search':               'Szukaj',
    'browser.refresh':              'Odśwież',
    'browser.sortNewest':           'Najnowsze',
    'browser.sortPopular':          'Najpopularniejsze',
    'browser.sortDownloads':        'Najczęściej pobierane',
    'browser.sortRating':           'Najlepiej oceniane',
    'browser.sortAlpha':            'A → Z',
    'browser.sortBy':               'Sortuj według:',
    'browser.mySubscriptions':         'Moje subskrypcje',
    'browser.myFollows':               'Moje obserwacje',
    'browser.follow':                  'Obserwuj tę kolekcję',
    'browser.unfollow':                'Przestań obserwować tę kolekcję',
    'browser.tag':                  'Tag:',
    'browser.tagAll':               'Wszystkie tagi',
    'browser.clearSearch':          'Wyczyść wyszukiwanie',
    'browser.byAuthor':             'autor: {name}',
    'browser.clearAuthor':          'Pokaż wszystkich autorów',
    'browser.filterByAuthor':       'Pokaż tylko mody tego autora',
    'browser.bundledMods':          'Dołączone mody',
    'browser.bundledEmpty':         'Ta kolekcja nie zawiera żadnych modów.',
    'browser.backToCollection':     'Wróć do kolekcji',
    'browser.installCollection':    'Zainstaluj kolekcję',
    'browser.updateCollection':     'Aktualizuj kolekcję',
    'browser.uninstallCollection':  '🗑 Odinstaluj kolekcję',
    'browser.uninstallConfirm':     'Usunąć profil „{profile}” utworzony z „{name}”?',
    'browser.uninstallAlsoMods':    'Usunąć także z dysku {count} mod(ów) dołączonych do tej kolekcji?',
    'browser.uninstallOk':          'Profil „{profile}” usunięty.',
    'browser.uninstallOkWithMods':  'Profil „{profile}” usunięty; {count} dołączonych modów usuniętych z dysku.',
    'browser.uninstallFail':        'Odinstalowanie nie powiodło się: {error}',
    'browser.collectionInstallOk':  '„{name}”: {count}/{total} modów zainstalowanych. Profil „{profile}” jest teraz aktywny.',
    'browser.collectionInstallFailures': '({count} nieudanych — zobacz log)',
    'browser.back':                 'Wróć',
    'browser.empty':                'Żaden mod nie pasuje do wyszukiwania.',
    'browser.loading':              'Ładowanie modów…',
    'browser.error':                'Nie udało się załadować modów: {error}',
    'browser.notAuth':              'Nie połączono z mod.io. Połącz się w zakładce Ustawienia.',
    'browser.openSettings':         'Otwórz ustawienia',
    'browser.prev':                 '‹ Poprzednia',
    'browser.next':                 'Następna ›',
    'browser.pageOf':               'Strona {page} / {total}',
    'browser.resultsCount':         '{shown} z {total} modów',
    'browser.detailPick':           'Wybierz moda z listy, aby zobaczyć jego szczegóły.',
    'browser.install':              'Zainstaluj',
    'browser.installing':           'Instalowanie…',
    'browser.installed':            '✓ Zainstalowano',
    'browser.update':               'Aktualizuj',
    'browser.installOk':            '„{name}” zainstalowany.',
    'browser.installFail':          'Instalacja nie powiodła się: {error}',
    'browser.subscribe':            '+ Subskrybuj',
    'browser.subscribed':           '✓ Subskrybowano',
    'browser.unsubscribe':          'Anuluj subskrypcję',
    'browser.uninstallMod':            '🗑 Odinstaluj',
    'browser.uninstallModConfirm':     'Usunąć « {name} » z dysku?',
    'browser.uninstallModOk':          '« {name} » odinstalowano.',
    'browser.endorse':              '♥ Poleć',
    'browser.endorsed':             '♥ Polecono',
    'browser.endorseFail':          'Nie udało się polecić: {error}',
    'browser.subFail':              'Nie udało się subskrybować: {error}',
    'browser.openOnModio':          'Otwórz w mod.io ↗',
    'browser.author':               'autor: {name}',
    'browser.downloads':            '{n} pobrań',
    'browser.subscribers':          '{n} subskrybentów',
    'browser.modsTotal':            '{n} modów',
    'browser.updated':              'Aktualizacja: {date}',
    'browser.size':                 'Rozmiar: {size}',
    'browser.version':              'Wersja: {v}',
    'browser.changelog':            'Lista zmian',
    'browser.description':          'Opis',
  },
  russian: {
    'hud.settings':                 'Настройки',
    'hud.refreshMods':              'Обновить список модов',
    'hud.searchMod':                'Поиск мода…',
    'hud.language':                 'Язык',
    'alert.loadPresetFail':         'Не удалось загрузить пресет: {error}',
    'alert.savePresetFail':         'Не удалось сохранить пресет: {error}',
    'alert.deletePresetFail':       'Не удалось удалить пресет: {error}',
    'alert.uninstallFail':          'Не удалось удалить: {error}',
    'profile.label':           'Профиль',
    'profile.new':             '＋ Новый',
    'profile.delete':          '🗑 Удалить',
    'profile.deleteConfirm':   'Удалить пресет «{name}»?',
    'profile.cantDeleteReserved': 'Профили «Default» и «Vanilla» нельзя удалить.',
    'profile.promptName':      'Имя нового пресета:',
    'mode.manage':             'Управление',
    'mode.order':              'Порядок загрузки',
    'mode.manage.title':       'Сортировать и включать/выключать моды',
    'mode.order.title':        'Изменить порядок загрузки перетаскиванием',
    'list.head.toggleAll':     'Включить / выключить все',
    'list.head.category':      'Категория',
    'list.head.name':          'Название мода',
    'list.head.size':          'Размер',
    'list.head.status':        'Статус',
    'list.empty':              'В настроенных папках моды не обнаружены.',
    'count.active':            '{n} / {total} активны',
    'pill.active':             'ВКЛ',
    'pill.off':                'ВЫКЛ',
    'detail.empty':            'Выберите мод из списка, чтобы увидеть его карточку.',
    'detail.banner.empty':     'Для этого мода баннер не предоставлен.',
    'detail.description':      'Описание',
    'detail.details':          'Подробности',
    'detail.meta.category':    'Категория',
    'detail.meta.difficulty':  'Сложность',
    'detail.meta.size':        'Размер',
    'detail.meta.folder':      'Папка',
    'detail.creator':          'автор: {name} · v{version}',
    'detail.openFolder':       'Открыть папку',
    'detail.uninstall':        'Удалить',
    'detail.uninstallConfirm': 'Удалить мод «{name}»?\n\nПапка будет удалена с диска.',
    'tab.placeholder':         'Эта вкладка будет перенесена во второй фазе миграции.',
    'tab.placeholderHint':     'POC pywebview в процессе — пока работает только вкладка {tab}.',
    'launch.title':            'Запустить Anno 117',
    'launch.error':            'Не удалось запустить игру: {err}',
    'mods.openFolder.title':   'Открыть папку модов',
    'mods.notFromManager':             'Установлено не через менеджер',
    'deps.conflict':           'Конфликт с: {names}\n\nЭтот мод несовместим с одним или несколькими активными модами.',
    'deps.missingInstalled':   'Отсутствующая зависимость (не установлена): {names}\n\nНеобходимые моды отсутствуют в папке модов.',
    'deps.missingActive':      'Отсутствующая зависимость (отключена): {names}\n\nНеобходимые моды установлены, но не активны.',
    'deps.deprecated':         'Заменён: {names}\n\nЭтот мод заменён активным модом. Рекомендуется отключить его.',
    'deps.dialog.conflict':    '«{mod}» несовместим со следующими активными модами:',
    'deps.dialog.missingInstalled': '«{mod}» требует следующие моды, которые не установлены:',
    'deps.dialog.missingActive': '«{mod}» требует следующие моды, которые установлены, но отключены:',
    'deps.dialog.deprecated':  '«{mod}» заменён следующими активными модами:',
    'deps.dialog.enable':      'Включить',
    'deps.dialog.disable':     'Отключить',
    'deps.dialog.disableThis': 'Отключить этот мод',
    'deps.dialog.install':     'Установить',
    'deps.dialog.installing':  'Установка…',
    'deps.dialog.close':       'Закрыть',
    'mods.versionMismatch':        'Установлено: v{lv} → Доступно: v{rv}\n\nНесоответствие номеров версий. Нажмите, чтобы обновить мод напрямую с mod.io.',
    'mods.versionMismatchInfo':    'Установлено: v{lv} · mod.io: v{rv}\n\nЛокальная версия, по всей видимости, новее опубликованной на mod.io.',
    'mods.versionMismatchSameFile': 'Установлено: v{lv} · mod.io: v{rv}\n\nМетки версий отличаются, но установленный файл актуален. Вероятно, непоследовательность автора (modinfo.json не обновлён).',
    'mods.link.cta':                   '🔗 Связать с mod.io',
    'mods.link.title':                 'Связать « {name} » с записью mod.io',
    'mods.link.searchPlaceholder':     'Поиск в mod.io…',
    'mods.link.confirm':               'Связать',
    'mods.link.empty':                 'Нет совпадений — попробуйте другое имя.',
    'mods.link.cancel':                'Отмена',
    'tab.news':                'Новости',
    'tab.activation':          'Активация',
    'tab.browser':             'Каталог модов',
    'tab.collections':         'Коллекции',
    'tab.install':             'Ручная установка',
    'tab.log':                 'Журнал Modloader',
    'tab.tweak':               'Настройка',
    'tab.settings':            'Настройки',
    'settings.section.paths':       'Пути',
    'settings.section.behaviour':   'Поведение',
    'settings.section.advanced':    'Дополнительно',
    'settings.gamePath':            'Исполняемый файл Anno 117',
    'settings.gamePath.empty':      'Не настроено — укажите путь к Anno117.exe',
    'settings.docsPath':            'Переопределение папки «Документы»',
    'settings.docsPath.empty':      'Определяется автоматически (используется ~/Documents или префикс Proton)',
    'settings.browseFile':          'Выбрать файл…',
    'settings.browseFolder':        'Выбрать папку…',
    'settings.autoDetect':          'Определить автоматически',
    'settings.clear':               'Очистить',
    'settings.open':                'Открыть',
    'settings.modLocation':         'Расположение хранилища модов',
    'settings.modLocation.documents': 'Папка «Документы» (рекомендуется)',
    'settings.modLocation.game':      'Папка установки игры',
    'settings.enableNewMods':       'Только что установленные моды',
    'settings.enableNewMods.on':    'Всегда активировать',
    'settings.enableNewMods.off':   'Никогда не активировать',
    'settings.enableNewMods.keep':  'Сохранять прежнее состояние',
    'settings.textScale':              'Размер текста (чтение)',
    'settings.textScale.small':        'Маленький',
    'settings.textScale.medium':       'Средний',
    'settings.textScale.large':        'Большой',
    'settings.derived.docsMods':    'Папка модов (Документы)',
    'settings.derived.gameMods':    'Папка модов (игра)',
    'settings.derived.profile':     'active-profile.txt',
    'settings.derived.appdata':     'AppData',
    'settings.derived.presets':     'Пресеты',
    'settings.pathError':           'Не удалось сохранить путь: {err}',
    'settings.detectError':         'Не удалось определить автоматически: {err}',
    'settings.section.modio':       'Интеграция с mod.io',
    'settings.modio.hint':          'Введите свой персональный API-ключ mod.io, чтобы включить вкладки «Каталог» и «Коллекции». Сгенерируйте ключ на',
    'settings.modio.apiKey':        'API-ключ',
    'settings.modio.apiKeyPlaceholder': 'Вставьте сюда свой API-ключ mod.io',
    'settings.modio.save':          'Сохранить',
    'settings.modio.disconnectConfirm': 'Удалить сохранённый API-ключ mod.io?',
    'settings.modio.emptyKey':      'API-ключ пуст.',
    'log.refresh':                  '↻ Обновить',
    'log.copy':                     '⧉ Копировать',
    'log.openFile':                 'Открыть файл',
    'log.loading':                  'Загрузка…',
    'log.empty':                    'mod-loader.log пуст.',
    'log.notFound':                 'mod-loader.log не найден по пути:\n{path}',
    'log.truncated':                'Журнал обрезан до последних 2 МБ',
    'install.title':                'Ручная установка',
    'install.hint':                 'Перетащите ZIP мода сюда или кликните для выбора. Архив должен содержать файл modinfo.json (или .jsonc).',
    'install.drop':                 'Перетащите мод .zip сюда',
    'install.or':                   '— или —',
    'install.browse':               'Выбрать ZIP-файл…',
    'install.targetLabel':          'Назначение установки:',
    'install.installing':           'Установка {name}…',
    'install.success':              '{name} установлен.',
    'install.cancelled':            'Отменено.',
    'install.overwriteConfirm':     'Папка мода «{name}» уже существует. Заменить?',
    'tweak.listHeader':             'Настраиваемые моды',
    'tweak.optionWord':             'опции',
    'tweak.noTweakable':            'Ни один из установленных модов не предоставляет опций.',
    'tweak.pickHint':                'Выберите мод слева, чтобы настроить его опции.',
    'tweak.noOptions':              'У этого мода нет настраиваемых опций.',
    'tweak.resetMod':               'Сбросить этот мод',
    'tweak.resetAll':               'Сбросить всё',
    'tweak.resetModConfirm':        'Сбросить все опции этого мода к значениям по умолчанию?',
    'tweak.resetAllConfirm':        'Сбросить опции всех модов? Файл active-options.jsonc будет удалён.',
    'tweak.defaultsSection':           '— Значения по умолчанию —',
    'tweak.colorPicker.open':          'Открыть выбор цвета',
    'tweak.colorPicker.title':         'Выбор цвета',
    'tweak.colorPicker.before':        'До',
    'tweak.colorPicker.after':         'После',
    'tweak.colorPicker.cancel':        'Отмена',
    'tweak.colorPicker.apply':         'Применить',
    'news.refresh':                 '↻ Обновить',
    'news.loading':                 'Получение последних публикаций…',
    'news.empty':                   'Нет новостей для отображения.',
    'news.error':                   'Не удалось получить новости: {err}',
    'news.cached':                  'в кэше (10 мин)',
    'news.includeReddit':           'Включать публикации r/anno',
    'news.visitUnion':              'Открыть Anno Union ↗',
    'news.back':                       'Назад к новостям',
    'news.openOnUnion':                'Открыть на Anno Union ↗',
    'settings.modio.clearKey':      'Очистить ключ',
    'modio.badge.connected':        '● Подключено',
    'modio.badge.keyOnly':          '◐ Только API-ключ',
    'modio.badge.notSet':           '○ Не настроено',
    'modio.session':                'Сессия',
    'modio.expires':                'истекает {date}',
    'modio.disconnect':             'Отключить',
    'modio.disconnectConfirm':      'Отключиться от mod.io? Ваш API-ключ останется сохранён; вы сможете подключиться снова позже.',
    'modio.needKeyFirst':           'Сначала сохраните свой API-ключ выше, затем сможете подключиться.',
    'modio.startConnect':           'Подключиться к mod.io',
    'modio.email':                  'Адрес электронной почты',
    'modio.emailPlaceholder':       'vy@example.com',
    'modio.emailRequired':          'Введите свой email.',
    'modio.termsAgree':             'Я принимаю',
    'modio.termsLink':              'Условия использования mod.io',
    'modio.cancel':                 'Отмена',
    'common.cancel':                   'Отмена',
    'common.confirm':                  'Подтвердить',
    'modio.sendCode':               'Отправить код',
    'modio.sending':                'Отправка…',
    'modio.code':                   'Код безопасности',
    'modio.codeRequired':           'Введите 5-значный код, полученный по email.',
    'modio.codeSent':               '5-значный код отправлен на {email}. Проверьте входящие (и спам).',
    'modio.connect':                'Подключить',
    'modio.connecting':             'Подключение…',
    // Mod Browser
    'browser.title':                'Каталог модов',
    'browser.searchPlaceholder':    'Поиск модов…',
    'browser.search':               'Найти',
    'browser.refresh':              'Обновить',
    'browser.sortNewest':           'Новейшие',
    'browser.sortPopular':          'Популярные',
    'browser.sortDownloads':        'Самые скачиваемые',
    'browser.sortRating':           'Лучшие по рейтингу',
    'browser.sortAlpha':            'А → Я',
    'browser.sortBy':               'Сортировать по:',
    'browser.mySubscriptions':         'Мои подписки',
    'browser.myFollows':               'Мои отслеживания',
    'browser.follow':                  'Подписаться на коллекцию',
    'browser.unfollow':                'Отписаться от коллекции',
    'browser.tag':                  'Тег:',
    'browser.tagAll':               'Все теги',
    'browser.clearSearch':          'Очистить поиск',
    'browser.byAuthor':             'автор: {name}',
    'browser.clearAuthor':          'Показать всех авторов',
    'browser.filterByAuthor':       'Показать только моды этого автора',
    'browser.bundledMods':          'Включённые моды',
    'browser.bundledEmpty':         'В этой коллекции нет модов.',
    'browser.backToCollection':     'Назад к коллекции',
    'browser.installCollection':    'Установить коллекцию',
    'browser.updateCollection':     'Обновить коллекцию',
    'browser.uninstallCollection':  '🗑 Удалить коллекцию',
    'browser.uninstallConfirm':     'Удалить профиль «{profile}», созданный из «{name}»?',
    'browser.uninstallAlsoMods':    'Также удалить с диска {count} мод(ов), включённых в эту коллекцию?',
    'browser.uninstallOk':          'Профиль «{profile}» удалён.',
    'browser.uninstallOkWithMods':  'Профиль «{profile}» удалён; {count} включённых модов удалено с диска.',
    'browser.uninstallFail':        'Не удалось удалить: {error}',
    'browser.collectionInstallOk':  '«{name}»: {count}/{total} модов установлено. Профиль «{profile}» теперь активен.',
    'browser.collectionInstallFailures': '({count} с ошибками — см. журнал)',
    'browser.back':                 'Назад',
    'browser.empty':                'Ни один мод не соответствует поиску.',
    'browser.loading':              'Загрузка модов…',
    'browser.error':                'Не удалось загрузить моды: {error}',
    'browser.notAuth':              'Не подключено к mod.io. Подключитесь во вкладке «Настройки».',
    'browser.openSettings':         'Открыть настройки',
    'browser.prev':                 '‹ Назад',
    'browser.next':                 'Вперёд ›',
    'browser.pageOf':               'Страница {page} / {total}',
    'browser.resultsCount':         '{shown} из {total} модов',
    'browser.detailPick':           'Выберите мод из списка, чтобы увидеть его подробности.',
    'browser.install':              'Установить',
    'browser.installing':           'Установка…',
    'browser.installed':            '✓ Установлено',
    'browser.update':               'Обновить',
    'browser.installOk':            '«{name}» установлен.',
    'browser.installFail':          'Установка не удалась: {error}',
    'browser.subscribe':            '+ Подписаться',
    'browser.subscribed':           '✓ Подписан',
    'browser.unsubscribe':          'Отписаться',
    'browser.uninstallMod':            '🗑 Удалить',
    'browser.uninstallModConfirm':     'Удалить « {name} » с диска?',
    'browser.uninstallModOk':          '« {name} » удалён.',
    'browser.endorse':              '♥ Рекомендовать',
    'browser.endorsed':             '♥ Рекомендовано',
    'browser.endorseFail':          'Не удалось рекомендовать: {error}',
    'browser.subFail':              'Не удалось подписаться: {error}',
    'browser.openOnModio':          'Открыть на mod.io ↗',
    'browser.author':               'автор: {name}',
    'browser.downloads':            '{n} загрузок',
    'browser.subscribers':          '{n} подписчиков',
    'browser.modsTotal':            '{n} модов',
    'browser.updated':              'Обновлено {date}',
    'browser.size':                 'Размер: {size}',
    'browser.version':              'Версия: {v}',
    'browser.changelog':            'Список изменений',
    'browser.description':          'Описание',
  },
  brazilian: {
    'hud.settings':                 'Configurações',
    'hud.refreshMods':              'Atualizar lista de mods',
    'hud.searchMod':                'Pesquisar mod…',
    'hud.language':                 'Idioma',
    'alert.loadPresetFail':         'Falha ao carregar o preset: {error}',
    'alert.savePresetFail':         'Falha ao salvar o preset: {error}',
    'alert.deletePresetFail':       'Falha ao excluir o preset: {error}',
    'alert.uninstallFail':          'Falha na desinstalação: {error}',
    'profile.label':           'Perfil',
    'profile.new':             '＋ Novo',
    'profile.delete':          '🗑 Excluir',
    'profile.deleteConfirm':   'Excluir o preset «{name}»?',
    'profile.cantDeleteReserved': 'Os perfis «Default» e «Vanilla» não podem ser excluídos.',
    'profile.promptName':      'Nome do novo preset:',
    'mode.manage':             'Gerenciar',
    'mode.order':              'Ordem de carregamento',
    'mode.manage.title':       'Ordenar e ativar/desativar mods',
    'mode.order.title':        'Reordenar a ordem de carregamento por arrastar e soltar',
    'list.head.toggleAll':     'Ativar / desativar todos',
    'list.head.category':      'Categoria',
    'list.head.name':          'Nome do mod',
    'list.head.size':          'Tamanho',
    'list.head.status':        'Status',
    'list.empty':              'Nenhum mod detectado nas pastas configuradas.',
    'count.active':            '{n} / {total} ativos',
    'pill.active':             'ON',
    'pill.off':                'OFF',
    'detail.empty':            'Selecione um mod da lista para ver sua ficha.',
    'detail.banner.empty':     'Nenhum banner fornecido para este mod.',
    'detail.description':      'Descrição',
    'detail.details':          'Detalhes',
    'detail.meta.category':    'Categoria',
    'detail.meta.difficulty':  'Dificuldade',
    'detail.meta.size':        'Tamanho',
    'detail.meta.folder':      'Pasta',
    'detail.creator':          'por {name} · v{version}',
    'detail.openFolder':       'Abrir pasta',
    'detail.uninstall':        'Desinstalar',
    'detail.uninstallConfirm': 'Desinstalar o mod «{name}»?\n\nA pasta será excluída do disco.',
    'tab.placeholder':         'Esta aba será portada na fase 2 da migração.',
    'tab.placeholderHint':     'POC pywebview em andamento — apenas a aba {tab} funciona por enquanto.',
    'launch.title':            'Iniciar Anno 117',
    'launch.error':            'Não foi possível iniciar o jogo: {err}',
    'mods.openFolder.title':   'Abrir a pasta de mods',
    'mods.notFromManager':             'Não instalado pelo gerenciador',
    'deps.conflict':           'Conflito com: {names}\n\nEste mod é incompatível com um ou mais mods ativos.',
    'deps.missingInstalled':   'Dependência ausente (não instalada): {names}\n\nOs mods necessários não estão presentes na pasta de mods.',
    'deps.missingActive':      'Dependência ausente (desativada): {names}\n\nOs mods necessários estão instalados mas não ativos.',
    'deps.deprecated':         'Substituído por: {names}\n\nEste mod foi substituído por um mod ativo. Considere desativá-lo.',
    'deps.dialog.conflict':    '"{mod}" é incompatível com os seguintes mods ativos:',
    'deps.dialog.missingInstalled': '"{mod}" requer os seguintes mods que não estão instalados:',
    'deps.dialog.missingActive': '"{mod}" requer os seguintes mods que estão instalados mas desativados:',
    'deps.dialog.deprecated':  '"{mod}" foi substituído pelos seguintes mods ativos:',
    'deps.dialog.enable':      'Ativar',
    'deps.dialog.disable':     'Desativar',
    'deps.dialog.disableThis': 'Desativar este mod',
    'deps.dialog.install':     'Instalar',
    'deps.dialog.installing':  'Instalando…',
    'deps.dialog.close':       'Fechar',
    'mods.versionMismatch':        'Instalado: v{lv} → Disponível: v{rv}\n\nHá uma incompatibilidade nos números de versão. Clique para atualizar o mod diretamente do mod.io.',
    'mods.versionMismatchInfo':    'Instalado: v{lv} · mod.io: v{rv}\n\nA versão local parece mais recente do que a publicada no mod.io.',
    'mods.versionMismatchSameFile': 'Instalado: v{lv} · mod.io: v{rv}\n\nOs rótulos de versão diferem mas o arquivo instalado está atualizado. Provavelmente uma inconsistência do autor (modinfo.json não atualizado).',
    'mods.link.cta':                   '🔗 Associar ao mod.io',
    'mods.link.title':                 'Associar « {name} » a um registro mod.io',
    'mods.link.searchPlaceholder':     'Pesquisar no mod.io…',
    'mods.link.confirm':               'Associar',
    'mods.link.empty':                 'Sem resultados — tente outro nome.',
    'mods.link.cancel':                'Cancelar',
    'tab.news':                'Notícias',
    'tab.activation':          'Ativação',
    'tab.browser':             'Catálogo de mods',
    'tab.collections':         'Coleções',
    'tab.install':             'Instalação manual',
    'tab.log':                 'Log do Modloader',
    'tab.tweak':               'Ajustes',
    'tab.settings':            'Configurações',
    'settings.section.paths':       'Caminhos',
    'settings.section.behaviour':   'Comportamento',
    'settings.section.advanced':    'Avançado',
    'settings.gamePath':            'Executável do Anno 117',
    'settings.gamePath.empty':      'Não configurado — defina o caminho de Anno117.exe',
    'settings.docsPath':            'Pasta Documentos personalizada',
    'settings.docsPath.empty':      'Detectada automaticamente (usa ~/Documents ou o prefixo Proton)',
    'settings.browseFile':          'Procurar arquivo…',
    'settings.browseFolder':        'Procurar pasta…',
    'settings.autoDetect':          'Detectar automaticamente',
    'settings.clear':               'Limpar',
    'settings.open':                'Abrir',
    'settings.modLocation':         'Local de armazenamento dos mods',
    'settings.modLocation.documents': 'Pasta Documentos (recomendado)',
    'settings.modLocation.game':      'Pasta de instalação do jogo',
    'settings.enableNewMods':       'Mods recém-instalados',
    'settings.enableNewMods.on':    'Sempre ativar',
    'settings.enableNewMods.off':   'Nunca ativar',
    'settings.enableNewMods.keep':  'Manter o estado anterior',
    'settings.textScale':              'Tamanho do texto (leitura)',
    'settings.textScale.small':        'Pequeno',
    'settings.textScale.medium':       'Médio',
    'settings.textScale.large':        'Grande',
    'settings.derived.docsMods':    'Pasta de mods (Documentos)',
    'settings.derived.gameMods':    'Pasta de mods (jogo)',
    'settings.derived.profile':     'active-profile.txt',
    'settings.derived.appdata':     'AppData',
    'settings.derived.presets':     'Presets',
    'settings.pathError':           'Não foi possível salvar o caminho: {err}',
    'settings.detectError':         'Falha na detecção automática: {err}',
    'settings.section.modio':       'Integração com mod.io',
    'settings.modio.hint':          'Insira sua chave API pessoal do mod.io para ativar as abas Catálogo e Coleções. Gere uma em',
    'settings.modio.apiKey':        'Chave API',
    'settings.modio.apiKeyPlaceholder': 'Cole aqui sua chave API mod.io',
    'settings.modio.save':          'Salvar',
    'settings.modio.disconnectConfirm': 'Remover a chave API mod.io salva?',
    'settings.modio.emptyKey':      'A chave API está vazia.',
    'log.refresh':                  '↻ Atualizar',
    'log.copy':                     '⧉ Copiar',
    'log.openFile':                 'Abrir arquivo',
    'log.loading':                  'Carregando…',
    'log.empty':                    'mod-loader.log está vazio.',
    'log.notFound':                 'mod-loader.log não encontrado em:\n{path}',
    'log.truncated':                'Log truncado nos últimos 2 MB',
    'install.title':                'Instalação manual',
    'install.hint':                 'Solte um ZIP de mod aqui ou clique para procurar. O arquivo deve conter um modinfo.json (ou .jsonc).',
    'install.drop':                 'Solte um mod .zip aqui',
    'install.or':                   '— ou —',
    'install.browse':               'Procurar um arquivo ZIP…',
    'install.targetLabel':          'Destino da instalação:',
    'install.installing':           'Instalando {name}…',
    'install.success':              '{name} instalado.',
    'install.cancelled':            'Cancelado.',
    'install.overwriteConfirm':     'Já existe uma pasta de mod chamada «{name}». Substituir?',
    'tweak.listHeader':             'Mods configuráveis',
    'tweak.optionWord':             'opções',
    'tweak.noTweakable':            'Nenhum dos seus mods instalados expõe opções.',
    'tweak.pickHint':                'Selecione um mod à esquerda para ajustar suas opções.',
    'tweak.noOptions':              'Este mod não tem opções configuráveis.',
    'tweak.resetMod':               'Redefinir este mod',
    'tweak.resetAll':               'Redefinir tudo',
    'tweak.resetModConfirm':        'Redefinir todas as opções deste mod aos valores padrão?',
    'tweak.resetAllConfirm':        'Redefinir as opções de todos os mods? O arquivo active-options.jsonc será excluído.',
    'tweak.defaultsSection':           '— Valores padrão —',
    'tweak.colorPicker.open':          'Abrir seletor de cor',
    'tweak.colorPicker.title':         'Seletor de cor',
    'tweak.colorPicker.before':        'Antes',
    'tweak.colorPicker.after':         'Depois',
    'tweak.colorPicker.cancel':        'Cancelar',
    'tweak.colorPicker.apply':         'Aplicar',
    'news.refresh':                 '↻ Atualizar',
    'news.loading':                 'Buscando últimas postagens…',
    'news.empty':                   'Nenhuma notícia para exibir.',
    'news.error':                   'Não foi possível buscar notícias: {err}',
    'news.cached':                  'em cache (10 min)',
    'news.includeReddit':           'Incluir postagens de r/anno',
    'news.visitUnion':              'Abrir Anno Union ↗',
    'news.back':                       'Voltar às notícias',
    'news.openOnUnion':                'Abrir no Anno Union ↗',
    'settings.modio.clearKey':      'Limpar chave',
    'modio.badge.connected':        '● Conectado',
    'modio.badge.keyOnly':          '◐ Apenas chave API',
    'modio.badge.notSet':           '○ Não definido',
    'modio.session':                'Sessão',
    'modio.expires':                'expira em {date}',
    'modio.disconnect':             'Desconectar',
    'modio.disconnectConfirm':      'Desconectar do mod.io? Sua chave API permanecerá salva; você pode reconectar mais tarde.',
    'modio.needKeyFirst':           'Salve primeiro sua chave API acima, depois você pode conectar.',
    'modio.startConnect':           'Conectar ao mod.io',
    'modio.email':                  'Endereço de e-mail',
    'modio.emailPlaceholder':       'voce@exemplo.com',
    'modio.emailRequired':          'Por favor, informe seu e-mail.',
    'modio.termsAgree':             'Aceito os',
    'modio.termsLink':              'Termos de Uso do mod.io',
    'modio.cancel':                 'Cancelar',
    'common.cancel':                   'Cancelar',
    'common.confirm':                  'Confirmar',
    'modio.sendCode':               'Enviar código',
    'modio.sending':                'Enviando…',
    'modio.code':                   'Código de segurança',
    'modio.codeRequired':           'Insira o código de 5 caracteres recebido por e-mail.',
    'modio.codeSent':               'Um código de 5 caracteres foi enviado para {email}. Verifique sua caixa (e o spam).',
    'modio.connect':                'Conectar',
    'modio.connecting':             'Conectando…',
    // Mod Browser
    'browser.title':                'Catálogo de mods',
    'browser.searchPlaceholder':    'Pesquisar mods…',
    'browser.search':               'Pesquisar',
    'browser.refresh':              'Atualizar',
    'browser.sortNewest':           'Mais recentes',
    'browser.sortPopular':          'Mais populares',
    'browser.sortDownloads':        'Mais baixados',
    'browser.sortRating':           'Mais bem avaliados',
    'browser.sortAlpha':            'A → Z',
    'browser.sortBy':               'Ordenar por:',
    'browser.mySubscriptions':         'Minhas inscrições',
    'browser.myFollows':               'Meus seguidos',
    'browser.follow':                  'Seguir esta coleção',
    'browser.unfollow':                'Deixar de seguir esta coleção',
    'browser.tag':                  'Tag:',
    'browser.tagAll':               'Todas as tags',
    'browser.clearSearch':          'Limpar pesquisa',
    'browser.byAuthor':             'por {name}',
    'browser.clearAuthor':          'Mostrar todos os autores',
    'browser.filterByAuthor':       'Mostrar apenas mods deste autor',
    'browser.bundledMods':          'Mods incluídos',
    'browser.bundledEmpty':         'Esta coleção não lista mods incluídos.',
    'browser.backToCollection':     'Voltar à coleção',
    'browser.installCollection':    'Instalar coleção',
    'browser.updateCollection':     'Atualizar coleção',
    'browser.uninstallCollection':  '🗑 Desinstalar coleção',
    'browser.uninstallConfirm':     'Excluir o perfil «{profile}» criado a partir de «{name}»?',
    'browser.uninstallAlsoMods':    'Também apagar do disco os {count} mod(s) incluídos nesta coleção?',
    'browser.uninstallOk':          'Perfil «{profile}» removido.',
    'browser.uninstallOkWithMods':  'Perfil «{profile}» removido; {count} mod(s) incluídos apagados do disco.',
    'browser.uninstallFail':        'Falha na desinstalação: {error}',
    'browser.collectionInstallOk':  '«{name}»: {count}/{total} mods instalados. O perfil «{profile}» agora está ativo.',
    'browser.collectionInstallFailures': '({count} com falha — veja o log)',
    'browser.back':                 'Voltar',
    'browser.empty':                'Nenhum mod corresponde à sua pesquisa.',
    'browser.loading':              'Carregando mods…',
    'browser.error':                'Não foi possível carregar os mods: {error}',
    'browser.notAuth':              'Não conectado ao mod.io. Conecte-se na aba Configurações.',
    'browser.openSettings':         'Abrir configurações',
    'browser.prev':                 '‹ Anterior',
    'browser.next':                 'Próximo ›',
    'browser.pageOf':               'Página {page} / {total}',
    'browser.resultsCount':         '{shown} de {total} mods',
    'browser.detailPick':           'Selecione um mod da lista para ver seus detalhes.',
    'browser.install':              'Instalar',
    'browser.installing':           'Instalando…',
    'browser.installed':            '✓ Instalado',
    'browser.update':               'Atualizar',
    'browser.installOk':            '«{name}» instalado.',
    'browser.installFail':          'Falha na instalação: {error}',
    'browser.subscribe':            '+ Inscrever-se',
    'browser.subscribed':           '✓ Inscrito',
    'browser.unsubscribe':          'Cancelar inscrição',
    'browser.uninstallMod':            '🗑 Desinstalar',
    'browser.uninstallModConfirm':     'Remover « {name} » do disco?',
    'browser.uninstallModOk':          '« {name} » desinstalado.',
    'browser.endorse':              '♥ Recomendar',
    'browser.endorsed':             '♥ Recomendado',
    'browser.endorseFail':          'Não foi possível recomendar: {error}',
    'browser.subFail':              'Não foi possível inscrever: {error}',
    'browser.openOnModio':          'Abrir no mod.io ↗',
    'browser.author':               'por {name}',
    'browser.downloads':            '{n} downloads',
    'browser.subscribers':          '{n} inscritos',
    'browser.modsTotal':            '{n} mods',
    'browser.updated':              'Atualizado em {date}',
    'browser.size':                 'Tamanho: {size}',
    'browser.version':              'Versão: {v}',
    'browser.changelog':            'Notas de versão',
    'browser.description':          'Descrição',
  },
  japanese: {
    'hud.settings':                 '設定',
    'hud.refreshMods':              'MOD一覧を更新',
    'hud.searchMod':                'MODを検索…',
    'hud.language':                 '言語',
    'alert.loadPresetFail':         'プリセットの読み込みに失敗しました: {error}',
    'alert.savePresetFail':         'プリセットの保存に失敗しました: {error}',
    'alert.deletePresetFail':       'プリセットの削除に失敗しました: {error}',
    'alert.uninstallFail':          'アンインストールに失敗しました: {error}',
    'profile.label':           'プロファイル',
    'profile.new':             '＋ 新規',
    'profile.delete':          '🗑 削除',
    'profile.deleteConfirm':   'プリセット「{name}」を削除しますか？',
    'profile.cantDeleteReserved': '「Default」および「Vanilla」プロファイルは削除できません。',
    'profile.promptName':      '新しいプリセットの名前:',
    'mode.manage':             '管理',
    'mode.order':              '読み込み順',
    'mode.manage.title':       'MODの並び替えと有効/無効の切り替え',
    'mode.order.title':        'ドラッグ＆ドロップで読み込み順を変更',
    'list.head.toggleAll':     'すべて有効/無効',
    'list.head.category':      'カテゴリ',
    'list.head.name':          'MOD名',
    'list.head.size':          'サイズ',
    'list.head.status':        'ステータス',
    'list.empty':              '設定されたフォルダにMODが見つかりません。',
    'count.active':            '{n} / {total} 有効',
    'pill.active':             'ON',
    'pill.off':                'OFF',
    'detail.empty':            'リストからMODを選択して詳細を表示します。',
    'detail.banner.empty':     'このMODにはバナーがありません。',
    'detail.description':      '説明',
    'detail.details':          '詳細',
    'detail.meta.category':    'カテゴリ',
    'detail.meta.difficulty':  '難易度',
    'detail.meta.size':        'サイズ',
    'detail.meta.folder':      'フォルダ',
    'detail.creator':          '作者: {name} · v{version}',
    'detail.openFolder':       'フォルダを開く',
    'detail.uninstall':        'アンインストール',
    'detail.uninstallConfirm': 'MOD「{name}」をアンインストールしますか？\n\nフォルダがディスクから削除されます。',
    'tab.placeholder':         'このタブは移行のフェーズ2で対応されます。',
    'tab.placeholderHint':     'pywebview POC作業中 — 現時点では{tab}タブのみ動作します。',
    'launch.title':            'Anno 117を起動',
    'launch.error':            'ゲームを起動できませんでした: {err}',
    'mods.openFolder.title':   'MODフォルダを開く',
    'mods.notFromManager':             'マネージャー経由でインストールされていません',
    'deps.conflict':           '競合: {names}\n\nこのModは1つ以上の有効なModと非互換です。',
    'deps.missingInstalled':   '依存関係なし（未インストール）: {names}\n\n必要なModがModsフォルダに存在しません。',
    'deps.missingActive':      '依存関係なし（無効化）: {names}\n\n必要なModはインストール済みですが有効化されていません。',
    'deps.deprecated':         '廃止（置き換え）: {names}\n\nこのModは有効なModに置き換えられました。無効化を検討してください。',
    'deps.dialog.conflict':    '「{mod}」は以下の有効なModと競合しています:',
    'deps.dialog.missingInstalled': '「{mod}」は以下の未インストールのModを必要とします:',
    'deps.dialog.missingActive': '「{mod}」は以下のModを必要としますが、インストール済みで無効化されています:',
    'deps.dialog.deprecated':  '「{mod}」は以下の有効なModによって置き換えられています:',
    'deps.dialog.enable':      '有効化',
    'deps.dialog.disable':     '無効化',
    'deps.dialog.disableThis': 'このModを無効化',
    'deps.dialog.install':     'インストール',
    'deps.dialog.installing':  'インストール中…',
    'deps.dialog.close':       '閉じる',
    'mods.versionMismatch':        'インストール済み: v{lv} → 利用可能: v{rv}\n\nバージョン番号が一致しません。クリックしてmod.ioから最新バージョンに更新してください。',
    'mods.versionMismatchInfo':    'インストール済み: v{lv} · mod.io: v{rv}\n\nローカルバージョンはmod.ioで公開されているものより新しいようです。',
    'mods.versionMismatchSameFile': 'インストール済み: v{lv} · mod.io: v{rv}\n\nバージョンラベルは異なりますが、インストール済みファイルは最新です。作者の不整合（modinfo.jsonが未更新）の可能性があります。',
    'mods.link.cta':                   '🔗 mod.ioに関連付け',
    'mods.link.title':                 '« {name} » を mod.io のレコードに関連付け',
    'mods.link.searchPlaceholder':     'mod.io で検索…',
    'mods.link.confirm':               '関連付け',
    'mods.link.empty':                 '一致なし — 別の名前で試してください。',
    'mods.link.cancel':                'キャンセル',
    'tab.news':                'ニュース',
    'tab.activation':          '有効化',
    'tab.browser':             'MODブラウザ',
    'tab.collections':         'コレクション',
    'tab.install':             '手動インストール',
    'tab.log':                 'Modloaderログ',
    'tab.tweak':               '調整',
    'tab.settings':            '設定',
    'settings.section.paths':       'パス',
    'settings.section.behaviour':   '動作',
    'settings.section.advanced':    '詳細',
    'settings.gamePath':            'Anno 117 実行ファイル',
    'settings.gamePath.empty':      '未設定 — Anno117.exe のパスを指定してください',
    'settings.docsPath':            'Documentsフォルダの上書き',
    'settings.docsPath.empty':      '自動検出（~/Documents または Proton プレフィックスを使用）',
    'settings.browseFile':          'ファイルを参照…',
    'settings.browseFolder':        'フォルダを参照…',
    'settings.autoDetect':          '自動検出',
    'settings.clear':               'クリア',
    'settings.open':                '開く',
    'settings.modLocation':         'MODの保存場所',
    'settings.modLocation.documents': 'Documentsフォルダ（推奨）',
    'settings.modLocation.game':      'ゲームインストールフォルダ',
    'settings.enableNewMods':       '新しくインストールされたMOD',
    'settings.enableNewMods.on':    '常に有効化',
    'settings.enableNewMods.off':   '有効化しない',
    'settings.enableNewMods.keep':  '以前の状態を維持',
    'settings.textScale':              'テキストサイズ（本文）',
    'settings.textScale.small':        '小',
    'settings.textScale.medium':       '中',
    'settings.textScale.large':        '大',
    'settings.derived.docsMods':    'MODフォルダ（Documents）',
    'settings.derived.gameMods':    'MODフォルダ（ゲーム）',
    'settings.derived.profile':     'active-profile.txt',
    'settings.derived.appdata':     'AppData',
    'settings.derived.presets':     'プリセット',
    'settings.pathError':           'パスを保存できませんでした: {err}',
    'settings.detectError':         '自動検出に失敗しました: {err}',
    'settings.section.modio':       'mod.io 連携',
    'settings.modio.hint':          'MODブラウザとコレクションタブを有効にするには、個人のmod.io APIキーを入力してください。次の場所で生成できます:',
    'settings.modio.apiKey':        'APIキー',
    'settings.modio.apiKeyPlaceholder': 'mod.io APIキーをここに貼り付けてください',
    'settings.modio.save':          '保存',
    'settings.modio.disconnectConfirm': '保存されたmod.io APIキーを削除しますか？',
    'settings.modio.emptyKey':      'APIキーが空です。',
    'log.refresh':                  '↻ 更新',
    'log.copy':                     '⧉ コピー',
    'log.openFile':                 'ファイルを開く',
    'log.loading':                  '読み込み中…',
    'log.empty':                    'mod-loader.log は空です。',
    'log.notFound':                 'mod-loader.log が見つかりません:\n{path}',
    'log.truncated':                'ログを最後の2 MBに切り詰めました',
    'install.title':                '手動インストール',
    'install.hint':                 'MODのZIPをここにドロップするか、クリックして参照してください。アーカイブには modinfo.json（または .jsonc）が必要です。',
    'install.drop':                 'MODの.zipをここにドロップ',
    'install.or':                   '— または —',
    'install.browse':               'ZIPファイルを参照…',
    'install.targetLabel':          'インストール先:',
    'install.installing':           '{name} をインストール中…',
    'install.success':              '{name} をインストールしました。',
    'install.cancelled':            'キャンセルされました。',
    'install.overwriteConfirm':     '「{name}」という名前のMODフォルダが既に存在します。置き換えますか？',
    'tweak.listHeader':             '調整可能なMOD',
    'tweak.optionWord':             'オプション',
    'tweak.noTweakable':            'インストール済みのMODにはオプションを公開しているものがありません。',
    'tweak.pickHint':                '左側でMODを選択してオプションを調整してください。',
    'tweak.noOptions':              'このMODには設定可能なオプションがありません。',
    'tweak.resetMod':               'このMODをリセット',
    'tweak.resetAll':               'すべてリセット',
    'tweak.resetModConfirm':        'このMODのすべてのオプションをデフォルトに戻しますか？',
    'tweak.resetAllConfirm':        'すべてのMODのオプションをリセットしますか？ active-options.jsonc ファイルが削除されます。',
    'tweak.defaultsSection':           '— デフォルト値 —',
    'tweak.colorPicker.open':          'カラーピッカーを開く',
    'tweak.colorPicker.title':         'カラーピッカー',
    'tweak.colorPicker.before':        '変更前',
    'tweak.colorPicker.after':         '変更後',
    'tweak.colorPicker.cancel':        'キャンセル',
    'tweak.colorPicker.apply':         '適用',
    'news.refresh':                 '↻ 更新',
    'news.loading':                 '最新の投稿を取得中…',
    'news.empty':                   '表示するニュースはありません。',
    'news.error':                   'ニュースを取得できませんでした: {err}',
    'news.cached':                  'キャッシュ済み（10分）',
    'news.includeReddit':           'r/anno の投稿を含める',
    'news.visitUnion':              'Anno Union を開く ↗',
    'news.back':                       'ニュースに戻る',
    'news.openOnUnion':                'Anno Union で開く ↗',
    'settings.modio.clearKey':      'キーをクリア',
    'modio.badge.connected':        '● 接続済み',
    'modio.badge.keyOnly':          '◐ APIキーのみ',
    'modio.badge.notSet':           '○ 未設定',
    'modio.session':                'セッション',
    'modio.expires':                '{date} に期限切れ',
    'modio.disconnect':             '切断',
    'modio.disconnectConfirm':      'mod.io から切断しますか？ APIキーは保存されたままなので、後で再接続できます。',
    'modio.needKeyFirst':           '先に上のAPIキーを保存してから接続してください。',
    'modio.startConnect':           'mod.io に接続',
    'modio.email':                  'メールアドレス',
    'modio.emailPlaceholder':       'you@example.com',
    'modio.emailRequired':          'メールアドレスを入力してください。',
    'modio.termsAgree':             '次に同意します:',
    'modio.termsLink':              'mod.io 利用規約',
    'modio.cancel':                 'キャンセル',
    'common.cancel':                   'キャンセル',
    'common.confirm':                  '確認',
    'modio.sendCode':               'コードを送信',
    'modio.sending':                '送信中…',
    'modio.code':                   'セキュリティコード',
    'modio.codeRequired':           'メールで届いた5文字のコードを入力してください。',
    'modio.codeSent':               '5文字のコードを {email} に送信しました。受信トレイ（および迷惑メール）を確認してください。',
    'modio.connect':                '接続',
    'modio.connecting':             '接続中…',
    // Mod Browser
    'browser.title':                'MODブラウザ',
    'browser.searchPlaceholder':    'MODを検索…',
    'browser.search':               '検索',
    'browser.refresh':              '更新',
    'browser.sortNewest':           '新着順',
    'browser.sortPopular':          '人気順',
    'browser.sortDownloads':        'ダウンロード数順',
    'browser.sortRating':           '評価順',
    'browser.sortAlpha':            'A → Z',
    'browser.sortBy':               '並び替え:',
    'browser.mySubscriptions':         'マイサブスクリプション',
    'browser.myFollows':               'マイフォロー',
    'browser.follow':                  'このコレクションをフォロー',
    'browser.unfollow':                'このコレクションのフォローを解除',
    'browser.tag':                  'タグ:',
    'browser.tagAll':               'すべてのタグ',
    'browser.clearSearch':          '検索をクリア',
    'browser.byAuthor':             '作者: {name}',
    'browser.clearAuthor':          'すべての作者を表示',
    'browser.filterByAuthor':       'この作者のMODのみ表示',
    'browser.bundledMods':          '同梱MOD',
    'browser.bundledEmpty':         'このコレクションには同梱MODがありません。',
    'browser.backToCollection':     'コレクションに戻る',
    'browser.installCollection':    'コレクションをインストール',
    'browser.updateCollection':     'コレクションを更新',
    'browser.uninstallCollection':  '🗑 コレクションをアンインストール',
    'browser.uninstallConfirm':     '「{name}」から作成されたプロファイル「{profile}」を削除しますか？',
    'browser.uninstallAlsoMods':    'このコレクションに含まれる {count} 個のMODもディスクから削除しますか？',
    'browser.uninstallOk':          'プロファイル「{profile}」を削除しました。',
    'browser.uninstallOkWithMods':  'プロファイル「{profile}」を削除しました。同梱の {count} 個のMODをディスクから削除しました。',
    'browser.uninstallFail':        'アンインストールに失敗しました: {error}',
    'browser.collectionInstallOk':  '「{name}」: {count}/{total} のMODをインストールしました。プロファイル「{profile}」が有効になりました。',
    'browser.collectionInstallFailures': '({count} 件失敗 — ログを参照)',
    'browser.back':                 '戻る',
    'browser.empty':                '検索条件に一致するMODがありません。',
    'browser.loading':              'MODを読み込み中…',
    'browser.error':                'MODを読み込めませんでした: {error}',
    'browser.notAuth':              'mod.io に接続されていません。設定タブで接続してください。',
    'browser.openSettings':         '設定を開く',
    'browser.prev':                 '‹ 前へ',
    'browser.next':                 '次へ ›',
    'browser.pageOf':               'ページ {page} / {total}',
    'browser.resultsCount':         '{total} 中 {shown} のMOD',
    'browser.detailPick':           'リストからMODを選択して詳細を表示します。',
    'browser.install':              'インストール',
    'browser.installing':           'インストール中…',
    'browser.installed':            '✓ インストール済み',
    'browser.update':               '更新',
    'browser.installOk':            '「{name}」をインストールしました。',
    'browser.installFail':          'インストールに失敗しました: {error}',
    'browser.subscribe':            '+ 購読',
    'browser.subscribed':           '✓ 購読中',
    'browser.unsubscribe':          '購読解除',
    'browser.uninstallMod':            '🗑 アンインストール',
    'browser.uninstallModConfirm':     '« {name} » をディスクから削除しますか？',
    'browser.uninstallModOk':          '« {name} » をアンインストールしました。',
    'browser.endorse':              '♥ 推薦',
    'browser.endorsed':             '♥ 推薦済み',
    'browser.endorseFail':          '推薦できませんでした: {error}',
    'browser.subFail':              '購読できませんでした: {error}',
    'browser.openOnModio':          'mod.io で開く ↗',
    'browser.author':               '作者: {name}',
    'browser.downloads':            '{n} ダウンロード',
    'browser.subscribers':          '{n} 購読者',
    'browser.modsTotal':            '{n} 個のMOD',
    'browser.updated':              '更新日: {date}',
    'browser.size':                 'サイズ: {size}',
    'browser.version':              'バージョン: {v}',
    'browser.changelog':            '変更履歴',
    'browser.description':          '説明',
  },
  korean: {
    'hud.settings':                 '설정',
    'hud.refreshMods':              '모드 목록 새로고침',
    'hud.searchMod':                '모드 검색…',
    'hud.language':                 '언어',
    'alert.loadPresetFail':         '프리셋을 불러오지 못했습니다: {error}',
    'alert.savePresetFail':         '프리셋을 저장하지 못했습니다: {error}',
    'alert.deletePresetFail':       '프리셋을 삭제하지 못했습니다: {error}',
    'alert.uninstallFail':          '제거에 실패했습니다: {error}',
    'profile.label':           '프로필',
    'profile.new':             '＋ 새로 만들기',
    'profile.delete':          '🗑 삭제',
    'profile.deleteConfirm':   '프리셋 「{name}」을(를) 삭제하시겠습니까?',
    'profile.cantDeleteReserved': '「Default」 및 「Vanilla」 프로필은 삭제할 수 없습니다.',
    'profile.promptName':      '새 프리셋 이름:',
    'mode.manage':             '관리',
    'mode.order':              '로딩 순서',
    'mode.manage.title':       '모드 정렬 및 활성화/비활성화',
    'mode.order.title':        '드래그 앤 드롭으로 로딩 순서 재정렬',
    'list.head.toggleAll':     '전체 활성화 / 비활성화',
    'list.head.category':      '카테고리',
    'list.head.name':          '모드 이름',
    'list.head.size':          '크기',
    'list.head.status':        '상태',
    'list.empty':              '설정된 폴더에서 모드를 찾을 수 없습니다.',
    'count.active':            '{n} / {total} 활성화됨',
    'pill.active':             'ON',
    'pill.off':                'OFF',
    'detail.empty':            '목록에서 모드를 선택하여 상세 정보를 확인하세요.',
    'detail.banner.empty':     '이 모드에는 배너가 없습니다.',
    'detail.description':      '설명',
    'detail.details':          '세부 정보',
    'detail.meta.category':    '카테고리',
    'detail.meta.difficulty':  '난이도',
    'detail.meta.size':        '크기',
    'detail.meta.folder':      '폴더',
    'detail.creator':          '제작: {name} · v{version}',
    'detail.openFolder':       '폴더 열기',
    'detail.uninstall':        '제거',
    'detail.uninstallConfirm': '모드 「{name}」을(를) 제거하시겠습니까?\n\n폴더가 디스크에서 삭제됩니다.',
    'tab.placeholder':         '이 탭은 마이그레이션 2단계에서 이전됩니다.',
    'tab.placeholderHint':     'pywebview POC 진행 중 — 현재 {tab} 탭만 작동합니다.',
    'launch.title':            'Anno 117 실행',
    'launch.error':            '게임을 실행할 수 없습니다: {err}',
    'mods.openFolder.title':   '모드 폴더 열기',
    'mods.notFromManager':             '관리자를 통해 설치되지 않음',
    'deps.conflict':           '충돌: {names}\n\n이 모드는 하나 이상의 활성 모드와 호환되지 않습니다.',
    'deps.missingInstalled':   '누락된 종속성 (미설치): {names}\n\n필요한 모드가 모드 폴더에 없습니다.',
    'deps.missingActive':      '누락된 종속성 (비활성): {names}\n\n필요한 모드가 설치되어 있지만 활성화되지 않았습니다.',
    'deps.deprecated':         '대체됨: {names}\n\n이 모드는 활성 모드로 대체되었습니다. 비활성화를 고려하세요.',
    'deps.dialog.conflict':    '"{mod}"이(가) 다음 활성 모드와 충돌합니다:',
    'deps.dialog.missingInstalled': '"{mod}"은(는) 다음 미설치 모드를 필요로 합니다:',
    'deps.dialog.missingActive': '"{mod}"은(는) 다음 모드를 필요로 하지만 설치되어 있으나 비활성 상태입니다:',
    'deps.dialog.deprecated':  '"{mod}"은(는) 다음 활성 모드로 대체되었습니다:',
    'deps.dialog.enable':      '활성화',
    'deps.dialog.disable':     '비활성화',
    'deps.dialog.disableThis': '이 모드 비활성화',
    'deps.dialog.install':     '설치',
    'deps.dialog.installing':  '설치 중…',
    'deps.dialog.close':       '닫기',
    'mods.versionMismatch':        '설치됨: v{lv} → 사용 가능: v{rv}\n\n버전 번호가 일치하지 않습니다. 클릭하여 mod.io에서 최신 버전으로 업데이트하세요.',
    'mods.versionMismatchInfo':    '설치됨: v{lv} · mod.io: v{rv}\n\n로컬 버전이 mod.io에 게시된 것보다 최신인 것 같습니다.',
    'mods.versionMismatchSameFile': '설치됨: v{lv} · mod.io: v{rv}\n\n버전 레이블이 다르지만 설치된 파일은 최신입니다. 작성자의 불일치(modinfo.json 미업데이트)일 가능성이 있습니다.',
    'mods.link.cta':                   '🔗 mod.io에 연결',
    'mods.link.title':                 '« {name} »을(를) mod.io 기록에 연결',
    'mods.link.searchPlaceholder':     'mod.io 검색…',
    'mods.link.confirm':               '연결',
    'mods.link.empty':                 '일치 항목 없음 — 다른 이름으로 시도해 보세요.',
    'mods.link.cancel':                '취소',
    'tab.news':                '뉴스',
    'tab.activation':          '활성화',
    'tab.browser':             '모드 브라우저',
    'tab.collections':         '컬렉션',
    'tab.install':             '수동 설치',
    'tab.log':                 'Modloader 로그',
    'tab.tweak':               '조정',
    'tab.settings':            '설정',
    'settings.section.paths':       '경로',
    'settings.section.behaviour':   '동작',
    'settings.section.advanced':    '고급',
    'settings.gamePath':            'Anno 117 실행 파일',
    'settings.gamePath.empty':      '미설정 — Anno117.exe 경로를 지정하세요',
    'settings.docsPath':            '문서 폴더 재정의',
    'settings.docsPath.empty':      '자동 감지됨 (~/Documents 또는 Proton 프리픽스 사용)',
    'settings.browseFile':          '파일 찾기…',
    'settings.browseFolder':        '폴더 찾기…',
    'settings.autoDetect':          '자동 감지',
    'settings.clear':               '지우기',
    'settings.open':                '열기',
    'settings.modLocation':         '모드 저장 위치',
    'settings.modLocation.documents': '문서 폴더 (권장)',
    'settings.modLocation.game':      '게임 설치 폴더',
    'settings.enableNewMods':       '새로 설치된 모드',
    'settings.enableNewMods.on':    '항상 활성화',
    'settings.enableNewMods.off':   '항상 비활성화',
    'settings.enableNewMods.keep':  '이전 상태 유지',
    'settings.textScale':              '글자 크기 (본문)',
    'settings.textScale.small':        '작게',
    'settings.textScale.medium':       '중간',
    'settings.textScale.large':        '크게',
    'settings.derived.docsMods':    '모드 폴더 (문서)',
    'settings.derived.gameMods':    '모드 폴더 (게임)',
    'settings.derived.profile':     'active-profile.txt',
    'settings.derived.appdata':     'AppData',
    'settings.derived.presets':     '프리셋',
    'settings.pathError':           '경로를 저장할 수 없습니다: {err}',
    'settings.detectError':         '자동 감지 실패: {err}',
    'settings.section.modio':       'mod.io 연동',
    'settings.modio.hint':          '모드 브라우저와 컬렉션 탭을 활성화하려면 개인 mod.io API 키를 입력하세요. 다음에서 생성하세요:',
    'settings.modio.apiKey':        'API 키',
    'settings.modio.apiKeyPlaceholder': 'mod.io API 키를 여기에 붙여넣기',
    'settings.modio.save':          '저장',
    'settings.modio.disconnectConfirm': '저장된 mod.io API 키를 제거하시겠습니까?',
    'settings.modio.emptyKey':      'API 키가 비어 있습니다.',
    'log.refresh':                  '↻ 새로고침',
    'log.copy':                     '⧉ 복사',
    'log.openFile':                 '파일 열기',
    'log.loading':                  '로딩 중…',
    'log.empty':                    'mod-loader.log이 비어 있습니다.',
    'log.notFound':                 '다음 위치에서 mod-loader.log를 찾을 수 없습니다:\n{path}',
    'log.truncated':                '로그가 마지막 2 MB로 잘렸습니다',
    'install.title':                '수동 설치',
    'install.hint':                 '모드 ZIP을 여기에 놓거나 클릭하여 찾아보세요. 아카이브에는 modinfo.json (또는 .jsonc) 파일이 포함되어 있어야 합니다.',
    'install.drop':                 '모드 .zip을 여기에 놓으세요',
    'install.or':                   '— 또는 —',
    'install.browse':               'ZIP 파일 찾기…',
    'install.targetLabel':          '설치 위치:',
    'install.installing':           '{name} 설치 중…',
    'install.success':              '{name} 설치됨.',
    'install.cancelled':            '취소됨.',
    'install.overwriteConfirm':     '「{name}」이라는 모드 폴더가 이미 있습니다. 교체하시겠습니까?',
    'tweak.listHeader':             '조정 가능한 모드',
    'tweak.optionWord':             '옵션',
    'tweak.noTweakable':            '설치된 모드 중 옵션을 제공하는 것이 없습니다.',
    'tweak.pickHint':                '왼쪽에서 모드를 선택하여 옵션을 조정하세요.',
    'tweak.noOptions':              '이 모드에는 설정 가능한 옵션이 없습니다.',
    'tweak.resetMod':               '이 모드 재설정',
    'tweak.resetAll':               '모두 재설정',
    'tweak.resetModConfirm':        '이 모드의 모든 옵션을 기본값으로 재설정하시겠습니까?',
    'tweak.resetAllConfirm':        '모든 모드의 옵션을 재설정하시겠습니까? active-options.jsonc 파일이 삭제됩니다.',
    'tweak.defaultsSection':           '— 기본값 —',
    'tweak.colorPicker.open':          '색상 선택기 열기',
    'tweak.colorPicker.title':         '색상 선택기',
    'tweak.colorPicker.before':        '이전',
    'tweak.colorPicker.after':         '이후',
    'tweak.colorPicker.cancel':        '취소',
    'tweak.colorPicker.apply':         '적용',
    'news.refresh':                 '↻ 새로고침',
    'news.loading':                 '최신 게시물 가져오는 중…',
    'news.empty':                   '표시할 뉴스가 없습니다.',
    'news.error':                   '뉴스를 가져올 수 없습니다: {err}',
    'news.cached':                  '캐시됨 (10분)',
    'news.includeReddit':           'r/anno 게시물 포함',
    'news.visitUnion':              'Anno Union 열기 ↗',
    'news.back':                       '뉴스로 돌아가기',
    'news.openOnUnion':                'Anno Union에서 열기 ↗',
    'settings.modio.clearKey':      '키 지우기',
    'modio.badge.connected':        '● 연결됨',
    'modio.badge.keyOnly':          '◐ API 키만',
    'modio.badge.notSet':           '○ 설정되지 않음',
    'modio.session':                '세션',
    'modio.expires':                '{date}에 만료',
    'modio.disconnect':             '연결 해제',
    'modio.disconnectConfirm':      'mod.io 연결을 해제하시겠습니까? API 키는 저장된 상태로 유지되며 나중에 다시 연결할 수 있습니다.',
    'modio.needKeyFirst':           '먼저 위에 API 키를 저장한 다음 연결할 수 있습니다.',
    'modio.startConnect':           'mod.io에 연결',
    'modio.email':                  '이메일 주소',
    'modio.emailPlaceholder':       'you@example.com',
    'modio.emailRequired':          '이메일을 입력하세요.',
    'modio.termsAgree':             '동의합니다:',
    'modio.termsLink':              'mod.io 이용 약관',
    'modio.cancel':                 '취소',
    'common.cancel':                   '취소',
    'common.confirm':                  '확인',
    'modio.sendCode':               '코드 전송',
    'modio.sending':                '전송 중…',
    'modio.code':                   '보안 코드',
    'modio.codeRequired':           '이메일로 받은 5자리 코드를 입력하세요.',
    'modio.codeSent':               '5자리 코드가 {email}로 전송되었습니다. 받은편지함 (및 스팸)을 확인하세요.',
    'modio.connect':                '연결',
    'modio.connecting':             '연결 중…',
    // Mod Browser
    'browser.title':                '모드 브라우저',
    'browser.searchPlaceholder':    '모드 검색…',
    'browser.search':               '검색',
    'browser.refresh':              '새로고침',
    'browser.sortNewest':           '최신순',
    'browser.sortPopular':          '인기순',
    'browser.sortDownloads':        '다운로드순',
    'browser.sortRating':           '평점순',
    'browser.sortAlpha':            'A → Z',
    'browser.sortBy':               '정렬 기준:',
    'browser.mySubscriptions':         '내 구독',
    'browser.myFollows':               '내 팔로우',
    'browser.follow':                  '이 컬렉션 팔로우',
    'browser.unfollow':                '이 컬렉션 팔로우 취소',
    'browser.tag':                  '태그:',
    'browser.tagAll':               '모든 태그',
    'browser.clearSearch':          '검색 지우기',
    'browser.byAuthor':             '제작: {name}',
    'browser.clearAuthor':          '모든 작성자 표시',
    'browser.filterByAuthor':       '이 작성자의 모드만 표시',
    'browser.bundledMods':          '포함된 모드',
    'browser.bundledEmpty':         '이 컬렉션에는 포함된 모드가 없습니다.',
    'browser.backToCollection':     '컬렉션으로 돌아가기',
    'browser.installCollection':    '컬렉션 설치',
    'browser.updateCollection':     '컬렉션 업데이트',
    'browser.uninstallCollection':  '🗑 컬렉션 제거',
    'browser.uninstallConfirm':     '「{name}」에서 생성된 프로필 「{profile}」을(를) 삭제하시겠습니까?',
    'browser.uninstallAlsoMods':    '이 컬렉션에 포함된 {count}개의 모드도 디스크에서 제거하시겠습니까?',
    'browser.uninstallOk':          '프로필 「{profile}」을(를) 제거했습니다.',
    'browser.uninstallOkWithMods':  '프로필 「{profile}」을(를) 제거했습니다. 포함된 {count}개의 모드를 디스크에서 삭제했습니다.',
    'browser.uninstallFail':        '제거에 실패했습니다: {error}',
    'browser.collectionInstallOk':  '「{name}」: {count}/{total} 모드 설치됨. 프로필 「{profile}」이(가) 이제 활성화되었습니다.',
    'browser.collectionInstallFailures': '({count}개 실패 — 로그 참조)',
    'browser.back':                 '뒤로',
    'browser.empty':                '검색과 일치하는 모드가 없습니다.',
    'browser.loading':              '모드 로드 중…',
    'browser.error':                '모드를 로드할 수 없습니다: {error}',
    'browser.notAuth':              'mod.io에 연결되지 않았습니다. 설정 탭에서 연결하세요.',
    'browser.openSettings':         '설정 열기',
    'browser.prev':                 '‹ 이전',
    'browser.next':                 '다음 ›',
    'browser.pageOf':               '{page} / {total} 페이지',
    'browser.resultsCount':         '{total}개 중 {shown}개 모드',
    'browser.detailPick':           '목록에서 모드를 선택하여 세부 정보를 확인하세요.',
    'browser.install':              '설치',
    'browser.installing':           '설치 중…',
    'browser.installed':            '✓ 설치됨',
    'browser.update':               '업데이트',
    'browser.installOk':            '「{name}」 설치됨.',
    'browser.installFail':          '설치에 실패했습니다: {error}',
    'browser.subscribe':            '+ 구독',
    'browser.subscribed':           '✓ 구독 중',
    'browser.unsubscribe':          '구독 취소',
    'browser.uninstallMod':            '🗑 제거',
    'browser.uninstallModConfirm':     '« {name} »을(를) 디스크에서 제거하시겠습니까?',
    'browser.uninstallModOk':          '« {name} » 제거됨.',
    'browser.endorse':              '♥ 추천',
    'browser.endorsed':             '♥ 추천됨',
    'browser.endorseFail':          '추천할 수 없습니다: {error}',
    'browser.subFail':              '구독할 수 없습니다: {error}',
    'browser.openOnModio':          'mod.io에서 열기 ↗',
    'browser.author':               '제작: {name}',
    'browser.downloads':            '{n}회 다운로드',
    'browser.subscribers':          '{n}명 구독',
    'browser.modsTotal':            '{n}개 모드',
    'browser.updated':              '업데이트: {date}',
    'browser.size':                 '크기: {size}',
    'browser.version':              '버전: {v}',
    'browser.changelog':            '변경 로그',
    'browser.description':          '설명',
  },
  simplified_chinese: {
    'hud.settings':                 '设置',
    'hud.refreshMods':              '刷新模组列表',
    'hud.searchMod':                '搜索模组…',
    'hud.language':                 '语言',
    'alert.loadPresetFail':         '加载预设失败：{error}',
    'alert.savePresetFail':         '保存预设失败：{error}',
    'alert.deletePresetFail':       '删除预设失败：{error}',
    'alert.uninstallFail':          '卸载失败：{error}',
    'profile.label':           '配置文件',
    'profile.new':             '＋ 新建',
    'profile.delete':          '🗑 删除',
    'profile.deleteConfirm':   '删除预设「{name}」？',
    'profile.cantDeleteReserved': '「Default」和「Vanilla」配置文件无法删除。',
    'profile.promptName':      '新预设名称：',
    'mode.manage':             '管理',
    'mode.order':              '加载顺序',
    'mode.manage.title':       '排序并启用/禁用模组',
    'mode.order.title':        '通过拖放重新排序加载顺序',
    'list.head.toggleAll':     '全部启用/禁用',
    'list.head.category':      '类别',
    'list.head.name':          '模组名称',
    'list.head.size':          '大小',
    'list.head.status':        '状态',
    'list.empty':              '在已配置的文件夹中未检测到模组。',
    'count.active':            '{n} / {total} 已启用',
    'pill.active':             'ON',
    'pill.off':                'OFF',
    'detail.empty':            '从列表中选择一个模组以查看其详情。',
    'detail.banner.empty':     '此模组未提供横幅。',
    'detail.description':      '描述',
    'detail.details':          '详情',
    'detail.meta.category':    '类别',
    'detail.meta.difficulty':  '难度',
    'detail.meta.size':        '大小',
    'detail.meta.folder':      '文件夹',
    'detail.creator':          '作者：{name} · v{version}',
    'detail.openFolder':       '打开文件夹',
    'detail.uninstall':        '卸载',
    'detail.uninstallConfirm': '卸载模组「{name}」？\n\n该文件夹将从磁盘中删除。',
    'tab.placeholder':         '此选项卡将在迁移第二阶段移植。',
    'tab.placeholderHint':     'pywebview POC 进行中 — 目前仅 {tab} 选项卡可用。',
    'launch.title':            '启动 Anno 117',
    'launch.error':            '无法启动游戏：{err}',
    'mods.openFolder.title':   '打开模组文件夹',
    'mods.notFromManager':             '未通过管理器安装',
    'deps.conflict':           '冲突：{names}\n\n此模组与一个或多个已激活的模组不兼容。',
    'deps.missingInstalled':   '缺少依赖（未安装）：{names}\n\n所需模组不在模组文件夹中。',
    'deps.missingActive':      '缺少依赖（已禁用）：{names}\n\n所需模组已安装但未激活。',
    'deps.deprecated':         '已被替代：{names}\n\n此模组已被激活的模组替代，建议禁用。',
    'deps.dialog.conflict':    '"{mod}"与以下已激活的模组冲突：',
    'deps.dialog.missingInstalled': '"{mod}"需要以下未安装的模组：',
    'deps.dialog.missingActive': '"{mod}"需要以下已安装但已禁用的模组：',
    'deps.dialog.deprecated':  '"{mod}"已被以下激活的模组替代：',
    'deps.dialog.enable':      '启用',
    'deps.dialog.disable':     '禁用',
    'deps.dialog.disableThis': '禁用此模组',
    'deps.dialog.install':     '安装',
    'deps.dialog.installing':  '安装中…',
    'deps.dialog.close':       '关闭',
    'mods.versionMismatch':        '已安装：v{lv} → 可用：v{rv}\n\n版本号不匹配。点击直接从 mod.io 更新模组。',
    'mods.versionMismatchInfo':    '已安装：v{lv} · mod.io：v{rv}\n\n本地版本似乎比 mod.io 上发布的更新。',
    'mods.versionMismatchSameFile': '已安装：v{lv} · mod.io：v{rv}\n\n版本标签不同，但已安装的文件是最新的。这可能是作者的不一致（modinfo.json 未更新）。',
    'mods.link.cta':                   '🔗 关联到 mod.io',
    'mods.link.title':                 '将 « {name} » 关联到 mod.io 记录',
    'mods.link.searchPlaceholder':     '搜索 mod.io…',
    'mods.link.confirm':               '关联',
    'mods.link.empty':                 '无匹配 — 请尝试其他名称。',
    'mods.link.cancel':                '取消',
    'tab.news':                '新闻',
    'tab.activation':          '激活',
    'tab.browser':             '模组浏览器',
    'tab.collections':         '合集',
    'tab.install':             '手动安装',
    'tab.log':                 'Modloader 日志',
    'tab.tweak':               '调整',
    'tab.settings':            '设置',
    'settings.section.paths':       '路径',
    'settings.section.behaviour':   '行为',
    'settings.section.advanced':    '高级',
    'settings.gamePath':            'Anno 117 可执行文件',
    'settings.gamePath.empty':      '未配置 — 设置 Anno117.exe 的路径',
    'settings.docsPath':            '文档文件夹覆盖',
    'settings.docsPath.empty':      '自动检测（使用 ~/Documents 或 Proton 前缀）',
    'settings.browseFile':          '浏览文件…',
    'settings.browseFolder':        '浏览文件夹…',
    'settings.autoDetect':          '自动检测',
    'settings.clear':               '清除',
    'settings.open':                '打开',
    'settings.modLocation':         '模组存储位置',
    'settings.modLocation.documents': '文档文件夹（推荐）',
    'settings.modLocation.game':      '游戏安装文件夹',
    'settings.enableNewMods':       '新安装的模组',
    'settings.enableNewMods.on':    '始终启用',
    'settings.enableNewMods.off':   '从不启用',
    'settings.enableNewMods.keep':  '保持先前状态',
    'settings.textScale':              '正文字号',
    'settings.textScale.small':        '小',
    'settings.textScale.medium':       '中',
    'settings.textScale.large':        '大',
    'settings.derived.docsMods':    '模组文件夹（文档）',
    'settings.derived.gameMods':    '模组文件夹（游戏）',
    'settings.derived.profile':     'active-profile.txt',
    'settings.derived.appdata':     'AppData',
    'settings.derived.presets':     '预设',
    'settings.pathError':           '无法保存路径：{err}',
    'settings.detectError':         '自动检测失败：{err}',
    'settings.section.modio':       'mod.io 集成',
    'settings.modio.hint':          '输入您的个人 mod.io API 密钥以启用模组浏览器和合集选项卡。请在以下位置生成：',
    'settings.modio.apiKey':        'API 密钥',
    'settings.modio.apiKeyPlaceholder': '在此粘贴您的 mod.io API 密钥',
    'settings.modio.save':          '保存',
    'settings.modio.disconnectConfirm': '删除已保存的 mod.io API 密钥？',
    'settings.modio.emptyKey':      'API 密钥为空。',
    'log.refresh':                  '↻ 刷新',
    'log.copy':                     '⧉ 复制',
    'log.openFile':                 '打开文件',
    'log.loading':                  '加载中…',
    'log.empty':                    'mod-loader.log 为空。',
    'log.notFound':                 '未在以下位置找到 mod-loader.log：\n{path}',
    'log.truncated':                '日志已截断为最后 2 MB',
    'install.title':                '手动安装',
    'install.hint':                 '在此处放下模组 ZIP，或点击浏览。压缩包必须包含 modinfo.json（或 .jsonc）文件。',
    'install.drop':                 '在此处放下 .zip 模组',
    'install.or':                   '— 或 —',
    'install.browse':               '浏览 ZIP 文件…',
    'install.targetLabel':          '安装目标：',
    'install.installing':           '正在安装 {name}…',
    'install.success':              '{name} 已安装。',
    'install.cancelled':            '已取消。',
    'install.overwriteConfirm':     '名为「{name}」的模组文件夹已存在。是否替换？',
    'tweak.listHeader':             '可调整的模组',
    'tweak.optionWord':             '选项',
    'tweak.noTweakable':            '已安装的模组中没有提供选项的。',
    'tweak.pickHint':                '在左侧选择模组以调整其选项。',
    'tweak.noOptions':              '此模组没有可配置的选项。',
    'tweak.resetMod':               '重置此模组',
    'tweak.resetAll':               '全部重置',
    'tweak.resetModConfirm':        '将此模组的所有选项重置为默认值？',
    'tweak.resetAllConfirm':        '重置所有模组的选项？active-options.jsonc 文件将被删除。',
    'tweak.defaultsSection':           '— 默认值 —',
    'tweak.colorPicker.open':          '打开颜色选择器',
    'tweak.colorPicker.title':         '颜色选择器',
    'tweak.colorPicker.before':        '之前',
    'tweak.colorPicker.after':         '之后',
    'tweak.colorPicker.cancel':        '取消',
    'tweak.colorPicker.apply':         '应用',
    'news.refresh':                 '↻ 刷新',
    'news.loading':                 '正在获取最新帖子…',
    'news.empty':                   '没有可显示的新闻。',
    'news.error':                   '无法获取新闻：{err}',
    'news.cached':                  '已缓存（10 分钟）',
    'news.includeReddit':           '包含 r/anno 帖子',
    'news.visitUnion':              '打开 Anno Union ↗',
    'news.back':                       '返回新闻',
    'news.openOnUnion':                '在 Anno Union 上打开 ↗',
    'settings.modio.clearKey':      '清除密钥',
    'modio.badge.connected':        '● 已连接',
    'modio.badge.keyOnly':          '◐ 仅 API 密钥',
    'modio.badge.notSet':           '○ 未设置',
    'modio.session':                '会话',
    'modio.expires':                '于 {date} 过期',
    'modio.disconnect':             '断开连接',
    'modio.disconnectConfirm':      '断开与 mod.io 的连接？您的 API 密钥将保持已保存状态；您可以稍后重新连接。',
    'modio.needKeyFirst':           '先在上方保存您的 API 密钥，然后才能连接。',
    'modio.startConnect':           '连接到 mod.io',
    'modio.email':                  '电子邮箱地址',
    'modio.emailPlaceholder':       'you@example.com',
    'modio.emailRequired':          '请输入您的邮箱。',
    'modio.termsAgree':             '我同意 mod.io 的',
    'modio.termsLink':              '使用条款',
    'modio.cancel':                 '取消',
    'common.cancel':                   '取消',
    'common.confirm':                  '确认',
    'modio.sendCode':               '发送验证码',
    'modio.sending':                '发送中…',
    'modio.code':                   '安全码',
    'modio.codeRequired':           '输入您邮箱中收到的 5 位验证码。',
    'modio.codeSent':               '已向 {email} 发送 5 位验证码。请检查收件箱（和垃圾邮件）。',
    'modio.connect':                '连接',
    'modio.connecting':             '连接中…',
    // Mod Browser
    'browser.title':                '模组浏览器',
    'browser.searchPlaceholder':    '搜索模组…',
    'browser.search':               '搜索',
    'browser.refresh':              '刷新',
    'browser.sortNewest':           '最新',
    'browser.sortPopular':          '最热门',
    'browser.sortDownloads':        '最多下载',
    'browser.sortRating':           '评价最高',
    'browser.sortAlpha':            'A → Z',
    'browser.sortBy':               '排序：',
    'browser.mySubscriptions':         '我的订阅',
    'browser.myFollows':               '我的关注',
    'browser.follow':                  '关注此合集',
    'browser.unfollow':                '取消关注此合集',
    'browser.tag':                  '标签：',
    'browser.tagAll':               '所有标签',
    'browser.clearSearch':          '清除搜索',
    'browser.byAuthor':             '作者：{name}',
    'browser.clearAuthor':          '显示所有作者',
    'browser.filterByAuthor':       '仅显示此作者的模组',
    'browser.bundledMods':          '包含的模组',
    'browser.bundledEmpty':         '此合集未列出任何包含的模组。',
    'browser.backToCollection':     '返回合集',
    'browser.installCollection':    '安装合集',
    'browser.updateCollection':     '更新合集',
    'browser.uninstallCollection':  '🗑 卸载合集',
    'browser.uninstallConfirm':     '删除从「{name}」创建的配置文件「{profile}」？',
    'browser.uninstallAlsoMods':    '是否也从磁盘删除此合集中包含的 {count} 个模组？',
    'browser.uninstallOk':          '配置文件「{profile}」已删除。',
    'browser.uninstallOkWithMods':  '配置文件「{profile}」已删除；{count} 个包含的模组已从磁盘删除。',
    'browser.uninstallFail':        '卸载失败：{error}',
    'browser.collectionInstallOk':  '「{name}」：已安装 {count}/{total} 个模组。配置文件「{profile}」现已激活。',
    'browser.collectionInstallFailures': '（{count} 个失败 — 请查看日志）',
    'browser.back':                 '返回',
    'browser.empty':                '没有模组与您的搜索匹配。',
    'browser.loading':              '加载模组中…',
    'browser.error':                '无法加载模组：{error}',
    'browser.notAuth':              '未连接到 mod.io。请在设置选项卡中连接。',
    'browser.openSettings':         '打开设置',
    'browser.prev':                 '‹ 上一页',
    'browser.next':                 '下一页 ›',
    'browser.pageOf':               '第 {page} / {total} 页',
    'browser.resultsCount':         '共 {total} 个模组中的 {shown} 个',
    'browser.detailPick':           '从列表中选择模组以查看其详情。',
    'browser.install':              '安装',
    'browser.installing':           '安装中…',
    'browser.installed':            '✓ 已安装',
    'browser.update':               '更新',
    'browser.installOk':            '「{name}」已安装。',
    'browser.installFail':          '安装失败：{error}',
    'browser.subscribe':            '+ 订阅',
    'browser.subscribed':           '✓ 已订阅',
    'browser.unsubscribe':          '取消订阅',
    'browser.uninstallMod':            '🗑 卸载',
    'browser.uninstallModConfirm':     '从磁盘删除 « {name} »？',
    'browser.uninstallModOk':          '« {name} » 已卸载。',
    'browser.endorse':              '♥ 推荐',
    'browser.endorsed':             '♥ 已推荐',
    'browser.endorseFail':          '无法推荐：{error}',
    'browser.subFail':              '无法订阅：{error}',
    'browser.openOnModio':          '在 mod.io 上打开 ↗',
    'browser.author':               '作者：{name}',
    'browser.downloads':            '{n} 次下载',
    'browser.subscribers':          '{n} 个订阅者',
    'browser.modsTotal':            '{n} 个模组',
    'browser.updated':              '更新于 {date}',
    'browser.size':                 '大小：{size}',
    'browser.version':              '版本：{v}',
    'browser.changelog':            '更新日志',
    'browser.description':          '描述',
  },
  traditional_chinese: {
    'hud.settings':                 '設定',
    'hud.refreshMods':              '重新整理模組列表',
    'hud.searchMod':                '搜尋模組…',
    'hud.language':                 '語言',
    'alert.loadPresetFail':         '載入預設失敗：{error}',
    'alert.savePresetFail':         '儲存預設失敗：{error}',
    'alert.deletePresetFail':       '刪除預設失敗：{error}',
    'alert.uninstallFail':          '解除安裝失敗：{error}',
    'profile.label':           '設定檔',
    'profile.new':             '＋ 新增',
    'profile.delete':          '🗑 刪除',
    'profile.deleteConfirm':   '刪除預設「{name}」？',
    'profile.cantDeleteReserved': '「Default」和「Vanilla」設定檔無法刪除。',
    'profile.promptName':      '新預設名稱：',
    'mode.manage':             '管理',
    'mode.order':              '載入順序',
    'mode.manage.title':       '排序與啟用/停用模組',
    'mode.order.title':        '透過拖放重新排序載入順序',
    'list.head.toggleAll':     '全部啟用 / 停用',
    'list.head.category':      '類別',
    'list.head.name':          '模組名稱',
    'list.head.size':          '大小',
    'list.head.status':        '狀態',
    'list.empty':              '在已設定的資料夾中未偵測到模組。',
    'count.active':            '{n} / {total} 已啟用',
    'pill.active':             'ON',
    'pill.off':                'OFF',
    'detail.empty':            '從列表中選擇模組以檢視其詳細資料。',
    'detail.banner.empty':     '此模組未提供橫幅。',
    'detail.description':      '描述',
    'detail.details':          '詳細資料',
    'detail.meta.category':    '類別',
    'detail.meta.difficulty':  '難度',
    'detail.meta.size':        '大小',
    'detail.meta.folder':      '資料夾',
    'detail.creator':          '作者：{name} · v{version}',
    'detail.openFolder':       '開啟資料夾',
    'detail.uninstall':        '解除安裝',
    'detail.uninstallConfirm': '解除安裝模組「{name}」？\n\n該資料夾將從磁碟中刪除。',
    'tab.placeholder':         '此分頁將在遷移第二階段移植。',
    'tab.placeholderHint':     'pywebview POC 進行中 — 目前只有 {tab} 分頁可用。',
    'launch.title':            '啟動 Anno 117',
    'launch.error':            '無法啟動遊戲：{err}',
    'mods.openFolder.title':   '開啟模組資料夾',
    'mods.notFromManager':             '未透過管理員安裝',
    'deps.conflict':           '衝突：{names}\n\n此模組與一個或多個已啟用的模組不相容。',
    'deps.missingInstalled':   '缺少依賴（未安裝）：{names}\n\n所需模組不在模組資料夾中。',
    'deps.missingActive':      '缺少依賴（已停用）：{names}\n\n所需模組已安裝但未啟用。',
    'deps.deprecated':         '已被取代：{names}\n\n此模組已被啟用的模組取代，建議停用。',
    'deps.dialog.conflict':    '「{mod}」與以下已啟用的模組衝突：',
    'deps.dialog.missingInstalled': '「{mod}」需要以下未安裝的模組：',
    'deps.dialog.missingActive': '「{mod}」需要以下已安裝但已停用的模組：',
    'deps.dialog.deprecated':  '「{mod}」已被以下啟用的模組取代：',
    'deps.dialog.enable':      '啟用',
    'deps.dialog.disable':     '停用',
    'deps.dialog.disableThis': '停用此模組',
    'deps.dialog.install':     '安裝',
    'deps.dialog.installing':  '安裝中…',
    'deps.dialog.close':       '關閉',
    'mods.versionMismatch':        '已安裝：v{lv} → 可用：v{rv}\n\n版本號不符。點擊直接從 mod.io 更新模組。',
    'mods.versionMismatchInfo':    '已安裝：v{lv} · mod.io：v{rv}\n\n本地版本似乎比 mod.io 上發布的更新。',
    'mods.versionMismatchSameFile': '已安裝：v{lv} · mod.io：v{rv}\n\n版本標籤不同，但已安裝的檔案是最新的。這可能是作者的不一致（modinfo.json 未更新）。',
    'mods.link.cta':                   '🔗 關聯到 mod.io',
    'mods.link.title':                 '將 « {name} » 關聯到 mod.io 記錄',
    'mods.link.searchPlaceholder':     '搜尋 mod.io…',
    'mods.link.confirm':               '關聯',
    'mods.link.empty':                 '無相符 — 請嘗試其他名稱。',
    'mods.link.cancel':                '取消',
    'tab.news':                '新聞',
    'tab.activation':          '啟用',
    'tab.browser':             '模組瀏覽器',
    'tab.collections':         '合輯',
    'tab.install':             '手動安裝',
    'tab.log':                 'Modloader 紀錄',
    'tab.tweak':               '調整',
    'tab.settings':            '設定',
    'settings.section.paths':       '路徑',
    'settings.section.behaviour':   '行為',
    'settings.section.advanced':    '進階',
    'settings.gamePath':            'Anno 117 執行檔',
    'settings.gamePath.empty':      '未設定 — 設定 Anno117.exe 的路徑',
    'settings.docsPath':            '文件資料夾覆寫',
    'settings.docsPath.empty':      '自動偵測（使用 ~/Documents 或 Proton 前綴）',
    'settings.browseFile':          '瀏覽檔案…',
    'settings.browseFolder':        '瀏覽資料夾…',
    'settings.autoDetect':          '自動偵測',
    'settings.clear':               '清除',
    'settings.open':                '開啟',
    'settings.modLocation':         '模組儲存位置',
    'settings.modLocation.documents': '文件資料夾（建議）',
    'settings.modLocation.game':      '遊戲安裝資料夾',
    'settings.enableNewMods':       '新安裝的模組',
    'settings.enableNewMods.on':    '一律啟用',
    'settings.enableNewMods.off':   '一律不啟用',
    'settings.enableNewMods.keep':  '保留先前狀態',
    'settings.textScale':              '正文字級',
    'settings.textScale.small':        '小',
    'settings.textScale.medium':       '中',
    'settings.textScale.large':        '大',
    'settings.derived.docsMods':    '模組資料夾（文件）',
    'settings.derived.gameMods':    '模組資料夾（遊戲）',
    'settings.derived.profile':     'active-profile.txt',
    'settings.derived.appdata':     'AppData',
    'settings.derived.presets':     '預設',
    'settings.pathError':           '無法儲存路徑：{err}',
    'settings.detectError':         '自動偵測失敗：{err}',
    'settings.section.modio':       'mod.io 整合',
    'settings.modio.hint':          '輸入您的個人 mod.io API 金鑰以啟用模組瀏覽器和合輯分頁。請在以下位置產生：',
    'settings.modio.apiKey':        'API 金鑰',
    'settings.modio.apiKeyPlaceholder': '在此貼上您的 mod.io API 金鑰',
    'settings.modio.save':          '儲存',
    'settings.modio.disconnectConfirm': '移除已儲存的 mod.io API 金鑰？',
    'settings.modio.emptyKey':      'API 金鑰為空。',
    'log.refresh':                  '↻ 重新整理',
    'log.copy':                     '⧉ 複製',
    'log.openFile':                 '開啟檔案',
    'log.loading':                  '載入中…',
    'log.empty':                    'mod-loader.log 為空。',
    'log.notFound':                 '在以下位置找不到 mod-loader.log：\n{path}',
    'log.truncated':                '紀錄已截斷至最後 2 MB',
    'install.title':                '手動安裝',
    'install.hint':                 '將模組 ZIP 拖放至此，或點擊瀏覽。封存檔必須包含 modinfo.json（或 .jsonc）檔案。',
    'install.drop':                 '在此處拖放 .zip 模組',
    'install.or':                   '— 或 —',
    'install.browse':               '瀏覽 ZIP 檔案…',
    'install.targetLabel':          '安裝目的地：',
    'install.installing':           '正在安裝 {name}…',
    'install.success':              '{name} 已安裝。',
    'install.cancelled':            '已取消。',
    'install.overwriteConfirm':     '名為「{name}」的模組資料夾已存在。是否替換？',
    'tweak.listHeader':             '可調整的模組',
    'tweak.optionWord':             '選項',
    'tweak.noTweakable':            '已安裝的模組中沒有提供選項的。',
    'tweak.pickHint':                '在左側選擇模組以調整其選項。',
    'tweak.noOptions':              '此模組沒有可設定的選項。',
    'tweak.resetMod':               '重設此模組',
    'tweak.resetAll':               '全部重設',
    'tweak.resetModConfirm':        '將此模組的所有選項重設為預設值？',
    'tweak.resetAllConfirm':        '重設所有模組的選項？active-options.jsonc 檔案將被刪除。',
    'tweak.defaultsSection':           '— 預設值 —',
    'tweak.colorPicker.open':          '打開顏色選擇器',
    'tweak.colorPicker.title':         '顏色選擇器',
    'tweak.colorPicker.before':        '之前',
    'tweak.colorPicker.after':         '之後',
    'tweak.colorPicker.cancel':        '取消',
    'tweak.colorPicker.apply':         '套用',
    'news.refresh':                 '↻ 重新整理',
    'news.loading':                 '正在擷取最新貼文…',
    'news.empty':                   '沒有新聞可顯示。',
    'news.error':                   '無法擷取新聞：{err}',
    'news.cached':                  '已快取（10 分鐘）',
    'news.includeReddit':           '包含 r/anno 貼文',
    'news.visitUnion':              '開啟 Anno Union ↗',
    'news.back':                       '返回新聞',
    'news.openOnUnion':                '在 Anno Union 上開啟 ↗',
    'settings.modio.clearKey':      '清除金鑰',
    'modio.badge.connected':        '● 已連線',
    'modio.badge.keyOnly':          '◐ 僅 API 金鑰',
    'modio.badge.notSet':           '○ 未設定',
    'modio.session':                '工作階段',
    'modio.expires':                '於 {date} 到期',
    'modio.disconnect':             '中斷連線',
    'modio.disconnectConfirm':      '中斷與 mod.io 的連線？您的 API 金鑰會保持儲存；您可以稍後重新連線。',
    'modio.needKeyFirst':           '請先在上方儲存您的 API 金鑰，然後才能連線。',
    'modio.startConnect':           '連線到 mod.io',
    'modio.email':                  '電子郵件地址',
    'modio.emailPlaceholder':       'you@example.com',
    'modio.emailRequired':          '請輸入您的電子郵件。',
    'modio.termsAgree':             '我同意 mod.io 的',
    'modio.termsLink':              '使用條款',
    'modio.cancel':                 '取消',
    'common.cancel':                   '取消',
    'common.confirm':                  '確認',
    'modio.sendCode':               '傳送驗證碼',
    'modio.sending':                '傳送中…',
    'modio.code':                   '安全碼',
    'modio.codeRequired':           '輸入您電子郵件中收到的 5 位驗證碼。',
    'modio.codeSent':               '已將 5 位驗證碼傳送至 {email}。請檢查收件匣（和垃圾郵件）。',
    'modio.connect':                '連線',
    'modio.connecting':             '連線中…',
    // Mod Browser
    'browser.title':                '模組瀏覽器',
    'browser.searchPlaceholder':    '搜尋模組…',
    'browser.search':               '搜尋',
    'browser.refresh':              '重新整理',
    'browser.sortNewest':           '最新',
    'browser.sortPopular':          '最熱門',
    'browser.sortDownloads':        '最多下載',
    'browser.sortRating':           '評價最高',
    'browser.sortAlpha':            'A → Z',
    'browser.sortBy':               '排序方式：',
    'browser.mySubscriptions':         '我的訂閱',
    'browser.myFollows':               '我的關注',
    'browser.follow':                  '關注此合集',
    'browser.unfollow':                '取消關注此合集',
    'browser.tag':                  '標籤：',
    'browser.tagAll':               '所有標籤',
    'browser.clearSearch':          '清除搜尋',
    'browser.byAuthor':             '作者：{name}',
    'browser.clearAuthor':          '顯示所有作者',
    'browser.filterByAuthor':       '僅顯示此作者的模組',
    'browser.bundledMods':          '包含的模組',
    'browser.bundledEmpty':         '此合輯未列出任何包含的模組。',
    'browser.backToCollection':     '返回合輯',
    'browser.installCollection':    '安裝合輯',
    'browser.updateCollection':     '更新合輯',
    'browser.uninstallCollection':  '🗑 解除安裝合輯',
    'browser.uninstallConfirm':     '刪除由「{name}」建立的設定檔「{profile}」？',
    'browser.uninstallAlsoMods':    '是否也從磁碟刪除此合輯中包含的 {count} 個模組？',
    'browser.uninstallOk':          '設定檔「{profile}」已移除。',
    'browser.uninstallOkWithMods':  '設定檔「{profile}」已移除；{count} 個包含的模組已從磁碟刪除。',
    'browser.uninstallFail':        '解除安裝失敗：{error}',
    'browser.collectionInstallOk':  '「{name}」：已安裝 {count}/{total} 個模組。設定檔「{profile}」現在已啟用。',
    'browser.collectionInstallFailures': '（{count} 個失敗 — 請查看紀錄）',
    'browser.back':                 '返回',
    'browser.empty':                '沒有模組符合您的搜尋。',
    'browser.loading':              '載入模組中…',
    'browser.error':                '無法載入模組：{error}',
    'browser.notAuth':              '未連線到 mod.io。請在設定分頁中連線。',
    'browser.openSettings':         '開啟設定',
    'browser.prev':                 '‹ 上一頁',
    'browser.next':                 '下一頁 ›',
    'browser.pageOf':               '第 {page} / {total} 頁',
    'browser.resultsCount':         '共 {total} 個模組中的 {shown} 個',
    'browser.detailPick':           '從列表中選擇模組以檢視其詳細資料。',
    'browser.install':              '安裝',
    'browser.installing':           '安裝中…',
    'browser.installed':            '✓ 已安裝',
    'browser.update':               '更新',
    'browser.installOk':            '「{name}」已安裝。',
    'browser.installFail':          '安裝失敗：{error}',
    'browser.subscribe':            '+ 訂閱',
    'browser.subscribed':           '✓ 已訂閱',
    'browser.unsubscribe':          '取消訂閱',
    'browser.uninstallMod':            '🗑 解除安裝',
    'browser.uninstallModConfirm':     '從磁碟刪除 « {name} »？',
    'browser.uninstallModOk':          '« {name} » 已解除安裝。',
    'browser.endorse':              '♥ 推薦',
    'browser.endorsed':             '♥ 已推薦',
    'browser.endorseFail':          '無法推薦：{error}',
    'browser.subFail':              '無法訂閱：{error}',
    'browser.openOnModio':          '在 mod.io 上開啟 ↗',
    'browser.author':               '作者：{name}',
    'browser.downloads':            '{n} 次下載',
    'browser.subscribers':          '{n} 位訂閱者',
    'browser.modsTotal':            '{n} 個模組',
    'browser.updated':              '更新於 {date}',
    'browser.size':                 '大小：{size}',
    'browser.version':              '版本：{v}',
    'browser.changelog':            '變更紀錄',
    'browser.description':          '描述',
  },
};

window.annoApp = function () {
  return {
    // ── State ──────────────────────────────────────────────────────────────
    version: '',
    release: { checked: false, up_to_date: true, latest: '', url: '' },
    currentTab: 'activation',
    modUpdates: {},             // {mod_id: latest_modfile_id} — refreshed at boot for the Activation row buttons
    // Activation → "link to mod.io" picker for hand-installed mods.
    // Opens with the local mod's name pre-filled in the search; the user
    // confirms the match by clicking a result. Never picks anything
    // automatically.
    // App-styled replacement for window.confirm() — see confirmDialog()
    // method below. Resolves via _confirmModalAnswer() to keep the
    // promise-based call site (await this.confirmDialog(msg)) ergonomic.
    confirmModal: { open: false, message: '', resolve: null },
    linkPicker: {
      open: false,
      folder: '',          // basename of the local mod folder being linked
      localName: '',       // pretty name shown in the picker header
      search: '',          // editable search query (seeded from localName)
      results: [],
      loading: false,
      error: '',
      busyId: 0,           // mod_id being linked while the call is in flight
    },
    depDialog: {
      open: false,
      type: '',       // 'conflict' | 'missingInstalled' | 'missingActive' | 'deprecated'
      modId: '',      // local id of the mod that has the issue
      modName: '',
      items: [],      // [{id, name}] — concerned mods (conflicting / missing / deprecating)
      busyId: '',     // name_id currently being installed
      error: '',
    },
    mods: [],
    selectedModId: null,
    selectedBannerUrl: '',
    _bannerCache: new Map(),
    search: '',
    profileName: 'Default',
    presets: [],                // user-saved preset names (filled by refreshMods)
    sortBy: 'status',           // 'status' | 'category' | 'name'
    sortDir: 1,                 // 1 = asc, -1 = desc, 0 = unsorted (status only)
    mode: 'manage',             // 'manage' | 'order'
    profileOrder: [],           // mod ids in active-profile.txt order (Load Order view)
    _dragId: null,              // id of the row currently being dragged
    languages: [],              // [{key, name, flag}, ...] from the backend
    currentLang: 'english',     // selected language key
    langOpen: false,            // popover open state
    settings: {},               // mirror of the persisted settings.json
    pathsInfo: {},              // resolved paths from the backend (Settings tab)
    modioStatus: { api_key_set: false, has_token: false, token_valid: false,
                   expires_text: '', terms_agreed: false },
    modioAuth: { step: 'idle', email: '', code: '', termsAgreed: true,
                 error: '', busy: false },
    log: { content: '', path: '', exists: false, truncated: false, loaded: false },
    _logTimer: null,            // setInterval id while the Log tab is open
    install: { busy: false, message: '', error: false, dragOver: false },
    _dragDepth: 0,              // dragenter counter — kills the flicker that
                                // happens when the cursor crosses child nodes
    tweak: {
      mods: [],                 // [{id, name, category, folder, option_count}, ...]
      selectedId: null,
      schema: {},               // current selected mod's options schema
      values: {},               // current values (saved or default per option)
      saving: '',               // key being saved (lights up the row briefly)
    },
    // In-app colour picker state — single global popover positioned near the
    // swatch that opened it. Kept on Alpine root so the popover can live
    // outside the tweak DOM (which is itself rendered via x-html and would
    // otherwise nuke the picker on every value change).
    colorPicker: {
      open: false,
      key: '',                  // tweak option key being edited
      h: 0, s: 0, v: 0,         // HSV state of the current preview
      alpha: 0xFF,              // preserved from the previous int
      prevHex: '#000000',       // colour the picker was opened with (for the "before" swatch)
      x: 0, y: 0,               // fixed-position coords of the popover anchor
      drag: null,               // 'sv' | 'hue' while a drag is in flight
      palette: ANNO_PALETTE,    // in-game banner palette (alias for x-for binding)
    },
    news: { items: [], loading: false, error: '', cached: false, loaded: false,
            // Lazy-loaded detail state. `cache` keys by wp_id so re-opening the
            // same post is instant; the open card is tracked in `current`.
            detail: { open: false, item: null, html: '', loading: false, error: '' },
            cache: {} },
    _newsTimer: null,           // background poll started on first News open
    browser: {
      // List state
      items: [],                // current page of mod summaries from mod.io
      total: 0,                 // result_total reported by mod.io
      offset: 0,                // current pagination offset
      limit: 24,                // page size (multiple of 4 cards/row)
      search: '',               // committed search query (the input is uncontrolled)
      sort: '-date_updated',    // mod.io _sort syntax
      tagFilter: '',            // '' = all, otherwise the exact tag name to filter on
      tagsCatalog: [],          // array of {name, tags: [str, ...]} groups from mod.io
      authorFilter: { id: 0, name: '' }, // {id, name} when filtering by submitter
      subscribedOnly: false,    // toggle: list /me/subscribed instead of /games/{}/mods
      followedOnly: false,      // toggle (Collections tab): list /me/following/collections
      followedColls: {},        // {coll_id: true} cache for the ★/☆ button on collection cards
      followBusy: {},           // {coll_id: true} while a follow/unfollow call runs
      dependencies: [],         // mods bundled by the currently-open collection
      dependenciesLoading: false,
      // Single-step navigation stack: when the user opens a mod from a
      // collection's "Mods inclus" list we stash the collection here so the
      // back button can restore it instead of dropping back to the grid.
      parent: null,             // null | { detail, dependencies, isCollection }
      detailOpen: false,        // false = grid of cards, true = detail page
      loading: false,
      loaded: false,            // false until the first list call resolves
      error: '',
      notAuth: false,           // surface "go connect in Settings" CTA
      // Detail state
      selectedId: null,
      detail: null,             // full mod object once fetched
      detailLoading: false,
      // Cross-cutting actions
      subscribed: {},           // {modId: true} membership cache
      installedFolders: {},     // {folderName: true} — derived from local mods scanner
      installedIds: {},         // {modioId: true} — persisted in settings.json after each install
      installedMeta: {},        // {modioId: {modfile_id, version}} — drives "Update" vs "Installed" CTA
      installing: {},           // {modId: true} while a download+install is in flight
      subBusy: {},              // {modId: true} while a subscribe/unsubscribe call runs
      endorseBusy: {},          // {modId: true} while a rating call runs
      endorsed: {},             // {modId: true} optimistic flip after a successful endorse
      flash: '',                // transient success line under the detail panel
      flashError: false,
    },

    // Sidebar tab definitions (icons stay text-glyph for the POC; phase 2 will
    // swap them for the data/ui/4k icon set the Tk version already uses).
    // Static tab metadata; the human-readable label is computed live from the
    // translation table so the labels swap when the language changes.
    _tabsRaw: [
      { id: 'activation',   key: 'tab.activation',   img: 'icons/activation.png',  group: 'mods' },
      { id: 'browser',      key: 'tab.browser',      img: 'icons/browser.png',     group: 'mods' },
      { id: 'collections',  key: 'tab.collections',  img: 'icons/collections.png', group: 'mods' },
      { id: 'install',      key: 'tab.install',      img: 'icons/install.png',     group: 'mods' },
      { id: 'news',         key: 'tab.news',         img: 'icons/news.png',        group: 'tools' },
      { id: 'log',          key: 'tab.log',          img: 'icons/log.png',         group: 'tools' },
      { id: 'tweak',        key: 'tab.tweak',        img: 'icons/tweak.png',       group: 'tools' },
      // Settings lives in the bottom HUD row (gear circle), not the tab pill.
    ],
    get tabs() {
      return this._tabsRaw.map((t) => ({ ...t, label: this.t(t.key) }));
    },

    // ── Lifecycle ──────────────────────────────────────────────────────────
    async init() {
      // Stop the webview from navigating to a file when the user drops it
      // outside the install zone — without this, dropping a .zip anywhere on
      // the page makes WebKit2GTK try to open the file as a new document.
      document.addEventListener('dragover', (e) => { e.preventDefault(); }, false);
      document.addEventListener('drop', (e) => {
        // If the drop happened on the install zone, its own handler runs
        // first and we already preventDefault'd there. This catches drops
        // anywhere else.
        e.preventDefault();
      }, false);

      // pywebview injects window.pywebview.api asynchronously; wait for it.
      await this.waitForApi();
      const info = await window.pywebview.api.app_info();
      this.version = info.version;
      // Best-effort latest-release check — non blocking, failure is silent.
      // Drives the green/red dot next to the version label.
      window.pywebview.api.check_latest_release().then((r) => {
        if (r) this.release = {
          checked: true,
          up_to_date: !!r.up_to_date,
          latest: String(r.latest || ''),
          url: String(r.url || 'https://github.com/taludas/anno-117-mod-manager/releases'),
        };
      }).catch(() => {});
      try {
        this.languages = await window.pywebview.api.get_languages();
        this.currentLang = await window.pywebview.api.get_language();
      } catch (e) {
        console.error('language init failed:', e);
      }
      await this.refreshMods();
      // Pull mod.io status once at boot so the gated-tab redirect in
      // selectTab() can decide based on the real token state, not the
      // {token_valid: false} default.
      try {
        this.modioStatus = (await window.pywebview.api.modio_status())
                           || this.modioStatus;
      } catch (e) {
        console.error('modio_status init failed:', e);
      }
      // Hydrate _modio_install.json markers + check for available updates
      // so the Activation rows can show their per-row Update/Uninstall
      // buttons from the very first render. Both calls are best-effort —
      // a missing marker or no auth just hides the relevant icon.
      await this._refreshInstalledIds();
      // Auto-link hand-installed mods whose modinfo.ModID strictly
      // matches a mod.io name_id — same idea as the "check the marker
      // file" pass above, but extending it to mods that don't have a
      // marker yet. Linked mods get the version-aware Update / Uninstall
      // affordances on the very first boot. Non-matches keep the
      // manual 🔗 button.
      try {
        const r = await window.pywebview.api.modio_auto_link_unmarked();
        if (r && r.ok && r.linked > 0) {
          await this._refreshInstalledIds();  // pick up the new markers
        }
      } catch (_) { /* silent */ }
      this._refreshModUpdates();  // fire-and-forget, doesn't block boot
      // Restore the previously-selected profile, if any. We persist the
      // user's choice in settings so a relaunch lands on the same preset
      // they were working from. Falls back to Default if the saved name
      // no longer matches an existing preset (or is reserved).
      try {
        const s = await window.pywebview.api.get_settings();
        const saved = s && s.active_profile_name;
        if (saved && (saved === 'Default' || saved === 'Vanilla' ||
                      this.presets.includes(saved))) {
          this.profileName = saved;
          if (saved !== 'Default') {
            // Re-apply the preset to active-profile.txt so the in-memory
            // state and on-disk profile actually match.
            await window.pywebview.api.load_preset(saved);
            await this.refreshMods();
          }
        }
        // Restore the Browser's My Subscriptions filter — kept across
        // launches so the user doesn't re-tick on every start.
        if (s && typeof s.browser_subscribed_only === 'boolean') {
          this.browser.subscribedOnly = s.browser_subscribed_only;
        }
        if (s && typeof s.browser_followed_only === 'boolean') {
          this.browser.followedOnly = s.browser_followed_only;
        }
        // Reading text size — apply the saved class to <body> so the news
        // reader / mod descriptions render at the chosen scale on boot,
        // not just after the user re-touches the setting.
        this.applyTextScale(s && s.text_scale);
      } catch (e) {
        console.error('restore active profile failed:', e);
      }
      // Auto-detect the game executable on first launch so the user can
      // jump straight in without having to click the "Auto-detect" button
      // in Settings. We only run it when no valid game_path is configured
      // (covers fresh installs AND cases where the user moved/uninstalled
      // the game since last run). Best-effort: a failure just leaves the
      // setting empty, the user can fall back to the manual button.
      try {
        const info = await window.pywebview.api.get_paths_info();
        if (info && (!info.game_path || !info.game_path_exists)) {
          await window.pywebview.api.detect_game_path();
        }
      } catch (_) { /* silent */ }
      // Refresh contextual data each time the user opens a tab that needs it.
      // For the log we also kick off a 2-second poll so the user sees new
      // entries land while the game is running, and stop the poll the moment
      // they navigate away.
      this.$watch('currentTab', (next, prev) => {
        if (next === 'settings') this.refreshSettings();
        if (next === 'tweak')    this.refreshTweakable();
        if (next === 'news' && !this.news.loaded) this.refreshNews(false);
        if (next === 'browser' || next === 'collections') {
          // Browser and Collections share the same state — only the API
          // filter differs. Switch tab → close any open detail page and
          // re-fetch with the right collections_only flag.
          this.browser.detailOpen = false;
          this.browser.offset = 0;
          if (!this.browser.loaded && !this.browser.loading) {
            this.browserOpen();
          } else if (prev !== next) {
            this.browserFetch();
            this._refreshInstalledIds();
          } else {
            this._refreshInstalledIds();
          }
        }
        if (next === 'log') {
          this.refreshLog();
          this._stopLogPolling();
          this._logTimer = setInterval(() => this.refreshLog(), 2000);
        }
        if (prev === 'log' && next !== 'log') {
          this._stopLogPolling();
        }
        // News had a fire-and-forget setInterval that never got cleared —
        // it kept polling /news every 5 minutes for the lifetime of the
        // window. Stop it as soon as the user leaves the tab.
        if (prev === 'news' && next !== 'news') {
          this._stopNewsPolling();
        }
      });

    },

    async refreshNews(force) {
      this.news = { ...this.news, loading: true, error: '' };
      try {
        const res = await window.pywebview.api.fetch_news(!!force);
        if (res && res.ok) {
          // Preserve detail+cache across reloads — they're orthogonal to the
          // list itself, and wiping them would close an open detail page on
          // every background poll.
          this.news = {
            ...this.news,
            items: res.items || [],
            cached: !!res.cached,
            loading: false,
            loaded: true,
            error: '',
          };
        } else {
          this.news = { ...this.news, loading: false, loaded: true,
                        error: (res && res.error) || 'fetch failed' };
        }
      } catch (e) {
        console.error('fetch_news threw:', e);
        this.news = { ...this.news, loading: false, loaded: true, error: String(e) };
      }
      // First time we fetch, kick off a 5-minute background poll so the
      // feed stays fresh even when the user is on another tab. Subsequent
      // fetches reuse the same timer (TTL on the Python cache prevents
      // hammering when force=false).
      if (!this._newsTimer) {
        this._newsTimer = setInterval(() => this.refreshNews(true), 5 * 60 * 1000);
      }
    },

    /** Open the in-app reader for an Anno Union post. Reddit and mod.io
     *  cards keep their existing behaviour (external link / deep-link) —
     *  only Anno Union cards get the embedded reader. Lazy-fetches the
     *  full HTML on first click and caches by wp_id so re-opening the
     *  same post is instant. */
    async openNewsDetail(item) {
      if (!item) return;
      if (item.source !== 'anno_union' || !item.wp_id) {
        // Non-WP sources keep the legacy external-link flow.
        this.openExternalUrl(item.url || '');
        return;
      }
      // Cache stores both the sanitised HTML and the full-resolution hero
      // URL — the list cold-fetch only carries `medium` thumbnails (cheap
      // for cards), and we need the `source_url` from the lazy fetch so
      // the in-app reader's hero isn't upscaled and pixelated.
      const cached = this.news.cache[item.wp_id];
      const seedItem = (cached && cached.imgUrl)
        ? { ...item, img_url: cached.imgUrl }
        : item;
      this.news.detail = {
        open: true, item: seedItem,
        html: (cached && cached.html) || '',
        loading: !cached,
        error: '',
      };
      if (cached) return;
      try {
        const res = await window.pywebview.api.fetch_anno_union_post(item.wp_id);
        if (res && res.ok) {
          this.news.cache = {
            ...this.news.cache,
            [item.wp_id]: { html: res.content_html || '', imgUrl: res.img_url || '' },
          };
          const mergedItem = res.img_url
            ? { ...this.news.detail.item, img_url: res.img_url }
            : this.news.detail.item;
          this.news.detail = { ...this.news.detail,
                                item: mergedItem,
                                html: res.content_html || '',
                                loading: false, error: '' };
        } else {
          this.news.detail = { ...this.news.detail, loading: false,
                                error: (res && res.error) || 'fetch failed' };
        }
      } catch (e) {
        this.news.detail = { ...this.news.detail, loading: false, error: String(e) };
      }
    },
    closeNewsDetail() {
      this.news.detail = { open: false, item: null, html: '', loading: false, error: '' };
    },

    /** Delegate clicks inside the in-app reader's article to openExternalUrl
     *  whenever the user hits a link — without this, WebKit2GTK navigates
     *  the webview itself, which (a) breaks the back button, (b) glitches
     *  on raw .mp4 URLs (the video-link substitute we inject for native
     *  WP uploads). Walks up to the closest <a>; ignores plain text. */
    onArticleClick(evt) {
      const a = evt.target.closest && evt.target.closest('a');
      if (!a) return;
      const href = a.getAttribute('href') || '';
      if (!/^https?:\/\//i.test(href)) return;
      evt.preventDefault();
      this.openExternalUrl(href);
    },

    _stopLogPolling() {
      if (this._logTimer) {
        clearInterval(this._logTimer);
        this._logTimer = null;
      }
    },

    _stopNewsPolling() {
      if (this._newsTimer) {
        clearInterval(this._newsTimer);
        this._newsTimer = null;
      }
    },

    async refreshLog() {
      try {
        const res = await window.pywebview.api.read_modloader_log();
        this.log = {
          content: (res && res.content) || '',
          path:    (res && res.path) || '',
          exists:  !!(res && res.exists),
          truncated: !!(res && res.truncated),
          loaded:  true,
        };
      } catch (e) {
        console.error('read_modloader_log failed:', e);
        this.log = { content: '', path: '', exists: false, truncated: false, loaded: true };
      }
    },

    async copyLogToClipboard() {
      try {
        await navigator.clipboard.writeText(this.log.content || '');
      } catch (e) {
        // Older webkit2gtk fallback — drop into a textarea + execCommand.
        const ta = document.createElement('textarea');
        ta.value = this.log.content || '';
        document.body.appendChild(ta);
        ta.select();
        try { document.execCommand('copy'); } catch (_) {}
        document.body.removeChild(ta);
      }
    },

    get currentLanguage() {
      return this.languages.find((l) => l.key === this.currentLang) || null;
    },

    /** Localised string lookup. Falls back to English if the active language
     *  doesn't have the key, and finally to the key itself so missing
     *  translations surface visibly. ``vars`` interpolates {placeholder}
     *  tokens. */
    t(key, vars) {
      const en = TRANSLATIONS.english[key];
      const localized = (TRANSLATIONS[this.currentLang] && TRANSLATIONS[this.currentLang][key]) || en || key;
      if (!vars) return localized;
      return localized.replace(/\{(\w+)\}/g, (_, name) =>
        (vars[name] !== undefined ? String(vars[name]) : `{${name}}`));
    },

    async selectLanguage(key) {
      this.langOpen = false;
      if (key === this.currentLang) return;
      this.currentLang = key;
      try {
        const res = await window.pywebview.api.set_language(key);
        if (!res || !res.ok) {
          console.error('set_language failed:', res && res.error);
        }
      } catch (e) {
        console.error('set_language threw:', e);
      }
    },

    // ── Settings ────────────────────────────────────────────────────────────
    async refreshSettings() {
      try {
        this.settings = (await window.pywebview.api.get_settings()) || {};
        this.pathsInfo = (await window.pywebview.api.get_paths_info()) || {};
        this.modioStatus = (await window.pywebview.api.modio_status()) || this.modioStatus;
      } catch (e) {
        console.error('refresh settings failed:', e);
      }
    },

    // ── mod.io OAuth ───────────────────────────────────────────────────────

    modioStartConnect() {
      this.modioAuth = { step: 'email', email: '', code: '',
                         termsAgreed: this.modioStatus.terms_agreed || true,
                         error: '', busy: false };
    },

    modioCancelConnect() {
      this.modioAuth = { ...this.modioAuth, step: 'idle', error: '', busy: false };
    },

    async modioSubmitEmail() {
      // Read straight from the DOM — we deliberately don't bind oninput on the
      // text field, because each keystroke would trigger an x-html re-render
      // and destroy the focused input, kicking the user out mid-typing.
      const input = document.getElementById('modio-email-input');
      const email = ((input && input.value) || '').trim();
      this.modioAuth = { ...this.modioAuth, email };
      if (!email) { this.modioAuth.error = this.t('modio.emailRequired'); return; }
      this.modioAuth = { ...this.modioAuth, busy: true, error: '' };
      try {
        const res = await window.pywebview.api.modio_email_request(email);
        if (res && res.ok) {
          this.modioAuth = { ...this.modioAuth, step: 'code', busy: false };
        } else {
          this.modioAuth = { ...this.modioAuth, busy: false,
                             error: (res && res.error) || 'request failed' };
        }
      } catch (e) {
        this.modioAuth = { ...this.modioAuth, busy: false, error: String(e) };
      }
    },

    async modioSubmitCode() {
      const input = document.getElementById('modio-code-input');
      const code = ((input && input.value) || '').trim().toUpperCase();
      this.modioAuth = { ...this.modioAuth, code };
      if (!code) { this.modioAuth.error = this.t('modio.codeRequired'); return; }
      this.modioAuth = { ...this.modioAuth, busy: true, error: '' };
      try {
        const res = await window.pywebview.api.modio_email_exchange(
          code, !!this.modioAuth.termsAgreed);
        if (res && res.ok) {
          this.modioAuth = { step: 'idle', email: '', code: '',
                             termsAgreed: true, error: '', busy: false };
          await this.refreshSettings();
        } else {
          this.modioAuth = { ...this.modioAuth, busy: false,
                             error: (res && res.error) || 'exchange failed' };
        }
      } catch (e) {
        this.modioAuth = { ...this.modioAuth, busy: false, error: String(e) };
      }
    },

    async modioDisconnect() {
      if (!await this.confirmDialog(this.t('modio.disconnectConfirm'))) return;
      try {
        await window.pywebview.api.modio_disconnect();
        await this.refreshSettings();
      } catch (e) {
        console.error('modio_disconnect threw:', e);
      }
    },

    // ── Mod Browser ────────────────────────────────────────────────────────
    /** First open of the Browser tab — refresh subscribed list (small,
     *  one-shot) then trigger the initial mod listing. Subsequent opens
     *  reuse the existing list (browserRefresh forces a re-fetch). */
    async browserOpen() {
      // Folders of locally installed mods (kept for the legacy heuristic
      // in browserIsInstalled — the authoritative source is the persisted
      // mod.io ID list below).
      this.browser.installedFolders = {};
      try {
        for (const m of (this.mods || [])) {
          if (m.folder) this.browser.installedFolders[m.folder] = true;
        }
      } catch (_) {}
      // Hydrate "already installed" state from the marker files so the
      // ✓ Installé / Mettre à jour badge survives across launches. Goes
      // through _refreshInstalledIds so installedMeta (modfile_id, folder)
      // also gets populated — without it, browserHasUpdate falls back to
      // "always show update" and the CTA flickers from "Update" on first
      // open to "Installed" after the first refresh.
      await this._refreshInstalledIds();
      // Subscribed list — best-effort.
      await this._refreshSubscribed();
      // Followed collections list — drives the ★/☆ on collection cards
      // and the "Mes follows" filter.
      this._refreshFollowedCollections();  // fire-and-forget
      // Endorsements the user has already cast — needed to render the
      // gold heart on previously-endorsed mods (the list endpoint doesn't
      // carry user_rating, only /me/ratings does).
      try {
        const res = await window.pywebview.api.modio_my_ratings();
        if (res && res.ok) {
          const map = {};
          for (const r of (res.data || [])) {
            if (Number(r.rating) > 0 && r.mod_id) map[r.mod_id] = true;
          }
          this.browser.endorsed = map;
        }
      } catch (_) {}
      // Tag taxonomy for the filter dropdown — one-shot, doesn't change.
      try {
        const res = await window.pywebview.api.modio_tags();
        if (res && res.ok) this.browser.tagsCatalog = res.data || [];
      } catch (_) {}
      await this.browserFetch();
    },

    async browserRefresh() {
      this.browser.offset = 0;
      await this.browserFetch();
    },

    browserSetSort(sort) {
      if (this.browser.sort === sort) return;
      this.browser.sort = sort;
      this.browser.offset = 0;
      this.browserFetch();
    },

    browserSetTag(tag) {
      const next = tag || '';
      if (this.browser.tagFilter === next) return;
      this.browser.tagFilter = next;
      this.browser.offset = 0;
      this.browserFetch();
    },

    /** Click an author name → restrict the listing to that submitter.
     *  Closes the detail page if open so the user lands directly on the
     *  filtered grid. Pass id=0 to clear the filter. */
    browserSetAuthor(userId, displayName) {
      const id = Number(userId) || 0;
      this.browser.authorFilter = id
        ? { id, name: String(displayName || '') }
        : { id: 0, name: '' };
      this.browser.offset = 0;
      this.browser.detailOpen = false;
      this.browserFetch();
    },

    browserClearAuthor() { this.browserSetAuthor(0, ''); },

    /** Toggle the "My Subscriptions" filter on the Browser tab. Resets
     *  pagination and re-fetches; the swap to /me/subscribed happens in
     *  browserFetch based on this flag. The choice is persisted to
     *  settings.json so a restart preserves the filter — the user
     *  explicitly opted in and shouldn't have to re-tick on every launch. */
    browserToggleSubscribed() {
      this.browser.subscribedOnly = !this.browser.subscribedOnly;
      this.browser.offset = 0;
      // Fire-and-forget; failure to persist is non-fatal (next session just
      // starts with the default again).
      try {
        window.pywebview.api.update_setting(
          'browser_subscribed_only', this.browser.subscribedOnly);
      } catch (_) {}
      this.browserFetch();
    },

    browserPrev() {
      if (this.browser.offset <= 0) return;
      this.browser.offset = Math.max(0, this.browser.offset - this.browser.limit);
      this.browserFetch();
    },

    browserNext() {
      const next = this.browser.offset + this.browser.limit;
      if (next >= this.browser.total) return;
      this.browser.offset = next;
      this.browserFetch();
    },

    async browserFetch() {
      this.browser.loading = true;
      this.browser.error = '';
      this.browser.notAuth = false;
      try {
        const isCollections = this.currentTab === 'collections';
        // Each tab has its own filter that swaps the endpoint:
        //   Browser     + subscribedOnly → /me/subscribed
        //   Collections + followedOnly   → /me/following/collections
        // Filters are mutually exclusive across tabs (each tab only honours
        // its own flag), and the cross-tab one is ignored to avoid a stale
        // toggle from one view leaking into the other.
        const subOnly = !isCollections && this.browser.subscribedOnly;
        const followOnly = isCollections && this.browser.followedOnly;
        const res = followOnly
          ? await window.pywebview.api.modio_followed_collections(
              this.browser.search,
              this.browser.limit,
              this.browser.offset,
              this.browser.sort,
            )
          : subOnly
          ? await window.pywebview.api.modio_subscribed(
              this.browser.search,
              this.browser.limit,
              this.browser.offset,
              this.browser.sort,
            )
          : await window.pywebview.api.modio_browse(
              this.browser.search,
              // Tags only apply to the mods taxonomy — drop them on Collections
              // so a stale Browser tag doesn't filter the collection listing
              // down to nothing.
              (!isCollections && this.browser.tagFilter) ? [this.browser.tagFilter] : null,
              this.browser.limit,
              this.browser.offset,
              this.browser.sort,
              this.browser.authorFilter.id || 0,
              isCollections,
            );
        if (res && res.ok) {
          this.browser.items = res.data || [];
          this.browser.total = res.result_total || 0;
          this.browser.loaded = true;
          this.browser.loading = false;
          // Seed endorsed from per-mod user_rating when the API exposes it
          // (the endpoint usually doesn't, so /me/ratings on browserOpen is
          // the authoritative source — this is just a free top-up).
          const endorsed = { ...this.browser.endorsed };
          for (const m of this.browser.items) {
            if (m && Number(m.user_rating) > 0) endorsed[m.id] = true;
          }
          this.browser.endorsed = endorsed;
          // Re-read the installed marker files from disk on every fetch so
          // a manual rm -rf or an Uninstall through the Activation tab
          // mid-session is reflected without having to leave + re-enter
          // the Browser tab.
          try {
            const r = await window.pywebview.api.modio_installed_ids();
            if (r && r.ok) {
              const map = {};
              for (const id of (r.ids || [])) map[id] = true;
              this.browser.installedIds = map;
            }
          } catch (_) {}
        } else {
          const err = (res && res.error) || 'fetch failed';
          this.browser.loading = false;
          this.browser.loaded = true;
          if (/not authenticated/i.test(err)) {
            this.browser.notAuth = true;
          } else {
            this.browser.error = err;
          }
        }
      } catch (e) {
        this.browser.loading = false;
        this.browser.loaded = true;
        this.browser.error = String(e);
      }
    },

    /** Open the full-width detail view for ``modId``. ``isCollection``
     *  defaults to whatever the active tab dictates so card clicks "just
     *  work" — pass it explicitly when navigating into a mod from inside
     *  a collection's bundled list (where the source tab is Collections
     *  but the target is a regular mod). */
    async browserSelect(modId, isCollection) {
      if (!modId) return;
      const asCollection = (isCollection === undefined)
        ? (this.currentTab === 'collections')
        : !!isCollection;
      this.browser.selectedId = modId;
      this.browser.detailOpen = true;
      this.browser.dependencies = [];
      // The summary stub from the grid lights up the panel instantly
      // (the get_mod fetch can take a beat). Bundled-mod clicks have no
      // matching item in the current grid, so the stub will be undefined
      // and the panel just shows blank for that brief window — fine.
      const stub = this.browser.items.find((m) => m.id === modId);
      this.browser.detail = stub ? { ...stub } : null;
      this.browser.detailLoading = true;
      try {
        const res = await window.pywebview.api.modio_get(modId, asCollection);
        if (res && res.ok) this.browser.detail = res.mod || stub || null;
      } catch (e) {
        console.error('modio_get threw:', e);
      } finally {
        this.browser.detailLoading = false;
      }
      if (asCollection) {
        this.browser.dependenciesLoading = true;
        try {
          const dr = await window.pywebview.api.modio_dependencies(modId, true);
          if (dr && dr.ok) this.browser.dependencies = dr.data || [];
        } catch (e) {
          console.error('modio_dependencies threw:', e);
        } finally {
          this.browser.dependenciesLoading = false;
        }
      }
    },

    /** Drill into one of a collection's bundled mods. Stash the current
     *  detail (the collection) so the back button can come back to it
     *  instead of falling all the way back to the grid. */
    async browserOpenChildMod(modId) {
      if (!modId) return;
      // Snapshot the collection so we can restore it on back.
      this.browser.parent = {
        detail: this.browser.detail,
        dependencies: this.browser.dependencies,
        isCollection: true,
      };
      await this.browserSelect(modId, false);
    },

    /** Back button. If we drilled into a child mod from a collection,
     *  pop back to the collection instead of dropping all the way to
     *  the grid (one-level breadcrumb). */
    browserBack() {
      if (this.browser.parent) {
        const p = this.browser.parent;
        this.browser.detail = p.detail;
        this.browser.dependencies = p.dependencies || [];
        this.browser.selectedId = p.detail ? p.detail.id : null;
        this.browser.parent = null;
        return;
      }
      this.browser.detailOpen = false;
    },

    async browserToggleSubscribe(modId) {
      if (!modId || this.browser.subBusy[modId]) return;
      this.browser.subBusy = { ...this.browser.subBusy, [modId]: true };
      const wasSubscribed = !!this.browser.subscribed[modId];
      try {
        const res = wasSubscribed
          ? await window.pywebview.api.modio_unsubscribe(modId)
          : await window.pywebview.api.modio_subscribe(modId);
        if (res && res.ok) {
          const next = { ...this.browser.subscribed };
          if (wasSubscribed) delete next[modId]; else next[modId] = true;
          this.browser.subscribed = next;
          // When the "My Subscriptions" filter is on, the list itself comes
          // from /me/subscribed — unsubscribing means the row no longer
          // belongs there. Drop it locally instead of waiting for the next
          // browserFetch (or a tab switch) to re-query.
          if (wasSubscribed && this.browser.subscribedOnly &&
              this.currentTab === 'browser') {
            this.browser.items = this.browser.items.filter((m) => m.id !== modId);
            this.browser.total = Math.max(0, (this.browser.total || 0) - 1);
          }
        } else {
          this._browserFlash(this.t('browser.subFail',
            { error: (res && res.error) || 'unknown' }), true);
        }
      } catch (e) {
        this._browserFlash(this.t('browser.subFail', { error: String(e) }), true);
      } finally {
        const next = { ...this.browser.subBusy };
        delete next[modId];
        this.browser.subBusy = next;
      }
    },

    async browserEndorse(modId) {
      if (!modId || this.browser.endorseBusy[modId]) return;
      this.browser.endorseBusy = { ...this.browser.endorseBusy, [modId]: true };
      try {
        const res = await window.pywebview.api.modio_endorse(modId, true);
        if (res && res.ok) {
          this.browser.endorsed = { ...this.browser.endorsed, [modId]: true };
        } else {
          this._browserFlash(this.t('browser.endorseFail',
            { error: (res && res.error) || 'unknown' }), true);
        }
      } catch (e) {
        this._browserFlash(this.t('browser.endorseFail', { error: String(e) }), true);
      } finally {
        const next = { ...this.browser.endorseBusy };
        delete next[modId];
        this.browser.endorseBusy = next;
      }
    },

    /** Click on a mod.io news card → switch to the right tab (Browser for
     *  mods, Collections for collections), make sure the listing is loaded,
     *  then open the detail page directly. Falls back to opening the mod.io
     *  URL externally if anything goes wrong. */
    async openModioFromNews(modioId, kind) {
      if (!modioId) return;
      const targetTab = (kind === 'collection') ? 'collections' : 'browser';
      // Need a valid mod.io session — if not, route through selectTab so the
      // user lands on Settings with the gold flash on the mod.io card.
      if (!(this.modioStatus && this.modioStatus.token_valid)) {
        this.selectTab(targetTab, false);
        return;
      }
      // If we're not already on the right tab, switch (this triggers
      // browserOpen on first visit through the watcher).
      if (this.currentTab !== targetTab) {
        this.currentTab = targetTab;
      }
      // Wait for the listing to be in flight before drilling in — gives
      // selectTab/browserOpen a tick to populate the items array so the
      // stub render works.
      await this.$nextTick();
      // Clear any active filters that might hide this exact mod, then open
      // the detail page directly. browserSelect uses currentTab to decide
      // mod-vs-collection, which we just set above.
      this.browser.search = '';
      this.browser.tagFilter = '';
      this.browser.authorFilter = { id: 0, name: '' };
      this.browser.parent = null;
      await this.browserSelect(modioId, kind === 'collection');
    },

    /** Drop the preset created by an install_collection, optionally also
     *  wiping every mod folder bundled in the collection. Two confirms
     *  so the user can drop the profile alone or take the mods with it. */
    async browserUninstallCollection(collectionId) {
      const detail = this.browser.detail;
      const name = (detail && detail.name) || `collection ${collectionId}`;
      const presetName = this._collectionPresetName(name, collectionId);
      // total = bundled mods we currently know about (live load is server-side)
      const total = (this.browser.dependencies || []).length;
      if (!await this.confirmDialog(this.t('browser.uninstallConfirm',
            { name, profile: presetName }))) return;
      const alsoMods = total > 0 && await this.confirmDialog(this.t('browser.uninstallAlsoMods',
            { count: total }));
      try {
        const res = await window.pywebview.api.modio_uninstall_collection(
          collectionId, alsoMods);
        if (res && res.ok) {
          const removed = (res.mods_removed || []).length;
          const msg = alsoMods
            ? this.t('browser.uninstallOkWithMods',
                { profile: res.profile_name || presetName, count: removed })
            : this.t('browser.uninstallOk',
                { profile: res.profile_name || presetName });
          this._browserFlash(msg, false);
          // If the deleted preset was the active one, switch to Default —
          // and apply it so active-profile.txt actually reflects Default
          // (otherwise the file still points at the gone preset).
          if (this.profileName === (res.profile_name || presetName)) {
            await this.switchProfile('Default');
          } else {
            await this.refreshMods();
          }
          await this._refreshInstalledIds();
        } else {
          this._browserFlash(this.t('browser.uninstallFail',
            { error: (res && res.error) || 'unknown' }), true);
        }
      } catch (e) {
        this._browserFlash(this.t('browser.uninstallFail',
          { error: String(e) }), true);
      }
    },

    async browserInstall(modId) {
      if (!modId || this.browser.installing[modId]) return;
      const detail = this.browser.detail;
      const name = (detail && detail.name) || `mod ${modId}`;
      // On the Collections tab, the install action covers every bundled
      // mod and creates a dedicated profile — handled by a separate
      // backend method below.
      const isCollection = (this.currentTab === 'collections') && !this.browser.parent;
      this.browser.installing = { ...this.browser.installing, [modId]: true };
      try {
        const res = isCollection
          ? await window.pywebview.api.modio_install_collection(modId)
          : await window.pywebview.api.modio_install_mod(modId);
        if (res && res.ok) {
          if (isCollection) {
            const okCount = res.installed || 0;
            const total = res.total || okCount;
            const failCount = (res.failed || []).length;
            const profileName = res.profile_name || name;
            const okMsg = this.t('browser.collectionInstallOk',
              { name, count: okCount, total, profile: profileName });
            const failMsg = failCount
              ? ' ' + this.t('browser.collectionInstallFailures', { count: failCount })
              : '';
            this._browserFlash(okMsg + failMsg, failCount > 0);
            // The backend already activated this preset on disk — mirror that
            // in the UI state and persist so a relaunch lands on it too.
            this.profileName = profileName;
            try { await window.pywebview.api.update_setting('active_profile_name', profileName); }
            catch (_) {}
            // Refresh active mods + presets so the Activation tab shows the
            // freshly-created profile selected.
            this.refreshMods();
          } else {
            if (res.folder) {
              this.browser.installedFolders = {
                ...this.browser.installedFolders, [res.folder]: true };
            }
            this.browser.installedIds = {
              ...this.browser.installedIds, [modId]: true };
            this._browserFlash(this.t('browser.installOk', { name }), false);
            this.refreshMods();
          }
          // Either way, refresh the persisted markers so the ✓ Installé
          // badge flips on every newly-installed card. Subscribed cache
          // also gets a refresh because the backend auto-subscribes on
          // install (api.py:modio_install_mod) and the badge / My
          // Subscriptions filter both read from this.browser.subscribed.
          // Chain: wait for markers before checking version updates so
          // _refreshModUpdates sees the new mod in installedMeta.
          this._refreshInstalledIds().then(() => this._refreshModUpdates());
          this._refreshSubscribed();
        } else {
          this._browserFlash(this.t('browser.installFail',
            { error: (res && res.error) || 'unknown' }), true);
        }
      } catch (e) {
        this._browserFlash(this.t('browser.installFail', { error: String(e) }), true);
      } finally {
        const next = { ...this.browser.installing };
        delete next[modId];
        this.browser.installing = next;
      }
    },

    /** Uninstall a mod previously installed through the Browser. The folder
     *  to delete comes from installedMeta (written by modio_installed_ids
     *  on every refresh) so we don't need a backend round-trip to look it
     *  up. Subscribe state is left alone — uninstalling locally shouldn't
     *  silently unsubscribe the user; they can do that explicitly via the
     *  ✓ button on the card if they want. */
    async browserUninstall(modId) {
      if (!modId) return;
      const meta = this.browser.installedMeta[modId];
      const folder = meta && meta.folder;
      if (!folder) {
        this._browserFlash(this.t('browser.installFail',
          { error: 'no folder marker' }), true);
        return;
      }
      const detail = this.browser.detail;
      const card = (this.browser.items || []).find((m) => m.id === modId);
      const name = (detail && detail.id === modId && detail.name)
                   || (card && card.name) || `mod ${modId}`;
      if (!await this.confirmDialog(this.t('browser.uninstallModConfirm', { name }))) return;
      try {
        const res = await window.pywebview.api.uninstall_mod(folder);
        if (res && res.ok) {
          this._browserFlash(this.t('browser.uninstallModOk', { name }), false);
          // Drop the local "installed" markers immediately so the CTA flips
          // back to "Install" without waiting for the next refresh.
          const ids = { ...this.browser.installedIds }; delete ids[modId];
          const m   = { ...this.browser.installedMeta }; delete m[modId];
          const fld = { ...this.browser.installedFolders }; delete fld[folder];
          this.browser.installedIds = ids;
          this.browser.installedMeta = m;
          this.browser.installedFolders = fld;
          // Refresh the Activation list (the mod just disappeared from disk).
          this.refreshMods();
          // Re-read markers from disk too — covers the case where the user
          // had multiple folders pointing at the same mod_id (rare but
          // possible after a manual copy).
          this._refreshInstalledIds();
        } else {
          this._browserFlash(this.t('browser.installFail',
            { error: (res && res.error) || 'unknown' }), true);
        }
      } catch (e) {
        this._browserFlash(this.t('browser.installFail', { error: String(e) }), true);
      }
    },

    /** Authoritative for regular mods: did the user install this mod through
     *  the manager? Backed by the persisted _modio_install.json markers
     *  scanned at every browserFetch.
     *
     *  For collections we have no per-mod marker — instead we check whether
     *  the preset that modio_install_collection would create already exists
     *  (this.presets is the live preset list refreshed by refreshMods). */
    browserIsInstalled(mod) {
      if (!mod) return false;
      if (this.currentTab === 'collections') {
        const presetName = this._collectionPresetName(mod.name, mod.id);
        return Array.isArray(this.presets) && this.presets.includes(presetName);
      }
      return !!this.browser.installedIds[mod.id];
    },

    /** Mirror of the backend safe-name logic in modio_install_collection.
     *  Keep the two in sync — used only to render the "already installed"
     *  state on the collection card / detail. */
    _collectionPresetName(name, id) {
      let safe = String(name || '').replace(/[^A-Za-z0-9 _\-]/g, '_').trim().slice(0, 50);
      if (!safe || safe === 'Default' || safe === 'Vanilla') {
        safe = `Collection_${Number(id) || 0}`;
      }
      return safe;
    },

    /** Tab click handler. Onglets gated by mod.io auth (browser, collections)
     *  redirect to Settings when no valid token, scrolling straight to the
     *  mod.io card so the user knows what to fix — instead of showing an
     *  empty Browser with a small "go connect" message. */
    selectTab(tabId, isDisabled) {
      if (isDisabled) return;
      const needsModio = (tabId === 'browser' || tabId === 'collections');
      if (needsModio && !(this.modioStatus && this.modioStatus.token_valid)) {
        this.currentTab = 'settings';
        // Wait for the Settings template to render, then jump to the mod.io card.
        // Two nextTicks: one for the x-html re-render, another for layout pass.
        this.$nextTick(() => this.$nextTick(() => {
          const el = document.getElementById('settings-modio-card');
          if (el) {
            el.scrollIntoView({ behavior: 'smooth', block: 'start' });
            // Brief gold pulse so the eye lands on the right card
            el.classList.add('is-flash');
            setTimeout(() => el.classList.remove('is-flash'), 1600);
          }
        }));
        return;
      }
      this.currentTab = tabId;
    },

    _browserFlash(msg, isError) {
      this.browser.flash = msg;
      this.browser.flashError = !!isError;
      clearTimeout(this._browserFlashTimer);
      this._browserFlashTimer = setTimeout(() => {
        this.browser.flash = '';
        this.browser.flashError = false;
      }, 6000);
    },

    async setSetting(key, value) {
      try {
        const res = await window.pywebview.api.update_setting(key, value);
        if (!res || !res.ok) {
          console.error('update_setting failed:', res && res.error);
          return;
        }
        this.settings[key] = value;
      } catch (e) {
        console.error('update_setting threw:', e);
      }
    },

    /** Reading text size — only affects long-prose containers (news
     *  reader, mod descriptions). UI controls (HUD, cards, buttons)
     *  stay at fixed sizes so layouts don't shift. Driven by a body
     *  class that flips a CSS variable used inside those containers. */
    applyTextScale(value) {
      const v = (value === 'medium' || value === 'large') ? value : 'small';
      document.body.classList.remove(
        'text-scale-small', 'text-scale-medium', 'text-scale-large');
      document.body.classList.add('text-scale-' + v);
    },
    /** Drop-in replacement for window.confirm() that uses the in-app
     *  modal instead of the browser-native dialog (which doesn't follow
     *  the annolayouts theme on WebKit2GTK / WebView2). Returns a promise
     *  resolved with `true` on confirm, `false` on cancel/escape/backdrop. */
    confirmDialog(message) {
      return new Promise((resolve) => {
        this.confirmModal = { open: true, message: String(message || ''), resolve };
      });
    },
    _confirmModalAnswer(value) {
      const r = this.confirmModal.resolve;
      this.confirmModal = { open: false, message: '', resolve: null };
      if (r) r(!!value);
    },

    /** Inline loader markup (wreath + logo + breath/fill animation).
     *  Used in place of plain "Chargement…" text on the long-fetch states
     *  (News list, News detail, Browser list). The label sits below the
     *  wreath in small caps gold so it still reads as the original copy. */
    renderLoader(label) {
      return `
        <div class="loader">
          <div class="loader__stage">
            <div class="loader__wreath">
              <img class="loader__wreath-base"  src="icons/loader/wreath.svg" alt="" />
              <img class="loader__wreath-light" src="icons/loader/wreath.svg" alt="" />
            </div>
            <img class="loader__logo" src="icons/loader/logo.png" alt="" />
          </div>
          ${label ? `<div class="loader__label">${escapeHtml(label)}</div>` : ''}
        </div>`;
    },

    async setTextScale(value) {
      this.applyTextScale(value);
      await this.setSetting('text_scale', value);
    },

    async pickGamePath(asFile) {
      try {
        const path = asFile
          ? await window.pywebview.api.pick_file('Sélectionner Anno117.exe',
              ['Anno executable (Anno117.exe;*.exe)'])
          : await window.pywebview.api.pick_folder('Sélectionner le dossier d\'installation');
        if (!path) return;
        const res = await window.pywebview.api.set_game_path(path);
        if (!res || !res.ok) {
          alert(this.t('settings.pathError', { err: (res && res.error) || '?' }));
          return;
        }
        await this.refreshSettings();
        await this.refreshMods();
      } catch (e) {
        console.error('pickGamePath threw:', e);
      }
    },

    async detectGamePath() {
      try {
        const res = await window.pywebview.api.detect_game_path();
        if (!res || !res.ok) {
          alert(this.t('settings.detectError', { err: (res && res.error) || '?' }));
          return;
        }
        await this.refreshSettings();
        await this.refreshMods();
      } catch (e) {
        console.error('detect_game_path threw:', e);
      }
    },

    async pickDocsPath() {
      try {
        const path = await window.pywebview.api.pick_folder('Sélectionner le dossier Documents');
        if (!path) return;
        const res = await window.pywebview.api.set_custom_docs_path(path);
        if (!res || !res.ok) {
          alert(this.t('settings.pathError', { err: (res && res.error) || '?' }));
          return;
        }
        await this.refreshSettings();
        await this.refreshMods();
      } catch (e) {
        console.error('pickDocsPath threw:', e);
      }
    },

    async clearDocsPath() {
      try {
        await window.pywebview.api.set_custom_docs_path('');
        await this.refreshSettings();
        await this.refreshMods();
      } catch (e) {
        console.error('clearDocsPath threw:', e);
      }
    },

    async saveModioKey(value) {
      const trimmed = (value || '').trim();
      if (!trimmed) {
        alert(this.t('settings.modio.emptyKey'));
        return;
      }
      await this.setSetting('modio_api_key', trimmed);
      await this.refreshSettings();
    },

    async clearModioKey() {
      if (!await this.confirmDialog(this.t('settings.modio.disconnectConfirm'))) return;
      await this.setSetting('modio_api_key', '');
      await this.refreshSettings();
    },

    // ── Manual install ──────────────────────────────────────────────────────
    async pickAndInstall() {
      try {
        const path = await window.pywebview.api.pick_file(
          'Sélectionner le fichier ZIP du mod',
          ['ZIP archive (*.zip)']);
        if (!path) return;
        const display = path.split(/[\\/]/).pop();
        await this._performInstall(
          (allow) => window.pywebview.api.install_zip_from_path(path, allow),
          display);
      } catch (e) {
        console.error('pickAndInstall threw:', e);
      }
    },

    onZipDragEnter(ev) {
      ev.preventDefault();
      this._dragDepth += 1;
      this.install.dragOver = true;
      console.log('[install] dragenter, depth=', this._dragDepth,
                  'types=', ev.dataTransfer && Array.from(ev.dataTransfer.types || []));
    },

    onZipDragOver(ev) {
      ev.preventDefault();
      // dropEffect must be set on every dragover for the cursor to show "+"
      if (ev.dataTransfer) ev.dataTransfer.dropEffect = 'copy';
    },

    onZipDragLeave(ev) {
      this._dragDepth = Math.max(0, this._dragDepth - 1);
      if (this._dragDepth === 0) this.install.dragOver = false;
    },

    onZipDrop(ev) {
      // The actual install happens in app.py via pywebview's DOM event
      // bridge (see _on_native_drop). Here we just reset the drag visual.
      // ev.preventDefault is enforced at document level by the Python handler.
      this._dragDepth = 0;
      this.install.dragOver = false;
    },

    /** Called from Python (via window.evaluate_js) when a native file drop
     *  is detected anywhere in the app. We switch to the Install tab so the
     *  status banner is visible, then mark the install as busy. */
    onNativeDropStart(name) {
      this.currentTab = 'install';
      this.install = { ...this.install, busy: true, error: false,
                       message: this.t('install.installing', { name }) };
    },

    /** Called from Python with the install result and the source ZIP path.
     *  Handles the overwrite-confirm round-trip back through the JS API. */
    async onNativeDropResult(res, path) {
      const display = (path || '').split(/[\\/]/).pop() || '';
      if (res && !res.ok && res.exists_already) {
        this.install.busy = false;
        if (!await this.confirmDialog(this.t('install.overwriteConfirm', { name: res.folder || display }))) {
          this._setInstallStatus(this.t('install.cancelled'), true);
          return;
        }
        this.install.busy = true;
        try {
          res = await window.pywebview.api.install_zip_from_path(path, true);
        } catch (e) {
          this._setInstallStatus(String(e), true);
          return;
        }
      }
      if (!res || !res.ok) {
        this._setInstallStatus((res && res.error) || 'unknown error', true);
        return;
      }
      this._setInstallStatus(this.t('install.success', { name: res.folder || display }), false);
      await this.refreshMods();
      this._autoLinkAndRefresh();
    },

    /** ``callFactory`` is invoked with a boolean ``allow_overwrite`` so we can
     *  retry the same operation cleanly when the user agrees to overwrite an
     *  existing mod folder. */
    async _performInstall(callFactory, displayName) {
      this.install = { ...this.install, busy: true, error: false,
                       message: this.t('install.installing', { name: displayName }) };
      try {
        let res = await callFactory(false);
        if (res && !res.ok && res.exists_already) {
          this.install.busy = false;
          if (!await this.confirmDialog(this.t('install.overwriteConfirm', { name: res.folder || displayName }))) {
            this._setInstallStatus(this.t('install.cancelled'), true);
            return;
          }
          this.install.busy = true;
          res = await callFactory(true);
        }
        if (!res || !res.ok) {
          this._setInstallStatus((res && res.error) || 'unknown error', true);
          return;
        }
        this._setInstallStatus(this.t('install.success', { name: res.folder || displayName }), false);
        await this.refreshMods();
        this._autoLinkAndRefresh();
      } catch (e) {
        this._setInstallStatus(String(e), true);
      } finally {
        this.install.busy = false;
      }
    },

    /** After any ZIP install: auto-link the new mod to mod.io (if its ModID
     *  slug matches), refresh the marker cache, then re-check for version
     *  updates so the warning badge appears without a full app restart. */
    async _autoLinkAndRefresh() {
      try {
        const r = await window.pywebview.api.modio_auto_link_unmarked();
        if (r && r.ok && r.linked > 0) await this._refreshInstalledIds();
      } catch (_) {}
      this._refreshModUpdates();
    },

    /** Open the dependency-issue dialog for mod m.
     *  Reads the pre-computed dep arrays from renderRow context, so callers
     *  pass the resolved data directly rather than re-computing it. */
    openDepDialog(modId, modName, type, items) {
      this.depDialog = { open: true, type, modId, modName, items };
    },
    closeDepDialog() {
      this.depDialog = { ...this.depDialog, open: false };
    },
    /** Enable a required-but-inactive dep, then close dialog. */
    async depDialogEnable(depId) {
      this.closeDepDialog();
      await this.toggleMod(depId, true);
    },
    /** Disable a conflicting mod, then close dialog. */
    async depDialogDisable(depId) {
      this.closeDepDialog();
      await this.toggleMod(depId, false);
    },
    /** Disable the mod that has the issue (deprecated case). */
    async depDialogDisableSelf() {
      const id = this.depDialog.modId;
      this.closeDepDialog();
      await this.toggleMod(id, false);
    },
    /** Install a missing dep directly by its name_id (mod.io slug). */
    async depDialogInstall(nameId) {
      this.depDialog.busyId = nameId;
      this.depDialog.error = '';
      try {
        const res = await window.pywebview.api.modio_install_by_name_id(nameId);
        if (res && res.ok) {
          this.closeDepDialog();
          await this.refreshMods();
          this._refreshInstalledIds().then(() => this._refreshModUpdates());
        } else {
          this.depDialog.error = (res && res.error) || 'unknown error';
        }
      } catch (e) {
        this.depDialog.error = String(e);
      } finally {
        this.depDialog.busyId = '';
      }
    },

    _setInstallStatus(message, isError) {
      this.install = { ...this.install, message, error: !!isError, busy: false };
    },

    _fileToBase64(file) {
      return new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.onload = () => {
          // dataURL prefix → "data:<mime>;base64,<payload>" — strip the head
          const s = String(reader.result || '');
          const comma = s.indexOf(',');
          resolve(comma === -1 ? s : s.slice(comma + 1));
        };
        reader.onerror = () => reject(reader.error || new Error('read failed'));
        reader.readAsDataURL(file);
      });
    },

    // ── Tweaking ────────────────────────────────────────────────────────────
    async refreshTweakable() {
      try {
        this.tweak.mods = await window.pywebview.api.list_tweakable_mods();
      } catch (e) {
        console.error('list_tweakable_mods failed:', e);
        this.tweak.mods = [];
      }
      // If nothing is selected and we have at least one mod, auto-select it
      if (!this.tweak.selectedId && this.tweak.mods.length) {
        await this.selectTweakMod(this.tweak.mods[0].id);
      } else if (this.tweak.selectedId) {
        // Refresh the schema/values for the currently selected mod
        await this.selectTweakMod(this.tweak.selectedId);
      }
    },

    async selectTweakMod(id) {
      this.tweak.selectedId = id;
      try {
        const res = await window.pywebview.api.get_mod_options(id);
        if (res && res.ok) {
          this.tweak.schema = res.schema || {};
          this.tweak.values = res.values || {};
        } else {
          this.tweak.schema = {};
          this.tweak.values = {};
        }
      } catch (e) {
        console.error('get_mod_options failed:', e);
      }
    },

    async setTweakOption(key, value) {
      const id = this.tweak.selectedId;
      if (!id) return;
      // Optimistic local update + brief saving indicator on the row
      this.tweak.values[key] = value;
      this.tweak.saving = key;
      try {
        await window.pywebview.api.set_mod_option(id, key, value);
      } catch (e) {
        console.error('set_mod_option failed:', e);
      } finally {
        // Clear the saving flag after a short tick so the visual cue is visible
        setTimeout(() => { if (this.tweak.saving === key) this.tweak.saving = ''; }, 300);
      }
    },

    // Bridge from a hex `#RRGGBB` back to the signed int ARGB string the mod
    // expects. Reads the current int value first to preserve its alpha, then
    // delegates to setTweakOption so the text field, optimistic update and
    // pywebview save go through the same path as a manual edit.
    async setTweakColorOption(key, hex) {
      const prev = this.tweak.values[key];
      const intStr = hexToArgbIntStr(hex, prev);
      if (intStr === null) return;
      const text = document.querySelector('input.tweak-color__text[data-key="' + key + '"]');
      if (text) text.value = intStr;
      await this.setTweakOption(key, intStr);
    },

    // ── In-app colour picker ──────────────────────────────────────────────
    // Open the popover anchored above the swatch that triggered it. Initial
    // HSV is derived from the current int value (alpha extracted and stored
    // separately so a later commit preserves it).
    openColorPicker(key, intStr, evt) {
      const cp = this.colorPicker;
      cp.key = key;
      const n = parseInt(intStr, 10);
      const u = Number.isFinite(n) ? (n >>> 0) : 0xFF000000;
      cp.alpha = (u >>> 24) & 0xFF;
      if (cp.alpha === 0) cp.alpha = 0xFF;
      const r = (u >> 16) & 0xFF, g = (u >> 8) & 0xFF, b = u & 0xFF;
      const [h, s, v] = rgbToHsv(r, g, b);
      cp.h = h; cp.s = s; cp.v = v;
      cp.prevHex = rgbToHex(r, g, b);
      // Anchor: prefer the swatch's bounding box; fall back to mouse coords.
      // Popover is 260×340-ish, position above-left of the swatch unless that
      // would clip off the viewport.
      const PANEL_W = 268, PANEL_H = 520;
      let ax = 0, ay = 0;
      if (evt && evt.currentTarget && evt.currentTarget.getBoundingClientRect) {
        const r2 = evt.currentTarget.getBoundingClientRect();
        ax = r2.left;
        ay = r2.top - PANEL_H - 8;
      } else if (evt) {
        ax = evt.clientX; ay = evt.clientY - PANEL_H - 8;
      }
      const vw = window.innerWidth, vh = window.innerHeight;
      cp.x = Math.max(8, Math.min(ax, vw - PANEL_W - 8));
      cp.y = Math.max(8, Math.min(ay, vh - PANEL_H - 8));
      cp.open = true;
    },
    closeColorPicker() {
      this.colorPicker.open = false;
      this.colorPicker.drag = null;
    },
    // Live hex/int previews used by the picker UI bindings.
    cpHex() {
      const [r, g, b] = hsvToRgb(this.colorPicker.h, this.colorPicker.s, this.colorPicker.v);
      return rgbToHex(r, g, b);
    },
    cpInt() {
      return hexToArgbIntStr(this.cpHex(), String(((this.colorPicker.alpha << 24) | 0) | 0));
    },
    // Background colour of the SV square = pure hue (s=1, v=1) so the WYSIWYG
    // gradients (white→hue, transparent→black) overlay cleanly on top.
    cpHueColor() {
      const [r, g, b] = hsvToRgb(this.colorPicker.h, 1, 1);
      return rgbToHex(r, g, b);
    },
    cpSetHex(hex) {
      const m = /^#?([0-9a-f]{6})$/i.exec((hex || '').trim());
      if (!m) return;
      const [r, g, b] = hexToRgb('#' + m[1]);
      const [h, s, v] = rgbToHsv(r, g, b);
      this.colorPicker.h = h; this.colorPicker.s = s; this.colorPicker.v = v;
    },
    cpSetInt(intStr) {
      const n = parseInt(intStr, 10);
      if (!Number.isFinite(n)) return;
      const u = n >>> 0;
      const a = (u >>> 24) & 0xFF;
      if (a !== 0) this.colorPicker.alpha = a;
      this.cpSetHex(argbIntToHex(intStr));
    },
    // Pointer-driven SV/hue manipulation. Single global handler attached on
    // mousedown and torn down on mouseup so we don't leak listeners or steal
    // pointer events from the rest of the app.
    cpStartDrag(target, evt) {
      this.colorPicker.drag = target;
      this.cpUpdateFromEvent(evt);
      const move = (e) => this.cpUpdateFromEvent(e);
      const up = () => {
        this.colorPicker.drag = null;
        document.removeEventListener('mousemove', move);
        document.removeEventListener('mouseup', up);
      };
      document.addEventListener('mousemove', move);
      document.addEventListener('mouseup', up);
      evt.preventDefault();
    },
    cpUpdateFromEvent(evt) {
      const drag = this.colorPicker.drag;
      if (!drag) return;
      const sel = drag === 'sv' ? '.color-picker__sv' : '.color-picker__hue';
      const el = document.querySelector(sel);
      if (!el) return;
      const r = el.getBoundingClientRect();
      const x = Math.max(0, Math.min(1, (evt.clientX - r.left) / r.width));
      const y = Math.max(0, Math.min(1, (evt.clientY - r.top) / r.height));
      if (drag === 'sv') {
        this.colorPicker.s = x;
        this.colorPicker.v = 1 - y;
      } else {
        this.colorPicker.h = y * 360;
      }
    },
    async commitColorPicker() {
      const key = this.colorPicker.key;
      const hex = this.cpHex();
      this.closeColorPicker();
      if (key) await this.setTweakColorOption(key, hex);
    },

    async resetTweakMod() {
      const id = this.tweak.selectedId;
      if (!id) return;
      if (!await this.confirmDialog(this.t('tweak.resetModConfirm'))) return;
      try {
        await window.pywebview.api.reset_mod_options(id);
        await this.selectTweakMod(id);  // re-fetch defaults
      } catch (e) {
        console.error('reset_mod_options failed:', e);
      }
    },

    async resetAllTweaks() {
      if (!await this.confirmDialog(this.t('tweak.resetAllConfirm'))) return;
      try {
        await window.pywebview.api.reset_all_options();
        if (this.tweak.selectedId) await this.selectTweakMod(this.tweak.selectedId);
      } catch (e) {
        console.error('reset_all_options failed:', e);
      }
    },

    async openExternalUrl(url) {
      // open_path delegates to xdg-open / startfile / open which all handle
      // https:// URLs in addition to local paths.
      try {
        await window.pywebview.api.open_path(url);
      } catch (e) {
        console.error('openExternalUrl threw:', e);
      }
    },

    waitForApi() {
      return new Promise((resolve) => {
        if (window.pywebview && window.pywebview.api) return resolve();
        window.addEventListener('pywebviewready', resolve, { once: true });
      });
    },

    // ── Mods ───────────────────────────────────────────────────────────────
    async refreshMods() {
      try {
        this.mods = await window.pywebview.api.list_mods();
      } catch (e) {
        console.error('list_mods failed', e);
        this.mods = [];
      }
      try {
        this.presets = await window.pywebview.api.list_presets();
      } catch (e) {
        console.error('list_presets failed', e);
        this.presets = [];
      }
    },

    async switchProfile(name) {
      if (!name) return;
      try {
        const res = await window.pywebview.api.load_preset(name);
        if (!res || !res.ok) {
          alert(this.t('alert.loadPresetFail', { error: (res && res.error) || '?' }));
          return;
        }
        this.profileName = name;
        // Persist the choice so the next launch lands on the same preset.
        try { await window.pywebview.api.update_setting('active_profile_name', name); }
        catch (_) {}
        await this.refreshMods();
      } catch (e) {
        console.error('load_preset threw:', e);
      }
    },

    async createPreset() {
      const name = prompt(this.t('profile.promptName'));
      if (!name) return;
      const trimmed = name.trim();
      if (!trimmed) return;
      try {
        const res = await window.pywebview.api.save_preset(trimmed);
        if (!res || !res.ok) {
          alert(this.t('alert.savePresetFail', { error: (res && res.error) || '?' }));
          return;
        }
        this.profileName = trimmed;
        await this.refreshMods();
      } catch (e) {
        console.error('save_preset threw:', e);
      }
    },

    async deletePreset() {
      const name = this.profileName;
      if (!name || name === 'Default' || name === 'Vanilla') {
        alert(this.t('profile.cantDeleteReserved'));
        return;
      }
      if (!await this.confirmDialog(this.t('profile.deleteConfirm', { name }))) return;
      try {
        const res = await window.pywebview.api.delete_preset(name);
        if (!res || !res.ok) {
          alert(this.t('alert.deletePresetFail', { error: (res && res.error) || '?' }));
          return;
        }
        // Apply Default to active-profile.txt too — without this the file
        // still reflects the just-deleted preset and the user has to bounce
        // through Vanilla → Default to get the mods re-enabled.
        await this.switchProfile('Default');
      } catch (e) {
        console.error('delete_preset threw:', e);
      }
    },

    // The list excludes sub-mods from top-level rows; sub-mods will be shown
    // indented beneath their parent in renderModRows.
    get topLevelMods() {
      return this.mods.filter((m) => !m.parent_path);
    },

    get categories() {
      const set = new Set();
      this.topLevelMods.forEach((m) => { if (m.category) set.add(m.category); });
      return [...set].sort((a, b) => a.localeCompare(b));
    },

    get filteredMods() {
      const q = this.search.trim().toLowerCase();
      let out = this.topLevelMods;
      if (this.filterCategory) {
        out = out.filter((m) => m.category === this.filterCategory);
      }
      if (q) {
        out = out.filter((m) =>
          (m.name || '').toLowerCase().includes(q) ||
          (m.category || '').toLowerCase().includes(q)
        );
      }
      // Sort — copy first so we don't mutate the underlying mods array.
      const dir = this.sortDir;
      const key = this.sortBy;
      const sorted = [...out];
      if (key === 'status' && dir !== 0) {
        sorted.sort((a, b) => (Number(b.active) - Number(a.active)) * dir);
      } else if (key === 'name' && dir !== 0) {
        sorted.sort((a, b) => (a.name || '').localeCompare(b.name || '') * dir);
      } else if (key === 'category' && dir !== 0) {
        sorted.sort((a, b) => ((a.category || '').localeCompare(b.category || '') * dir)
                              || (a.name || '').localeCompare(b.name || ''));
      }
      return sorted;
    },

    subModsOf(parentPath) {
      return this.mods.filter((m) => m.parent_path === parentPath);
    },

    get selectedMod() {
      return this.mods.find((m) => m.id === this.selectedModId) || null;
    },

    get activeCount() {
      return this.topLevelMods.filter((m) => m.active).length;
    },

    get totalSizeBytes() {
      return this.topLevelMods.reduce((s, m) => s + (m.size_bytes || 0), 0);
    },

    get activeSizeBytes() {
      return this.topLevelMods.filter((m) => m.active).reduce((s, m) => s + (m.size_bytes || 0), 0);
    },

    /** 'all' if every top-level mod is active, 'none' if none are, otherwise
     *  'partial' — used to drive the tri-state header checkbox. */
    get headerSelectionState() {
      const top = this.topLevelMods;
      if (!top.length) return 'none';
      const active = top.filter((m) => m.active).length;
      if (active === 0) return 'none';
      if (active === top.length) return 'all';
      return 'partial';
    },

    async toggleAllFromHeader() {
      // 'all' → deactivate everything, otherwise activate everything (common
      // sense: if some are off, the user usually wants them all on).
      const next = this.headerSelectionState !== 'all';
      await this.setAllActive(next);
    },

    formatSize(bytes) {
      if (!bytes) return '0 KB';
      const mb = bytes / (1024 * 1024);
      if (mb >= 1) return `${mb.toFixed(1)} MB`;
      return `${Math.max(1, Math.round(bytes / 1024))} KB`;
    },

    async toggleMod(id) {
      const mod = this.mods.find((m) => m.id === id);
      if (!mod) return;
      const next = !mod.active;
      // Optimistic UI update — flip immediately, then call Python. If the
      // backend reports failure we roll back so the checkbox stays in sync
      // with the file on disk.
      mod.active = next;
      try {
        const res = await window.pywebview.api.toggle_mod(id, next);
        if (!res || !res.ok) {
          mod.active = !next;
          console.error('toggle_mod failed:', res && res.error);
        }
      } catch (e) {
        mod.active = !next;
        console.error('toggle_mod threw:', e);
      }
    },

    async setAllActive(active) {
      try {
        const res = await window.pywebview.api.set_all_active(active);
        if (!res || !res.ok) {
          console.error('set_all_active failed:', res && res.error);
          return;
        }
        await this.refreshMods();
      } catch (e) {
        console.error('set_all_active threw:', e);
      }
    },

    async openModFolder(path) {
      if (!path) return;
      try {
        await window.pywebview.api.open_path(path);
      } catch (e) {
        console.error('open_path threw:', e);
      }
    },

    async openModsFolder() {
      try {
        const res = await window.pywebview.api.open_mods_folder();
        if (!res || !res.ok) {
          console.error('open_mods_folder failed:', res && res.error);
        }
      } catch (e) {
        console.error('open_mods_folder threw:', e);
      }
    },

    setSort(col) {
      // Status cycles between active-first / inactive-first; the other columns
      // cycle asc → desc → off so users can disable a sort to fall back to
      // the previous one.
      if (this.sortBy === col) {
        if (col === 'status') {
          this.sortDir = this.sortDir === 1 ? -1 : 1;
        } else {
          this.sortDir = this.sortDir === 1 ? -1 : (this.sortDir === -1 ? 0 : 1);
          if (this.sortDir === 0) this.sortBy = 'status';
        }
      } else {
        this.sortBy = col;
        this.sortDir = 1;
      }
    },

    sortIndicator(col) {
      if (this.sortBy !== col) return '';
      if (this.sortDir === 1) return '▲';
      if (this.sortDir === -1) return '▼';
      return '';
    },

    async setMode(m) {
      this.mode = m;
      if (m === 'order') {
        await this.refreshProfileOrder();
      }
    },

    async refreshProfileOrder() {
      try {
        this.profileOrder = await window.pywebview.api.get_profile_order();
      } catch (e) {
        console.error('get_profile_order failed:', e);
        this.profileOrder = [];
      }
    },

    /** In 'order' mode, list mods following the profile's actual line order.
     *  Mods that aren't yet recorded in the file are appended at the end
     *  (sorted by name) so newly-installed mods don't disappear from view. */
    get orderedTopLevelMods() {
      const top = this.topLevelMods;
      const idToMod = new Map(top.map((m) => [m.id, m]));
      const out = [];
      const seen = new Set();
      for (const id of this.profileOrder) {
        if (idToMod.has(id) && !seen.has(id)) {
          out.push(idToMod.get(id));
          seen.add(id);
        }
      }
      const remaining = top.filter((m) => !seen.has(m.id))
        .sort((a, b) => (a.name || '').localeCompare(b.name || ''));
      return out.concat(remaining);
    },

    onDragStart(id, ev) {
      this._dragId = id;
      ev.dataTransfer.effectAllowed = 'move';
      // Some browsers require dataTransfer.setData to actually start the drag
      try { ev.dataTransfer.setData('text/plain', id); } catch (_) {}
    },

    onDragOver(ev) {
      ev.preventDefault();
      ev.dataTransfer.dropEffect = 'move';
    },

    async onDrop(targetId, ev) {
      ev.preventDefault();
      const draggedId = this._dragId;
      this._dragId = null;
      if (!draggedId || draggedId === targetId) return;
      // Reorder profileOrder locally
      const order = this.orderedTopLevelMods.map((m) => m.id);
      const fromIdx = order.indexOf(draggedId);
      const toIdx = order.indexOf(targetId);
      if (fromIdx < 0 || toIdx < 0) return;
      order.splice(fromIdx, 1);
      order.splice(toIdx, 0, draggedId);
      this.profileOrder = order;
      // Persist
      try {
        const res = await window.pywebview.api.reorder_mods(order);
        if (!res || !res.ok) {
          console.error('reorder_mods failed:', res && res.error);
          await this.refreshProfileOrder();
        }
      } catch (e) {
        console.error('reorder_mods threw:', e);
      }
    },

    onDragEnd() {
      this._dragId = null;
    },

    async uninstallMod(folder, name) {
      if (!folder) return;
      if (!await this.confirmDialog(this.t('detail.uninstallConfirm', { name }))) return;
      try {
        const res = await window.pywebview.api.uninstall_mod(folder);
        if (!res || !res.ok) {
          alert(this.t('alert.uninstallFail', { error: (res && res.error) || '?' }));
          return;
        }
        if (this.selectedMod && this.selectedMod.folder === folder) {
          this.selectedModId = null;
        }
        await this.refreshMods();
        // Drop the mod.io install marker cache so the Browser tab no longer
        // claims this mod is installed if the user navigates back there.
        this._refreshInstalledIds();
      } catch (e) {
        console.error('uninstall_mod threw:', e);
      }
    },

    /** Re-read every _modio_install.json marker from disk and replace
     *  this.browser.installedIds. Called any time an install/uninstall
     *  may have happened (entering Browser, after uninstallMod, after
     *  browserInstall, after a manual browserRefresh). */
    async _refreshInstalledIds() {
      try {
        const r = await window.pywebview.api.modio_installed_ids();
        if (r && r.ok) {
          const map = {};
          for (const id of (r.ids || [])) map[id] = true;
          this.browser.installedIds = map;
          this.browser.installedMeta = r.meta || {};
        }
      } catch (_) {}
    },

    /** True when the mod is installed AND the locally recorded modfile_id
     *  differs from the latest one on mod.io. Used to decide whether the
     *  CTA should read "Update" or just "Installed". When the marker
     *  predates the modfile_id field (legacy installs) we fall back to
     *  "always show update" so the user can refresh; that matches the old
     *  behaviour and is recoverable in one click. */
    browserHasUpdate(m) {
      if (!m || !this.browser.installedIds[m.id]) return false;
      const local = this.browser.installedMeta[m.id];
      if (!local || !local.modfile_id) return true;
      const remote = (m.modfile && Number(m.modfile.id)) || 0;
      return remote && local.modfile_id !== remote;
    },

    /** Pull the current latest modfile_id for every mod we have a marker
     *  for. Drives the Update button on each Activation row (compared
     *  against the local modfile_id in installedMeta). Best-effort: if the
     *  user is not authenticated or the call fails, modUpdates stays empty
     *  and the buttons just don't show — uninstall still works. */
    async _refreshModUpdates() {
      try {
        const meta = this.browser.installedMeta || {};
        const ids = Object.keys(meta).map(Number).filter(Boolean);
        if (!ids.length) { this.modUpdates = {}; return; }
        const res = await window.pywebview.api.modio_check_updates(ids);
        if (res && res.ok) this.modUpdates = res.updates || {};
      } catch (_) {}
    },

    /** True when the local mod folder was installed via the manager — i.e.
     *  there's a _modio_install.json marker whose folder field matches.
     *  Used to gate the Update button and to flag manually-installed mods
     *  with a small "not from the manager" note. */
    modIsFromManager(m) {
      if (!m || !m.folder) return false;
      const meta = this.browser.installedMeta || {};
      for (const v of Object.values(meta)) {
        if (v && v.folder === m.folder) return true;
      }
      return false;
    },
    modManagerModId(m) {
      if (!m || !m.folder) return 0;
      const meta = this.browser.installedMeta || {};
      for (const [mid, v] of Object.entries(meta)) {
        if (v && v.folder === m.folder) return Number(mid);
      }
      return 0;
    },
    _normVer(v) {
      return (v || '').trim().replace(/^[vV]/, '');
    },
    _versionCmp(a, b) {
      const pa = this._normVer(a).split('.');
      const pb = this._normVer(b).split('.');
      const len = Math.max(pa.length, pb.length);
      for (let i = 0; i < len; i++) {
        const na = parseInt(pa[i] || '0', 10);
        const nb = parseInt(pb[i] || '0', 10);
        // Segment non-numérique (ex. "1.3.a") → ordre indéterminé, on ne supprime pas l'update
        if (isNaN(na) || isNaN(nb)) return 0;
        if (na > nb) return 1;
        if (na < nb) return -1;
      }
      return 0;
    },
    modVersionMismatch(m) {
      const mid = this.modManagerModId(m);
      if (!mid) return false;
      const remote = this.modUpdates[mid];
      if (!remote || !remote.version) return false;
      return this._normVer(m.version) !== this._normVer(remote.version);
    },
    modUpdateAvailable(m) {
      const mid = this.modManagerModId(m);
      if (!mid) return false;
      const local = (this.browser.installedMeta || {})[mid];
      const remote = this.modUpdates[mid];
      if (!local || !remote) return false;
      if (local.modfile_id === remote.modfile_id) return false;
      // Ne pas proposer la mise à jour si la version locale est déjà plus haute (évite une rétrogradation)
      if (remote.version && m.version && this._versionCmp(m.version, remote.version) > 0) return false;
      return true;
    },

    /** Activation-row Uninstall — same trigger as the Browser's row
     *  Uninstall, but driven from the local mod (we already have the
     *  folder, no need to look up the marker). Refreshes the mod list and
     *  marker cache so the row disappears immediately. */
    async activationUninstall(folder, name) {
      if (!folder) return;
      if (!await this.confirmDialog(this.t('detail.uninstallConfirm', { name: name || folder }))) return;
      try {
        const res = await window.pywebview.api.uninstall_mod(folder);
        if (res && res.ok) {
          await this.refreshMods();
          await this._refreshInstalledIds();
        } else {
          alert((res && res.error) || 'unknown');
        }
      } catch (e) {
        alert(String(e));
      }
    },

    /** Activation-row Update — re-runs modio_install_mod which re-downloads
     *  the latest modfile and overwrites the local copy. After success we
     *  refresh markers + the update map so the button hides itself. */
    async activationUpdate(modId) {
      if (!modId) return;
      try {
        const res = await window.pywebview.api.modio_install_mod(modId);
        if (res && res.ok) {
          await this.refreshMods();
          await this._refreshInstalledIds();
          await this._refreshModUpdates();
        } else {
          alert((res && res.error) || 'unknown');
        }
      } catch (e) {
        alert(String(e));
      }
    },

    /** Open the "link to mod.io" picker for a hand-installed mod row.
     *  Pre-fills the search with the local mod name to give a head start;
     *  the user always picks the match manually from the result list. */
    async openLinkPicker(folder, localName) {
      this.linkPicker = {
        open: true,
        folder: folder || '',
        localName: localName || folder || '',
        search: localName || '',
        results: [],
        loading: false,
        error: '',
        busyId: 0,
      };
      await this.linkPickerSearch();
    },
    closeLinkPicker() {
      this.linkPicker = {
        open: false, folder: '', localName: '', search: '',
        results: [], loading: false, error: '', busyId: 0,
      };
    },
    /** Re-run the mod.io browse query with the current search string.
     *  Bound to @input on the search field so the list refreshes as the
     *  user types — debounced lightly via a per-call cancel token. */
    async linkPickerSearch() {
      const token = ++this._linkPickerToken;
      this.linkPicker.loading = true;
      this.linkPicker.error = '';
      try {
        const res = await window.pywebview.api.modio_browse(
          this.linkPicker.search || '', null, 10, 0, '-popular', 0, false);
        if (token !== this._linkPickerToken) return;  // stale
        if (res && res.ok) {
          this.linkPicker.results = res.data || [];
          this.linkPicker.loading = false;
        } else {
          this.linkPicker.results = [];
          this.linkPicker.loading = false;
          this.linkPicker.error = (res && res.error) || 'fetch failed';
        }
      } catch (e) {
        if (token !== this._linkPickerToken) return;
        this.linkPicker.loading = false;
        this.linkPicker.error = String(e);
      }
    },
    _linkPickerToken: 0,
    /** Confirm an association: writes the marker, refreshes installed
     *  state + update map, then closes the picker. The mod gains the
     *  Update / Uninstall icons immediately. */
    async confirmLinkMod(modId) {
      if (!modId || this.linkPicker.busyId) return;
      this.linkPicker.busyId = modId;
      try {
        const res = await window.pywebview.api.modio_link_mod(
          this.linkPicker.folder, modId);
        if (res && res.ok) {
          await this._refreshInstalledIds();
          await this._refreshModUpdates();
          await this._refreshSubscribed();
          this.closeLinkPicker();
        } else {
          this.linkPicker.error = (res && res.error) || 'unknown';
          this.linkPicker.busyId = 0;
        }
      } catch (e) {
        this.linkPicker.error = String(e);
        this.linkPicker.busyId = 0;
      }
    },

    /** Same idea as _refreshSubscribed but for collections. Pulls the user's
     *  followed-collections list (single host, capped at 100 — well above
     *  what any sane user would track) and turns it into a {coll_id: true}
     *  map for the star button on each collection card. */
    async _refreshFollowedCollections() {
      try {
        const res = await window.pywebview.api.modio_followed_collections();
        if (res && res.ok) {
          const map = {};
          for (const c of (res.data || [])) map[c.id] = true;
          this.browser.followedColls = map;
        }
      } catch (_) {}
    },

    /** Toggle "Mes follows" filter on the Collections tab. Same shape as
     *  browserToggleSubscribed but routes through modio_followed_collections
     *  instead of modio_subscribed. Persisted to settings.json so it
     *  survives restart. */
    browserToggleFollowed() {
      this.browser.followedOnly = !this.browser.followedOnly;
      this.browser.offset = 0;
      try {
        window.pywebview.api.update_setting(
          'browser_followed_only', this.browser.followedOnly);
      } catch (_) {}
      this.browserFetch();
    },

    /** Star/unstar a collection. mod.io auto-subscribes the user to every
     *  mod in the bundle on follow (and the reverse on unfollow), so we
     *  refresh the subscribed cache too — otherwise the per-mod ✓ badges
     *  on Browser cards would lag behind. */
    async browserToggleFollowCollection(collId, nameId) {
      if (!collId || !nameId || this.browser.followBusy[collId]) return;
      this.browser.followBusy = { ...this.browser.followBusy, [collId]: true };
      const wasFollowed = !!this.browser.followedColls[collId];
      try {
        const res = wasFollowed
          ? await window.pywebview.api.modio_unfollow_collection(nameId)
          : await window.pywebview.api.modio_follow_collection(nameId);
        if (res && res.ok) {
          const next = { ...this.browser.followedColls };
          if (wasFollowed) delete next[collId]; else next[collId] = true;
          this.browser.followedColls = next;
          // Cascade affected the per-mod subscribed state — refresh both
          // caches so the UI matches mod.io's server side immediately.
          this._refreshSubscribed();
          // Same drop-from-list trick as browserToggleSubscribe: when "Mes
          // follows" is on, the list IS /me/following/collections, so
          // unfollowing here should remove the card right away.
          if (wasFollowed && this.browser.followedOnly &&
              this.currentTab === 'collections') {
            this.browser.items = this.browser.items.filter((m) => m.id !== collId);
            this.browser.total = Math.max(0, (this.browser.total || 0) - 1);
          }
        } else {
          this._browserFlash(this.t('browser.installFail',
            { error: (res && res.error) || 'unknown' }), true);
        }
      } catch (e) {
        this._browserFlash(this.t('browser.installFail', { error: String(e) }), true);
      } finally {
        const next = { ...this.browser.followBusy };
        delete next[collId];
        this.browser.followBusy = next;
      }
    },

    /** Re-fetch /me/subscribed and rebuild the {modId: true} cache used by
     *  the "✓ Subscribed" badge on cards and the My Subscriptions filter.
     *  Called on Browser open and after every install (the backend
     *  auto-subscribes silently, but the frontend cache is what drives the
     *  UI so it has to be told). */
    async _refreshSubscribed() {
      try {
        const res = await window.pywebview.api.modio_subscribed();
        if (res && res.ok) {
          const map = {};
          for (const m of (res.data || [])) map[m.id] = true;
          this.browser.subscribed = map;
        }
      } catch (_) {}
    },

    async fetchBannerForSelected() {
      const mod = this.selectedMod;
      if (!mod) { this.selectedBannerUrl = ''; return; }
      if (this._bannerCache.has(mod.id)) {
        // LRU touch: re-insert to mark as most-recently used so the eviction
        // below kicks the right (oldest) entry next time we add a new one.
        const cached = this._bannerCache.get(mod.id);
        this._bannerCache.delete(mod.id);
        this._bannerCache.set(mod.id, cached);
        this.selectedBannerUrl = cached;
        return;
      }
      this.selectedBannerUrl = '';
      if (!mod.banner) return;
      try {
        const res = await window.pywebview.api.get_mod_banner(mod.id);
        const url = (res && res.ok && res.data_url) || '';
        // Bound the cache: each banner is up to ~5 MB of data-URL on the
        // backend (api.py:_data_url_for cap), so an unbounded Map across a
        // long session would chew through hundreds of megabytes. 25 entries
        // is plenty to cover quick back-and-forth navigation.
        this._bannerCache.set(mod.id, url);
        while (this._bannerCache.size > 25) {
          const oldest = this._bannerCache.keys().next().value;
          this._bannerCache.delete(oldest);
        }
        if (this.selectedMod && this.selectedMod.id === mod.id) {
          this.selectedBannerUrl = url;
        }
      } catch (e) {
        console.error('get_mod_banner threw:', e);
      }
    },

    selectMod(id) {
      this.selectedModId = id;
      this.fetchBannerForSelected();
    },

    async launchGame() {
      try {
        const res = await window.pywebview.api.launch_game();
        if (!res || !res.ok) {
          console.error('launch_game failed:', res && res.error);
          alert(this.t('launch.error', { err: (res && res.error) || '?' }));
        }
      } catch (e) {
        console.error('launch_game threw:', e);
      }
    },

    // ── Templates ──────────────────────────────────────────────────────────
    renderTab(tab) {
      switch (tab) {
        case 'activation': return this.activationTemplate();
        case 'settings':   return this.settingsTemplate();
        case 'log':        return this.logTemplate();
        case 'install':    return this.installTemplate();
        case 'tweak':      return this.tweakingTemplate();
        case 'news':       return this.newsTemplate();
        case 'browser':    return this.browserTemplate();
        case 'collections': return this.browserTemplate();
        default:           return this.placeholderTemplate(tab);
      }
    },

    placeholderTemplate(tab) {
      return `
        <div class="placeholder">
          <div class="placeholder__inner">
            <div class="ornament">───── ◆ ─────</div>
            <p>${escapeHtml(this.t('tab.placeholder'))}</p>
            <p class="placeholder__hint">${escapeHtml(this.t('tab.placeholderHint', { tab: this.t('tab.activation') }))}</p>
          </div>
        </div>`;
    },

    newsTemplate() {
      const n = this.news;

      // Refresh button moved to the bottom HUD so the toolbar stays focused
      // on news-specific options (Reddit toggle + Anno Union shortcut).
      const toolbar = `
        <div class="news__toolbar">
          ${n.loading ? `<span class="news__cached">${escapeHtml(this.t('news.loading'))}</span>` : ''}
          <label class="news__toggle">
            <input type="checkbox" ${this.settings.show_reddit_news ? 'checked' : ''}
                   onchange="annoRoot().setSetting('show_reddit_news', this.checked).then(() => annoRoot().refreshNews(true))" />
            <span>${escapeHtml(this.t('news.includeReddit'))}</span>
          </label>
          <button class="settings__btn"
                  onclick="annoRoot().openExternalUrl('https://www.anno-union.com/en/blogs/')">
            ${escapeHtml(this.t('news.visitUnion'))}
          </button>
          ${n.cached && !n.loading ? `<span class="news__cached">${escapeHtml(this.t('news.cached'))}</span>` : ''}
        </div>`;

      let body;
      // Detail view (in-app reader for Anno Union posts) takes over the
      // body when open. Reddit/mod.io cards still open externally / via
      // the existing Browser deep-link.
      if (n.detail && n.detail.open) {
        const d = n.detail;
        const it = d.item || {};
        const inner = d.loading
          ? this.renderLoader(this.t('news.loading'))
          : d.error
            ? `<div class="news__empty news__empty--error">${escapeHtml(this.t('news.error', { err: d.error }))}</div>`
            : `<article class="news-detail__article" onclick="annoRoot().onArticleClick(event)">${sanitizeModioHtml(d.html || '')}</article>`;
        body = `
          <div class="news-detail">
            <div class="news-detail__bar">
              <button class="settings__btn"
                      onclick="annoRoot().closeNewsDetail()">← ${escapeHtml(this.t('news.back'))}</button>
              <button class="settings__btn"
                      onclick="annoRoot().openExternalUrl('${escapeAttr(it.url || '')}')">
                ${escapeHtml(this.t('news.openOnUnion'))}
              </button>
            </div>
            ${it.img_url
                ? `<div class="news-detail__hero"><img src="${escapeAttr(it.img_url)}" alt="" /></div>`
                : ''}
            <div class="news-detail__head">
              <span class="news-card__badge"
                    style="background: ${escapeAttr(it.badge_color || '#444')}">${escapeHtml(it.badge_text || '?')}</span>
              <span class="news-card__date">${escapeHtml(it.date || '')}</span>
            </div>
            <h2 class="news-detail__title">${escapeHtml(it.title || '')}</h2>
            ${inner}
          </div>`;
      } else if (n.loading && !n.items.length) {
        body = this.renderLoader(this.t('news.loading'));
      } else if (n.error) {
        body = `<div class="news__empty news__empty--error">${escapeHtml(this.t('news.error', { err: n.error }))}</div>`;
      } else if (!n.items.length) {
        body = `<div class="news__empty">${escapeHtml(this.t('news.empty'))}</div>`;
      } else {
        body = `<div class="news__grid">${n.items.map((item) => {
          // Three click targets per card source:
          //  - mod.io  → in-app Browser/Collections deep link
          //  - anno_union → in-app reader (lazy fetches the full HTML)
          //  - reddit  → external (no clean public content endpoint)
          let click;
          if (item.modio_id && (item.modio_kind === 'mod' || item.modio_kind === 'collection')) {
            click = `annoRoot().openModioFromNews(${Number(item.modio_id)}, '${escapeAttr(item.modio_kind)}')`;
          } else if (item.source === 'anno_union' && item.wp_id) {
            click = `annoRoot().openNewsDetail(annoRoot().news.items.find((x) => x.wp_id === ${Number(item.wp_id)}))`;
          } else {
            click = `annoRoot().openExternalUrl('${escapeAttr(item.url || '')}')`;
          }
          return `
          <article class="news-card" onclick="${click}">
            ${item.img_url
                ? `<div class="news-card__media"><img src="${escapeAttr(item.img_url)}" alt="" loading="lazy" /></div>`
                : `<div class="news-card__media news-card__media--placeholder"><span>📜</span></div>`}
            <div class="news-card__body">
              <div class="news-card__meta">
                <span class="news-card__badge"
                      style="background: ${escapeAttr(item.badge_color || '#444')}">${escapeHtml(item.badge_text || '?')}</span>
                <span class="news-card__date">${escapeHtml(item.date || '')}</span>
              </div>
              <h3 class="news-card__title">${escapeHtml(item.title || '')}</h3>
              ${item.excerpt
                  ? `<p class="news-card__excerpt">${escapeHtml(item.excerpt)}</p>`
                  : ''}
            </div>
          </article>`;
        }).join('')}</div>`;
      }

      return `
        <div class="news">
          ${toolbar}
          <div class="news__body">${body}</div>
        </div>`;
    },

    browserTemplate() {
      const b = this.browser;
      const fmtNumber = (n) => {
        const v = Number(n) || 0;
        if (v >= 1_000_000) return (v / 1_000_000).toFixed(1) + 'M';
        if (v >= 1_000)     return (v / 1_000).toFixed(1) + 'K';
        return String(v);
      };
      const fmtDate = (ts) => {
        const t = Number(ts) || 0;
        if (!t) return '';
        try { return new Date(t * 1000).toLocaleDateString(); } catch (_) { return ''; }
      };
      const fmtSize = (bytes) => {
        const v = Number(bytes) || 0;
        if (v >= 1024 * 1024) return (v / (1024 * 1024)).toFixed(1) + ' MB';
        if (v >= 1024)        return (v / 1024).toFixed(0) + ' KB';
        return v + ' B';
      };

      // Toolbar — search + sort dropdown + refresh
      const sortOptions = [
        ['-date_updated', 'browser.sortNewest'],
        ['-popular',      'browser.sortPopular'],
        // mod.io quirk: the `_sort=downloads` field is inverted vs the rest of
        // the API — `-downloads` returns the LEAST downloaded mods first,
        // plain `downloads` returns the MOST. Verified against /games/11358/
        // mods on 2026-05-05. Don't add the `-` "to be consistent" with the
        // others or the user-facing label "Most downloaded" stops matching
        // the result order.
        ['downloads',     'browser.sortDownloads'],
        ['-rating',       'browser.sortRating'],
        ['name',          'browser.sortAlpha'],
      ];
      // The HUD bottom row already provides the search input and the refresh
      // button when the Browser tab is active — keep this internal toolbar
      // focused on what's specific to the Browser (sort + active-search chip
      // + result counter).
      // Flatten the tag taxonomy from mod.io into one optgroup per tag
      // group ("Type", "Difficulty", …). Each option's value is the tag
      // name itself, which is what mod.io's tags-in= filter matches on.
      // Collections use a different taxonomy (Category / Tags) that the
      // /games/{gid}/tags endpoint doesn't expose, so we skip the filter
      // entirely on that tab rather than show stale mod tags.
      const tagGroups = this.currentTab === 'collections'
        ? []
        : (b.tagsCatalog || []).filter(
            (g) => Array.isArray(g.tags) && g.tags.length && !g.hidden);
      const toolbar = `
        <div class="browser__toolbar">
          <label class="browser__sort-label">${escapeHtml(this.t('browser.sortBy'))}</label>
          <select class="browser__sort"
                  onchange="annoRoot().browserSetSort(this.value)">
            ${sortOptions.map(([val, key]) => `
              <option value="${escapeAttr(val)}" ${b.sort === val ? 'selected' : ''}>
                ${escapeHtml(this.t(key))}
              </option>`).join('')}
          </select>
          ${this.currentTab === 'browser' ? `
            <button class="browser__toggle ${b.subscribedOnly ? 'is-active' : ''}"
                    title="${escapeAttr(this.t('browser.mySubscriptions'))}"
                    onclick="annoRoot().browserToggleSubscribed()">
              ${escapeHtml(this.t('browser.mySubscriptions'))}
            </button>` : ''}
          ${this.currentTab === 'collections' ? `
            <button class="browser__toggle ${b.followedOnly ? 'is-active' : ''}"
                    title="${escapeAttr(this.t('browser.myFollows'))}"
                    onclick="annoRoot().browserToggleFollowed()">
              ${escapeHtml(this.t('browser.myFollows'))}
            </button>` : ''}
          ${tagGroups.length ? `
            <label class="browser__sort-label">${escapeHtml(this.t('browser.tag'))}</label>
            <select class="browser__sort"
                    onchange="annoRoot().browserSetTag(this.value)">
              <option value="" ${b.tagFilter === '' ? 'selected' : ''}>${escapeHtml(this.t('browser.tagAll'))}</option>
              ${tagGroups.map((g) => `
                <optgroup label="${escapeAttr(g.name || '')}">
                  ${g.tags.map((t) => {
                    const tagName = (t && (t.name || t)) || '';
                    return `<option value="${escapeAttr(tagName)}" ${b.tagFilter === tagName ? 'selected' : ''}>${escapeHtml(tagName)}</option>`;
                  }).join('')}
                </optgroup>`).join('')}
            </select>` : ''}
          ${b.search ? `
            <span class="browser__active-search" title="${escapeAttr(b.search)}">
              « ${escapeHtml(b.search)} »
              <button class="browser__clear-search" title="${escapeAttr(this.t('browser.clearSearch'))}"
                      onclick="annoRoot().browser.search = ''; annoRoot().browser.offset = 0; annoRoot().browserFetch()">✕</button>
            </span>` : ''}
          ${b.authorFilter.id ? `
            <span class="browser__active-search" title="${escapeAttr(b.authorFilter.name)}">
              ${escapeHtml(this.t('browser.byAuthor', { name: b.authorFilter.name }))}
              <button class="browser__clear-search" title="${escapeAttr(this.t('browser.clearAuthor'))}"
                      onclick="annoRoot().browserClearAuthor()">✕</button>
            </span>` : ''}
          <span class="browser__count">
            ${b.loaded && !b.loading
              ? escapeHtml(this.t('browser.resultsCount',
                  { shown: b.items.length, total: b.total }))
              : ''}
          </span>
        </div>`;

      // List body — three states: notAuth, error/empty, populated
      let listBody;
      if (b.notAuth) {
        listBody = `
          <div class="browser__empty">
            <p>${escapeHtml(this.t('browser.notAuth'))}</p>
            <button class="settings__btn settings__btn--accent"
                    onclick="annoRoot().currentTab = 'settings'">
              ${escapeHtml(this.t('browser.openSettings'))}
            </button>
          </div>`;
      } else if (b.loading && !b.items.length) {
        listBody = this.renderLoader(this.t('browser.loading'));
      } else if (b.error) {
        listBody = `<div class="browser__empty browser__empty--error">${escapeHtml(this.t('browser.error', { error: b.error }))}</div>`;
      } else if (!b.items.length) {
        listBody = `<div class="browser__empty">${escapeHtml(this.t('browser.empty'))}</div>`;
      } else {
        // mod.io-style card grid (responsive, ~280px min). Each card is fully
        // clickable to open the detail page; the Subscribe button at the
        // bottom stops propagation so it doesn't also navigate.
        listBody = `<div class="mod-grid">${b.items.map((m) => {
          const id          = Number(m.id);
          // On the Collections grid the +/✓ button on the card flips role:
          // it follows/unfollows the collection on mod.io (which auto-subs
          // every mod inside) instead of subscribing to a single mod —
          // there's no per-mod subscribe gesture for a collection.
          const isCardCollection = this.currentTab === 'collections' && !b.parent;
          const isSubd      = isCardCollection
                              ? !!b.followedColls[m.id]
                              : !!b.subscribed[m.id];
          const wasEndorsed = !!b.endorsed[m.id];
          const isInstalling = !!b.installing[m.id];
          const isInstalled  = this.browserIsInstalled(m);
          const subBusy     = isCardCollection
                              ? !!b.followBusy[m.id]
                              : !!b.subBusy[m.id];
          const endorseBusy = !!b.endorseBusy[m.id];
          const submittedBy = (m.submitted_by && m.submitted_by.username) || '?';
          const submittedById = (m.submitted_by && Number(m.submitted_by.id)) || 0;
          const logoUrl = (m.logo && (m.logo.thumb_320x180 || m.logo.thumb_640x360 || m.logo.original)) || '';
          const stats = m.stats || {};
          const modfile = m.modfile || {};
          const desc = (m.description_plaintext || m.summary || '').trim();
          const tags = Array.isArray(m.tags) ? m.tags : [];
          const firstTag = tags.length ? (tags[0].name || '') : '';
          const moreTags = Math.max(0, tags.length - 1);
          const dateStr = (() => {
            const t = Number(m.date_updated) || 0;
            if (!t) return '';
            try { return new Date(t * 1000).toLocaleDateString(); } catch (_) { return ''; }
          })();
          // Primary CTA at the bottom of the card. This is a manager, not a
          // discovery site, so the install action is the dominant gesture.
          const hasUpdate = this.browserHasUpdate(m);
          const installLabel = isInstalling ? this.t('browser.installing')
                              : isInstalled
                                  ? (hasUpdate ? this.t('browser.update') : this.t('browser.installed'))
                                  : this.t('browser.install');
          return `
            <article class="mod-card"
                     onclick="annoRoot().browserSelect(${id})">
              <div class="mod-card__media">
                ${logoUrl
                    ? `<img src="${escapeAttr(logoUrl)}" alt="" />`
                    : `<span class="mod-card__placeholder">📦</span>`}
                <button class="mod-card__hover-action mod-card__hover-action--endorse ${wasEndorsed ? 'is-active' : ''}"
                        ${endorseBusy || wasEndorsed ? 'disabled' : ''}
                        title="${escapeAttr(wasEndorsed ? this.t('browser.endorsed') : this.t('browser.endorse'))}"
                        onclick="event.stopPropagation(); annoRoot().browserEndorse(${id})">♥</button>
                <button class="mod-card__hover-action mod-card__hover-action--subscribe ${isSubd ? 'is-active' : ''}"
                        ${subBusy ? 'disabled' : ''}
                        title="${escapeAttr(isSubd
                          ? this.t(isCardCollection ? 'browser.unfollow' : 'browser.unsubscribe')
                          : this.t(isCardCollection ? 'browser.follow' : 'browser.subscribe'))}"
                        onclick="event.stopPropagation(); ${isCardCollection
                          ? `annoRoot().browserToggleFollowCollection(${id}, '${escapeAttr(m.name_id || '')}')`
                          : `annoRoot().browserToggleSubscribe(${id})`}">${isSubd ? '✓' : '+'}</button>
              </div>
              <div class="mod-card__body">
                <h3 class="mod-card__title">${escapeHtml(m.name || '')}</h3>
                <div class="mod-card__meta">
                  ${submittedById
                      ? `<a class="mod-card__author mod-card__author--link"
                            title="${escapeAttr(this.t('browser.filterByAuthor'))}"
                            onclick="event.stopPropagation(); annoRoot().browserSetAuthor(${submittedById}, '${escapeAttr(submittedBy)}')">${escapeHtml(submittedBy)}</a>`
                      : `<span class="mod-card__author">${escapeHtml(submittedBy)}</span>`}
                  ${dateStr ? `<span class="mod-card__date">↻ ${escapeHtml(dateStr)}</span>` : ''}
                </div>
                ${desc ? `<p class="mod-card__summary">${escapeHtml(desc)}</p>` : ''}
                <div class="mod-card__tags">
                  ${firstTag ? `<span class="mod-card__tag">${escapeHtml(firstTag)}</span>` : '<span></span>'}
                  ${moreTags > 0 ? `<span class="mod-card__more">+ ${moreTags} more</span>` : ''}
                </div>
                <div class="mod-card__stats">
                  ${this.currentTab === 'collections'
                      ? `<span title="${escapeAttr(this.t('browser.modsTotal', { n: stats.mods_total || 0 }))}">📚 ${escapeHtml(fmtNumber(stats.mods_total || 0))}</span>`
                      : `<span title="${escapeAttr(this.t('browser.subscribers', { n: stats.subscribers_total || 0 }))}">👥 ${escapeHtml(fmtNumber(stats.subscribers_total || 0))}</span>`}
                  ${(() => {
                      // Collections expose total bundle size at the top level,
                      // regular mods carry it on the active modfile.
                      const sz = (this.currentTab === 'collections')
                        ? Number(m.filesize) || 0
                        : Number((modfile || {}).filesize) || 0;
                      return sz
                        ? `<span title="${escapeAttr(this.t('browser.size', { size: fmtSize(sz) }))}">📦 ${escapeHtml(fmtSize(sz))}</span>`
                        : '';
                    })()}
                  <span title="${escapeAttr(this.t('browser.downloads', { n: stats.downloads_total || 0 }))}">⬇ ${escapeHtml(fmtNumber(stats.downloads_total || 0))}</span>
                </div>
                <div class="mod-card__actions">
                  ${isInstalled && !hasUpdate ? '' : `
                    <button class="mod-card__install ${isInstalled ? 'is-installed' : ''}"
                            ${isInstalling ? 'disabled' : ''}
                            onclick="event.stopPropagation(); annoRoot().browserInstall(${id})">
                      ${escapeHtml(installLabel)}
                    </button>`}
                  ${isInstalled ? `
                    <button class="mod-card__uninstall ${hasUpdate ? '' : 'mod-card__uninstall--solo'}"
                            ${isInstalling ? 'disabled' : ''}
                            title="${escapeAttr(this.t('browser.uninstallMod'))}"
                            onclick="event.stopPropagation(); annoRoot().browserUninstall(${id})">
                      ${escapeHtml(this.t('browser.uninstallMod'))}
                    </button>` : ''}
                </div>
              </div>
            </article>`;
        }).join('')}</div>`;
      }

      // Pagination
      const page = b.limit > 0 ? Math.floor(b.offset / b.limit) + 1 : 1;
      const pages = b.limit > 0 ? Math.max(1, Math.ceil(b.total / b.limit)) : 1;
      const pagination = (b.loaded && !b.notAuth && !b.error && b.items.length) ? `
        <div class="browser__pagination">
          <button class="settings__btn settings__btn--small"
                  ${b.offset <= 0 || b.loading ? 'disabled' : ''}
                  onclick="annoRoot().browserPrev()">
            ${escapeHtml(this.t('browser.prev'))}
          </button>
          <span class="browser__page">${escapeHtml(this.t('browser.pageOf', { page, total: pages }))}</span>
          <button class="settings__btn settings__btn--small"
                  ${(b.offset + b.limit) >= b.total || b.loading ? 'disabled' : ''}
                  onclick="annoRoot().browserNext()">
            ${escapeHtml(this.t('browser.next'))}
          </button>
        </div>` : '';

      // Two top-level layouts: the cards grid (default) or a full-width
      // detail page (entered by clicking a card, exited via the back button).
      if (b.detailOpen) {
        return `
          <div class="browser">
            ${this._renderBrowserDetail(b, fmtNumber, fmtDate, fmtSize)}
          </div>`;
      }

      return `
        <div class="browser">
          ${toolbar}
          <div class="browser__scroll">
            ${listBody}
            ${pagination}
          </div>
        </div>`;
    },

    /** Compact list of bundled mods on a collection's detail page.
     *  Each row is clickable: click sends the user back to Browser at the
     *  matching mod so they can inspect or install it individually. */
    _renderBrowserDeps(b, fmtNumber, fmtSize) {
      const heading = `<h3 class="browser-detail__section">${escapeHtml(this.t('browser.bundledMods'))}</h3>`;
      if (b.dependenciesLoading) {
        return `${heading}<div class="browser-detail__deps-empty">${escapeHtml(this.t('browser.loading'))}</div>`;
      }
      if (!b.dependencies || !b.dependencies.length) {
        return `${heading}<div class="browser-detail__deps-empty">${escapeHtml(this.t('browser.bundledEmpty'))}</div>`;
      }
      return `${heading}
        <ul class="browser-detail__deps">
          ${b.dependencies.map((dep) => {
            const mid = Number(dep.mod_id || dep.id) || 0;
            const name = dep.name || dep.name_id || `mod ${mid}`;
            const author = (dep.submitted_by && dep.submitted_by.username) || '';
            const logo = (dep.logo && (dep.logo.thumb_320x180 || dep.logo.thumb_640x360 || dep.logo.original)) || '';
            return `
              <li class="browser-detail__dep"
                  onclick="annoRoot().browserOpenChildMod(${mid})">
                <div class="browser-detail__dep-media">
                  ${logo
                      ? `<img src="${escapeAttr(logo)}" alt="" />`
                      : `<span class="browser-detail__dep-ph">📦</span>`}
                </div>
                <div class="browser-detail__dep-info">
                  <span class="browser-detail__dep-name">${escapeHtml(name)}</span>
                  ${author ? `<span class="browser-detail__dep-author">${escapeHtml(this.t('browser.byAuthor', { name: author }))}</span>` : ''}
                </div>
              </li>`;
          }).join('')}
        </ul>`;
    },

    /** Full-width detail page with a back button in the top-left. */
    _renderBrowserDetail(b, fmtNumber, fmtDate, fmtSize) {
      const backLabel = b.parent
        ? this.t('browser.backToCollection')
        : this.t('browser.back');
      const backBar = `
        <div class="browser-detail__back-bar">
          <button class="settings__btn settings__btn--small"
                  onclick="annoRoot().browserBack()">
            ← ${escapeHtml(backLabel)}
          </button>
        </div>`;
      if (!b.detail) {
        return `${backBar}
                <div class="browser-detail browser-detail--empty">
                  <p>${escapeHtml(this.t('browser.detailPick'))}</p>
                </div>`;
      }
      const d = b.detail;
      const id = Number(d.id) || 0;
      const author = (d.submitted_by && d.submitted_by.username) || '?';
      const authorId = (d.submitted_by && Number(d.submitted_by.id)) || 0;
      const heroUrl = (d.logo && (d.logo.thumb_640x360 || d.logo.original)) || '';
      const profileUrl = d.profile_url || `https://mod.io/g/anno-117/m/${d.name_id || ''}`;
      const stats = d.stats || {};
      const positivePct = (() => {
        const pos = Number(stats.ratings_positive) || 0;
        const tot = pos + (Number(stats.ratings_negative) || 0);
        return tot > 0 ? Math.round((pos / tot) * 100) : null;
      })();
      const modfile = d.modfile || {};
      const isCollectionTab = (this.currentTab === 'collections') && !b.parent;
      // Detail-page subscribe button: on Collections it stands for follow,
      // not subscribe (no per-mod sub gesture for a collection bundle).
      const isSubscribed = isCollectionTab
                           ? !!b.followedColls[id]
                           : !!b.subscribed[id];
      const isInstalling = !!b.installing[id];
      const isInstalled  = this.browserIsInstalled(d);
      const subBusy      = isCollectionTab
                           ? !!b.followBusy[id]
                           : !!b.subBusy[id];
      const endorseBusy  = !!b.endorseBusy[id];
      const wasEndorsed  = !!b.endorsed[id];

      // Collection install puts up a different verb — we're not installing
      // one mod, we're installing a bunch of them and creating a profile.
      // For collections we keep the old behaviour (Update/Install always)
      // because there's no per-mod modfile_id we can reliably compare against
      // the bundle's contents — only individual mods get the version check.
      const hasUpdate = this.browserHasUpdate(d);
      const installLabel = isInstalling
        ? this.t('browser.installing')
        : (isCollectionTab
            ? (isInstalled
                ? this.t('browser.updateCollection')
                : this.t('browser.installCollection'))
            : (isInstalled
                ? (hasUpdate ? this.t('browser.update') : this.t('browser.installed'))
                : this.t('browser.install')));
      const installClass = isInstalled
        ? 'settings__btn'
        : 'settings__btn settings__btn--accent';
      const subLabel = isCollectionTab
        ? (isSubscribed ? this.t('browser.unfollow') : this.t('browser.follow'))
        : (isSubscribed ? this.t('browser.unsubscribe') : this.t('browser.subscribe'));

      // Description: prefer the rich HTML mod.io serves (with proper headings,
      // lists, emphasis) over the flat plaintext form. mod.io strips dangerous
      // tags server-side, so injecting it into the panel is safe; we still
      // run it through a small sanitiser as a belt-and-braces measure.
      const descHtml = d.description ? sanitizeModioHtml(d.description) : '';
      const descPlain = (d.description_plaintext || d.summary || '').trim();

      // Flash message (success or error) under the actions row
      const flashHtml = b.flash ? `
        <div class="browser-detail__flash ${b.flashError ? 'is-error' : 'is-ok'}">
          ${escapeHtml(b.flash)}
        </div>` : '';

      // Header layout is image-left + info-right (grid). Endorse and Subscribe
      // are real buttons in the right column with strong distinctive colours
      // so the user can see them at a glance without hunting in overlays.
      const heroBlock = heroUrl
        ? `<div class="browser-detail__hero"><img src="${escapeAttr(heroUrl)}" alt="" /></div>`
        : `<div class="browser-detail__hero browser-detail__hero--placeholder"><span>📦</span></div>`;

      return `
        ${backBar}
        <div class="browser-detail">
          <div class="browser-detail__header">
            ${heroBlock}
            <div class="browser-detail__head-info">
              <h2 class="browser-detail__title">${escapeHtml(d.name || '')}</h2>
              <div class="browser-detail__author">
                ${escapeHtml(this.t('browser.author', { name: '' })).replace(/\s*$/, '')}
                ${authorId
                    ? `<a class="browser-detail__author-link"
                          title="${escapeAttr(this.t('browser.filterByAuthor'))}"
                          onclick="annoRoot().browserSetAuthor(${authorId}, '${escapeAttr(author)}')">${escapeHtml(author)}</a>`
                    : escapeHtml(author)}
              </div>
              <div class="browser-detail__stats">
                <span>⬇ ${escapeHtml(fmtNumber(stats.downloads_total || 0))}</span>
                ${isCollectionTab
                    ? `<span title="${escapeAttr(this.t('browser.modsTotal', { n: stats.mods_total || 0 }))}">📚 ${escapeHtml(fmtNumber(stats.mods_total || 0))}</span>`
                    : `<span>👥 ${escapeHtml(fmtNumber(stats.subscribers_total || 0))}</span>`}
                ${positivePct !== null ? `<span>♥ ${positivePct}%</span>` : ''}
              </div>
              <div class="browser-detail__head-actions">
                <button class="browser-detail__big-btn browser-detail__big-btn--endorse ${wasEndorsed ? 'is-active' : ''}"
                        ${endorseBusy || wasEndorsed ? 'disabled' : ''}
                        onclick="annoRoot().browserEndorse(${id})">
                  ${escapeHtml(wasEndorsed ? this.t('browser.endorsed') : this.t('browser.endorse'))}
                </button>
                <button class="browser-detail__big-btn browser-detail__big-btn--subscribe ${isSubscribed ? 'is-active' : ''}"
                        ${subBusy ? 'disabled' : ''}
                        onclick="${isCollectionTab
                          ? `annoRoot().browserToggleFollowCollection(${id}, '${escapeAttr(d.name_id || '')}')`
                          : `annoRoot().browserToggleSubscribe(${id})`}">
                  ${escapeHtml(isSubscribed
                    ? (isCollectionTab ? this.t('browser.unfollow') : this.t('browser.subscribed'))
                    : subLabel)}
                </button>
              </div>
            </div>
          </div>

          <div class="browser-detail__body">
            ${d.date_updated ? `<div class="browser-detail__updated">${escapeHtml(this.t('browser.updated', { date: fmtDate(d.date_updated) }))}</div>` : ''}

            <div class="browser-detail__actions">
              ${(isInstalled && !hasUpdate && !isCollectionTab) ? '' : `
                <button class="${installClass}"
                        ${isInstalling ? 'disabled' : ''}
                        onclick="annoRoot().browserInstall(${id})">
                  ${isInstalled && !isInstalling ? '✓ ' : ''}${escapeHtml(installLabel)}
                </button>`}
              ${(!isCollectionTab && isInstalled) ? `
                <button class="settings__btn settings__btn--danger"
                        ${isInstalling ? 'disabled' : ''}
                        onclick="annoRoot().browserUninstall(${id})">
                  ${escapeHtml(this.t('browser.uninstallMod'))}
                </button>` : ''}
              ${isCollectionTab && isInstalled ? `
                <button class="settings__btn settings__btn--danger"
                        onclick="annoRoot().browserUninstallCollection(${id})">
                  ${escapeHtml(this.t('browser.uninstallCollection'))}
                </button>` : ''}
              <button class="settings__btn"
                      onclick="annoRoot().openExternalUrl('${escapeAttr(profileUrl)}')">
                ${escapeHtml(this.t('browser.openOnModio'))}
              </button>
            </div>

            ${flashHtml}

            ${this.currentTab === 'collections' ? this._renderBrowserDeps(b, fmtNumber, fmtSize) : ''}

            ${modfile.version || modfile.filesize ? `
              <div class="browser-detail__meta">
                ${modfile.version ? `<span>${escapeHtml(this.t('browser.version', { v: modfile.version }))}</span>` : ''}
                ${modfile.filesize ? `<span>${escapeHtml(this.t('browser.size', { size: fmtSize(modfile.filesize) }))}</span>` : ''}
              </div>` : ''}

            ${descHtml || descPlain ? `
              <h3 class="browser-detail__section">${escapeHtml(this.t('browser.description'))}</h3>
              ${descHtml
                  ? `<div class="browser-detail__desc rich-text">${descHtml}</div>`
                  : `<pre class="browser-detail__desc">${escapeHtml(descPlain)}</pre>`}` : ''}

            ${modfile.changelog ? `
              <h3 class="browser-detail__section">${escapeHtml(this.t('browser.changelog'))}</h3>
              <pre class="browser-detail__changelog">${escapeHtml(modfile.changelog)}</pre>` : ''}
          </div>
        </div>`;
    },

    tweakingTemplate() {
      const t = this.tweak;
      const selected = t.mods.find((m) => m.id === t.selectedId) || null;

      // Left list of tweakable mods
      const list = t.mods.length ? t.mods.map((m) => `
        <li class="tweak-list__item ${m.id === t.selectedId ? 'is-selected' : ''}"
            onclick="annoRoot().selectTweakMod('${escapeAttr(m.id)}')">
          <div class="tweak-list__name">${escapeHtml(m.name)}</div>
          <div class="tweak-list__meta">${escapeHtml(m.category || '—')} · ${m.option_count} ${escapeHtml(this.t('tweak.optionWord'))}</div>
        </li>`).join('') : `<li class="tweak-list__empty">${escapeHtml(this.t('tweak.noTweakable'))}</li>`;

      // Right panel: dynamic form built from the schema
      let form;
      if (!selected) {
        form = `<div class="tweak-form__empty">
                  <div class="ornament">───── ◆ ─────</div>
                  ${escapeHtml(this.t('tweak.pickHint'))}
                </div>`;
      } else if (!Object.keys(t.schema).length) {
        form = `<div class="tweak-form__empty">${escapeHtml(this.t('tweak.noOptions'))}</div>`;
      } else {
        // Build {key, html, isModified} per option then split into a
        // "modified" block on top and a "defaults" block below, with a
        // gold separator between when both groups exist. Each modified
        // row also gets a `is-modified` class for the gold left rail —
        // double cue (regrouped + marked) is what the visual brief asked
        // for. Original schema order is preserved within each block.
        const items = Object.entries(t.schema).map(([key, spec]) => {
          if (!spec || typeof spec !== 'object') return null;
          const label = spec.label || key;
          const type = (spec.type || 'text').toLowerCase();
          const labels = Array.isArray(spec.labels) ? spec.labels : [];
          const values = Array.isArray(spec.values) ? spec.values : [];
          const defaultStr = String(spec.default ?? '');
          const current = t.values[key] !== undefined ? String(t.values[key]) : defaultStr;
          const isModified = current !== defaultStr;
          const savingCls = t.saving === key ? 'is-saving' : '';
          let control = '';
          let hint = '';

          if (type === 'enum') {
            control = `
              <select class="tweak-control"
                      onchange="annoRoot().setTweakOption('${escapeAttr(key)}', this.value)">
                ${values.map((v, i) => {
                  const sel = String(v) === current ? ' selected' : '';
                  const lbl = labels[i] || v;
                  return `<option value="${escapeAttr(String(v))}"${sel}>${escapeHtml(String(lbl))}</option>`;
                }).join('')}
              </select>`;
            const idx = values.indexOf(current) >= 0 ? values.indexOf(current) : values.findIndex((v) => String(v) === current);
            if (idx >= 0 && labels[idx]) hint = String(labels[idx]);

          } else if (type === 'slider') {
            const min = parseFloat(values[0]) || 0;
            const max = parseFloat(values[1]) || 100;
            const step = parseFloat(values[2]) || 1;
            const num = parseFloat(current);
            const safe = isFinite(num) ? Math.max(min, Math.min(max, num)) : min;
            control = `
              <div class="tweak-slider">
                <span class="tweak-slider__bound">${min}</span>
                <input type="range"
                       min="${min}" max="${max}" step="${step}"
                       value="${safe}"
                       oninput="this.nextElementSibling.textContent = this.value"
                       onchange="annoRoot().setTweakOption('${escapeAttr(key)}', this.value)" />
                <span class="tweak-slider__value">${safe}</span>
                <span class="tweak-slider__bound">${max}</span>
              </div>`;
            if (labels.length) hint = String(labels[0]);

          } else if (type === 'toggle') {
            const isOn = String(current).toLowerCase() === 'true';
            control = `
              <label class="tweak-toggle">
                <input type="checkbox" ${isOn ? 'checked' : ''}
                       onchange="annoRoot().setTweakOption('${escapeAttr(key)}', this.checked ? 'true' : 'false')" />
                <span class="tweak-toggle__pill ${isOn ? 'is-on' : ''}">
                  <span class="tweak-toggle__dot"></span>
                </span>
                <span class="tweak-toggle__text">${isOn ? 'ON' : 'OFF'}</span>
              </label>`;
            const lbl = labels[isOn ? 0 : 1];
            if (lbl) hint = String(lbl);

          } else { // text fallback
            // Mods that name an option after a colour ("color"/"colour", any
            // case) get a native colour picker glued to the text field. The
            // text input stays editable for power users who want to type a
            // raw signed-int ARGB value directly.
            const isColor = /colou?r/i.test(key) || /colou?r/i.test(label);
            if (isColor) {
              const hex = argbIntToHex(current);
              control = `
                <div class="tweak-color">
                  <button type="button"
                          class="tweak-color__swatch"
                          title="${escapeAttr(this.t('tweak.colorPicker.open'))}"
                          style="background:${hex}"
                          onclick="annoRoot().openColorPicker('${escapeAttr(key)}', this.nextElementSibling.value, event)"></button>
                  <input class="tweak-control tweak-color__text" type="text"
                         data-key="${escapeAttr(key)}"
                         value="${escapeAttr(current)}"
                         oninput="var h=window.argbIntToHex(this.value); if(h) this.previousElementSibling.style.background=h"
                         onchange="annoRoot().setTweakOption('${escapeAttr(key)}', this.value)" />
                </div>`;
            } else {
              control = `
                <input class="tweak-control" type="text"
                       value="${escapeAttr(current)}"
                       onchange="annoRoot().setTweakOption('${escapeAttr(key)}', this.value)" />`;
            }
            if (labels.length) hint = String(labels[0]);
          }

          const html = `
            <div class="tweak-row ${savingCls} ${isModified ? 'is-modified' : ''}">
              <div class="tweak-row__label">${escapeHtml(label)}</div>
              ${control}
              ${hint ? `<div class="tweak-row__hint">${escapeHtml(hint)}</div>` : ''}
            </div>`;
          return { html, isModified };
        }).filter(Boolean);

        const modifiedHtml = items.filter((x) => x.isModified).map((x) => x.html).join('');
        const defaultHtml  = items.filter((x) => !x.isModified).map((x) => x.html).join('');
        const separator = (modifiedHtml && defaultHtml) ? `
          <div class="tweak-form__separator">
            <span>${escapeHtml(this.t('tweak.defaultsSection'))}</span>
          </div>` : '';
        const rows = modifiedHtml + separator + defaultHtml;

        form = `
          <div class="tweak-form__header">
            <h3 class="tweak-form__title">${escapeHtml(selected.name)}</h3>
            <button class="settings__btn settings__btn--danger settings__btn--small"
                    onclick="annoRoot().resetTweakMod()">${escapeHtml(this.t('tweak.resetMod'))}</button>
          </div>
          <div class="tweak-form__rows">${rows}</div>`;
      }

      return `
        <div class="tweak">
          <aside class="tweak-list">
            <div class="tweak-list__header">
              <span>${escapeHtml(this.t('tweak.listHeader'))}</span>
              <button class="settings__btn settings__btn--small"
                      ${t.mods.length ? '' : 'disabled'}
                      onclick="annoRoot().resetAllTweaks()">${escapeHtml(this.t('tweak.resetAll'))}</button>
            </div>
            <ul>${list}</ul>
          </aside>
          <section class="tweak-form">${form}</section>
        </div>`;
    },

    installTemplate() {
      const i = this.install;
      const dropClasses = ['install__drop'];
      if (i.dragOver) dropClasses.push('is-over');
      if (i.busy)     dropClasses.push('is-busy');

      const status = i.message
        ? `<div class="install__status ${i.error ? 'is-error' : 'is-ok'}">${escapeHtml(i.message)}</div>`
        : '';

      return `
        <div class="install">
          <div class="install__inner">
            <h2 class="install__title">${escapeHtml(this.t('install.title'))}</h2>
            <p class="install__hint">${escapeHtml(this.t('install.hint'))}</p>

            <div class="${dropClasses.join(' ')}"
                 ondragenter="annoRoot().onZipDragEnter(event)"
                 ondragover="annoRoot().onZipDragOver(event)"
                 ondragleave="annoRoot().onZipDragLeave(event)"
                 ondrop="annoRoot().onZipDrop(event)"
                 onclick="annoRoot().pickAndInstall()">
              <div class="install__drop-icon">⤓</div>
              <div class="install__drop-line">${escapeHtml(this.t('install.drop'))}</div>
              <div class="install__drop-sub">${escapeHtml(this.t('install.or'))}</div>
              <button class="settings__btn settings__btn--accent install__pick"
                      onclick="event.stopPropagation(); annoRoot().pickAndInstall()">
                ${escapeHtml(this.t('install.browse'))}
              </button>
            </div>

            ${status}

            <div class="install__targets">
              <div><span>${escapeHtml(this.t('install.targetLabel'))}</span>
                <code>${escapeHtml(this.pathsInfo.documents_mods_root || (this.settings.mod_location_mode === 'GameDirectory'
                  ? (this.pathsInfo.game_mods_root || '—') : '—'))}</code>
              </div>
            </div>
          </div>
        </div>`;
    },

    logTemplate() {
      const log = this.log;
      // Colour each line based on its severity token. Stays close to the Tk
      // version's choices (red for error, amber for warn).
      const renderLines = (text) => {
        if (!text) return '';
        return text.split('\n').map((raw) => {
          const upper = raw.toUpperCase();
          let cls = '';
          if (upper.includes('[ERRO') || upper.includes('ERROR')) cls = 'log-line--error';
          else if (upper.includes('WARN')) cls = 'log-line--warn';
          else if (upper.includes('[INFO]')) cls = 'log-line--info';
          return `<div class="log-line ${cls}">${escapeHtml(raw) || '&nbsp;'}</div>`;
        }).join('');
      };

      let body;
      if (!log.loaded) {
        body = `<div class="log-view__empty">${escapeHtml(this.t('log.loading'))}</div>`;
      } else if (!log.exists) {
        body = `<div class="log-view__empty">${escapeHtml(this.t('log.notFound', { path: log.path || '?' }))}</div>`;
      } else if (!log.content) {
        body = `<div class="log-view__empty">${escapeHtml(this.t('log.empty'))}</div>`;
      } else {
        body = renderLines(log.content);
      }

      return `
        <div class="log-view">
          <div class="log-view__toolbar">
            <button class="settings__btn" onclick="annoRoot().refreshLog()">${escapeHtml(this.t('log.refresh'))}</button>
            <button class="settings__btn" onclick="annoRoot().copyLogToClipboard()"
                    ${log.exists && log.content ? '' : 'disabled'}>${escapeHtml(this.t('log.copy'))}</button>
            <button class="settings__btn"
                    ${log.path ? '' : 'disabled'}
                    onclick="annoRoot().openModFolder('${escapeAttr(log.path || '')}')">${escapeHtml(this.t('log.openFile'))}</button>
            <span class="log-view__path" title="${escapeAttr(log.path || '')}">${escapeHtml(log.path || '—')}</span>
            ${log.truncated ? `<span class="log-view__warn">${escapeHtml(this.t('log.truncated'))}</span>` : ''}
          </div>
          <div class="log-view__body">${body}</div>
        </div>`;
    },

    _renderModioBadge() {
      const s = this.modioStatus;
      if (s.token_valid) {
        return `<span class="settings__badge is-on">${escapeHtml(this.t('modio.badge.connected'))}</span>`;
      }
      if (s.api_key_set) {
        return `<span class="settings__badge is-pending">${escapeHtml(this.t('modio.badge.keyOnly'))}</span>`;
      }
      return `<span class="settings__badge is-off">${escapeHtml(this.t('modio.badge.notSet'))}</span>`;
    },

    _renderModioAuth() {
      const a = this.modioAuth;
      const s = this.modioStatus;
      const error = a.error
        ? `<div class="settings__inline-error">${escapeHtml(a.error)}</div>` : '';

      // Connected state — show expiry + Disconnect, no auth form
      if (s.token_valid) {
        return `
          <div class="settings__row settings__row--inline modio-connected">
            <span class="settings__label">${escapeHtml(this.t('modio.session'))}</span>
            <span class="modio-expiry">${escapeHtml(this.t('modio.expires', { date: s.expires_text || '?' }))}</span>
            <button class="settings__btn settings__btn--danger settings__btn--small"
                    onclick="annoRoot().modioDisconnect()">
              ${escapeHtml(this.t('modio.disconnect'))}
            </button>
          </div>`;
      }

      // No API key — block any auth attempt with a hint
      if (!s.api_key_set) {
        return `
          <div class="settings__inline-hint">
            ${escapeHtml(this.t('modio.needKeyFirst'))}
          </div>`;
      }

      // API key set, no valid token — drive the email→code state machine
      if (a.step === 'email') {
        return `
          <div class="settings__row modio-auth">
            <label class="settings__label">${escapeHtml(this.t('modio.email'))}</label>
            <div class="settings__field">
              <input class="settings__input" id="modio-email-input" type="email"
                     placeholder="${escapeAttr(this.t('modio.emailPlaceholder'))}"
                     value="${escapeAttr(a.email)}"
                     onkeydown="if(event.key==='Enter'){annoRoot().modioSubmitEmail()}" />
            </div>
            <label class="settings__radio modio-terms">
              <input type="checkbox" ${a.termsAgreed ? 'checked' : ''}
                     onchange="annoRoot().modioAuth.termsAgreed = this.checked" />
              <span>${escapeHtml(this.t('modio.termsAgree'))}
                <a class="settings__link"
                   onclick="annoRoot().openExternalUrl('https://mod.io/terms')">${escapeHtml(this.t('modio.termsLink'))}</a>
              </span>
            </label>
            ${error}
            <div class="settings__actions">
              <button class="settings__btn"
                      onclick="annoRoot().modioCancelConnect()">${escapeHtml(this.t('modio.cancel'))}</button>
              <button class="settings__btn settings__btn--accent"
                      ${a.busy ? 'disabled' : ''}
                      onclick="annoRoot().modioSubmitEmail()">
                ${escapeHtml(this.t(a.busy ? 'modio.sending' : 'modio.sendCode'))}
              </button>
            </div>
          </div>`;
      }

      if (a.step === 'code') {
        return `
          <div class="settings__row modio-auth">
            <label class="settings__label">${escapeHtml(this.t('modio.code'))}</label>
            <div class="settings__inline-hint">
              ${escapeHtml(this.t('modio.codeSent', { email: a.email }))}
            </div>
            <div class="settings__field">
              <input class="settings__input modio-code" id="modio-code-input"
                     placeholder="XXXXX" maxlength="5"
                     value="${escapeAttr(a.code)}"
                     oninput="this.value = this.value.toUpperCase()"
                     onkeydown="if(event.key==='Enter'){annoRoot().modioSubmitCode()}" />
            </div>
            ${error}
            <div class="settings__actions">
              <button class="settings__btn"
                      onclick="annoRoot().modioCancelConnect()">${escapeHtml(this.t('modio.cancel'))}</button>
              <button class="settings__btn settings__btn--accent"
                      ${a.busy ? 'disabled' : ''}
                      onclick="annoRoot().modioSubmitCode()">
                ${escapeHtml(this.t(a.busy ? 'modio.connecting' : 'modio.connect'))}
              </button>
            </div>
          </div>`;
      }

      // Idle, with API key — invite to start the flow
      return `
        <div class="settings__row settings__row--inline modio-auth-idle">
          <button class="settings__btn settings__btn--accent"
                  onclick="annoRoot().modioStartConnect()">
            ${escapeHtml(this.t('modio.startConnect'))}
          </button>
        </div>`;
    },

    settingsTemplate() {
      const p = this.pathsInfo || {};
      const gameSet = !!(p.game_path && p.game_path_exists);
      const docsSet = !!(p.custom_docs_path && p.custom_docs_path_exists);
      const modLoc = this.settings.mod_location_mode || 'Documents';
      const enableNew = this.settings.enable_new_mods || 'on';
      return `
        <div class="settings">
          <div class="settings__inner">

            <section class="settings__card">
              <h3 class="settings__title">${escapeHtml(this.t('settings.section.paths'))}</h3>

              <div class="settings__row">
                <label class="settings__label">${escapeHtml(this.t('settings.gamePath'))}</label>
                <div class="settings__field">
                  <input class="settings__input" type="text" readonly
                         value="${escapeAttr(p.game_path || '')}"
                         placeholder="${escapeAttr(this.t('settings.gamePath.empty'))}" />
                  <span class="settings__status ${gameSet ? 'is-ok' : 'is-bad'}">${gameSet ? '✓' : '✕'}</span>
                </div>
                <div class="settings__actions">
                  <button class="settings__btn" onclick="annoRoot().pickGamePath(true)">${escapeHtml(this.t('settings.browseFile'))}</button>
                  <button class="settings__btn" onclick="annoRoot().pickGamePath(false)">${escapeHtml(this.t('settings.browseFolder'))}</button>
                  <button class="settings__btn settings__btn--accent" onclick="annoRoot().detectGamePath()">${escapeHtml(this.t('settings.autoDetect'))}</button>
                </div>
              </div>

              <div class="settings__row">
                <label class="settings__label">${escapeHtml(this.t('settings.docsPath'))}</label>
                <div class="settings__field">
                  <input class="settings__input" type="text" readonly
                         value="${escapeAttr(p.custom_docs_path || '')}"
                         placeholder="${escapeAttr(this.t('settings.docsPath.empty'))}" />
                  <span class="settings__status ${docsSet ? 'is-ok' : ''}">${docsSet ? '✓' : '–'}</span>
                </div>
                <div class="settings__actions">
                  <button class="settings__btn" onclick="annoRoot().pickDocsPath()">${escapeHtml(this.t('settings.browseFolder'))}</button>
                  <button class="settings__btn settings__btn--danger"
                          ${docsSet ? '' : 'disabled'}
                          onclick="annoRoot().clearDocsPath()">${escapeHtml(this.t('settings.clear'))}</button>
                </div>
              </div>

              <div class="settings__derived">
                <div><span>${escapeHtml(this.t('settings.derived.docsMods'))}</span><code>${escapeHtml(p.documents_mods_root || '—')}</code></div>
                <div><span>${escapeHtml(this.t('settings.derived.gameMods'))}</span><code>${escapeHtml(p.game_mods_root || '—')}</code></div>
                <div><span>${escapeHtml(this.t('settings.derived.profile'))}</span><code>${escapeHtml(p.active_profile_path || '—')}</code></div>
              </div>
            </section>

            <section class="settings__card">
              <h3 class="settings__title">${escapeHtml(this.t('settings.section.behaviour'))}</h3>

              <div class="settings__row settings__row--inline">
                <label class="settings__label">${escapeHtml(this.t('settings.modLocation'))}</label>
                <div class="settings__radio-group">
                  <label class="settings__radio">
                    <input type="radio" name="mod_location_mode" value="Documents"
                           ${modLoc === 'Documents' ? 'checked' : ''}
                           onchange="annoRoot().setSetting('mod_location_mode','Documents')" />
                    <span>${escapeHtml(this.t('settings.modLocation.documents'))}</span>
                  </label>
                  <label class="settings__radio">
                    <input type="radio" name="mod_location_mode" value="GameDirectory"
                           ${modLoc === 'GameDirectory' ? 'checked' : ''}
                           onchange="annoRoot().setSetting('mod_location_mode','GameDirectory')" />
                    <span>${escapeHtml(this.t('settings.modLocation.game'))}</span>
                  </label>
                </div>
              </div>

              <div class="settings__row settings__row--inline">
                <label class="settings__label">${escapeHtml(this.t('settings.enableNewMods'))}</label>
                <select class="activation__profile"
                        onchange="annoRoot().setSetting('enable_new_mods', this.value)">
                  <option value="on" ${enableNew === 'on' ? 'selected' : ''}>${escapeHtml(this.t('settings.enableNewMods.on'))}</option>
                  <option value="off" ${enableNew === 'off' ? 'selected' : ''}>${escapeHtml(this.t('settings.enableNewMods.off'))}</option>
                  <option value="keep" ${enableNew === 'keep' ? 'selected' : ''}>${escapeHtml(this.t('settings.enableNewMods.keep'))}</option>
                </select>
              </div>

              <div class="settings__row settings__row--inline">
                <label class="settings__label">${escapeHtml(this.t('settings.textScale'))}</label>
                <div class="settings__radio-group">
                  ${['small','medium','large'].map((sz) => `
                    <label class="settings__radio">
                      <input type="radio" name="text_scale" value="${sz}"
                             ${(this.settings.text_scale || 'small') === sz ? 'checked' : ''}
                             onchange="annoRoot().setTextScale('${sz}')" />
                      <span>${escapeHtml(this.t('settings.textScale.' + sz))}</span>
                    </label>`).join('')}
                </div>
              </div>
            </section>

            <section class="settings__card" id="settings-modio-card">
              <h3 class="settings__title settings__title--with-logo">
                <img class="settings__logo" src="icons/modio.png" alt="mod.io" />
                <span>${escapeHtml(this.t('settings.section.modio'))}</span>
                ${this._renderModioBadge()}
              </h3>
              <p class="settings__hint">${escapeHtml(this.t('settings.modio.hint'))}
                <a class="settings__link" href="https://mod.io/me/access"
                   onclick="event.preventDefault(); annoRoot().openExternalUrl('https://mod.io/me/access')">https://mod.io/me/access</a>
              </p>
              <div class="settings__row">
                <label class="settings__label">${escapeHtml(this.t('settings.modio.apiKey'))}</label>
                <div class="settings__field">
                  <input class="settings__input" type="password"
                         x-ref="modioKey"
                         value="${escapeAttr(this.settings.modio_api_key || '')}"
                         placeholder="${escapeAttr(this.t('settings.modio.apiKeyPlaceholder'))}" />
                  <span class="settings__status ${this.settings.modio_api_key ? 'is-ok' : ''}">${this.settings.modio_api_key ? '✓' : '–'}</span>
                </div>
                <div class="settings__actions">
                  <button class="settings__btn settings__btn--accent"
                          onclick="annoRoot().saveModioKey($refs.modioKey.value)">${escapeHtml(this.t('settings.modio.save'))}</button>
                  <button class="settings__btn settings__btn--danger"
                          ${this.settings.modio_api_key ? '' : 'disabled'}
                          onclick="annoRoot().clearModioKey()">${escapeHtml(this.t('settings.modio.clearKey'))}</button>
                </div>
              </div>

              ${this._renderModioAuth()}
            </section>

            <section class="settings__card">
              <h3 class="settings__title">${escapeHtml(this.t('settings.section.advanced'))}</h3>
              <div class="settings__derived">
                <div><span>${escapeHtml(this.t('settings.derived.appdata'))}</span>
                  <code>${escapeHtml(p.appdata_dir || '—')}</code>
                  <button class="settings__btn settings__btn--small"
                          onclick="annoRoot().openModFolder('${escapeAttr(p.appdata_dir || '')}')">${escapeHtml(this.t('settings.open'))}</button>
                </div>
                <div><span>${escapeHtml(this.t('settings.derived.presets'))}</span>
                  <code>${escapeHtml(p.presets_dir || '—')}</code>
                  <button class="settings__btn settings__btn--small"
                          onclick="annoRoot().openModFolder('${escapeAttr(p.presets_dir || '')}')">${escapeHtml(this.t('settings.open'))}</button>
                </div>
              </div>
            </section>

          </div>
        </div>`;
    },

    activationTemplate() {
      // Returned as a single HTML string and injected via x-html so the POC
      // stays in one file. Phase 2 will split this into Alpine components or
      // a small templating helper; for now it keeps the structure obvious.
      const orderMode = this.mode === 'order';

      // Build once per render so renderRow lookups are O(1)
      const modById = {};
      for (const m of this.mods) modById[m.id] = m;
      // Map: mod_id → names of active mods that declare it incompatible (deprecated-by)
      const deprecatedByMap = {};
      for (const o of this.mods) {
        if (!o.active) continue;
        for (const depId of (o.deps_incompatible || [])) {
          if (!deprecatedByMap[depId]) deprecatedByMap[depId] = [];
          deprecatedByMap[depId].push(o.name || o.id);
        }
      }

      const renderRow = (m, isSubMod = false) => {
        const active = m.active ? 'is-on' : '';
        const selected = m.id === this.selectedModId ? 'is-selected' : '';
        const subClass = isSubMod ? 'mod-row--sub' : '';
        const dragClass = orderMode && !isSubMod ? 'mod-row--draggable' : '';
        const category = m.category || '—';
        const initials = (category || '?').slice(0, 2).toUpperCase();
        const dragAttrs = (orderMode && !isSubMod) ? `
              draggable="true"
              ondragstart="annoRoot().onDragStart('${escapeAttr(m.id)}', event)"
              ondragover="annoRoot().onDragOver(event)"
              ondrop="annoRoot().onDrop('${escapeAttr(m.id)}', event)"
              ondragend="annoRoot().onDragEnd()"` : '';
        // ── Dependency checks (top-level active mods only) ──────────────
        const depConflictNames    = (!isSubMod && m.active)
          ? (m.deps_incompatible || []).filter(id => modById[id] && modById[id].active)
              .map(id => modById[id].name || id)
          : [];
        const depMissingInstNames = (!isSubMod && m.active)
          ? (m.deps_require || []).filter(id => !modById[id])
          : [];
        const depMissingActNames  = (!isSubMod && m.active)
          ? (m.deps_require || []).filter(id => modById[id] && !modById[id].active)
              .map(id => modById[id].name || id)
          : [];
        const depDeprecatedBy     = (!isSubMod && m.active)
          ? (deprecatedByMap[m.id] || [])
          : [];
        const hasConflict   = depConflictNames.length > 0;
        const hasMissingDep = depMissingInstNames.length > 0 || depMissingActNames.length > 0;
        const isDeprecated  = !hasConflict && !hasMissingDep && depDeprecatedBy.length > 0;
        const hasDepWarn    = hasConflict || hasMissingDep || isDeprecated;

        // Per-row actions: the Update icon only shows up when there's an
        // actual newer modfile on mod.io for this folder; the Uninstall
        // icon is always there for top-level mods (sub-mods uninstall with
        // their parent). Manually-installed mods (no marker) get a small
        // info bullet so the user knows why no Update is offered.
        const fromManager    = !isSubMod && this.modIsFromManager(m);
        const showUpdate     = !isSubMod && this.modUpdateAvailable(m);
        const managerMid     = !isSubMod ? this.modManagerModId(m) : 0;
        const showInfo       = !isSubMod && !fromManager;
        const showUninst     = !isSubMod;
        const showVerWarn    = !isSubMod && this.modVersionMismatch(m);
        const remoteVer      = showVerWarn ? (() => {
          const r = this.modUpdates[this.modManagerModId(m)];
          return r ? this._normVer(r.version) : '';
        })() : '';
        // Warn badge is clickable to update when remote > local; info-only otherwise
        const warnClickable  = showVerWarn && showUpdate;
        // Distinguish: same modfile (author label inconsistency) vs local is newer
        const warnSameFile   = showVerWarn && !showUpdate && (() => {
          const mid2 = this.modManagerModId(m);
          const loc2 = (this.browser.installedMeta || {})[mid2];
          const rem2 = this.modUpdates[mid2];
          return !!(loc2 && rem2 && loc2.modfile_id === rem2.modfile_id);
        })();
        const warnTitle      = showVerWarn
          ? warnClickable
            ? this.t('mods.versionMismatch',         { lv: this._normVer(m.version), rv: remoteVer })
            : warnSameFile
              ? this.t('mods.versionMismatchSameFile', { lv: this._normVer(m.version), rv: remoteVer })
              : this.t('mods.versionMismatchInfo',     { lv: this._normVer(m.version), rv: remoteVer })
          : '';
        // ↻ only shown when modfile is newer but no version-string mismatch detected
        const showUpdateBtn  = showUpdate && !showVerWarn;

        // Dep badge tooltip text
        const depBadgeTitle = hasConflict
          ? this.t('deps.conflict',          { names: depConflictNames.join(', ') })
          : hasMissingDep
            ? (depMissingInstNames.length
                ? this.t('deps.missingInstalled', { names: depMissingInstNames.join(', ') })
                : this.t('deps.missingActive',    { names: depMissingActNames.join(', ') }))
            : isDeprecated
              ? this.t('deps.deprecated',        { names: depDeprecatedBy.join(', ') })
              : '';
        const depBadgeLabel = hasConflict ? '✘' : isDeprecated ? '↓' : '!';

        const actions = (hasDepWarn || showVerWarn || showUpdateBtn || showUninst || showInfo) ? `
            <div class="mod-row__actions" onclick="event.stopPropagation()">
              ${showInfo ? `
                <button class="mod-row__action mod-row__action--link"
                        title="${escapeAttr(this.t('mods.notFromManager') + ' — ' + this.t('mods.link.cta'))}"
                        onclick="annoRoot().openLinkPicker('${escapeAttr(m.folder)}', '${escapeAttr(m.name)}')">🔗</button>` : ''}
              ${hasDepWarn ? (() => {
                const dtype = hasConflict ? 'conflict'
                            : hasMissingDep
                              ? (depMissingInstNames.length ? 'missingInstalled' : 'missingActive')
                              : 'deprecated';
                const ditems = hasConflict
                  ? depConflictNames.map((n, i) => ({ id: (m.deps_incompatible||[])[i], name: n }))
                  : hasMissingDep
                    ? (depMissingInstNames.length
                        ? depMissingInstNames.map(id => ({ id, name: id }))
                        : depMissingActNames.map((n, i) => ({ id: (m.deps_require||[])[i], name: n })))
                    : depDeprecatedBy.map(n => ({ id: '', name: n }));
                const ditemsJson = escapeAttr(JSON.stringify(ditems));
                return `<button class="mod-row__action ${hasConflict ? 'mod-row__action--conflict' : 'mod-row__action--dep-warn'}"
                        title="${escapeAttr(depBadgeTitle)}"
                        onclick="event.stopPropagation(); annoRoot().openDepDialog('${escapeAttr(m.id)}','${escapeAttr(m.name)}','${dtype}',JSON.parse(this.dataset.items))"
                        data-items="${ditemsJson}">${depBadgeLabel}</button>`;
              })() : ''}
              ${showVerWarn ? `
                <button class="mod-row__action mod-row__action--version-warn${warnClickable ? '' : ' mod-row__action--version-warn-info'}"
                        title="${escapeAttr(warnTitle)}"
                        ${warnClickable ? `onclick="annoRoot().activationUpdate(${managerMid})"` : 'style="cursor:default"'}>!</button>` : ''}
              ${showUpdateBtn ? `
                <button class="mod-row__action mod-row__action--update"
                        title="${escapeAttr(this.t('browser.update'))}"
                        onclick="annoRoot().activationUpdate(${managerMid})">↻</button>` : ''}
              ${showUninst ? `
                <button class="mod-row__action mod-row__action--uninstall"
                        title="${escapeAttr(this.t('detail.uninstall'))}"
                        onclick="annoRoot().activationUninstall('${escapeAttr(m.folder)}', '${escapeAttr(m.name)}')">🗑</button>` : ''}
            </div>` : '';
        // Name colour: red for conflict, orange for dep issues, default otherwise
        const nameClass = hasConflict ? 'mod-row__name--conflict'
                        : hasDepWarn  ? 'mod-row__name--dep-warn'
                        : '';
        return `
          <li class="mod-row ${selected} ${subClass} ${dragClass}"
              onclick="annoRoot().selectMod('${escapeAttr(m.id)}')"
              ${dragAttrs}>
            <span class="mod-row__check ${active}"
                  onclick="event.stopPropagation(); annoRoot().toggleMod('${escapeAttr(m.id)}')"></span>
            <span class="mod-row__medallion">${orderMode && !isSubMod ? '⋮⋮' : initials}</span>
            <span class="mod-row__category-cell">${escapeHtml(category)}</span>
            <div class="mod-row__text">
              <div class="mod-row__name ${nameClass}">${escapeHtml(m.name)}</div>
              <div class="mod-row__version">v${escapeHtml(m.version)}</div>
            </div>
            <span class="mod-row__size">${this.formatSize(m.size_bytes)}</span>
            <span class="pill ${m.active ? '' : 'pill--ghost'}">${escapeHtml(m.active ? this.t('pill.active') : this.t('pill.off'))}</span>
            ${actions}
          </li>`;
      };

      const sourceMods = orderMode ? this.orderedTopLevelMods : this.filteredMods;
      const rows = sourceMods.flatMap((m) => {
        const own = renderRow(m, false);
        // In order mode we hide sub-mods to keep the drag-drop list flat;
        // they'll come along with their parent in the saved order.
        const subs = orderMode ? [] : this.subModsOf(m.path).map((s) => renderRow(s, true));
        return [own, ...subs];
      }).join('');

      const sel = this.selectedMod;
      const banner = sel && this.selectedBannerUrl
        ? `<img class="mod-detail__banner" src="${this.selectedBannerUrl}" alt="" />`
        : `<div class="mod-detail__banner mod-detail__banner--placeholder">
             <div class="ornament">───── ◆ ─────</div>
             ${sel ? escapeHtml(this.t('detail.banner.empty')) : ''}
           </div>`;

      const detail = sel ? `
        ${banner}
        <div class="mod-detail__header">
          <h3 class="mod-detail__title">${escapeHtml(sel.name)}</h3>
          <div class="mod-detail__creator">${escapeHtml(this.t('detail.creator', { name: sel.creator || '?', version: sel.version }))}</div>
        </div>
        ${sel.description ? `
        <div class="mod-detail__section">
          <h4>${escapeHtml(this.t('detail.description'))}</h4>
          <p>${escapeHtml(sel.description)}</p>
        </div>` : ''}
        <div class="mod-detail__section">
          <h4>${escapeHtml(this.t('detail.details'))}</h4>
          <dl class="mod-detail__meta">
            <dt>${escapeHtml(this.t('detail.meta.category'))}</dt><dd>${escapeHtml(sel.category || '—')}</dd>
            <dt>${escapeHtml(this.t('detail.meta.difficulty'))}</dt><dd>${escapeHtml(sel.difficulty)}</dd>
            <dt>${escapeHtml(this.t('detail.meta.size'))}</dt><dd>${this.formatSize(sel.size_bytes)}</dd>
            <dt>${escapeHtml(this.t('detail.meta.folder'))}</dt><dd>${escapeHtml(sel.folder || basename(sel.path))}</dd>
          </dl>
        </div>
        <div class="mod-detail__actions">
          <button class="mod-detail__btn"
                  onclick="annoRoot().openModFolder('${escapeAttr(sel.path)}')">
            ${escapeHtml(this.t('detail.openFolder'))}
          </button>
          ${sel.parent_path ? '' : `
          <button class="mod-detail__btn mod-detail__btn--danger"
                  onclick="annoRoot().uninstallMod('${escapeAttr(sel.folder)}', '${escapeAttr(sel.name)}')">
            ${escapeHtml(this.t('detail.uninstall'))}
          </button>`}
        </div>` : `
        <div class="mod-detail__empty">
          <div class="ornament">───── ◆ ─────</div>
          ${escapeHtml(this.t('detail.empty'))}
        </div>`;

      const totalSize = this.formatSize(this.totalSizeBytes);
      const activeSize = this.formatSize(this.activeSizeBytes);

      const allProfiles = ['Default', 'Vanilla', ...this.presets];
      const profileOpts = allProfiles.map((p) => {
        const sel = p === this.profileName ? ' selected' : '';
        return `<option value="${escapeAttr(p)}"${sel}>${escapeHtml(p)}</option>`;
      }).join('');
      const isReserved = this.profileName === 'Default' || this.profileName === 'Vanilla';

      return `
        <div class="activation">
          <div class="activation__toolbar">
            <label>${escapeHtml(this.t('profile.label'))}</label>
            <select class="activation__profile"
                    onchange="annoRoot().switchProfile(this.value)">
              ${profileOpts}
            </select>
            <button class="activation__btn"
                    onclick="annoRoot().createPreset()">${escapeHtml(this.t('profile.new'))}</button>
            <button class="activation__btn activation__btn--danger"
                    onclick="annoRoot().deletePreset()"
                    ${isReserved ? 'disabled' : ''}>${escapeHtml(this.t('profile.delete'))}</button>

            <div class="activation__mode">
              <button class="activation__mode-btn ${this.mode === 'manage' ? 'is-active' : ''}"
                      onclick="annoRoot().setMode('manage')"
                      title="${escapeAttr(this.t('mode.manage.title'))}">${escapeHtml(this.t('mode.manage'))}</button>
              <button class="activation__mode-btn ${this.mode === 'order' ? 'is-active' : ''}"
                      onclick="annoRoot().setMode('order')"
                      title="${escapeAttr(this.t('mode.order.title'))}">${escapeHtml(this.t('mode.order'))}</button>
            </div>

            <span class="activation__count">${escapeHtml(this.t('count.active', { n: this.activeCount, total: this.topLevelMods.length }))}</span>
            <span class="activation__count activation__count--size">${activeSize} / ${totalSize}</span>
          </div>

          <div class="activation__list-wrap">
            <div class="mod-row mod-row--head">
              <span class="mod-row__check mod-row__check--head mod-row__check--${this.headerSelectionState}"
                    onclick="annoRoot().toggleAllFromHeader()"
                    title="${escapeAttr(this.t('list.head.toggleAll'))}"></span>
              <span></span>
              <span class="mod-row__head ${orderMode ? 'is-disabled' : ''}"
                    ${orderMode ? '' : `onclick="annoRoot().setSort('category')"`}>${escapeHtml(this.t('list.head.category'))} ${orderMode ? '' : this.sortIndicator('category')}</span>
              <span class="mod-row__head ${orderMode ? 'is-disabled' : ''}"
                    ${orderMode ? '' : `onclick="annoRoot().setSort('name')"`}>${escapeHtml(this.t('list.head.name'))} ${orderMode ? '' : this.sortIndicator('name')}</span>
              <span class="mod-row__head">${escapeHtml(this.t('list.head.size'))}</span>
              <span class="mod-row__head ${orderMode ? 'is-disabled' : ''}"
                    ${orderMode ? '' : `onclick="annoRoot().setSort('status')"`}>${escapeHtml(this.t('list.head.status'))} ${orderMode ? '' : this.sortIndicator('status')}</span>
              <span><!-- actions column --></span>
            </div>
            <ul class="activation__list">
              ${this.topLevelMods.length ? rows : `<li class="mod-detail__empty">${escapeHtml(this.t('list.empty'))}</li>`}
            </ul>
          </div>

          <aside class="mod-detail">
            ${detail}
          </aside>
        </div>`;
    },
  };
};

// ── helpers ────────────────────────────────────────────────────────────────
function escapeHtml(s) {
  if (s == null) return '';
  return String(s)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#39;');
}

/** Sanitise mod.io's user-submitted HTML before injecting it into the
 *  detail panel. mod.io already strips dangerous tags server-side, but we
 *  belt-and-braces filter to a known-good allowlist:
 *    - Allow basic structural + inline tags used by their description
 *      editor (h1-h4, p, ul/ol/li, strong/b, em/i, br, blockquote, code,
 *      pre, hr, a). Drop everything else (including style, script, iframe,
 *      img, on*= attributes).
 *    - On <a>, keep only http(s) hrefs and force target=_blank rel=noopener.
 *  Implemented via DOMParser so we don't ship a regex-based sanitiser
 *  (which is famously hard to get right). */
const _SAFE_HTML_TAGS = new Set([
  'h1','h2','h3','h4','h5','h6','p','ul','ol','li','strong','b','em','i',
  'br','blockquote','code','pre','hr','a','div','span',
  // Anno Union wraps post images in <figure><img></figure>. URL allowlist
  // restricts img src to http(s) only — no data: or javascript: schemes.
  // <video> would be the natural fit for WP's native video shortcode but
  // WebKit2GTK 2.50 corrupts the GPU-decoded buffer (visible green/purple
  // glitch on H.264 MP4s) so we don't keep it as <video>; instead it's
  // rewritten to a thumbnail link that opens externally — see
  // _sanitizeModioHtmlImpl below.
  'img','figure','figcaption',
]);
// Memoise sanitiser output. Alpine re-runs renderTab on every reactive
// tick (e.g. every keystroke in any bound input), and DOMParser + walk
// on a long mod description is non-trivial. Key on the raw HTML so a
// switch to another mod naturally misses. Cap at 10 entries.
const _sanitizeCache = new Map();
function sanitizeModioHtml(html) {
  if (!html) return '';
  if (_sanitizeCache.has(html)) {
    const v = _sanitizeCache.get(html);
    _sanitizeCache.delete(html);
    _sanitizeCache.set(html, v); // LRU touch
    return v;
  }
  const out = _sanitizeModioHtmlImpl(html);
  _sanitizeCache.set(html, out);
  while (_sanitizeCache.size > 10) {
    _sanitizeCache.delete(_sanitizeCache.keys().next().value);
  }
  return out;
}
function _sanitizeModioHtmlImpl(html) {
  let doc;
  try {
    doc = new DOMParser().parseFromString(`<div id="root">${html}</div>`, 'text/html');
  } catch (_) {
    return '';
  }
  const root = doc.getElementById('root');
  if (!root) return '';
  const walk = (node) => {
    // Iterate over a static copy so removal during the loop is safe.
    for (const child of Array.from(node.childNodes)) {
      if (child.nodeType === 1) {
        const tag = child.tagName.toLowerCase();
        if (!_SAFE_HTML_TAGS.has(tag)) {
          // Replace the unsafe element with its (sanitised) text content
          // so we never lose the user's words, only the markup.
          const text = doc.createTextNode(child.textContent || '');
          child.replaceWith(text);
          continue;
        }
        // Strip every attribute. <a> hrefs are restored from the snapshot
        // captured below the recursion (we can't read the attribute from
        // here once we've nuked it, hence the two-pass approach).
        const attrs = Array.from(child.attributes);
        for (const a of attrs) child.removeAttribute(a.name);
        walk(child);
      } else if (child.nodeType !== 3 /* text */) {
        // Comments etc. — drop.
        child.remove();
      }
    }
  };

  // Replace each <video> with a thumbnail-link that opens the MP4
  // externally — done BEFORE the href/img capture below so the new <a>
  // and <img> we create get picked up by the standard preservation pass.
  // The link is tagged `data-external` so the article-level click handler
  // routes it through openExternalUrl instead of letting the webview try
  // to navigate to a raw MP4 URL.
  for (const v of Array.from(root.querySelectorAll('video'))) {
    const sourceEl = v.querySelector('source');
    const mp4 = sourceEl ? (sourceEl.getAttribute('src') || '') : '';
    if (!/^https?:\/\//i.test(mp4)) { v.remove(); continue; }
    const poster = v.getAttribute('poster') || '';
    const a = doc.createElement('a');
    a.setAttribute('href', mp4);
    a.setAttribute('data-external', '1');
    a.className = 'news-detail__video-link';
    if (/^https?:\/\//i.test(poster)) {
      const im = doc.createElement('img');
      im.setAttribute('src', poster);
      a.appendChild(im);
    }
    const play = doc.createElement('span');
    play.className = 'news-detail__video-play';
    play.textContent = '▶';
    a.appendChild(play);
    v.replaceWith(a);
  }

  // Capture hrefs + img src/alt BEFORE we strip attributes — keyed by element
  // identity so we can restore them on still-connected nodes after walk().
  const hrefs = new Map();
  for (const a of root.querySelectorAll('a')) {
    const h = a.getAttribute('href') || '';
    if (/^https?:\/\//i.test(h)) hrefs.set(a, h);
  }
  // Tagged class on the video links so we can re-apply it after walk()
  // (the attribute strip in walk would otherwise remove it and the
  // preservation loop below only restores href).
  const videoLinks = new Set(root.querySelectorAll('a.news-detail__video-link'));
  const imgs = new Map();
  for (const im of root.querySelectorAll('img')) {
    const src = im.getAttribute('src') || '';
    const alt = im.getAttribute('alt') || '';
    if (/^https?:\/\//i.test(src)) imgs.set(im, { src, alt });
  }
  walk(root);
  // Re-apply hrefs + force safe link attributes.
  for (const [a, href] of hrefs) {
    if (!a.isConnected) continue;
    a.setAttribute('href', href);
    a.setAttribute('target', '_blank');
    a.setAttribute('rel', 'noopener noreferrer');
  }
  // Re-apply img src/alt + lazy-load hint. Any img whose original src
  // wasn't http(s) (data:, javascript:, ...) was not captured above and
  // is now orphan — drop it so we don't render a broken <img>.
  for (const im of root.querySelectorAll('img')) {
    if (imgs.has(im)) {
      const { src, alt } = imgs.get(im);
      im.setAttribute('src', src);
      if (alt) im.setAttribute('alt', alt);
      im.setAttribute('loading', 'lazy');
    } else {
      im.remove();
    }
  }
  // Restore the video-link tag + the data-external marker so the
  // article-level click handler can route it to the OS browser.
  for (const a of videoLinks) {
    if (!a.isConnected) continue;
    a.setAttribute('class', 'news-detail__video-link');
    a.setAttribute('data-external', '1');
  }
  return root.innerHTML;
}

// For values interpolated INSIDE single-quoted attributes built in template
// strings (e.g. onclick="...('${val}')"). Escapes both ' and \ so a folder
// name with an apostrophe doesn't break the markup or the JS arg list.
function escapeAttr(s) {
  if (s == null) return '';
  return String(s)
    .replace(/\\/g, '\\\\')
    .replace(/'/g, "\\'")
    .replace(/"/g, '&quot;');
}

function basename(p) {
  if (!p) return '';
  return p.split(/[\\/]/).pop();
}

// In-game player-banner palette from Anno 117 — eyeballed off the colour
// picker screen so the picker offers the same shortcuts a player sees in
//-game. Order roughly mirrors the in-game grid (6 columns × 5 rows).
// Swap individual values if/when extracted from the game files.
const ANNO_PALETTE = [
  '#3960a8', '#6f3a7e', '#d4b133', '#4f9b5b', '#4fb3ce', '#c33531',
  '#2a1c1a', '#d4751b', '#2c3563', '#d83435', '#4ec535', '#2972d3',
  '#f0d34a', '#cc4ec0', '#4ec5b8', '#1e1c19', '#d8d8c8', '#1d6d80',
  '#e8a6c5', '#d39c5c', '#4dba47', '#d3d33c', '#b9d651', '#1a3260',
  '#2a5036', '#b27ec8', '#696969', '#1a4d4a', '#6e2828', '#2a677a',
];

// HSV/RGB conversion utilities used by the in-app colour picker. HSV is the
// natural model for the picker UI (saturation/value square + hue slider) but
// the wire format is RGB hex, so every interaction round-trips through both.
function hsvToRgb(h, s, v) {
  h = ((h % 360) + 360) % 360;
  const c = v * s;
  const x = c * (1 - Math.abs(((h / 60) % 2) - 1));
  const m = v - c;
  let r = 0, g = 0, b = 0;
  if (h < 60)       { r = c; g = x; }
  else if (h < 120) { r = x; g = c; }
  else if (h < 180) { g = c; b = x; }
  else if (h < 240) { g = x; b = c; }
  else if (h < 300) { r = x; b = c; }
  else              { r = c; b = x; }
  return [Math.round((r + m) * 255), Math.round((g + m) * 255), Math.round((b + m) * 255)];
}
function rgbToHsv(r, g, b) {
  r /= 255; g /= 255; b /= 255;
  const max = Math.max(r, g, b), min = Math.min(r, g, b);
  const d = max - min;
  let h = 0;
  if (d > 0) {
    if (max === r)      h = ((g - b) / d) % 6;
    else if (max === g) h = (b - r) / d + 2;
    else                h = (r - g) / d + 4;
    h *= 60;
    if (h < 0) h += 360;
  }
  return [h, max === 0 ? 0 : d / max, max];
}
function hexToRgb(hex) {
  const m = /^#?([0-9a-f]{6})$/i.exec(hex || '');
  if (!m) return [0, 0, 0];
  const n = parseInt(m[1], 16);
  return [(n >> 16) & 0xFF, (n >> 8) & 0xFF, n & 0xFF];
}
function rgbToHex(r, g, b) {
  return '#' + [r, g, b].map((x) => Math.max(0, Math.min(255, Math.round(x))).toString(16).padStart(2, '0')).join('');
}

// Mod option colour values are stored as signed 32-bit ARGB ints
// (Color.toArgb() style — e.g. -736208 = 0xFFF4C0F0 = pink). The tweak UI
// renders an in-app colour picker alongside the raw int field so users can
// pick a colour visually, but the canonical storage stays an int string.
function argbIntToHex(intStr) {
  const n = parseInt(intStr, 10);
  if (!Number.isFinite(n)) return '#000000';
  const u = n >>> 0;
  const r = (u >> 16) & 0xFF;
  const g = (u >> 8) & 0xFF;
  const b = u & 0xFF;
  return '#' + [r, g, b].map((x) => x.toString(16).padStart(2, '0')).join('');
}
// Round-trip back to the int string. Alpha is preserved from the previous
// value when present (so a mod that one day uses a non-FF alpha keeps it),
// with a 0xFF fallback when the previous value was 0/invalid (the picker
// has no alpha channel anyway, so emitting transparent would look broken).
function hexToArgbIntStr(hex, prevIntStr) {
  const m = /^#([0-9a-f]{6})$/i.exec(hex || '');
  if (!m) return null;
  const rgb = parseInt(m[1], 16);
  let alpha = 0xFF;
  const prev = parseInt(prevIntStr, 10);
  if (Number.isFinite(prev)) {
    const a = (prev >>> 24) & 0xFF;
    if (a !== 0) alpha = a;
  }
  return String(((alpha << 24) | rgb) | 0);
}

// Returns the Alpine root scope so the inline event handlers in the injected
// template strings can call back into the component (Alpine's @click only sees
// scope on the originating element, but x-html breaks that chain).
function annoRoot() {
  return Alpine.$data(document.body);
}
