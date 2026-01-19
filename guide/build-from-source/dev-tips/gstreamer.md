# GStreamer and its lovely pipelines

## The GStreamer model
GStreamer is one of the oldest libraries/frameworks built around the concept of __pipelines__. The usage of pipelines is
now present more than ever, basic standard for any multimedia editor, tool, and even in IDEs of game engines. GStreamer
provides many language bindings, is simple to use, offers many plugins, including vendor-specifics (like NVIDIA HWA
elements), for wide range of tasks. It has proven to be fast and robust, now used in many different systems and
industries.

## What's a pipeline?
The whole thing is to mimic how a pipeline of gas works. We have _something entering_ (input), and _something getting
out of it_, on the other end (the output). In software, pipelines are a set input entries, with elements chained
together, giving a set of output elements. Let's take a simple example with audio: we have someone sending video through
the network, broadcasting. Maybe you used something like that to watch football matches \*chukles\* **legally** on the
internet. What the software will usually have to do is to get the video stream, decode it and play the video, where
playing the video means to show images (continuous flow of images) and play audio alongside it. Here, we just described
a pipeline! In this example, we've got these elements:\
Network Source > Video Decoder\
Then in parallel:\
Video Decoder > Audio > Play on speakers\
Video Decoder > Image Viewer > Show to display

## GStreamer's system
GStreamer provides events and elements. You will most likely never have to deal with events, unless you have
synchronisation, continuity, gap, corruption, latency, issues, or anything more peculiar. The most important element
is... the _GstElement_. It's the main class that you will use. You connect
it to others, and magic happens.

### GstElement
Each class of GstElement offers different _functionalities_, depending on their class (never forget to use the tools and
check the docs). However, they have some common properties. They can receive/send signals, have _input_ & _output pads_,
as well as _properties_. One classic property is the "name" and "caps", which are important.

| Property | Purpose                                                                                 |
|----------|-----------------------------------------------------------------------------------------|
| name     | Name of the element, can be used to get an element by its name in a GstBin/GstPipeline. |
| caps     | Capabilities of the output pad(s) that the element has.                                 |

::: info
During _Preroll_ and _Playing_ phases, the capabilities can be **negotiated** to match with the chained elements. If you
want to enforce some capabilities, such as encoding, framerate (...). Use it to set them. Other capabilities may be left
free for easier management (such as the channels count in audio, for example) and will be **guessed**
(also negotiated) automatically.
:::

### GstPad
A pad is a connection point for an element in GStreamer. It can be for either _input_ to the element, or _output_ from
it. For some very specific cases, you may need to look at how to use _probes_ on it for event, or
stream filtering.

### GstPipeline
The GstPipeline is the element that manages all the elements of your pipeline. It represents the whole elements. You can
find elements in it, iterate over them. You can stop your whole pipeline to suspend recording, send event down through
the elements. It's mainly "just" a container for the elements (it inherits _GstBin_, so not totally wrong).

## GStreamer's text pipeline syntax
Most of the time, you will just use the text to pipeline tool that GStreamer offers through Gst.parse_launch.

### Basics
| Syntax                        | Description                                                                                  |
|-------------------------------|----------------------------------------------------------------------------------------------|
| \<element> \<prop_0>=\<value> | Declare an element and set its properties.                                                   |
| (\<typing>)\<value>           | Typing a property. It may be useful. Most common are int, bool and string.                   |
| \<input> ! \<output>          | Chain the output element with the input element. Like the shell's ```\|``` but it's ```!```        |
| \<elem_name>.                 | Use the element with the name. Can be used like ```name. ! <output>``` or ```<input> ! name.``` |
| \<elem_name>.\<pad_name>      | Select a specific pad of an element.                                                         |

To "separate", parallelize a part of the pipeline, you can use the "spacing" syntax along a named element.
```
<intput> name=in ! <something> in. ! <something_else>
```
Here you can see that we have _something_ followed by _in._, but just seprated by a simple space.
What this means is that because we have something ending with a dot, it will solve the name (be it an element, or
something more specific like an element's pad name) and make it as source for the next element.
In terms of flow, we have <input> pushing data through <something> **AND** <something_else> at the same time, in
parallel.

### Useful basic elements
| Name           | Description                                                                                                                  |
|----------------|------------------------------------------------------------------------------------------------------------------------------|
| appsrc         | Used to provide data from the app to the GST elements of the pipeline.                                                       |
| appsink        | Used to get the data from the GST elements into the app.                                                                     |
| queue          | A queue for pending elements. Can be used to regulate data amount (droping, leaking...) for the next elements.               |
| tee            | Element that does nothing, but can be used to set a named "point" in the pipeline. Number of inputs is the same as outputs.  |
| filesink       | Saves data to a file.                                                                                                        |
| valve          | Lets the stream flow to the next element, or blocks it.                                                                      |
| videoconverter | Automatically determines what elements to use to convert video from one set of capabilities to another.                      |
| audioconverter | Automatically determines what elements to use to convert audio from one set of capabilities to another.                      |
| audioresample  | Resamples the audio to another framerate.                                                                                    |
| autovideosink  | Used to easily display a video (and also plays the associated audio I think).                                                |
| autoaudiosink  | Used to easily play an audio.                                                                                                |
| av_dec         | Video decoder from FFMPEG, supports many formats, and can have vendor-specific implementations for HWA (Intel provides one). |

In general, here are the naming conventions of the elements:

| Naming        | Description                                                                                                                                              |
|---------------|----------------------------------------------------------------------------------------------------------------------------------------------------------|
| *jitterbuffer | Buffers data and reorder it to properly stream it to the next element. Mainly used with network, because packets not always arrive in the correct order. |
| *src          | Source elements, nothing is set as input for them, as they do not provide input pads. It's a beginning part of the pipeline.                             |
| *sink         | Output elements, nothing is set as output for them, as they do not provide output pads. It's an ending of the pipeline.                                  |
| *enc          | Encoding elements, like for video with x264enc that converts video, image, into an H264 stream.                                                          |
| *dec          | Decodes a stream, like h264_dec, that can convert an H264 stream into a RAW RGB stream.                                                                  |

### Example pipelines
Simple video test:
```
videotestsrc ! videoconvert ! autovideosink
```
A bit more complex:
```
audiotestsrc ! audioresample ! tee name=t t. ! autoaudiosink 
```
Here, we generate an audio, resample it to something we want. Then, we play the audio, and record it in a wav file
at the time.

## Some useful tools
You may need to use some tools from time to time to see if it's your pipeline, or just your code. Here are the two main
ones:

| Name            | Description                                                                                                               |
|-----------------|---------------------------------------------------------------------------------------------------------------------------|
| gst-launch-1.0  | Runs text pipelines directly from the terminal.                                                                           |
| gst-inspect-1.0 | Shows GStreamer properties of available plugins and their elements. You can directly ask about an element, like _appsrc_. |

## You have particular needs for the pipeline?
No worries, although you've seen how to construct a GstPipeline using text, you can build it yourself by connecting the
elements to the pads manually/dynamically, add probes (need to stop events, or stream at particular points). You can
also pause, play, stop it any time you want.
