ARG VARIANT="3.10"
FROM mcr.microsoft.com/vscode/devcontainers/python:0-${VARIANT}

USER vscode

RUN curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash - && \
    sudo apt-get install -y nodejs

RUN sudo npm install -g @stoplight/prism-cli

RUN curl -sSf https://rye.astral.sh/get | RYE_VERSION="0.35.0" RYE_INSTALL_OPTION="--yes" bash
ENV PATH=/home/vscode/.rye/shims:$PATH

RUN echo "[[ -d .venv ]] && source .venv/bin/activate" >> /home/vscode/.bashrc