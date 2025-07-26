# Word Play Solver

Word list is from [wordplay-word-finder](https://github.com/wordplay-word-finder/wordplay-word-finder.github.io/).

This [Word Play](https://store.steampowered.com/app/3586660/Word_Play/) solver supports two modes:

#### Normal Mode

- Finds the longest possible word from the given inputs.

#### Efficient Mode

- Finds the 9-letter word that uses, in that order:
  1. The least asterisks,
  2. The most bad letters, and
  3. The most medium-bad letters.
- Assumes non-submitted letters are asterisks.
