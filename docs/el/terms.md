---
title: "Όροι και άδεια"
nav_order: 9
lang: el
source: terms.md
source_hash: "7fb5ea01ecb8"
nav_exclude: true
search_exclude: true
---
# Όροι και άδεια {#terms-and-licence}

## Οι όροι της Wargaming {#wargamings-terms}

Διαβάστηκαν στις 2026-11-07, Wargaming EULA έκδοση 14 (σε ισχύ από 10 Απριλίου 2024, όπως
αναφέρεται ως τρέχουσα):

- 5.3 (b): εκτός αν υπάρχει γραπτή άδεια, δεν επιτρέπεται το "... decompile,
  disassemble, reverse engineer or otherwise make unauthorized use of the
  Content".
- 12.1 (k): απαγορεύεται το "Creating, using, making available, or distributing
  any unauthorized software or tools, including hacks, cheats, exploits,
  scripts, bots, trainers, automation programs, or other software that
  interacts with a Product in any way and for any purpose, including
  intercepts, emulates, or redirects any communication between such software
  and Wargaming."
- 12.1 (l): "... any software designed to modify a Product and change the user
  experience ("mods") unless expressly permitted by Wargaming".
- 12.1 (p): "Circumventing or bypassing enforcement and security measures
  implemented by Wargaming".

Η λίστα των απαγορευμένων τροποποιήσεων του World of Tanks αφορά την ίδια τη μάχη: τροποποιήσεις
που "reveal the position of enemies in a way not included in the client", bots σκοπεύματος,
χρονόμετρα επαναφόρτωσης και τα παρόμοια. Ούτε η EULA ούτε αυτή η λίστα αναφέρουν τα replays.

Τι κάνει αυτός ο μετατροπέας: διαβάζει ένα αρχείο που έγραψε το παιχνίδι, μετά τη μάχη,
έξω από το παιχνίδι. Δεν αλλάζει τίποτα στο παιχνίδι, δεν μιλά με κανέναν διακομιστή, και
δεν δείχνει τίποτα κατά τη διάρκεια μιας μάχης. Αποκρυπτογραφεί όμως τη ροή με το κλειδί του
παιχνιδιού, το οποίο οι 5.3 (b) και 12.1 (p) μπορούν να διαβαστούν ότι καλύπτουν. Η χρήση του
είναι απόφαση του χρήστη· γι' αυτό είναι χωριστό πακέτο.

## Άδεια και πηγές {#licence-and-sources}

MIT ([`LICENSE`](https://github.com/Holdi601/3DHeat-Ext-WoT/blob/main/LICENSE)). Χρειάζεται το
numpy (BSD-3-Clause) και το pyarrow (Apache-2.0). Γράφτηκε για αυτό το έργο: ο κρυπτογράφος
Blowfish εδώ είναι δικός του, με τους πίνακές του υπολογισμένους από τα ψηφία του π όπως
τον ορίζει ο κρυπτογράφος. Τα γεγονότα για τη μορφή (ο περιέκτης, ο κρυπτογράφος, το πακέτο
θέσης) είναι κοινή γνώση μεταξύ των εργαλείων replay· το evido/wotreplay-parser
(BSD-3-Clause) τα τεκμηριώνει. Κανένας κώδικας δεν αντιγράφηκε από αυτό ή από άλλο έργο.

Τα `bigworld.py` και `table.py` είναι τα ίδια αρχεία με αυτά του μετατροπέα World of Warships
([3DHeat-Ext-WoWs](https://github.com/Holdi601/3DHeat-Ext-WoWs))· αλλάξτε τα και τα δύο μαζί.

---

Μέρος του [3DHeat](https://github.com/Holdi601/3DHeat) ([τεκμηρίωση](https://holdi601.github.io/3DHeat/)). Πηγή: [3DHeat-Ext-WoT](https://github.com/Holdi601/3DHeat-Ext-WoT).
