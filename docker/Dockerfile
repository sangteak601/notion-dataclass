FROM python:3.12-slim
ARG USERNAME=username
ARG USER_UID=1000
ARG USER_GID=$USER_UID
ENV SHELL /bin/bash

RUN groupadd --gid $USER_GID $USERNAME \
    && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME

RUN pip3 install notion-client

USER $USERNAME

CMD ["/bin/bash"]
