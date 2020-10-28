import time
import urllib.request
import urllib.parse
import json
import orizin_agent


def get_chat_id(yt_url):
    video_id = yt_url.replace("https://www.youtube.com/watch?v=", "")
    print("video_id: ", video_id)

    url = "https://www.googleapis.com/youtube/v3/videos?"
    parameters = {"key": YT_API_KEY, "id": video_id, "part": "liveStreamingDetails"}
    data = urllib.request.urlopen(url + urllib.parse.urlencode(parameters))
    data = json.loads(data.read().decode(encoding="utf-8"))

    live_streaming_details = data["items"][0]["liveStreamingDetails"]
    if "activeLiveChatId" in live_streaming_details.keys():
        chat_id = live_streaming_details["activeLiveChatId"]
        print("チャンネルIDの取得に成功しました。")
    else:
        chat_id = None
        print("指定された動画はライブ配信ではありません。")

    return chat_id


def get_chat(chat_id, page_token):
    url = "https://www.googleapis.com/youtube/v3/liveChat/messages?"
    parameters = {"key": YT_API_KEY, "liveChatId": chat_id, "part": "id,snippet,authorDetails"}
    if type(page_token) == str:
        parameters["pageToken"] = page_token

    data = urllib.request.urlopen(url + urllib.parse.urlencode(parameters))
    data = json.loads(data.read().decode(encoding="utf-8"))

    try:
        for item in data["items"]:
            message = item["snippet"]["displayMessage"]
            print(f"query: {message}")
            print("response: " + orizin_agent.make_response(message)[0])
            print()
        print("start: ", data["items"][0]["snippet"]["publishedAt"])
        print("end: ", data["items"][-1]["snippet"]["publishedAt"])

    except:
        pass

    return data['nextPageToken']


if __name__ == "__main__":
    YT_API_KEY = input("YouTube APIキーを入力 >>>")
    yt_url = input("YouTubeの動画のURLを入力 >>>")

    slp_time = 5
    iter_times = 90
    take_time = slp_time / 60 * iter_times
    print(f"{take_time}分後に終了する予定です。")
    print(f"work on {yt_url}")

    print(f"{yt_url} のチャットを取得します。")
    chat_id = get_chat_id(yt_url)

    next_page_token = None
    for i in range(iter_times):
        try:
            next_page_token = get_chat(chat_id, next_page_token)
            time.sleep(slp_time)
        except:
            break
