# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~# CatUserBot #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
# Copyright (C) 2020-2023 by TgCatUB@Github.

# This file is part of: https://github.com/TgCatUB/catuserbot
# and is released under the "GNU v3.0 License Agreement".

# Please see: https://github.com/TgCatUB/catuserbot/blob/master/LICENSE
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

FROM python:3.11-slim-bullseye

# System dependencies
RUN apt-get update && apt-get upgrade -y && \
    apt-get install -y --no-install-recommends \
    git \
    ffmpeg \
    libxml2-dev \
    libxslt1-dev \
    zlib1g-dev \
    g++ \
    curl \
    neofetch \
    && rm -rf /var/lib/apt/lists/*

# Working directory 
WORKDIR /userbot

# Timezone
ENV TZ=Asia/Jakarta

## Copy files and install requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Set environment paths
ENV PATH="/userbot/bin:$PATH"

CMD ["python3", "-m", "userbot"]
