# Date Countdown

Date Countdown est une intégration personnalisée pour Home Assistant qui permet de suivre les jours restants avant des événements personnalisés (anniversaires, anniversaires de mariage, mémoriaux, etc.) et d'afficher le saint du jour.

## Fonctionnalités
- Ajout, modification et suppression d'événements via l'interface graphique.
- Types d'événements : anniversaire, anniversaire de mariage, mémorial, promotion, événement spécial.
- Affichage des anniversaires de mariage avec leur nom spécifique (ex. : Noces d'Argent pour 25 ans).
- Option pour afficher le saint du jour.
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
- Activez ou désactivez l'option "Saint du jour".
- Les capteurs apparaîtront automatiquement dans Home Assistant (ex. : `sensor.nom_de_l_evenement`).

## Exemple d'utilisation
- Ajoutez un événement pour l'anniversaire de "Marie" le 15/07/1990.
- Un capteur `sensor.marie_s_birthday` affichera le nombre de jours restants et l'âge à venir.
- Pour les anniversaires de mariage, le capteur inclut le type (ex. : "Noces de Coton" pour 1 an).

## Support
Pour les problèmes ou suggestions, ouvrez une issue sur [GitHub](https://github.com/XAV59213/date_countdown).

## Crédits
Développé par @XAV59213.
