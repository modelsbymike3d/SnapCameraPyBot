import argparse
import os
import sys
import pyvirtualcam
import cv2
import time
from tqdm import tqdm


def process_video(input_file=None, output_file=None,
                  cam_index=None, time_delay=None, should_preview=None):
    print('Starting video processing')

    video_capture = cv2.VideoCapture(cam_index)
    input_video = cv2.VideoCapture(input_file)

    fps = input_video.get(cv2.CAP_PROP_FPS)
    width = int(input_video.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(input_video.get(cv2.CAP_PROP_FRAME_HEIGHT))
    num_frames = int(input_video.get(cv2.CAP_PROP_FRAME_COUNT))
    if should_preview:
        num_frames = min(num_frames, int(10 * fps))
    if not fps:
        print('Could not get video framerate')
        sys.exit(1)
    if not width or not height:
        print('Could not get video dimensions')
        sys.exit(1)

    print('Input video parameters:\n\tfps: {}\n\twidth: {}\n\theight: {}\n\tframes: {}'.format(
        fps, width, height, num_frames))

    print('Configuring virtual camera')
    cam = pyvirtualcam.Camera(width=width, height=height, fps=fps)
    print('Using virtual camera: {}'.format(cam.device))

    # Setup output file
    fourcc = cv2.VideoWriter_fourcc(*'MP4V')
    output_video = cv2.VideoWriter(output_file, fourcc, fps, (width, height))

    for i in tqdm(range(num_frames)):
        input_video.set(1, i)
        success, input_image = input_video.read()
        im_rgb = cv2.cvtColor(input_image, cv2.COLOR_BGR2RGB)
        cam.send(im_rgb)
        for j in range(3):
            cam.sleep_until_next_frame()
        time.sleep(time_delay)

        ret, output_image = video_capture.read()
        output_video.write(output_image)

    video_capture.release()
    input_video.release()
    output_video.release()

    return


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--file', '-f', help="The video file to process", type=str)
    parser.add_argument(
        '--out', '-o', help="Output name for the processed video. Defaults to input filename with '_lens' appended", type=str)
    parser.add_argument(
        '--index', '-i', help="Index of the webcam to be capturing output from. Default value is 1 and should usually work, but if you have additional webcams installed you may need to change", type=int)
    parser.add_argument(
        '--delay', '-d', help="Additional time delay (in seconds) to wait between each frame. May be helpful if the lens takes a moment to apply. Default value is 0")
    parser.add_argument(
        '--preview', '-p', help="Process only the first 10 seconds of the video to make sure everything is running correctly. Default is 'n' for no, pass 'y' for yes")
    args = parser.parse_args()

    if not args.file:
        print('Input file is required')
        sys.exit(1)

    # Set the defaults
    index = args.index or 1
    delay = args.delay or 0
    preview_arg = args.preview or 'n'
    preview = True if preview_arg == 'y' else False
    if not args.out:
        infile, ext = os.path.splitext(args.file)
        outfile = infile + '_lens'+ext
    else:
        outfile = args.out

    process_video(input_file=args.file, output_file=outfile,
                  cam_index=int(index), time_delay=float(delay), should_preview=preview)
