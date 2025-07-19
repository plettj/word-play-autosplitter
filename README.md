# Word Play Autosplitter

This is a bare-bones [LiveSplit](https://livesplit.org/)-compatible autosplitter for speedrunning [Mark Brown](https://www.youtube.com/channel/UCqJ-Xo29CKyLTjn6z2XwYAw)'s game [Word Play](https://store.steampowered.com/app/3586660/Word_Play/).

> [!NOTE]
>
> This autosplitter only works if you're playing Word Play on Windows.

## Usage

1. Open LiveSplit, and open the [layout](livesplit/Layouts/layout_wordplay_easy.lsl) and [split](livesplit/Splits/splits_wordplay_easy.lss) files found in `livesplit/`.
2. Also in Livesplit, select `Control` -> `Start TCP Server`.
3. Open [dist/wordplay_autosplitter.exe](dist/wordplay_autosplitter.exe) and follow the prompts.
4. Start playing!

## Development

To make changes to the autosplitter, simply edit [wordplay_autosplitter.py](wordplay_autosplitter.py). You can run it directly, but if you prefer to have a `.exe`, run the following:

```sh
pyinstaller --onefile --name wordplay_autosplitter wordplay_autosplitter.py
```

The autosplitter works by reading your Word Play `Player.log` file to figure out when you start and stop games, and pass rounds.

## License

1. Please use, modify, and distribute freely!
2. When applicable, crediting the [author](https://github.com/plettj) is appreciated.
