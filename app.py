from __future__ import unicode_literals
import errno,os,sys,util,tempfile,datetime,json
from os.path import join, dirname
from argparse import ArgumentParser
from flask import Flask, request, abort, render_template
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

# sys.path.append('/Users/kikuchitakashi/Docker/wedding_bot')
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
    SourceUser, SourceGroup, SourceRoom,
    TemplateSendMessage, ConfirmTemplate, MessageAction,
    ButtonsTemplate, ImageCarouselTemplate, ImageCarouselColumn, URIAction,
    PostbackAction, DatetimePickerAction,
    CarouselTemplate, CarouselColumn, PostbackEvent,
    StickerMessage, StickerSendMessage, LocationMessage, LocationSendMessage,
    ImageMessage, VideoMessage, AudioMessage, FileMessage,
    UnfollowEvent, FollowEvent, JoinEvent, LeaveEvent, BeaconEvent,
    FlexSendMessage, BubbleContainer, ImageComponent, BoxComponent,
    TextComponent, SpacerComponent, IconComponent, ButtonComponent,
    SeparatorComponent
)

app = Flask(__name__)

# 環境変数からchannel_secret・channel_access_tokenを取得
channel_secret = os.getenv('LINE_CHANNEL_SECRET', None)
channel_access_token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN', None)

if channel_secret is None:
    print('Specify LINE_CHANNEL_SECRET as environment variable.')
    sys.exit(1)
if channel_access_token is None:
    print('Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.')
    sys.exit(1)

line_bot_api = LineBotApi(channel_access_token)
handler = WebhookHandler(channel_secret)

static_tmp_path = os.path.join(os.path.dirname(__file__), 'static', 'tmp')

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

@app.route("/", methods=['GET'])
def hello():
    return 'hello'

@app.route("/hogehoge", methods=['GET'])
def hoge():
    return 'hogehoge'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    if event.message.text == "試合日程":
        carousel_columns = []

        column = CarouselColumn(
            text='6月xx日（日）大宮vs鹿島：ホーム',
            actions=[
                PostbackAction(
                    label='この日のチケットを購入',
                    data='action=buy&itemid=1'
                ),
            ]
        )
        carousel_columns.append(column)
        column = CarouselColumn(
            text='7月xx日（土）仙台vs仙台：アウェイ',
            actions=[
                PostbackAction(
                    label='この日のチケットを購入',
                    data='action=buy&itemid=1'
                ),
            ]
        )
        carousel_columns.append(column)
        carousel_template_message = TemplateSendMessage(
            alt_text='試合日程',
            template=CarouselTemplate(
                columns=carousel_columns,
                image_size="contain"
            )
        )
        line_bot_api.reply_message(
            event.reply_token,
            [
                carousel_template_message,
            ]
        )
    elif event.message.text == "大宮のグルメ情報":
        carousel_columns = []
        column = CarouselColumn(
            text='位置情報画面を開きますか？',
            actions=[
                URIAction(
                    label='はい',
                    uri='line://nv/location'
                ),
                MessageAction(
                    label='いいえ',
                    text='いいえ'
                )
            ]
        )
        carousel_columns.append(column)
        carousel_template_message = TemplateSendMessage(
            alt_text='位置情報画面',
            template=CarouselTemplate(
                columns=carousel_columns,
            )
        )
        line_bot_api.reply_message(
            event.reply_token,
            [
                carousel_template_message,
            ]
        )
    elif event.message.text == "選手情報":
        carousel_columns = []

        column = CarouselColumn(
            thumbnail_image_url='https://www.ardija.co.jp/files/person/2016/41/41_ienaga_s.jpg',
            text='家長昭博',
            actions=[
                PostbackAction(
                    label='詳細を表示',
                    data='action=buy&itemid=1'
                ),
            ]
        )
        carousel_columns.append(column)
        column = CarouselColumn(
            thumbnail_image_url='https://www.ardija.co.jp/files/news/201604/15_oyama.jpg',
            text='大山啓輔',
            actions=[
                PostbackAction(
                    label='詳細を表示',
                    data='action=buy&itemid=1'
                ),
            ]
        )
        carousel_columns.append(column)
        carousel_template_message = TemplateSendMessage(
            alt_text='選手情報',
            template=CarouselTemplate(
                columns=carousel_columns,
                image_size="contain"
            )
        )
        line_bot_api.reply_message(
            event.reply_token,
            [
                carousel_template_message,
            ]
        )
    elif event.message.text == "スタジアム案内":
        carousel_columns = []
        column = CarouselColumn(
            text='位置情報画面を開きますか？',
            actions=[
                URIAction(
                    label='はい',
                    uri='line://nv/location'
                ),
                MessageAction(
                    label='いいえ',
                    text='いいえ'
                )
            ]
        )
        carousel_columns.append(column)
        carousel_template_message = TemplateSendMessage(
            alt_text='位置情報画面',
            template=CarouselTemplate(
                columns=carousel_columns,
            )
        )
        line_bot_api.reply_message(
            event.reply_token,
            [
                carousel_template_message,
            ]
        )
    else:
        line_bot_api.reply_message(
            event.reply_token,
            [
                TextSendMessage(text=util.get_message(event.message.text)),
                # TextSendMessage(text="hoge"),
            ]
        )

if __name__ == "__main__":
    arg_parser = ArgumentParser(
        usage='Usage: python ' + __file__ + ' [--port <port>] [--help]'
    )
    arg_parser.add_argument('-p', '--port', type=int, default=5000, help='port')
    arg_parser.add_argument('-d', '--debug', default=True, help='debug')
    options = arg_parser.parse_args()

    app.run(debug=options.debug, port=options.port)

