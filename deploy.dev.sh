#!/bin/bash

export $(cat .env.dev | xargs) && docker-compose -f docker-compose.dev.yml up --build
