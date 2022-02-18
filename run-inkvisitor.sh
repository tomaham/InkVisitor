#!/bin/sh

cd packages/database
npm run import-local

cd ../server
npm run start:dev &

cd ../client
npm start

