FROM node:9.6.1

# set working directory
RUN mkdir /usr/src/app
WORKDIR /usr/src/app

# add `/usr/src/app/node_modules/.bin` to $PATH
ENV PATH /usr/src/app/node_modules/.bin:$PATH

# install and cache app dependencies
COPY package* /usr/src/app/

RUN npm install --silent
RUN npm install react-scripts@1.1.1 -g --silent

COPY src/ /usr/src/app/src/
COPY public/ /usr/src/app/public/

# start app
CMD ["npm", "run", "start"]
