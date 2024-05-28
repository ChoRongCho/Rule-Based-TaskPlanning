import cv2
import numpy as np
import pyrealsense2 as rs


def initialize():
    pipeline = rs.pipeline()
    config = rs.config()

    # Get device product line for setting a supporting resolution
    pipeline_wrapper = rs.pipeline_wrapper(pipeline)
    pipeline_profile = config.resolve(pipeline_wrapper)
    device = pipeline_profile.get_device()
    device_product_line = str(device.get_info(rs.camera_info.product_line))

    found_rgb = False
    for s in device.sensors:
        if s.get_info(rs.camera_info.name) == 'RGB Camera':
            found_rgb = True
            break
    if not found_rgb:
        print("The demo requires Depth camera with Color sensor")
        exit(0)

    config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
    config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

    cfg = pipeline.start(config)
    pp, ff = get_parameters(cfg=cfg)


def get_parameters(cfg):
    profile = cfg.get_stream(rs.stream.color)
    intr = profile.as_video_stream_profile().get_intrinsics()

    # get intrinsic parameter
    pp = (intr.ppx, intr.ppy)
    ff = (intr.fx, intr.fy)
    return pp, ff


def save_video_from_image():
    w = 640
    h = 480
    fps = 30

    # device = rs.context().devices[0]
    # pipeline = rs.pipeline()

    # Define the codec and create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter('output.avi', fourcc, 30.0, (640, 480))  # Adjust resolution if necessary

    # Configure depth and color streams
    pipeline = rs.pipeline()
    config = rs.config()
    config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
    config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

    # Start streaming
    pipeline.start(config)

    try:
        while True:
            # Wait for a coherent pair of frames: depth and color
            frames = pipeline.wait_for_frames()
            depth_frame = frames.get_depth_frame()
            color_frame = frames.get_color_frame()

            if not depth_frame or not color_frame:
                continue

            # Convert images to numpy arrays
            depth_image = np.asanyarray(depth_frame.get_data())
            color_image = np.asanyarray(color_frame.get_data())

            # Apply some processing if needed
            # For example, you can use depth and color images to do some analysis or add overlays

            # Write the frame into the file 'output.avi'
            out.write(color_image)

            # Display the resulting frame
            cv2.imshow('frame', color_image)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    finally:
        # Stop streaming
        pipeline.stop()
        # Release the VideoWriter object
        out.release()
        cv2.destroyAllWindows()



if __name__ == '__main__':
    save_video_from_image()

