import moviepy.editor as mp

clip = mp.VideoFileClip("day 23 rudeus.mp4")
clip.write_videofile("myvideo.gif")

