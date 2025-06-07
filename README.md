📆 Date Countdown
Date Countdown est une intégration personnalisée pour Home Assistant qui permet de suivre le compte à rebours des jours restants avant des événements personnels, tels que des anniversaires, anniversaires de mariage, mémoriaux, promotions, ou événements spéciaux. Les événements sont configurés via l'interface graphique, et des capteurs sont automatiquement générés pour une utilisation dans les dashboards Lovelace ou les automatisations.

✨ Fonctionnalités

Configuration via l'interface utilisateur : Ajoutez, modifiez ou supprimez des événements directement dans Home Assistant.
Types d'événements pris en charge :
🎂 Anniversaire : Suivi des anniversaires avec calcul de l'âge.
💍 Anniversaire de mariage : Inclut les intitulés des noces (par exemple, Noces de Coton, d'Argent, d'Or).
🕯️ Mémorial : Suivi des anniversaires de naissance des défunts, avec option pour la date de décès, calcul de l'âge qu'ils auraient eu (age_if_alive) et du nombre d'années depuis le décès (years_since_death).
🏆 Promotion : Suivi des anniversaires de promotions professionnelles.
🌟 Événement spécial : Suivi d'autres événements personnalisés.


Capteurs automatiques :
État principal : Nombre de jours restants jusqu'à la prochaine occurrence de l'événement.
Attributs : Incluent le nom, prénom, type d'événement, date, années, et des informations spécifiques comme le type de noces (pour les anniversaires de mariage) ou les données de décès (pour les mémoriaux).


Icônes personnalisées : Chaque type d'événement a une icône spécifique (par exemple, mdi:candle pour les mémoriaux).
Support complet en français : Interface et traductions en français.
Automatisations et notifications : Utilisez les capteurs pour déclencher des rappels ou des messages TTS.


🧱 Prérequis

Home Assistant version >= 2024.6.0.
HACS installé pour une installation facile.


⚙️ Installation via HACS

Ouvrez HACS > Intégrations.
Cliquez sur ⋮ > Dépôt personnalisé.
Ajoutez l’URL du dépôt : https://github.com/XAV59213/date_countdown.
Catégorie : Intégration.


Installez l'intégration Date Countdown.
Redémarrez Home Assistant.
Ajoutez l'intégration via Paramètres > Appareils & Services > Ajouter une intégration > Date Countdown.


🔧 Configuration
Ajout d’un événement

Accédez à Paramètres > Appareils & Services > Intégrations > Date Countdown.
Cliquez sur Configurer ou ajoutez une nouvelle instance.
Suivez le flux de configuration en deux étapes :
Étape 1 : Sélectionnez le type d’événement (Anniversaire, Anniversaire de mariage, Mémorial, Promotion, Événement spécial).
Étape 2 : Saisissez les détails :
Nom : Nom de l’événement ou de la personne (requis).
Prénom : Prénom de la personne (optionnel).
Date : Date de l’événement (format JJ/MM/AAAA, requis). Pour les mémoriaux, il s’agit de la date de naissance.
Date de décès : Pour les mémoriaux uniquement, date du décès (format JJ/MM/AAAA, optionnel).




Validez pour créer l’événement.

Modification ou suppression

Dans l’interface de l’intégration, sélectionnez Options pour :
Ajouter un nouvel événement.
Modifier un événement existant (même flux en deux étapes).
Supprimer un événement.



Capteurs générés
Chaque événement crée un capteur au format sensor.<type>_<nom>_<date> (par exemple, sensor.memorial_jean_01011950). Les capteurs ont :

État : Nombre de jours restants (en jours, unité : days).
Attributs :
friendly_name : Nom convivial (par exemple, "Jean - Mémorial").
first_name : Prénom (si spécifié).
event_date : Date de l’événement (format JJ/MM/AAAA).
event_type : Type d’événement (birthday, anniversary, memorial, etc.).
years : Nombre d’années jusqu’à la prochaine occurrence (par exemple, 76 pour un mémorial en 2026).
Pour les anniversaires de mariage :
wedding_type : Intitulé des noces (par exemple, "Noces d’Or" pour 50 ans).


Pour les mémoriaux :
death_date : Date de décès (si spécifiée, format JJ/MM/AAAA).
age_if_alive : Âge qu’aurait la personne aujourd’hui (par exemple, 75 ans en 2025 pour une naissance en 1950).
years_since_death : Nombre d’années depuis le décès (si death_date est spécifiée).






🚀 Exemples d’utilisation
Affichage dans Lovelace
Voici un exemple de carte Lovelace inspirée du modèle Jinja fourni, adapté pour afficher les mémoriaux à venir (limité aux deux plus proches) :
type: markdown
content: |
  ## 🕯️ **Mémoriaux à venir**
  Voici la liste des mémoriaux à venir :
  {{ '\n' }}
  {% set ns = namespace(found=false, events=[]) %}
  {% for entity in states.sensor %}
    {% set entity_id = entity.entity_id %}
    {% if entity_id | regex_search('memorial$') %}
      {% set state_value = states(entity_id) %}
      {% if state_value | is_number and state_value | float > 0 %}
        {% set ns.events = ns.events + [{'entity_id': entity_id, 'days': state_value | float}] %}
      {% endif %}
    {% endif %}
  {% endfor %}
  {% if ns.events %}
    {% set ns.found = true %}
    {% set sorted_events = ns.events | sort(attribute='days') %}
    {% for event in sorted_events %}
      {% if loop.index <= 2 %}
        - **{{ state_attr(event.entity_id, 'friendly_name') | default(event.entity_id, true) }}** : {{ event.days | int }} jours restants
          - **Prénom** : {{ state_attr(event.entity_id, 'first_name') | default('Non spécifié', true) }}
          - **Date de naissance** : {{ state_attr(event.entity_id, 'event_date') | default('Non spécifiée', true) }}
          - **Âge aujourd’hui** : {{ state_attr(event.entity_id, 'age_if_alive') | default('Inconnu', true) }} ans
          - **Âge au prochain anniversaire** : {{ state_attr(event.entity_id, 'years') | default('Inconnu', true) }} ans
          {% if state_attr(event.entity_id, 'death_date') %}
          - **Date de décès** : {{ state_attr(event.entity_id, 'death_date') }}
          - **Années depuis le décès** : {{ state_attr(event.entity_id, 'years_since_death') | default('Inconnu', true) }} ans
          {% endif %}
      {% endif %}
    {% endfor %}
  {% endif %}
  {% if not ns.found %}
    - Aucun mémorial à venir.
  {% endif %}

Exemple pour les anniversaires de mariage
Pour afficher les anniversaires de mariage avec leurs types de noces :
type: markdown
content: |
  ## 💍 **Anniversaires de mariage à venir**
  Voici la liste des anniversaires de mariage à venir :
  {{ '\n' }}
  {% set ns = namespace(found=false, events=[]) %}
  {% for entity in states.sensor %}
    {% set entity_id = entity.entity_id %}
    {% if entity_id | regex_search('anniversary$') %}
      {% set state_value = states(entity_id) %}
      {% if state_value | is_number and state_value | float > 0 %}
        {% set ns.events = ns.events + [{'entity_id': entity_id, 'days': state_value | float}] %}
      {% endif %}
    {% endif %}
  {% endfor %}
  {% if ns.events %}
    {% set ns.found = true %}
    {% set sorted_events = ns.events | sort(attribute='days') %}
    {% for event in sorted_events %}
      {% if loop.index <= 2 %}
        - **{{ state_attr(event.entity_id, 'friendly_name') | default(event.entity_id, true) }}** : {{ event.days | int }} jours restants
          - **Prénom(s)** : {{ state_attr(event.entity_id, 'first_name') | default('Non spécifié', true) }}
          - **Date de mariage** : {{ state_attr(event.entity_id, 'event_date') | default('Non spécifiée', true) }}
          - **Années** : {{ state_attr(event.entity_id, 'years') | default('Inconnu', true) }} ans
          - **Type de noces** : {{ state_attr(event.entity_id, 'wedding_type') | default('Non applicable', true) }}
      {% endif %}
    {% endfor %}
  {% endif %}
  {% if not ns.found %}
    - Aucun anniversaire de mariage à venir.
  {% endif %}

Automatisation pour les rappels
Exemple d’automatisation pour envoyer une notification 7 jours avant un mémorial :
automation:
  - alias: "Rappel Mémorial"
    trigger:
      platform: numeric_state
      entity_id: sensor.memorial_jean_01011950
      value_equal: 7
    action:
      service: notify.notify
      data:
        message: >
          Rappel : L’anniversaire de {{ state_attr('sensor.memorial_jean_01011950', 'friendly_name') }} approche dans 7 jours.
          Âge aujourd’hui : {{ state_attr('sensor.memorial_jean_01011950', 'age_if_alive') }} ans.
          {% if state_attr('sensor.memorial_jean_01011950', 'death_date') %}
          Années depuis le décès : {{ state_attr('sensor.memorial_jean_01011950', 'years_since_death') }} ans.
          {% endif %}


💬 Dépannage

L’intégration ne charge pas :
Vérifiez les journaux dans home-assistant.log pour des erreurs comme SyntaxError ou ImportError.
Assurez-vous que tous les fichiers sont à jour et que vous utilisez Home Assistant >= 2024.6.0.


Les capteurs n’apparaissent pas :
Redémarrez Home Assistant après avoir ajouté ou modifié des événements.
Vérifiez que les dates saisies sont au format JJ/MM/AAAA et valides.


Problèmes avec les mémoriaux :
Assurez-vous que death_date est au format JJ/MM/AAAA ou laissé vide.
Vérifiez les attributs age_if_alive et years_since_death dans Développeur > États.



Pour activer les journaux de débogage :
logger:
  default: info
  logs:
    custom_components.date_countdown: debug


👨‍💻 Crédits

Développeur : @XAV59213
Licence : MIT
Dépôt GitHub : https://github.com/XAV59213/date_countdown


📜 Notes techniques
Structure des capteurs
Chaque capteur est créé dans custom_components/date_countdown/sensor.py et suit la structure suivante :

Entity ID : sensor.<type>_<nom>_<date> (par exemple, sensor.memorial_jean_01011950).
État : Nombre de jours restants (entier, unité : days).
Attributs :{
  "friendly_name": "Jean - Mémorial",
  "first_name": "Marie",
  "event_date": "01/01/1950",
  "event_type": "memorial",
  "years": 76,
  "death_date": "15/06/2000",
  "age_if_alive": 75,
  "years_since_death": 25
}



Différence entre years et age_if_alive (pour les mémoriaux)

Years : Nombre d’années jusqu’à la prochaine occurrence de l’anniversaire (par exemple, 76 ans en 2026 pour une naissance en 1950).
Age if Alive : Âge qu’aurait la personne aujourd’hui, ajusté pour l’anniversaire de l’année en cours (par exemple, 75 ans en juin 2025 si l’anniversaire est passé).

Fichiers de l’intégration

custom_components/date_countdown/__init__.py : Initialisation de l’intégration.
custom_components/date_countdown/config_flow.py : Flux de configuration en deux étapes.
custom_components/date_countdown/sensor.py : Création et mise à jour des capteurs.
custom_components/date_countdown/const.py : Constantes (types d’événements, noces, etc.).
custom_components/date_countdown/translations/fr.json : Traductions en français.
custom_components/date_countdown/manifest.json : Métadonnées de l’intégration (version 1.3.0).
README.md : Documentation utilisateur.
hacs.json : Configuration pour HACS.


📢 Support
Pour signaler un bug, proposer une amélioration ou demander de l’aide :

Ouvrez une issue sur le dépôt GitHub : https://github.com/XAV59213/date_countdown/issues.

