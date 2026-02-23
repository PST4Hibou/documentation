# Environment Variables

Hibou environment variables allow you to edit your server setup configuration and customize it.

Updating your Appwrite environment variables requires you to edit your Hibou .env file.

### Audio

| Name                   | Description                                         |
|------------------------|-----------------------------------------------------|
| `AUDIO_ANGLE_COVERAGE` | Angle in degree covered by the mics. Default is 60. |
| `AUDIO_STREAM_LATENCY` |                                                     |
| `AUDIO_CHUNK_DURATION` | Duration in ms of one audio chunk. Default is 500.  |
| `AUDIO_VOLUME`         | Based software volume. Default is 9.                |
| `AUDIO_REC_HZ`         |                                                     |

### Recordings

| Name                          | Description                                                                   |
|-------------------            |-------------------------------------------------------------------------------|
| `REC_AUDIO_ENABLE`            | When true audio saved by channels in the output directory. Default is true.   |
| `REC_VIDEO_ENABLE`            | When true video saved by channels in the output directory. Default is true.   |
| `REC_VIDEO_ON_DETECTION`      | When true video saved by channels in the output directory. Default is false.  |
| `REC_SAVE_FP`                 | Directory where video are recorded. Default is `./recs`.                      |

### ADC devices

| Name                  | Description                                                                                       |
|-----------------------|---------------------------------------------------------------------------------------------------|
| `DEVICES_CONFIG_PATH` | File path to where device should be loaded from a file. Default is `./controllers_devices.json`   |

### Sound Processing

| Name                  | Description                                                                                       |
|-----------------------|---------------------------------------------------------------------------------------------------|
| `STATIONARY`          | When the noise reduction stationary is used. Default is true.                                     |

### Logs

| Name            | Description                                                                                           |
|-----------------|-------------------------------------------------------------------------------------------------------|
| `LOG_PATH`      | Directory where logs are saved. Default is `./logs/app.log`.                                          |
| `LOG_CONF_PATH` | Logging configuration for Python. Default is `logging.conf`.                                          |
| `LOG_LEVEL`     | Logging debug level. Possible values: DEBUG, INFO, WARNING, ERROR, CRITICAL, NOTSET. Default is INFO. |

### PTZ

| Name                | Description                                 |
|---------------------|---------------------------------------------|
| `PTZ_USERNAME`      | PTZ username.                               |
| `PTZ_PASSWORD`      | PTZ password.                               |
| `PTZ_HOST`          | PTZ host name address.                      |
| `PTZ_VIDEO_CHANNEL` | Can be either: 1, 2, 3                      |
| `PTZ_RTSP_PORT`     | RTSP port for video stream. Default is 554. |
| `PTZ_START_AZIMUTH` |                                             |
| `PTZ_END_AZIMUTH`   |                                             |

### AI

| Name              | Description                                                                       |
|-------------------|-----------------------------------------------------------------------------------|
| `AI_DEVICE`       | AI's models can either run on CPU (`cpu`) or GPU (`cuda`). Default is `cpu`.      |
| `AI_NUM_PROC`     | Number of processors used by AI. Default is 4                                     |
| `AI_CV_ENABLE`    | When computer vision detection is enable. Default is false.                       |
| `AI_CV_MODEL`     | Directory where model of computer vision is saved. Default is `yolo11n_drone.pt`  |
| `AI_CV_MODEL_TYPE`| AI's computer vision models use `yolo`. Default is `yolo`                         |
