from typing import List, Tuple, Union, Dict, Optional, Literal
from discord.commands import SlashCommandGroup
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime, timedelta
from discord.ext.pages import Paginator
from discord.ext import commands, tasks
from collections import Counter
from discord.ui import Select
from discord import Option
from io import BytesIO
from pathlib import Path
from enum import Enum

from colorama import Fore
from time import ctime
import aiosqlite
import requests
import aiohttp
import asyncio
import sqlite3
import discord
import random
import bisect
import qrcode
import shutil
import math
import uuid
import json
import time
import os

t = f"{Fore.LIGHTYELLOW_EX}{ctime()}{Fore.RESET}"