# Game of Sound

This is a try to sync each epoch of Conway's Game of Life with music.
It was tried by using either the beats or the tempo of the song (which are equal in a way).

Currently the speed is rather constant, which I don't know if it's a bug or not.
For the audio analysis [librosa](https://librosa.org/doc/main/index.html) and [scipy](https://scipy.org/) are used.
For the visuals [pygame](https://www.pygame.org/).

## Try your own kind of music
Just edit these lines at the beginning of the `./game_of_sound/main.py`:

```py
directory = 'assets/...';
song = '...'
song_path = f'{directory}/{song}.mp3'
```

## Running

The `python` environment is setup with [Poetry](https://python-poetry.org/).
That makes it rather easy to get started, after installation just run:

```shell
poetry install
poetry run game
```
