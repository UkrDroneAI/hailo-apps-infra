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