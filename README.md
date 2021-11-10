# Snap Camera Python Bot

Add lenses to videos nearly frame-by-frame

## Prerequisites

- [Snap Camera](https://snapcamera.snapchat.com/) (Windows/macOS only)
- [OBS](https://obsproject.com/) or another package compatible with [pyvirtualcam](https://github.com/letmaik/pyvirtualcam)
- [SplitCam](https://splitcam.com/) may be required. The OBS virtual camera is not accessible by Snap Camera on Windows, so to get around that I use SplitCam to take the output from OBS and expose it as yet another virtual webcam that Snap Camera can access.

## Setup and installation

This has been tested with Python 3.7.10 running through a conda environment on Windows 10 `conda create --name snapcam python=3.7.10`. Other versions of Python should work fine, but have not been tested.

Install dependencies with `pip install -U -r requirements.txt`. You can install with conda if you want, I just didn't see a way to install pyvirtualcam with conda so I stuck with pip.

## Running

Run `python main.py -h` for a list of all possible arguments.

- `-f` (required) is the input file to process. So far this script has been tested with a 1920x1080 mp4 file. 1280x720 should also work. I don't think Snap Camera can handle 4k video (or anything above HD), but feel free to try.
- `-o` (optional) is the output file the script should produce. If no value provided, it will default to `<original-filename>_lens.mp4`. Currently the script only outputs mp4 files.
- `-i` (optional, default 1) is the webcam device index. For Snap Camera this is probably `1` unless you have other webcams installed.
- `-d` (optional, default is 0) is the extra time delay (in seconds) to add between frame processing. If there are jump cuts in the video Snap Camera needs a little extra time to re-find faces and apply lenses, so if you are running into issues of dropped frames you may want to add a slight delay here.
- `-p` (optional, default is `n`) will run the script in preview mode and only process the first 10 seconds of video. This is helpful when troubleshooting to make sure everything is wired together correctly.

Simple usage: `python main.py -f rickroll.mp4`
With a delay: `python main.py -f rickroll.mp4 -d 0.1`
Preview mode: `python main.py -f rickroll.mp4 -p y`

In all three cases the output file will be `rickroll_lens.mp4`.

Before you run the script, make sure Snap Camera is ready with the correct input and lens. For me personally, I have SplitCam setup with the OBS virtual cam as the input device. Then on Snap Camera I have SplitCam set for the input. Double check the video resolutions inside SplitCam and Snap Camera to make sure they match the resolution of the video you are applying the lens to.

I'd love to see what you create! Feel free to tag me on Twitter [@modelsbymike3d](https://twitter.com/ModelsByMike3D) with your creations.

## Example output

<iframe src="https://giphy.com/embed/9DV9Tmqsi1ocMfSzkR" width="480" height="270" frameBorder="0" class="giphy-embed" allowFullScreen></iframe><p><a href="https://giphy.com/gifs/9DV9Tmqsi1ocMfSzkR">via GIPHY</a></p>

## Limitations

This script does not run in realtime. There are purposeful delays to make sure the image is read in, sent to SplitCam, sent to Snap Camera, and then waiting for the lens to be applied. For many lenses this is not an issue, but for lenses using things like chain physics, particles, VFX, or anything else that updates on a frame-by-frame basis, this will cause issues. Snap Camera will be running those effects at 30 fps but the script will be feeding the images in at a lower framerate. For now that is a limitation of wiring everything together and I'm also not sure if Snap Camera will run at a lower framerate.

The script also seems to get off by one frame. I still haven't tracked down why that is, but when combining your filtered video with the original footage that is something to keep in mind.

Please note that Snap Camera is designed to process webcam videos and is not designed for 8k ProRes video. Please use up to 1920x1080 mp4 video files for the script and just be aware that Snap Camera was not designed for super high fidelity use cases.

You also have no control over which faces get the lens, so if there are 10 faces in your video it is going to randomly choose the face(s) that get the lens. If you need to target specific faces, create a mask and mask out everyone else.

Far away faces are not detected well, nor are faces which start out turned too far to the side.

## Contributing

Contributions and improvements are welcome. If you run into any issues, open an issue and provide as much information as you can. I do not have a Mac computer to test with, so if you are running a Mac I unfortunately won't be able to help.

If you have any code contributions, feel free to fork the project and submit a pull request. Please keep any changes focused on processing video with Snap Camera.
