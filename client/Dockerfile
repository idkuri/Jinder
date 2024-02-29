FROM node:latest

WORKDIR /client

ENV HOME /client

COPY . .

RUN npm install

EXPOSE 3000

RUN npm run build

CMD ["npm", "start"]
