#!/usr/env/python3

import youtube_dl
import cv2 as cv
import os
from functools import partial
from multiprocessing.pool import ThreadPool as Pool
import time


class VideoScraper:
    def __init__(self, save_path="/Users/shreysahgal/Documents/dance_fall_data_collector/data", debug=False):
        self.num_procs : int = os.cpu_count()
        self.data_path : str = save_path
        self.debug = debug

    def process_video_parallel(self, url:str, num_imgs:int, vid_id:str, proc_id:int):

        if self.debug:
            print(f"hello from proc {proc_id}")

        cap : cv.VideoCapture  = cv.VideoCapture(url)
        num_frames : int = int(cap.get(cv.CAP_PROP_FRAME_COUNT))
        frames_per_proc : int = num_frames // self.num_procs
        cap.set(cv.CAP_PROP_POS_FRAMES, frames_per_proc * proc_id)

        img_count : int = 0
        frame_count : int = 0

        while img_count < num_imgs and frame_count < frames_per_proc:
            if self.debug:
                print(f"proc {proc_id} processing img {img_count}")
            ret, frame = cap.read()

            if not ret:
                break

            # fname : str = f"{str(proc_id)}_{str(img_count)}.png"
            fname : str = f"{vid_id}_{str(frames_per_proc * proc_id + frame_count)}.png"
            cv.imwrite(os.path.join(self.data_path, fname), frame)

            img_count += 1
            frame_count += (frames_per_proc // num_imgs)
            cap.set(1, frame_count)
        cap.release()

    def process_video(self, url:str, imgs_per_proc:int=5, format:str="480p"):
        start = time.time()

        ydl_opts = {}
        ydl = youtube_dl.YoutubeDL(ydl_opts)
        info_dict = ydl.extract_info(url, download=False)
        video_id = info_dict.get('id', None)
        
        video_url = None
        for f in info_dict.get('formats', None):
            if f.get('format_note', None) == format:
                video_url = f.get('url', None)
        if not video_url:
            print(f"Could not get video in format {format}.")
            return
        
        with Pool(self.num_procs) as pool:
            pool.map(partial(self.process_video_parallel, video_url, imgs_per_proc, video_id), range(self.num_procs))
            # tqdm(pool.imap(partial(self.process_video_parallel, video_url, imgs_per_proc, video_url), range(self.num_procs)), total=self.num_procs)
        
        elapsed = time.time() - start
        print(f"Processed {imgs_per_proc * self.num_procs} images in {elapsed:.2f}s")


if __name__ == '__main__':

    scraper = VideoScraper()

    dancing_urls = ["https://www.youtube.com/watch?v=qvrMhdQE6zM"]

    for url in dancing_urls:
        scraper.process_video(url, imgs_per_proc=5)
