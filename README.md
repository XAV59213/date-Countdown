# Date Countdown

Date Countdown est une intégration personnalisée pour Home Assistant qui permet de suivre les jours restants avant des événements personnalisés (anniversaires, anniversaires de mariage, mémoriaux, etc.), d'afficher le saint du jour, et de suivre les jours fériés en France. L'interface et les traductions sont en français.

## Fonctionnalités
- Ajout, modification et suppression d'événements via l'interface graphique.
- Types d'événements : anniversaire, anniversaire de mariage, mémorial, promotion, événement spécial.
- Affichage des anniversaires de mariage avec leur nom spécifique (ex. : Noces d'Argent pour 25 ans).
- Capteur pour le saint du jour (`sensor.saint_du_jour`), créé comme un appareil distinct nommé "Saint du Jour".
- Capteur pour les jours fériés en France (`sensor.jour_ferie`), créé comme un appareil distinct nommé "Jour Férié".
- Capteurs intégrés pour une utilisation dans les automatisations et l'interface Lovelace.

## Prérequis
- Home Assistant version 2024.6.0 ou supérieure.
- HACS (Home Assistant Community Store) pour une installation facile.

## Installation
1. Ajoutez ce dépôt à HACS comme dépôt personnalisé :
   - URL : `https://github.com/XAV59213/date_countdown`
   - Catégorie : Intégration
2. Recherchez et installez "Date Countdown" dans HACS.
3. Redémarrez Home Assistant.
4. Ajoutez l'intégration via **Configuration > Intégrations > Ajouter une intégration > Date Countdown**.

## Configuration
- Configurez les événements dans l'interface graphique (nom, date au format JJ/MM/AAAA, type, etc.).
- Les capteurs apparaîtront automatiquement dans Home Assistant (ex. : `sensor.nom_de_l_evenement`).
- Les capteurs `sensor.saint_du_jour` et `sensor.jour_ferie` sont créés automatiquement lors de la première installation.

## Entités générées
- **Capteurs d'événements** : `sensor.<type>_<nom>_<date>` (ex. : `sensor.birthday_marie_15071990`)
  - État : Nombre de jours restants avant l'événement.
  - Attributs :
    - `years` : Âge ou nombre d’années depuis l’événement.
    - `event_type` : Type d’événement (ex. : "birthday").
    - `first_name` : Prénom (si spécifié).
    - `is_public_holiday` : Nom du jour férié si la date coïncide (ex. : "Fête Nationale").
    - `wedding_type` : Type d’anniversaire de mariage (ex. : "Noces d'Argent", pour les anniversaires de mariage uniquement).
- **Capteur Saint du Jour** : `sensor.saint_du_jour`
  - État : Nom du saint du jour (ex. : "les Justin").
  - Attribut : `saint` (nom du saint).
  - Associé à l’appareil "Saint du Jour".
- **Capteur Jour Férié** : `sensor.jour_ferie`
  - État : Nom du jour férié ou "Aucun jour férié".
  - Attributs :
    - `next_holiday` : Prochain jour férié (ex. : "Lundi de Pentecôte").
    - `next_date` : Date du prochain jour férié (ex. : "09/06/2025").
  - Associé à l’appareil "Jour Férié".

## Exemple d'utilisation
- Ajoutez un événement pour l'anniversaire de "Marie" le 15/07/1990.
  - Un capteur `sensor.birthday_marie_15071990` affichera le nombre de jours restants et l'âge à venir (attribut `years`).
  - L’attribut `is_public_holiday` indiquera "null" (pas de jour férié ce jour-là).
- Ajoutez un événement pour l’anniversaire de mariage de "Paul" le 14/07/1990.
  - Un capteur `sensor.anniversary_paul_14071990` affichera le nombre de jours restants, l’âge du mariage (attribut `years`), et le type d’anniversaire (ex. : "Noces d'Argent" pour 25 ans).
  - L’attribut `is_public_holiday` indiquera "Fête Nationale".
- Les capteurs `sensor.saint_du_jour` et `sensor.jour_ferie` sont disponibles pour afficher le saint du jour et les jours fériés.

## Support
Pour les problèmes ou suggestions, ouvrez une issue sur [GitHub Issues](https://github.com/XAV59213/date_countdown/issues).

## Crédits
Développé par @XAV59213.
