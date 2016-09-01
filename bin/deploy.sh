#!/bin/bash
set -e -x

if [ "${TRAVIS_PULL_REQUEST}" = "false" ] && [ "${TRAVIS_BRANCH}" = "build" ]; then
  # switch to gh-pages branch
  git config user.email "<webapps@code4sa.org>"
  git config user.name "Open Gazettes (via TravisCI)"
  git fetch origin gh-pages
  git checkout FETCH_HEAD
  git checkout -b gh-pages

  # update the index file and rebuild site data
  curl http://code4sa-gazettes.s3.amazonaws.com/archive/index/gazette-index-latest.jsonlines -O
  python bin/build-index.py

  # ensure the site builds
  bundle install
  bundle exec jekyll build

  # save changes
  git add _data _gazettes
  git commit -m "Updated index via TravisCI"

  # now update gh-pages branch on github
  echo "Deploying to GitHub"

  # add git auth
  eval "$(ssh-agent -s)" #start the ssh agent
  set +x
  openssl aes-256-cbc -K $encrypted_152ca5bd4b01_key -iv $encrypted_152ca5bd4b01_iv -in deploy_key.enc -out deploy_key -d
  set -x
  chmod 600 deploy_key # this key should have push access
  ssh-add deploy_key

  git remote set-url origin git@github.com:code4sa/opengazettes.git
  git push origin -u gh-pages
else
  echo "Ignoring pull request or non-build branch"
  exit 0
fi
