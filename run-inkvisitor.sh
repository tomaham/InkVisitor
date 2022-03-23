#!/bin/sh

cd packages/database
npm run import-local

cd ../server
npm run start:development &

cd ../client
npm start

