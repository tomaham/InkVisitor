FROM node:current-alpine3.14

RUN apk add cmake

COPY packages packages

#Import database
WORKDIR "/packages/database"
RUN npm install
WORKDIR "/packages/server"
RUN npm install
WORKDIR "/packages/client"
RUN npm install
#RUN npm audit fix
WORKDIR "/"
EXPOSE 3000
EXPOSE 4000
EXPOSE 8080
COPY run-inkvisitor.sh run-inkvisitor.sh
#CMD ./run-inkvisitor.sh
CMD ["sh", "run-inkvisitor.sh"]

