# Word Play Autosplitter

This is a bare-bones [LiveSplit](https://livesplit.org/)-compatible autosplitter for [Mark Brown](https://www.youtube.com/channel/UCqJ-Xo29CKyLTjn6z2XwYAw)'s game [Word Play](https://store.steampowered.com/app/3586660/Word_Play/).

- Only for **Windows**.
- Uses **game logs** to determine start/end/splits, not game memory.
- **Stays open** in the background while you play.

### Usage

1. Open LiveSplit, and open the [layout](livesplit/Layouts/layout_wordplay_easy.lsl) and [split](livesplit/Splits/splits_wordplay_easy.lss) files found in `livesplit/`.
2. Also in Livesplit, select `Control` -> `Start TCP Server`.
3. Open [dist/wordplay_autosplitter.exe](dist/wordplay_autosplitter.exe) and follow the prompts.
4. Start playing!

### Development

To make changes to the autosplitter, simply edit [wordplay_autosplitter.py](wordplay_autosplitter.py). You can run it directly, but if you prefer to have a `.exe`, run the following:

```sh
pyinstaller --onefile --name wordplay_autosplitter wordplay_autosplitter.py
```

### License

1. Please use, modify, and distribute freely!
2. When applicable, crediting the [author](https://github.com/plettj) is appreciated.
