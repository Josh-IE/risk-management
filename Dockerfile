FROM lambci/lambda:build-python3.6

LABEL maintainer="<josh@techintel.dev>"

ENV NODE_PATH=/opt/nodejs/node8/node_modules:/opt/nodejs/node_modules:/var/runtime/node_modules:/var/runtime:/var/task:/var/runtime/node_modules \
    npm_config_unsafe-perm=true

RUN curl https://lambci.s3.amazonaws.com/fs/nodejs8.10.tgz | tar -zx -C /

RUN npm rebuild && npm install npm@latest -g

WORKDIR /var/task

# Fancy prompt to remind you are in zappashell
RUN echo 'export PS1="\[\e[36m\]zappashell>\[\e[m\] "' >> /root/.bashrc

COPY . .

CMD ["bash"]