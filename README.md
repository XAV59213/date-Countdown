# 📆 Date Countdown

**Date Countdown** est une intégration personnalisée pour Home Assistant permettant de suivre le nombre de jours restants avant des événements personnels tels que des anniversaires, anniversaires de mariage, promotions, mémoriaux ou événements spéciaux. Tout est géré depuis l’interface graphique, avec des capteurs automatiques prêts à être utilisés dans Lovelace ou les automatisations.

---

## ✨ Fonctionnalités

- Ajout, modification et suppression d’événements via l’interface utilisateur
- Prise en charge des événements suivants :
  - 🎂 Anniversaire
  - 💍 Anniversaire de mariage (avec intitulé : Noces de Coton, d’Argent, d’Or, etc.)
  - 🕯️ Mémorial
  - 🏆 Promotion
  - 🌟 Événement spécial
- Génération automatique de capteurs :
  - État : nombre de jours restants
  - Attributs : date, type, prénom, années, type de noces
- Icônes personnalisées selon le type d’événement
- Entièrement en français 🇫🇷

---

## 🧱 Prérequis

- Home Assistant `>= 2024.6.0`
- [HACS](https://hacs.xyz) installé

---

## ⚙️ Installation via HACS

1. Ouvrez **HACS > Intégrations**
2. Cliquez sur **⋮ > Dépôt personnalisé**
3. Ajoutez l’URL suivante : https://github.com/XAV59213/date_countdown

Catégorie : Intégration
4. Installez **Date Countdown**
5. Redémarrez Home Assistant
6. Ajoutez l’intégration via :
**Paramètres > Appareils & Services > Ajouter une intégration > Date Countdown**

---

## 🔧 Configuration

- Ajoutez les événements via l’interface :
- Nom
- Prénom (optionnel)
- Date (format `JJ/MM/AAAA`)
- Type d’événement
- Les capteurs sont automatiquement créés au format : sensor.<type><nom><date>

🚀 Utilisations possibles

    Notifications de rappel

    Affichage sur un dashboard

    Automatisations (ex : jouer un message TTS le jour J)

💬 Support

En cas de bug, suggestion ou amélioration :
👉 Ouvrir une issue sur GitHub
👨‍💻 Crédits

Développé par @XAV59213
📜 Licence

Ce projet est distribué sous la licence MIT.
