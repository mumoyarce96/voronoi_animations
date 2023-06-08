# -*- coding: utf-8 -*-
"""
Created on Sun Jun  4 20:05:37 2023

@author: Raimundo
"""
import pandas as pd

def update_frame_numbers(frame_number, frames_between):
    return frame_number + (frame_number - 1) * frames_between 


def interpolate_df(df, frames_between):
    df['Frame'] = df['Frame'].apply(update_frame_numbers, frames_between = frames_between)
    interpolated_frames = []
    for start_frame in df['Frame'].unique()[:-1]:
        end_frame = start_frame + frames_between + 1 
        # Calculate the step size for interpolation
        step_size = 1 / (frames_between + 1)
        
        # Iterate over the frames between start_frame and end_frame
        for i in range(frames_between):
            current_frame = start_frame + i + 1
            interpolation_ratio = (i + 1) * step_size
            
            # Interpolate X and Y positions for each player and team
            interpolated_data = df[df['Frame'] == start_frame].copy().reset_index(drop = True)
            interpolated_data['Frame'] = current_frame
            start_df = df[df['Frame'] == start_frame].reset_index()
            end_df = df[df['Frame'] == end_frame].reset_index()
            interpolated_data['X'] = start_df['X'] + interpolation_ratio * (end_df['X'] - start_df['X'])
            interpolated_data['Y'] = start_df['Y'] + interpolation_ratio * (end_df['Y'] - start_df['Y'])
            
            # Append the interpolated frame to the list
            interpolated_frames.append(interpolated_data)
    
    # Concatenate the original dataframe and the interpolated frames
    interpolated_df = pd.concat([df] + interpolated_frames, ignore_index=True).sort_values(by = ['Frame', 'Team', 'Player'])
    return interpolated_df