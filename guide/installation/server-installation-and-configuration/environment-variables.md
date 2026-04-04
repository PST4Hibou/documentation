# Environment Variables

Hibou environment variables allow you to edit your server setup configuration and customize it.

Updating your Appwrite environment variables requires you to edit your Hibou .env file.

### Audio

| Name                   | Description                                          | Default            |
|------------------------|------------------------------------------------------|--------------------|
| `AUDIO_ANGLE_COVERAGE` | Angle in degree covered by the mics.                 | 60                 |
| `AUDIO_STREAM_LATENCY` | Audio latency between the source and sink pads in ms.| 50                 |
| `AUDIO_CHUNK_DURATION` | Duration in ms of one audio chunk.                   | 500                |
| `AUDIO_VOLUME`         | Based software volume.                               | 9                  |
| `AUDIO_REC_HZ`         | sampling frequency for recorded audio                | 16000              |

### Recordings

| Name                          | Description                                                                       | Default       |
|-------------------------------|-----------------------------------------------------------------------------------|---------------|
| `REC_AUDIO_ENABLE`            | When true, enables audio recording by channels in the output directory.           | true          |
| `REC_VIDEO_ENABLE`            | When true, enables video recording by channels in the output directory            | false         |
| `REC_VIDEO_ON_DETECTION`      | When true, videos are saved by channels in the output directory upon detection.   | false         |
| `REC_SAVE_FP`                 | Directory where video are recorded.                                               | `./recs`      |

### ADC devices

| Name                  | Description                                                                                       | Default                       |
|-----------------------|---------------------------------------------------------------------------------------------------|-------------------------------|
| `DEVICES_CONFIG_PATH` | File path to where device should be loaded from a file.                                           | `./controllers_devices.json`  |

### Sound Processing

| Name                  | Description                                                                                       | Default                       |
|-----------------------|---------------------------------------------------------------------------------------------------|-------------------------------|
| `STATIONARY`          | When the noise reduction stationary is used.                                                      | true                          |

### Logs

| Name            | Description                                                                                             | Default                         |
|-----------------|---------------------------------------------------------------------------------------------------------|---------------------------------|
| `LOG_PATH`      | Directory where logs are saved.                                                                         | `./logs/app.log`                |
| `LOG_CONF_PATH` | Logging configuration for Python.                                                                       | `logging.conf`                  |
| `LOG_LEVEL`     | Logging debug level. Possible values: DEBUG, INFO, WARNING, ERROR, CRITICAL, NOTSET.                    | INFO                            |

### PTZ

| Name                | Description                                                 | Default           |
|---------------------|-------------------------------------------------------------|-------------------|
| `PTZ_USERNAME`      | PTZ username. Leave empty to skip initialization            | None              |
| `PTZ_PASSWORD`      | PTZ password. Leave empty to skip initialization            | None              |
| `PTZ_HOST`          | PTZ host name address. Leave empty to skip initialization   | None              |
| `PTZ_VIDEO_CHANNEL` | Can be either: 1, 2, 3                                      | 1                 |
| `PTZ_RTSP_PORT`     | RTSP port for video stream.                                 | 554               |
| `PTZ_START_AZIMUTH` | initial azimuth angle of the camera.                        | 1770              |
| `PTZ_END_AZIMUTH`   | final azimuth angle of a predefined movement.               | 2793              |

### AI

| Name                  | Description                                                                       | Default                   |
|-----------------------|-----------------------------------------------------------------------------------|---------------------------|
| `AI_DEVICE`           | AI's models can either run on CPU (`cpu`) or GPU (`cuda`).                        | `cpu`                     |
| `AI_NUM_PROC`         | Number of processors used by AI.                                                  | 4                         |
| `AI_CV_ENABLE`        | When computer vision detection is enable.                                         | false                     |
| `AI_CV_MODEL`         | Directory where model of computer vision is saved.                                | `yolo11n_drone.pt`        |
| `AI_CV_MODEL_TYPE`    | The computer vision model used                                                    | `yolo`                    |
| `AI_MODELS_FOLDER`    | Directory where AI models are saved.                                              | `/assets/audio_models/`   |

### IPC

| Name                                  | Description                                                                 | Default                    |
|---------------------------------------|-----------------------------------------------------------------------------|----------------------------|
| `IPC_PROXY_XSUB_PORT`                 | ZMQ proxy XSUB socket port                                                  | `5556`                     |
| `IPC_PROXY_XPUB_PORT`                 | ZMQ proxy XPUB socket port                                                  | `5557`                     |
| `IPC_ACOUSTIC_ANGLE_TOPIC`            | IPC topic for angles detected by the acoustic module                        | `"acoustic_angle"`         |
| `IPC_ACOUSTIC_DETECTION_TOPIC`        | IPC topic for detections from the acoustic module                           | `"acoustic_detection"`     |
| `IPC_DECISION_ANGLE_TOPIC`            | IPC topic for angles output by the decision module                          | `"decision_angle"`         |
| `IPC_DECISION_DETECTION_TOPIC`        | IPC topic for detections output by the decision module                      | `"decision_detection"`     |
| `IPC_VISION_DECISION_TOPIC`           | IPC topic for decisions output by the vision module                         | `"vision_decision"`        |
| `IPC_VISION_DETECTION_TOPIC`          | IPC topic for detections output by the vision module                        | `"vision_detection"`       |
| `IPC_VISION_ANGLE_TOPIC`              | IPC topic for angles output by the vision module                            | `"vision_angle"`           |
| `IPC_VIDEO_STREAMING_ANNOTATED_PORT`  | Port for the annotated video stream                                         | `5560`                     |
| `IPC_SYSTEM_STATUS_TOPIC`             | IPC topic for the overall system status                                     | `"system_status"`          |
