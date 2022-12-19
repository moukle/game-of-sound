import librosa
import numpy as np
import pygame
import scipy
import time

from .game_of_life import GameOfLife


def main() -> None:
    directory = 'assets/Johnny in the Jungle - Postcard from Norilsk';
    song = 'Johnny in the Jungle - Postcard from Norilsk - 01 We Are Trapped'
    song_path = f'{directory}/{song}.mp3'
    beats_npy = f'assets/output/{song}_beats'
    tempo_npy = f'assets/output/{song}_tempo'

    extract_beats_and_tempo(song_path, beats_npy, tempo_npy)  # NOTE: uncomment this line once you got your pickels
    beats = np.load(f'{beats_npy}.npy')
    tempo = np.load(f'{tempo_npy}.npy')

    GoL = GameOfLife(width=100, height=100, cellsize=20)

    # GO!
    # 1. Audio
    play_song(song_path)

    # 2. Visuals
    # draw_beats(beats, GoL)
    draw_by_tempo(tempo, GoL)


def extract_beats_and_tempo(input: str, output_beats: str, output_tempo: str) -> None:
    # 1. Load the audio as a waveform `y`
    #    Store the sampling rate as `sr`
    y, sr = librosa.load(input)

    # 2. Run the default beat tracker
    tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)

    # 3. Convert the frame indices of beat events into timestamps
    beat_times = librosa.frames_to_time(beat_frames, sr=sr)


    # 4. Estimate dynamic tempo with a proper log-normal prior
    onset_env = librosa.onset.onset_strength(y=y, sr=sr)
    prior_lognorm = scipy.stats.lognorm(loc=np.log(120), scale=120, s=1)
    dtempo_lognorm = librosa.beat.tempo(onset_envelope=onset_env, sr=sr,
                                        aggregate=None,
                                        prior=prior_lognorm)

    # 5. Save to pickle
    np.save(output_beats, beat_times)
    np.save(output_tempo, dtempo_lognorm)


def play_song(song_path: str) -> None:
    pygame.mixer.init()
    pygame.mixer.music.load(song_path)
    pygame.mixer.music.play()


def draw_beats(beats: np.array, game: GameOfLife) -> None:
    steps_per_beat = 5
    start = time.time()

    for beat in beats:
        elapsed = (time.time() - start)
        beat_steps = np.linspace(elapsed, beat, num=steps_per_beat, endpoint=False)
        for step in beat_steps:
            while elapsed < step:
                elapsed = (time.time() - start)
            game.step()
            game.draw()


def draw_by_tempo(tempo: np.array, game: GameOfLife) -> None:
    start = time.time()
    times = librosa.times_like(tempo)

    for _tempo, _time in zip(tempo, times):
        elapsed = (time.time() - start)
        steps = np.linspace(elapsed, _time, num=np.int(_tempo/10), endpoint=False)

        for step in steps:
            while elapsed < step:
                elapsed = (time.time() - start)
                time.sleep(0.01)
            game.step()
            game.draw()