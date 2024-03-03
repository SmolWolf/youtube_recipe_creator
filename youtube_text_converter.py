from pytube import YouTube
import xml.etree.ElementTree as ET  

def convert_xml_to_text(subtitle_xml_content):
    """
    Convert XML subtitle content to plain text.

    Args:
    subtitle_xml_content (str): XML content of subtitles.

    Returns:
    str: Plain text extracted from XML.
    """
    root = ET.fromstring(subtitle_xml_content)
    text_data = [f"{elem.text.strip() if elem.text else ' '}" for elem in root.iter()]
    return ' '.join(text_data)

def fetch_video_description_and_subtitles(id):
    """
    Fetches the video description and auto-generated subtitles for a YouTube video.

    Args:
    video_id (str): The YouTube video ID.

    Returns:
    str: Concatenated video description and subtitles text.
    """
    print(id)
    if not id.startswith("http"):
        prefix = "https://www.youtube.com/watch?v="
        id = prefix + id

    youtube_video = YouTube(id)
    youtube_video.streams
    video_description = youtube_video.description
    
    auto_generated_subtitles = youtube_video.captions.get("a.en")
    
    subtitles_xml_content = auto_generated_subtitles.xml_captions
    subtitles_text = convert_xml_to_text(subtitles_xml_content)
    return video_description + subtitles_text

