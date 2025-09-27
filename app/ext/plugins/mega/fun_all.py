# app/ext/plugins/mega/fun_all.py
from __future__ import annotations

import base64
import binascii
import random
import re
from typing import Callable, Dict, List

import discord
from discord import app_commands
from discord.ext import commands


# ---------- helpers (трансформеры текста) ----------

SMALLCAPS_MAP = {
    "a": "ᴀ", "b": "ʙ", "c": "ᴄ", "d": "ᴅ", "e": "ᴇ", "f": "ғ", "g": "ɢ",
    "h": "ʜ", "i": "ɪ", "j": "ᴊ", "k": "ᴋ", "l": "ʟ", "m": "ᴍ", "n": "ɴ",
    "o": "ᴏ", "p": "ᴘ", "q": "ǫ", "r": "ʀ", "s": "s", "t": "ᴛ", "u": "ᴜ",
    "v": "ᴠ", "w": "ᴡ", "x": "x", "y": "ʏ", "z": "ᴢ"
}
LEET_MAP = str.maketrans({
    "a": "4", "A": "4", "e": "3", "E": "3", "i": "1", "I": "1",
    "o": "0", "O": "0", "s": "5", "S": "5", "t": "7", "T": "7",
    "b": "8", "B": "8", "g": "9", "G": "9",
})

def to_fullwidth(s: str) -> str:
    out = []
    for ch in s:
        o = ord(ch)
        if 0x21 <= o <= 0x7E:
            out.append(chr(o - 0x21 + 0xFF01))
        elif ch == " ":
            out.append("　")
        else:
            out.append(ch)
    return "".join(out)

def to_smallcaps(s: str) -> str:
    return "".join(SMALLCAPS_MAP.get(ch, SMALLCAPS_MAP.get(ch.lower(), ch)) for ch in s)

def to_wide(s: str) -> str:
    return " ".join(list(s))

def to_mock(s: str) -> str:
    out, flip = [], True
    for ch in s:
        if ch.isalpha():
            out.append(ch.upper() if flip else ch.lower())
            flip = not flip
        else:
            out.append(ch)
    return "".join(out)

def to_altcase(s: str) -> str:
    return "".join(ch.upper() if random.random() < 0.5 else ch.lower() for ch in s)

def to_rot13(s: str) -> str:
    def rot(c: str) -> str:
        if "a" <= c <= "z": return chr((ord(c)-97+13)%26+97)
        if "A" <= c <= "Z": return chr((ord(c)-65+13)%26+65)
        return c
    return "".join(rot(c) for c in s)

def to_camel(s: str) -> str:
    parts = re.split(r"[\s_\-]+", s.strip())
    if not parts: return s
    return parts[0].lower() + "".join(p.capitalize() for p in parts[1:])

def to_pascal(s: str) -> str:
    return "".join(p.capitalize() for p in re.split(r"[\s_\-]+", s.strip()) if p)

def to_snake(s: str) -> str:
    return "_".join(re.split(r"[\s\-]+", s.strip().lower()))

def to_kebab(s: str) -> str:
    return "-".join(re.split(r"[\s_]+", s.strip().lower()))

def scramble_letters(s: str) -> str:
    chars = list(s); random.shuffle(chars); return "".join(chars)

def only_initials(s: str) -> str:
    return "".join(w[0] for w in re.split(r"\s+", s.strip()) if w)

def surround(s: str, left: str, right: str | None = None) -> str:
    right = left if right is None else right
    return f"{left}{s}{right}"

def markdown_bold(s: str) -> str: return surround(s, "**")
def markdown_italic(s: str) -> str: return surround(s, "*")
def markdown_underline(s: str) -> str: return surround(s, "__")
def markdown_strike(s: str) -> str: return surround(s, "~~")
def markdown_mono(s: str) -> str: return surround(s, "`")
def markdown_codeblock(s: str) -> str: return f"```\n{s}\n```"
def markdown_quote(s: str) -> str: return "\n".join("> " + line for line in s.splitlines())
def markdown_spoiler(s: str) -> str: return surround(s, "||")

def base64_encode(s: str) -> str:
    return base64.b64encode(s.encode("utf-8")).decode("ascii")
def base64_decode(s: str) -> str:
    try:
        return base64.b64decode(s.encode("ascii")).decode("utf-8", errors="replace")
    except binascii.Error:
        return "⚠️ Невалидный base64."

def to_binary(s: str) -> str:
    return " ".join(f"{ord(ch):08b}" for ch in s)
def from_binary(s: str) -> str:
    try:
        return "".join(chr(int(b, 2)) for b in s.split())
    except ValueError:
        return "⚠️ Невалидная бинарная строка."

def to_hex(s: str) -> str:
    return s.encode("utf-8").hex()
def from_hex(s: str) -> str:
    try:
        return bytes.fromhex(s).decode("utf-8", errors="replace")
    except ValueError:
        return "⚠️ Невалидный hex."

def vowel_swap(s: str) -> str:
    table = {"a":"e","e":"i","i":"o","o":"u","u":"a","A":"E","E":"I","I":"O","O":"U","U":"A"}
    return re.sub(r"[aeiouAEIOU]", lambda m: table[m.group()], s)

def remove_vowels(s: str) -> str:
    return re.sub(r"[aeiouAEIOU]", "", s)

def remove_consonants(s: str) -> str:
    return re.sub(r"[b-df-hj-np-tv-zB-DF-HJ-NP-TV-Z]", "", s)

def hashtagify(s: str) -> str:
    return "#" + re.sub(r"\s+", "", s)

def claptext(s: str) -> str:
    parts = re.split(r"\s+", s.strip())
    return " 👏 ".join(p for p in parts if p) or s

def owoify(s: str) -> str:
    s = re.sub(r"[lr]", "w", s)
    s = re.sub(r"[LR]", "W", s)
    faces = ["(・`ω´・)", "(uwu)", "(^•ω•^)", "(｡♥‿♥｡)"]
    return s + " " + random.choice(faces)
def uwuify(s: str) -> str: return owoify(s) + " uwu"

def add_emojis(s: str, left: str, right: str) -> str:
    return f"{left} {s} {right}"


# ---------- Cog с /fun и 5 подгруппами ----------

class FunAll(commands.Cog):
    """Одна группа /fun, в ней 5 подгрупп по 10 команд (итого 50)."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

        self.fun = app_commands.Group(name="fun", description="Развлечения и преобразования текста.")

        self.groups: Dict[str, app_commands.Group] = {
            "text": app_commands.Group(name="text", description="Базовые текстовые преобразования"),
            "format": app_commands.Group(name="format", description="Markdown/регистр/стили"),
            "encode": app_commands.Group(name="encode", description="Кодировки и форматы"),
            "memes": app_commands.Group(name="memes", description="Мемные преобразования"),
            "symbols": app_commands.Group(name="symbols", description="Символы и декоративные эффекты"),
        }

        # прикручиваем подгруппы к /fun
        for g in self.groups.values():
            self.fun.add_command(g)

        # Точное распределение 50 команд (5×10)
        self._bulk_register("text", [
            ("reverse", "Перевернуть строку", lambda s: s[::-1]),
            ("upper", "В верхний регистр", str.upper),
            ("lower", "В нижний регистр", str.lower),
            ("title", "Title Case", str.title),
            ("mock", "Чередующийся регистр (SpOnGeBoB)", to_mock),
            ("altcase", "Случайный регистр", to_altcase),
            ("wide", "Расставить пробелы между символами", to_wide),
            ("fullwidth", "Fullwidth/Ｖａｐｏｒ", to_fullwidth),
            ("smallcaps", "Малые капители ᴀʙᴄ", to_smallcaps),
            ("rot13", "ROT13", to_rot13),
        ])

        self._bulk_register("format", [
            ("bold", "Жирный **…**", markdown_bold),
            ("italic", "Курсив *…*", markdown_italic),
            ("underline", "Подчёркнутый __…__", markdown_underline),
            ("strike", "Зачёркнутый ~~…~~", markdown_strike),
            ("mono", "Моноширинный `…`", markdown_mono),
            ("code", "Кодовый блок ```", markdown_codeblock),
            ("quote", "Цитата > …", markdown_quote),
            ("spoiler", "Спойлер ||…||", markdown_spoiler),
            ("camel", "camelCase", to_camel),
            ("pascal", "PascalCase", to_pascal),
        ])

        self._bulk_register("encode", [
            ("base64", "Base64 encode", base64_encode),
            ("unbase64", "Base64 decode", base64_decode),
            ("binary", "В двоичный", to_binary),
            ("unbinary", "Из двоичного", from_binary),
            ("hex", "В hex", to_hex),
            ("unhex", "Из hex", from_hex),
            ("snake", "snake_case", to_snake),
            ("kebab", "kebab-case", to_kebab),
            ("initials", "Инициализация слов", only_initials),
            ("scramble", "Перемешать символы", scramble_letters),
        ])

        self._bulk_register("memes", [
            ("clap", "Текст через 👏", claptext),
            ("owo", "Owoify", owoify),
            ("uwu", "Uwuify", uwuify),
            ("vowelswap", "Сдвиг гласных (a→e→i…)", vowel_swap),
            ("novowels", "Убрать гласные", remove_vowels),
            ("noconsonants", "Убрать согласные", remove_consonants),
            ("hashtag", "Сделать #хештег", hashtagify),
            ("e3", "Заменить e→3", lambda s: s.replace("e", "3").replace("E", "3")),
            ("o0", "Заменить o→0", lambda s: s.replace("o", "0").replace("O", "0")),
            ("i1", "Заменить i→1", lambda s: s.replace("i", "1").replace("I", "1")),
        ])

        self._bulk_register("symbols", [
            ("mirror", "Отразить: текст | тскет", lambda s: f"{s} | {s[::-1]}"),
            ("repeat2", "Повторить ×2", lambda s: (s + " ") * 2),
            ("repeat3", "Повторить ×3", lambda s: (s + " ") * 3),
            ("spacestrip", "Убрать все пробелы", lambda s: re.sub(r"\s+", "", s)),
            ("spacedouble", "Двойные пробелы", lambda s: re.sub(r"\s+", "  ", s.strip())),
            ("parentheses", "В скобки (…)", lambda s: f"({s})"),
            ("brackets", "В квадратные […]", lambda s: f"[{s}]"),
            ("braces", "В фигурные {{…}}", lambda s: f"{{{s}}}"),
            ("hearts", "Добавить ❤️", lambda s: add_emojis(s, "❤️", "❤️")),
            ("fire", "Добавить 🔥", lambda s: add_emojis(s, "🔥", "🔥")),
        ])

        # /fun help
        @self.fun.command(name="help", description="Список всех сабкоманд /fun")
        async def _help(interaction: discord.Interaction):
            lines: List[str] = []
            for grp_name, grp in self.groups.items():
                names = ", ".join(f"`{c.name}`" for c in grp.commands)
                lines.append(f"**{grp_name}**: {names}")
            embed = discord.Embed(
                title="Справка по /fun",
                description="\n".join(lines),
                color=discord.Color.blurple(),
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)

    def _bulk_register(self, group_key: str, items: List[tuple[str, str, Callable[[str], str]]]) -> None:
        grp = self.groups[group_key]
        for name, desc, transform in items:
            async def _cb(interaction: discord.Interaction, text: str, _t=transform, _name=name):
                result = _t(text or "")
                embed = discord.Embed(title=f"/fun {group_key} {_name}", color=discord.Color.random())
                in_v = text[:1024] if text else "—"
                out_v = (result[:3990] + "…") if len(result) > 4000 else (result or "—")
                embed.add_field(name="Ввод", value=in_v, inline=False)
                embed.add_field(name="Результат", value=out_v, inline=False)
                await interaction.response.send_message(embed=embed)

            cmd = app_commands.Command(name=name, description=desc, callback=_cb)
            grp.add_command(cmd)

    async def cog_load(self) -> None:
        self.bot.tree.add_command(self.fun)

    async def cog_unload(self) -> None:
        try:
            self.bot.tree.remove_command(self.fun.name, type=self.fun.type)
        except Exception:
            pass


async def setup(bot: commands.Bot):
    await bot.add_cog(FunAll(bot))