'''Simple Streamlit UI for SENTINEL-AI Viva 1 demo.'''

import sys
import tempfile
from pathlib import Path

# Add backend modules to Python path
sys.path.insert(0, str(Path(__file__).parent.parent / 'backend'))

import cv2
import pandas as pd
import streamlit as st

from app.ingest.video_reader import VideoReader
from app.vision.pose_estimator import PoseEstimator
from app.vision.renderer import Renderer
from app.analytics.motion import MotionAnalyzer
from app.analytics.proximity import ProximityAnalyzer


st.set_page_config(page_title='SENTINEL-AI', layout='wide')

st.title('SENTINEL-AI')
st.subheader('Real-Time Violence & Anomaly Detection Demo')
st.markdown('Upload a short CCTV clip. The system extracts pose keypoints, computes motion/proximity, and renders an annotated output.')

uploaded_file = st.file_uploader('Upload video (mp4/avi/mov)', type=['mp4', 'avi', 'mov'])

if uploaded_file is not None:
    # Save uploaded file to a temp location
    suffix = Path(uploaded_file.name).suffix or '.mp4'
    tfile = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
    tfile.write(uploaded_file.read())
    tfile.close()

    st.video(tfile.name)

    col1, col2, col3 = st.columns(3)
    with col1:
        conf_threshold = st.slider('Pose confidence', 0.1, 0.9, 0.3, 0.05)
    with col2:
        velocity_threshold = st.slider('Velocity threshold', 10, 100, 40, 5)
    with col3:
        proximity_threshold = st.slider('Proximity threshold', 50, 300, 150, 10)

    if st.button('Analyze Video', type='primary'):
        progress_bar = st.progress(0)
        status_text = st.empty()

        reader = VideoReader(tfile.name)
        estimator = PoseEstimator(device='cpu')
        renderer = Renderer()
        motion = MotionAnalyzer(velocity_threshold=float(velocity_threshold))
        proximity = ProximityAnalyzer(distance_threshold=float(proximity_threshold))

        output_path = str(Path(tempfile.gettempdir()) / 'sentinel_output.mp4')
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        writer = cv2.VideoWriter(output_path, fourcc, int(reader.fps), (reader.width, reader.height))

        threat_history = []
        total_frames = reader.frame_count if reader.frame_count > 0 else 300

        for frame_id, frame, timestamp in reader:
            pose_result = estimator.predict(frame, conf=float(conf_threshold))
            motion_result = motion.update(pose_result)
            prox_result = proximity.analyze(pose_result)

            if motion_result['any_suspicious'] and prox_result['any_close']:
                threat = 'FIGHT'
                color = (0, 0, 255)
                color_markdown = 'red'
            elif motion_result['any_suspicious']:
                threat = 'WARNING'
                color = (0, 255, 255)
                color_markdown = 'orange'
            else:
                threat = 'NORMAL'
                color = (0, 255, 0)
                color_markdown = 'green'

            annotated = renderer.render(
                frame, pose_result,
                motion_flags=motion_result['suspicious_flags'],
                proximity_pairs=prox_result['pairs']
            )
            cv2.putText(annotated, '{} max_v={:.1f}'.format(threat, motion_result['max_velocity']),
                        (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
            writer.write(annotated)

            threat_history.append({
                'frame': frame_id,
                'persons': len(pose_result['persons']),
                'threat': threat,
                'max_velocity': motion_result['max_velocity']
            })

            progress = min((frame_id + 1) / total_frames, 1.0)
            progress_bar.progress(progress)
            status_text.markdown(':{}[Frame {} | Persons {} | Threat {}]'.format(
                color_markdown, frame_id, len(pose_result['persons']), threat))

        reader.release()
        writer.release()
        progress_bar.empty()
        status_text.empty()

        st.success('Analysis complete')

        df = pd.DataFrame(threat_history)

        c1, c2, c3 = st.columns(3)
        c1.metric('Total frames', len(df))
        c2.metric('Max persons/frame', int(df['persons'].max()))
        c3.metric('Peak velocity', round(df['max_velocity'].max(), 1))

        st.subheader('Threat Timeline')
        st.line_chart(df.set_index('frame')[['max_velocity']])

        st.subheader('Recent Frame Stats')
        st.dataframe(df.tail(15), use_container_width=True)

        st.subheader('Annotated Output')
        st.video(output_path)

        with open(output_path, 'rb') as f:
            st.download_button('Download annotated video', f, file_name='sentinel_annotated.mp4', mime='video/mp4')
