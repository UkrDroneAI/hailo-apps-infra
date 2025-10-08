from hailo_apps.hailo_app_python.core.gstreamer.gstreamer_helper_pipelines import QUEUE, OVERLAY_PIPELINE

def RTSP_SINK_PIPELINE(sync='true', name='hailo_rtsp', hight='480', width='640'):
    """
    Creates a GStreamer pipeline string for streaming the video.
    It includes the hailooverlay plugin to draw bounding boxes and labels on the video.
    
    Requirements:
    - sudo apt-get install gstreamer1.0-plugins-ugly
    - sudo apt install gstreamer1.0-rtsp
    - download and run mediamtx - https://github.com/bluenviron/mediamtx/releases

    Args:
        sync (str, optional): The sync property for the video sink. Defaults to 'true'.
        name (str, optional): The prefix name for the pipeline elements. Defaults to 'hailo_display'.

    Returns:
        str: A string representing the GStreamer pipeline for displaying the video.
    """
    # Construct the display pipeline string
    display_pipeline = (
        f'{OVERLAY_PIPELINE(name=f"{name}_overlay")} ! '
        f'{QUEUE(name=f"{name}_videoconvert_q")} ! '
        f'videoconvert name={name}_videoconvert n-threads=2 qos=false ! '
        # f'videoscale ! video/x-raw,format=NV12,width={width},height={hight} !'
        f'videoscale ! video/x-raw,width={width},height={hight} !'
        f'videorate ! video/x-raw,framerate=15/1 !'
        f'{QUEUE(name=f"{name}_q")} ! '
        # f'x264enc speed-preset=veryfast tune=zerolatency bitrate=800 ! rtspclientsink location=rtsp://localhost:8554/test'
        f'x264enc speed-preset=veryfast tune=zerolatency ! rtph264pay config-interval=-1 ! udpsink host=127.0.0.1 port=5602 sync=false'
    )

    return display_pipeline


def RTSP_SOURCE_PIPELINE(video_source, video_width=640, video_height=640,
                    name='source', no_webcam_compression=False, 
                    frame_rate=30, sync=True, 
                    video_format='RGB'):
    """
    Creates a GStreamer pipeline string for the video source with a separate fps caps
    for frame rate control.

    Args:
        video_source (str): The path or device name of the video source.
        video_width (int, optional): The width of the video. Defaults to 640.
        video_height (int, optional): The height of the video. Defaults to 640.
        video_format (str, optional): The video format. Defaults to 'RGB'.
        name (str, optional): The prefix name for the pipeline elements. Defaults to 'source'.

    Returns:
        str: A string representing the GStreamer pipeline for the video source.
    """
    # This pipeline receives an RTSP stream via UDP on port 5600, decodes H264, and converts to raw video.
    # It mimics: gst-launch-1.0 -v udpsrc port=5600 caps='application/x-rtp, media=(string)video, clock-rate=(int)90000, encoding-name=(string)H264' ! rtph264depay ! avdec_h264 ! videoconvert ! autovideosink sync=false
    source_element = (
        "udpsrc port=5600 "
        "caps=\"application/x-rtp, media=(string)video, clock-rate=(int)90000, encoding-name=(string)H264\" ! "
        "rtph264depay ! "
        "avdec_h264 ! "
        "videoconvert ! "
    )

    # Set up the fps caps.
    # If sync is True, constrain the rate with the given frame_rate.
    # Otherwise, pass through (no framerate limitation).
    if sync:
        fps_caps = f"video/x-raw, framerate={frame_rate}/1"
    else:
        fps_caps = "video/x-raw"

    source_pipeline = (
        f'{source_element} '
        f'{QUEUE(name=f"{name}_scale_q")} ! '
        f'videoscale name={name}_videoscale n-threads=2 ! '
        f'{QUEUE(name=f"{name}_convert_q")} ! '
        f'videoconvert n-threads=3 name={name}_convert qos=false ! '
        f'video/x-raw, pixel-aspect-ratio=1/1, format={video_format}, '
        f'width={video_width}, height={video_height} ! '
        f'videorate name={name}_videorate ! capsfilter name={name}_fps_caps caps="{fps_caps}" '
    )

    return source_pipeline