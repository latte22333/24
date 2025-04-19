import discord
from discord.ext import commands
import os
from discord import app_commands
import random
import subprocess
from discord import Intents, Client, Interaction, Game
from discord.app_commands import CommandTree
from datetime import timedelta, datetime, timezone
import aiohttp
from keep_alive import keep_alive
import asyncio

TOKEN=os.getenv("DISCORD_TOKEN")
bot = commands.Bot(command_prefix="!" , intents=discord.Intents.all())

def number_to_emoji(number):
    if 1 <= number <= 9:
        return f"{chr(0x0030 + number)}\uFE0F\u20E3"
    return None

@bot.event
async def on_ready ():
    activity_stetas=random.choice(("週末京都現実逃避","2:23 AM","SUMMER TRIANGLE","You and Me","10℃"))
    await bot.change_presence(activity=discord.Game(name="/help｜"f"Join server{len(bot.guilds)}｜""Listening "+activity_stetas))
    print("起動")
    try:
        synced = await bot.tree.sync()
        print(f"{len(synced)}個のコマンドを同期")
    except Exception as e:
        print(e)
from dotenv import load_dotenv


load_dotenv()

GUILD_ID=1363034682253508740
VERIFY_ROLE_ID=1363069009968365698

intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
intents.members = True


# ---------------- 認証ボタンの定義 ---------------- #
class VerifyButton(discord.ui.View):
    def __init__(self, user_id):
        super().__init__(timeout=60)
        self.user_id = user_id

    @discord.ui.button(label="認証を始める", style=discord.ButtonStyle.success)
    async def start_verify(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.user_id:
            await interaction.response.send_message("これはあなたの認証ボタンではありません。", ephemeral=True)
            return

        num1 = random.randint(1, 10)
        num2 = random.randint(1, 10)
        answer = num1 + num2

        # 正解＋不正解の選択肢をランダムに生成
        options = [answer]
        while len(options) < 4:
            fake = random.randint(1, 20)
            if fake != answer and fake not in options:
                options.append(fake)
        random.shuffle(options)

        # セレクトメニューを作成
        select = discord.ui.Select(
            placeholder=f"{num1} + {num2} = ?",
            options=[
                discord.SelectOption(label=str(option), value=str(option))
                for option in options
            ]
        )

        async def select_callback(interaction_select: discord.Interaction):
            selected = int(select.values[0])
            if selected == answer:
                role = interaction.guild.get_role(VERIFY_ROLE_ID)
                await interaction.user.add_roles(role)
                await interaction_select.response.send_message("✅ 正解です！ロールを付与しました。", ephemeral=True)
            else:
                await interaction_select.response.send_message("❌ 不正解です！再度やり直してください。", ephemeral=True)

        select.callback = select_callback

        view = discord.ui.View()
        view.add_item(select)

        await interaction.response.send_message(
            content="以下の選択肢から正しい答えを選択してください。",
            view=view,
            ephemeral=True
        )

# ---------------- スラッシュコマンド ---------------- #
@bot.tree.command(name="verify", description="...")
@app_commands.guilds(discord.Object(id=GUILD_ID))  # ギルド限定
async def verify(interaction: discord.Interaction):
    embed = discord.Embed(
        title="",
        description="## 📑 簡単な計算をして認証をしてください。",
        color=0x00ffcc
    )
    embed.set_image(url="https://i.pinimg.com/originals/78/41/b9/7841b9967f7bb4cd5ef200f24ee04adb.gif")
    view = VerifyButton(interaction.user.id)
    await interaction.response.send_message(embed=embed, view=view)

@bot.tree.command(name="r")
async def rules(interaction: discord.Interaction):
    embed = discord.Embed(
        description="## 📌 利用規約・注意事項【Crafted Bots】",
        color=3447003
    )

    embed.add_field(
        name="🎉 ようこそ、Crafted Bots -【全ての代行サービスを】へ",
        value="以下の利用規約・注意事項をご確認の上、ご利用をお願いいたします。",
        inline=False
    )
    embed.add_field(
        name="✅ ご利用にあたって",
        value="・本サーバーは、BOT販売・代行・設定支援などを目的とした開発者支援型サービスサーバーです。\n・全てのユーザーは以下の利用規約に同意したものとみなします。",
        inline=False
    )
    embed.add_field(
        name="🛡️ サービス全般について",
        value="・提供するBOT・ファイル・設定等は、商用利用不可／個人利用限定です。（※別途許可がある場合を除く）\n・再配布、転売、複製しての配布行為は禁止です。\n・各サービスは「現状有姿」で提供しており、動作保証・永久保証は行いません。",
        inline=False
    )
    embed.add_field(
        name="🧾 購入・依頼に関する注意事項",
        value="・購入後のキャンセル・返金は基本不可とします。\n・BOT起動代行などの継続サービスについては、料金未納の場合はサービスを停止させていただきます。",
        inline=False
    )
    embed.add_field(
        name="🧑‍⚖️ 禁止事項",
        value="・他利用者・運営への迷惑行為、誹謗中傷、荒らし行為\n・他サービスやコミュニティへの過度な勧誘・宣伝\n・サーバーの情報・ファイルを許可なく外部に公開する行為",
        inline=False
    )
    embed.add_field(
        name="⚠️ 運営からのお願い",
        value="・すべてのやりとりは、円滑かつ丁寧なコミュニケーションを心がけてください。",
        inline=False
    )
    embed.add_field(
        name="📝 改定について",
        value="・本利用規約は予告なく変更・更新される場合があります。",
        inline=False
    )
    embed.set_footer(text="Crafted Bots運営チーム")
    embed.set_author(name="py", icon_url="https://i.pinimg.com/564x/f2/bf/81/f2bf81b2bc34fbb6d5bc57dd33bfc551.jpg")

    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="buy")
async def buy(interaction: discord.Interaction):
    embed = discord.Embed(
        description="## 📌 ご購入される方へ【Crafted Bots】"
    )
    embed.add_field(
        name="Bot作成中のため数日間DMの方で依頼をおねがい致します。",
        value="",
        inline=False
    )
    embed.set_image(url="https://i.pinimg.com/originals/91/1f/f6/911ff6a5913ed95b4af78ab454184e88.gif")

    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="n")
async def consult(interaction: discord.Interaction):
    embed = discord.Embed(
        description="## 📌 質問・相談・見積もりされる方へ【Crafted Bots】"
    )
    embed.add_field(
        name="Bot作成中のため数日間DMの方で、質問・相談・見積もりをおねがい致します。",
        value="",
        inline=False
    )
    embed.set_image(url="https://i.pinimg.com/originals/ab/76/de/ab76def5a6d4bd6cef3c3bc614122ed8.gif")

    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="hello", description="...")
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message("hello")

# ---------------- 起動時イベント ---------------- #
@bot.event
async def on_ready():
    await bot.wait_until_ready()
    try:
        guild = discord.Object(id=GUILD_ID)
        synced = await bot.tree.sync(guild=guild)
        print(f"✅ {len(synced)}個のコマンドをギルド {GUILD_ID} に同期しました。")
    except Exception as e:
        print(f"同期エラー: {e}")

keep_alive()

bot.run(TOKEN)